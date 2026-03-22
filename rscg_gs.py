import dolfinx
import math
import numpy as np
import ufl
import sys
import os
import json
import adios4dolfinx



from dolfinx import mesh, fem
from dolfinx.fem import petsc
from dolfinx.fem import Function
from mpi4py import MPI
from ufl import SpatialCoordinate,grad, inner, imag, real, dx
from petsc4py.PETSc import ScalarType
from scipy.optimize import minimize_scalar
from mpi4py import MPI
from datetime import datetime
from dolfinx.io import XDMFFile



#External functions
from define_norms import l2_norm
from step_size import energy_at_tau
from inner_products import inner_products
from simulated_ground_state import load_ground_state_from_bp
from L2_projection import l2_projection
# from reference_domain import reference_domain, reference_function_space, boundary_conditions






######################################################### Computational domain ################################################################






### Define corners of the rectangle
xmin, ymin = -2, -2
xmax, ymax =  2,  2

comm = MPI.COMM_WORLD
rank = comm.rank

comm.Barrier()  # synchronize all ranks
t_start = MPI.Wtime()


### Define the desired mesh step size
k = 5
h = xmax*ymax*2**(-k)
### Calculate the number of divisions for each axis
N_x = math.ceil((xmax - xmin) / h)
N_y = math.ceil((ymax - ymin) / h)

dofs_estimate = (N_x + 1) * (N_y + 1)

if rank == 0:
    print(h)
    print("Dofs", dofs_estimate)
   

### Create the mesh
domain = mesh.create_rectangle(
    comm=comm,
    points=[[xmin, ymin], [xmax, ymax]],
    n=(N_x, N_y),
    cell_type=mesh.CellType.triangle,
)

topology = domain.topology
geometry = domain.geometry

### Get the number of nodes (vertices)
num_nodes_local = topology.index_map(0).size_local
num_nodes_global = topology.index_map(0).size_global

coords = geometry.x

### Create the Function space
V = fem.functionspace(domain, ("Lagrange", 1))

num_dofs_local = V.dofmap.index_map.size_local
num_dofs_global = V.dofmap.index_map.size_global








######################################################### Boundary conditions ################################################################










### Define initial conditions value
phi_D=Function(V,dtype=np.complex128)
phi_D.x.array[:]=ScalarType(0)
phi_D.x.scatter_forward()

### Create facet to cell connectivity required to determine boundary facets
tdim = topology.dim
fdim = tdim - 1
topology.create_connectivity(fdim, tdim)
boundary_facets = mesh.exterior_facet_indices(domain.topology)

boundary_dofs = fem.locate_dofs_topological(V, fdim, boundary_facets)
bc = fem.dirichletbc(phi_D, boundary_dofs)










######################################################### Physical quantities and parameters ################################################################






### Trapping potential
def V_pot(kappa, gamma_x, gamma_y, V):
    trap_potential = Function(V, dtype=ScalarType)
    trap_potential.interpolate(
        lambda x: kappa * (gamma_x**2 * x[0]**2 + gamma_y**2 * x[1]**2)
    )
    trap_potential.x.scatter_forward()
    return trap_potential


### Angular momentum
def Lz(phi,domain): 
    x = SpatialCoordinate(domain)
    Lz_phi = -1j* (x[0] * grad(phi)[1] - x[1] * grad(phi)[0])
    return Lz_phi



### Physical parameters
epsilon=0.1
omega_unscaled=1.1
beta_unscaled =1

gamma_x=1.25
gamma_y=0.98
kappa=0.5

omega=omega_unscaled/epsilon
beta=beta_unscaled/(epsilon**2)
potential= V_pot(kappa,gamma_x, gamma_y,V)/(epsilon**2)

#Integration degree
quadrature_degree=3

