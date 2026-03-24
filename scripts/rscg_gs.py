import dolfinx
import numpy as np
import ufl
import sys
import yaml

from dolfinx import fem
from dolfinx.fem import petsc, Function
from mpi4py import MPI
from ufl import  inner, dx
from scipy.optimize import minimize_scalar




# External functions
from fem_gpe.norms import l2_norm
from fem_gpe.step_size import energy_at_tau
from fem_gpe.inner_products import inner_products
from fem_gpe.load_precomputed import load_ground_state_from_bp
from fem_gpe.projection import l2_projection
from fem_gpe.boundary_conditions import homogeneous_dirichlet_bc
from fem_gpe.domain_setup import create_domain_and_space
from fem_gpe.initial_conditions import superposition_ic, init_projected_reference, choose_initial_condition
from fem_gpe.gpe_forms import V_pot, Lz, energy, au
from fem_gpe.save_results import save_ground_state



# Get config file from command line
if len(sys.argv) > 1:
    config_file = sys.argv[1]
else:
    raise ValueError("Please provide a config file, e.g. configs/ground_state/config.yaml")

with open(config_file, "r") as f:
    config = yaml.safe_load(f)




######################################################### Computational domain ################################################################






# Load mesh parameters from config
xmin = config["mesh"]["domain"]["xmin"]
ymin = config["mesh"]["domain"]["ymin"]
xmax = config["mesh"]["domain"]["xmax"]
ymax = config["mesh"]["domain"]["ymax"]

k = config["mesh"]["resolution"]["k"]
degree = config["mesh"]["element"]["degree"]

comm = MPI.COMM_WORLD
rank = comm.rank

# Define the mesh step size from the refinement level
h = 2**(-k)

# Mesh
domain, V, mesh_info = create_domain_and_space(comm, xmin, ymin, xmax, ymax, h, degree)

if rank == 0:
    print("h", mesh_info["h"])
    print("DOFs", mesh_info["num_dofs_global"])

# Boundary conditions
bc, boundary_dofs = homogeneous_dirichlet_bc(domain, V)




######################################################### Physical quantities and parameters ################################################################



# Physical parameters
epsilon = config["physics"]["epsilon"]

omega_unscaled = config["physics"]["omega_unscaled"]
beta_unscaled = config["physics"]["beta_unscaled"]

gamma_x = config["physics"]["potential_unscaled"]["gamma_x"]
gamma_y = config["physics"]["potential_unscaled"]["gamma_y"]
kappa = config["physics"]["potential_unscaled"]["trap_strength"]

potential_unscaled = V_pot(kappa, gamma_x, gamma_y, V)



omega=omega_unscaled/epsilon
beta=beta_unscaled/(epsilon**2)
potential= potential_unscaled/(epsilon**2)

# Integration degree
quadrature_degree = config["solver"]["quadrature_degree"]




######################################################### Choose Initial conditions ################################################################




# Initial condition from config
init_mode = config["initial_condition"]["mode"]
init_path = config["initial_condition"]["path"]

if init_mode in ["loaded_state", "projected_reference"] and init_path is None:
    raise ValueError(f"'path' must be provided for init_mode='{init_mode}'")

domain, V, bc, potential, phi_00 = choose_initial_condition(
    init_mode,
    init_path,
    domain,
    V,
    omega,
    quadrature_degree,
    kappa,
    gamma_x,
    gamma_y,
    epsilon,
    V_pot,
)


### Energy

energy_00 = energy(phi_00, domain, potential, beta, omega, quadrature_degree)
if MPI.COMM_WORLD.rank == 0:
    print(f"Initial energy: {energy_00}")







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

a = au(v, w, phi_00, domain, potential, omega, beta, quadrature_degree)
L = ufl.inner(phi_00, w) * dx_q

problem = petsc.LinearProblem(a, L, bcs=[bc])
rau_00 = problem.solve()
rau_00.x.scatter_forward()

# Global scalar rau_00_au_squared
rau_form = fem.form(au(rau_00, rau_00, phi_00, domain, potential, omega, beta, quadrature_degree))
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
energy_0 = energy(phi_0, domain, potential, beta, omega, quadrature_degree)

if MPI.COMM_WORLD.rank == 0:
    print(f"Energy: {energy_0}")








######################################################### Update rule ################################################################












tol = config["solver"]["tolerance"]
iteration = 0
error_energy=tol+1
counter=0

while error_energy>tol:
        iteration += 1
        counter +=1

        # Find Projected gradient
        v = ufl.TrialFunction(V)
        w = ufl.TestFunction(V)
        a = au(v, w, phi_0, domain, potential, omega, beta, quadrature_degree)
        L = inner(phi_0, w) * dx(degree=quadrature_degree)
        problem = petsc.LinearProblem(a, L, bcs=[bc])
        rau_0=problem.solve() #Ritz representation
        rau_0.x.scatter_forward()

        rau_0_au_squared=fem.assemble_scalar(fem.form(au(rau_0,rau_0,phi_0,domain, potential, omega, beta, quadrature_degree)))
        rau_0_au_squared = comm.allreduce(rau_0_au_squared, op=MPI.SUM)
        
        energy_gradient_0.x.array[:] = phi_0.x.array[:]- rau_0.x.array[:]/rau_0_au_squared #Projected gradient
        energy_gradient_0.x.scatter_forward()
        

        if counter == 10:
                polack_riberie=0
                counter=0
        else:

                
            #Find Polack-Riberie parameter
            grad_dif= energy_gradient_0-energy_gradient_00
            numerator = fem.assemble_scalar(fem.form(au(energy_gradient_0, grad_dif, phi_0, domain, potential, omega, beta, quadrature_degree)))
            numerator = comm.allreduce(numerator, op=MPI.SUM)
            denominator = fem.assemble_scalar(fem.form(au(energy_gradient_00, energy_gradient_00, phi_00, domain, potential, omega, beta, quadrature_degree)))
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

        energy_new = energy(phi_new, domain, potential, beta, omega, quadrature_degree).real

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
final_energy = energy(phi_new, domain, potential, beta, omega, quadrature_degree)
if rank == 0:
    print(f"Final energy: {final_energy}")









######################################################### Save the ground state, density and phase ################################################################


output_dir = save_ground_state(
    domain=domain,
    phi_real=phi_real,
    phi_imag=phi_imag,
    epsilon=epsilon,
    h=h,
    k=k,
    omega_unscaled=omega_unscaled,
    beta_unscaled=beta_unscaled,
    kappa=kappa,
    gamma_x=gamma_x,
    gamma_y=gamma_y,
    omega=omega,
    beta=beta,
    final_energy=final_energy,
    xmin=xmin,
    xmax=xmax,
    ymin=ymin,
    ymax=ymax,
    init_mode=init_mode,
    comm=comm,
    rank=rank,
)

sys.exit()
