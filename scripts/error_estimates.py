import dolfinx
import numpy as np
import ufl
import basix.ufl
import sys
import os
import json


from dolfinx.fem import petsc
from dolfinx import  fem
from petsc4py.PETSc import ScalarType
from mpi4py import MPI
from datetime import datetime


#External functions
from fem_gpe.norms import scaled_h1_norm
from fem_gpe.load_precomputed import load_ground_state_from_bp
from fem_gpe.phase_shift import phase_shift
from fem_gpe.boundary_conditions import homogeneous_dirichlet_bc


def load_metadata(run_dir):
    with open(os.path.join(run_dir, "metadata.json"), "r") as f:
        return json.load(f)



# MPI
comm = MPI.COMM_WORLD
rank = comm.rank

# Scaling parameter
epsilon = 0.1

#Integration degree
quadrature_degree = 3

#polynomial degree
degree = 1

# Load reference (fine) solution
ref_dir = "results/gs_20260323_125141_eps0.1_h0.00390625"
domain_ref, V_ref, phi_ref = load_ground_state_from_bp(ref_dir)


#Load coarse solution 
h_dir = "results/gs_20260323_131257_eps0.1_h0.125"
domain_coarse, V_coarse, phi_coarse = load_ground_state_from_bp(h_dir)



############################################################## Energy error ################################################################

ref_meta = load_metadata(ref_dir)
coarse_meta = load_metadata(h_dir)

energy_ref = ref_meta["final_energy"]
energy_coarse = coarse_meta["final_energy"]

energy_error = abs(energy_coarse - energy_ref)

############################################################## Computation of H1_ε -Finite Element error ################################################################


# Interpolate coarse solution onto the reference (fine) mesh
phi_coarse_to_fine = fem.Function(V_ref, dtype=ScalarType)

tdim = V_ref.mesh.topology.dim
cells_to = np.arange(
    V_ref.mesh.topology.index_map(tdim).size_local,
    dtype=np.int32,
)

interp_data = fem.create_interpolation_data(
    V_to=V_ref,
    V_from=phi_coarse.function_space,
    cells=cells_to,
    padding=1e-12,
)

phi_coarse_to_fine.interpolate_nonmatching(
    phi_coarse, cells=cells_to, interpolation_data=interp_data
)
phi_coarse_to_fine.x.scatter_forward()

# Phase-shift the interpolated coarse solution
phi_coarse_to_fine_shifted = phase_shift(phi_coarse_to_fine, V_ref, phi_ref)
phi_coarse_to_fine_shifted.x.scatter_forward()




# H1_ε -Finite Element error
H1_error_fem=scaled_h1_norm(epsilon,phi_ref-phi_coarse_to_fine_shifted,domain_ref,quadrature_degree)





############################################################## Computation of H1-interpolation error ################################################################



# Step 1: represent grad(phi_ref)(ufl expression) as a vector-valued finite element function on the same reference mesh.
V_ref_grad = fem.functionspace(
    domain_ref,
    ("Lagrange", degree, (domain_ref.geometry.dim,))
)

u = ufl.TrialFunction(V_ref_grad)
v = ufl.TestFunction(V_ref_grad)

a = ufl.inner(u, v) * ufl.dx
L = ufl.inner(ufl.grad(phi_ref), v) * ufl.dx

problem = dolfinx.fem.petsc.LinearProblem(a, L)
grad_phi_ref = problem.solve()
grad_phi_ref.x.scatter_forward()

# Step 2: Transfer phi_ref to coarse mesh (quadrature representation)
Qe_scalar = basix.ufl.quadrature_element(
    domain_coarse.topology.cell_name(),
    degree=quadrature_degree,
)

Vq_scalar = fem.functionspace(domain_coarse, Qe_scalar)

cells_coarse = np.arange(
    domain_coarse.topology.index_map(domain_coarse.topology.dim).size_local,
    dtype=np.int32,
)