### Total energy
def energy(phi, domain, potential, beta=beta, omega=omega):
    energy_functional = 0.5 * (
        inner(grad(phi), grad(phi))
        + inner(potential * phi, phi)
        + 0.5 * beta * inner(phi, phi)**2
        - omega * inner(Lz(phi, domain), phi)
    ) * dx(degree=quadrature_degree)

    local_energy = fem.assemble_scalar(fem.form(energy_functional))
    total_energy = domain.comm.allreduce(local_energy, op=MPI.SUM)

    return total_energy.real





### Linearization of E'(u)
def au(v, w, phi, domain, potential=potential, omega=omega, beta=beta):
    a_form = (
        inner(grad(v), grad(w))
        + potential * inner(v, w)
        - omega * inner(Lz(v, domain), w)
        + beta * inner((real(phi)**2 + imag(phi)**2) * v, w)
    ) * dx(degree=quadrature_degree)

    return a_form








######################################################### Initial conditions ################################################################



###################### BAO ##########################

def phi_init(omega,V,quadrature_degree):
    phi_0=Function(V,dtype=np.complex128)

    phi_0.interpolate(
        lambda x:
            (1 - omega) * (1/np.sqrt(np.pi)*np.exp(-(x[0]**2+x[1]**2)/2))\
            + omega * (1/ufl.sqrt(np.pi) * (x[0] * np.exp(-(x[0]**2 + x[1]**2)/2) + 1j * x[1] * np.exp(-(x[0]**2 + x[1]**2)/2)))
    )
    phi_0.x.scatter_forward()

    ### find L2 norm
    l2_norm_phi_0=l2_norm(phi_0, domain, quadrature_degree)

    ### Normalize
    phi_0.x.array[:] /= l2_norm_phi_0
    phi_0.x.scatter_forward()

    return phi_0


###################### Projection of a fine solution to a coarse mesh  ##########################


### Refine coarse mesh to the fine level
k_fine = 8
n_refinements = k_fine - k

domain_fine = domain
for _ in range(n_refinements):
    domain_fine.topology.create_entities(1)
    domain_fine = mesh.refine(domain_fine)[0]

# Fine function space
V_fine = fem.functionspace(domain_fine, ("CG", 1))

### Fine homogeneous Dirichlet BC
phi_D_fine = Function(V_fine, dtype=np.complex128)
phi_D_fine.x.array[:] = ScalarType(0)
phi_D_fine.x.scatter_forward()

topology_fine = domain_fine.topology
tdim_fine = topology_fine.dim
fdim_fine = tdim_fine - 1
topology_fine.create_connectivity(fdim_fine, tdim_fine)

boundary_facets_fine = mesh.exterior_facet_indices(domain_fine.topology)
boundary_dofs_fine = fem.locate_dofs_topological(V_fine, fdim_fine, boundary_facets_fine)
bc_fine = fem.dirichletbc(phi_D_fine, boundary_dofs_fine)

### Load fine reference state
file_path = "results/gs_20260322_123913_eps0.1_h0.015625"
domain_ref, V_ref, phi_ref = load_ground_state_from_bp(file_path)

### Enforce homogeneous Dirichlet BC on loaded fine state
phi_ref.x.array[boundary_dofs_fine] = ScalarType(0)
phi_ref.x.scatter_forward()

### Project fine reference state to coarse space
phi_fine_to_coarse = l2_projection(phi_ref, domain, V, bc)




### Initial wavefunction 

phi_00 = Function(V)

# 1) Bao initial conditions 
phi_00 = phi_init(omega, V, quadrature_degree)

# 2) Load and project a fine simulated ground state on a coarse mesh 
# phi_00 = phi_fine_to_coarse

# 3) Load a simulated ground state 

# file_path = "results/gs_20260322_121404_eps0.1_h0.5"
# domain, V, phi_00 = load_ground_state_from_bp(file_path)

# # rebuild BC on loaded mesh
# phi_D = Function(V, dtype=np.complex128)
# phi_D.x.array[:] = ScalarType(0)
# phi_D.x.scatter_forward()

# topology = domain.topology
# tdim = topology.dim
# fdim = tdim - 1
# topology.create_connectivity(fdim, tdim)
# boundary_facets = mesh.exterior_facet_indices(domain.topology)
# boundary_dofs = fem.locate_dofs_topological(V, fdim, boundary_facets)
# bc = fem.dirichletbc(phi_D, boundary_dofs)

# # rebuild potential on loaded mesh
# potential = V_pot(kappa, gamma_x, gamma_y, V) / (epsilon**2)





### Energy

energy_00 = energy(phi_00, domain, potential)
if MPI.COMM_WORLD.rank == 0:
    print(f"Initial energy: {energy_00}")









## Mass check of loaded state
mass_local = fem.assemble_scalar(
    fem.form(ufl.inner(phi_00, phi_00) * ufl.dx(degree=quadrature_degree))
)
mass_00 = domain.comm.allreduce(mass_local, op=MPI.SUM).real

if rank == 0:
    print(f"Initial mass: {mass_00:.16e}")





















######################################################### Set the RSCG method ################################################################



# Define the required functiones
phi_0 = Function(V)
phi_new = Function(V)
search_direction_00=Function(V)
search_direction_0=Function(V)
direction_00_projected=Function(V)
energy_gradient_00 = Function(V)
energy_gradient_0 = Function(V)


# Make sure phi_00 ghost values are current before using it in forms
phi_00.x.scatter_forward()

# Owned size
index_map = V.dofmap.index_map
bs = V.dofmap.index_map_bs
n_local = index_map.size_local * bs

# Variational problem
v = ufl.TrialFunction(V)
w = ufl.TestFunction(V)
dx_q = ufl.dx(metadata={"quadrature_degree": quadrature_degree})

a = au(v, w, phi_00, domain)
L = ufl.inner(phi_00, w) * dx_q

problem = petsc.LinearProblem(a, L, bcs=[bc])
rau_00 = problem.solve()
rau_00.x.scatter_forward()

# Global scalar rau_00_au_squared
rau_form = fem.form(au(rau_00, rau_00, phi_00, domain))
rau_00_au_squared_local = fem.assemble_scalar(rau_form)
rau_00_au_squared = domain.comm.allreduce(rau_00_au_squared_local, op=MPI.SUM)

# Energy gradient: write only owned entries
energy_gradient_00.x.array[:n_local] = (
    phi_00.x.array[:n_local] - rau_00.x.array[:n_local] / rau_00_au_squared
)
energy_gradient_00.x.scatter_forward()

# Initial search direction
search_direction_00.x.array[:n_local] = -energy_gradient_00.x.array[:n_local]
search_direction_00.x.scatter_forward()

# Update solution
tau_00 = 0.0
phi_0.x.array[:n_local] = (
    phi_00.x.array[:n_local] + tau_00 * search_direction_00.x.array[:n_local]
)
phi_0.x.scatter_forward()

# Normalize globally
norm_phi0 = l2_norm(phi_0,domain, quadrature_degree)
phi_0.x.array[:n_local] /= norm_phi0
phi_0.x.scatter_forward()

# Energy
energy_0 = energy(phi_0, domain, potential)
energy_error = energy_0 - energy_00


if MPI.COMM_WORLD.rank == 0:
    print(f"Energy: {energy_0}")








######################################################### Update rule ################################################################












tol=10**(-11)
iteration = 0
error_energy=tol+1
counter=0