interp_phi = fem.create_interpolation_data(
    V_to=Vq_scalar,
    V_from=phi_ref.function_space,
    cells=cells_coarse,
    padding=1e-5,
)

phi_ref_on_coarse = fem.Function(Vq_scalar, dtype=ScalarType)
phi_ref_on_coarse.interpolate_nonmatching(
    phi_ref,
    cells=cells_coarse,
    interpolation_data=interp_phi,
)
phi_ref_on_coarse.x.scatter_forward()


# Step 3: Transfer grad(phi_ref) to coarse mesh (quadrature representation)
Qe_vector = basix.ufl.quadrature_element(
    domain_coarse.topology.cell_name(),
    value_shape=(domain_coarse.geometry.dim,),
    degree=quadrature_degree,
)

Vq_vector = fem.functionspace(domain_coarse, Qe_vector)

interp_grad = fem.create_interpolation_data(
    V_to=Vq_vector,
    V_from=grad_phi_ref.function_space,
    cells=cells_coarse,
    padding=1e-5,
)

grad_phi_ref_on_coarse = fem.Function(Vq_vector, dtype=ScalarType)
grad_phi_ref_on_coarse.interpolate_nonmatching(
    grad_phi_ref,
    cells=cells_coarse,
    interpolation_data=interp_grad,
)
grad_phi_ref_on_coarse.x.scatter_forward()


# Step 4: Solve the scaled H1 projection problem on the coarse mesh
u = ufl.TrialFunction(V_coarse)
v = ufl.TestFunction(V_coarse)

a_coarse = (
    (1 / epsilon**2) * ufl.inner(u, v)
    + ufl.inner(ufl.grad(u), ufl.grad(v))
) * ufl.dx

L_coarse = (
    (1 / epsilon**2) * ufl.inner(phi_ref_on_coarse, v)
    + ufl.inner(grad_phi_ref_on_coarse, ufl.grad(v))
) * ufl.dx

bc_coarse, boundary_dofs_coarse = homogeneous_dirichlet_bc(domain_coarse, V_coarse)
problem = dolfinx.fem.petsc.LinearProblem(a_coarse, L_coarse, bcs=[bc_coarse])
Ih_phi_ref = problem.solve()
Ih_phi_ref.x.scatter_forward()


# Step 5: Interpolate the coarse scaled-H1 projection back to the reference mesh so that it can be compared directly with phi_ref 
Ih_phi_ref_on_ref = fem.Function(V_ref, dtype=ScalarType)

tdim_ref = V_ref.mesh.topology.dim
cells_to_ref = np.arange(
    V_ref.mesh.topology.index_map(tdim_ref).size_local,
    dtype=np.int32,
)

interp_data_back = fem.create_interpolation_data(
    V_to=V_ref,
    V_from=Ih_phi_ref.function_space,
    cells=cells_to_ref,
    padding=1e-12,
)

Ih_phi_ref_on_ref.interpolate_nonmatching(
    Ih_phi_ref,
    cells=cells_to_ref,
    interpolation_data=interp_data_back,
)
Ih_phi_ref_on_ref.x.scatter_forward()


# Step 6: Compute the scaled H1 interpolation error on the reference mesh
H1_interpolation_error = scaled_h1_norm(
    epsilon,
    phi_ref - Ih_phi_ref_on_ref,
    domain_ref,
    quadrature_degree,
)













############################################################## Save the results ################################################################

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
error_dir = "error_estimates"
error_file = os.path.join(error_dir, f"errors_{run_id}.json")

if rank == 0:
    os.makedirs(error_dir, exist_ok=True)

comm.Barrier()

error_data = {
    "reference_run": ref_dir,
    "coarse_run": h_dir,
    "H1_fem_error": float(H1_error_fem),
    "H1_interpolation_error": float(H1_interpolation_error),
    "energy_error": float(energy_error),
}

if rank == 0:
    with open(error_file, "w") as f:
        json.dump(error_data, f, indent=2)




sys.exit()