while error_energy>tol:
        iteration += 1
        counter +=1

        # Find Projected gradient
        v = ufl.TrialFunction(V)
        w = ufl.TestFunction(V)
        a = au(v, w, phi_0, domain)
        L = inner(phi_0, w) * dx(degree=quadrature_degree)
        problem = dolfinx.fem.petsc.LinearProblem(a, L, bcs=[bc])
        rau_0=problem.solve() #Ritz representation
        rau_0.x.scatter_forward()

        rau_0_au_squared=fem.assemble_scalar(fem.form(au(rau_0,rau_0,phi_0,domain)))
        rau_0_au_squared = comm.allreduce(rau_0_au_squared, op=MPI.SUM)
        
        energy_gradient_0.x.array[:] = phi_0.x.array[:]- rau_0.x.array[:]/rau_0_au_squared #Projected gradient
        energy_gradient_0.x.scatter_forward()
        

        if counter == 10:
                polack_riberie=0
                counter=0
        else:

                
            #Find Polack-Riberie parameter
            grad_dif= energy_gradient_0-energy_gradient_00
            numerator = fem.assemble_scalar(fem.form(au(energy_gradient_0, grad_dif, phi_0, domain)))
            numerator = comm.allreduce(numerator, op=MPI.SUM)
            denominator = fem.assemble_scalar(fem.form(au(energy_gradient_00, energy_gradient_00, phi_00, domain)))
            denominator = comm.allreduce(denominator, op=MPI.SUM)
            polack_riberie = max(0.0, numerator.real / denominator.real)


        #Find search direction
        direction_00_inner_product = fem.assemble_scalar(fem.form(inner(phi_0, search_direction_00) * dx(degree=quadrature_degree)))
        direction_00_inner_product = comm.allreduce(direction_00_inner_product, op=MPI.SUM)
        direction_00_projected.x.array[:] = search_direction_00.x.array[:] - (rau_0.x.array[:] / rau_0_au_squared) * direction_00_inner_product
        direction_00_projected.x.scatter_forward()
        search_direction_0.x.array[:] = -energy_gradient_0.x.array[:] + polack_riberie * direction_00_projected.x.array[:]
        search_direction_0.x.scatter_forward()


        #Find the step size
        (grad_phi_grad_phi, grad_phi_grad_d, grad_d_grad_d, grad_d_grad_phi,
            phi_phi, phi_d, d_d, d_phi,
            pot_phi_phi, pot_phi_d, pot_d_d, pot_d_phi,
            phi_Lz_phi, phi_Lz_d, d_Lz_phi, d_Lz_d,
            phi_phi_phi_phi,phi_phi_phi_d,phi_phi_d_phi,phi_d_phi_phi,d_phi_phi_phi,
            phi_d_phi_d,phi_phi_d_d,phi_d_d_phi,d_phi_phi_d,d_phi_d_phi,d_d_phi_phi,
            phi_d_d_d,d_phi_d_d,d_d_phi_d,d_d_d_phi,d_d_d_d)=inner_products(search_direction_0,phi_0,Lz,potential,domain,quadrature_degree)
        
        energy_function = lambda tau: energy_at_tau(tau, grad_phi_grad_phi, grad_phi_grad_d, grad_d_grad_d, grad_d_grad_phi,
            phi_phi, phi_d, d_d, d_phi,
            pot_phi_phi, pot_phi_d, pot_d_d, pot_d_phi,
            phi_Lz_phi, phi_Lz_d, d_Lz_phi, d_Lz_d,
            phi_phi_phi_phi,phi_phi_phi_d,phi_phi_d_phi,phi_d_phi_phi,d_phi_phi_phi,
            phi_d_phi_d,phi_phi_d_d,phi_d_d_phi,d_phi_phi_d,d_phi_d_phi,d_d_phi_phi,
            phi_d_d_d,d_phi_d_d,d_d_phi_d,d_d_d_phi,d_d_d_d, beta,omega)
        

        
        result = minimize_scalar(energy_function, method="bounded",  bounds=(1e-3, 10))        
        tau_0 = result.x 

     


        #Check if descent direction
        check_product=fem.assemble_scalar(fem.form(inner(search_direction_00,phi_0)*dx))
        check_product = comm.allreduce(check_product, op=MPI.SUM)
        check = 1-polack_riberie*(check_product)

 

        #Update solution
        phi_new.x.array[:] = phi_0.x.array[:] + tau_0 * search_direction_0.x.array[:]
        phi_new.x.scatter_forward()

        phi_new.x.array[:] = phi_new.x.array[:] / l2_norm(phi_new, domain, quadrature_degree)
        phi_new.x.scatter_forward()

        energy_new = energy(phi_new, domain, potential).real

        # Compute the difference of consequent wavefunctions
        error_energy = abs(energy_new - energy_0)
        error_solution = l2_norm(phi_new - phi_0, domain, quadrature_degree)

        if rank == 0:
            print("Energy convergence:", error_energy)
            print("Solution convergence:", error_solution)
            print("Polack-Riberire parameter:", polack_riberie)
            print('\n')
            print("", flush=True)


        #Update
        phi_00.x.array[:] = phi_0.x.array[:]
        phi_00.x.scatter_forward()

        energy_gradient_00.x.array[:]= energy_gradient_0.x.array[:]
        energy_gradient_00.x.scatter_forward()

        search_direction_00.x.array[:] = search_direction_0.x.array[:]
        search_direction_00.x.scatter_forward()

        phi_0.x.array[:] = phi_new.x.array[:]
        phi_0.x.scatter_forward()

        energy_0 = energy_new







### Measure execution time
comm.Barrier()
t_end = MPI.Wtime()

local_time = t_end - t_start
total_time = comm.allreduce(local_time, op=MPI.MAX)

if rank == 0:
    print(f"Total runtime: {total_time:.6f} seconds")






######################################################### Final ground state, phase, density ################################################################




### Final ground state: real and imaginary parts
phi_real = fem.Function(V)
phi_real.x.array[:] = np.real(phi_new.x.array)
phi_real.x.scatter_forward()
phi_real.name = "phi_real"

phi_imag = fem.Function(V)
phi_imag.x.array[:] = np.imag(phi_new.x.array)
phi_imag.x.scatter_forward()
phi_imag.name = "phi_imag"

### Final energy
final_energy = energy(phi_new, domain, potential)
if rank == 0:
    print(f"Final energy: {final_energy}")





















######################################################### Save the ground state, density and phase ################################################################


run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
folder_name = f"gs_{run_id}_eps{epsilon}_h{h}"
output_dir = os.path.join("results", folder_name)

if rank == 0:
    os.makedirs(output_dir, exist_ok=True)

comm.Barrier()

metadata = {
    "epsilon": epsilon,
    "h": h,
    "k": k,
    "omega_unscaled": omega_unscaled,
    "beta_unscaled": beta_unscaled,
    "kappa": kappa,
    "gamma_x": gamma_x,
    "gamma_y": gamma_y,
    "omega": omega,
    "beta": beta,
    "final_energy": float(final_energy),
    "xmin": xmin,
    "xmax": xmax,
    "ymin": ymin,
    "ymax": ymax,
    "N_x": N_x,
    "N_y": N_y
    
}

if rank == 0:
    with open(os.path.join(output_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

# 1) Ground state for restart / interpolation
checkpoint_file = os.path.join(output_dir, "ground_state.bp")

adios4dolfinx.write_mesh(checkpoint_file, domain)
adios4dolfinx.write_function(checkpoint_file, phi_real, time=0.0, name="phi_real")
adios4dolfinx.write_function(checkpoint_file, phi_imag, time=0.0, name="phi_imag")

# 2) Ground state for later Python / Matplotlib postprocessing
xdmf_path = os.path.join(output_dir, "ground_state.xdmf")

with XDMFFile(comm, xdmf_path, "w") as xdmf:
    xdmf.write_mesh(domain)
    xdmf.write_function(phi_real)
    xdmf.write_function(phi_imag)

if rank == 0:
    print(f"Saved results in: {output_dir}")


sys.exit()
