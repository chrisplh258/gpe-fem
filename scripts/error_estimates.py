import dolfinx
import numpy as np
import ufl
import basix.ufl
import sys
import os
import json
import yaml
import csv
import re

from dolfinx.fem import petsc
from dolfinx import fem
from petsc4py.PETSc import ScalarType
from mpi4py import MPI
from datetime import datetime

# External functions
from fem_gpe.norms import scaled_h1_norm
from fem_gpe.load_precomputed import load_ground_state_from_bp
from fem_gpe.phase_shift import phase_shift
from fem_gpe.boundary_conditions import homogeneous_dirichlet_bc


# ======================= Load config =======================

if len(sys.argv) > 1:
    config_file = sys.argv[1]
else:
    raise ValueError("Provide config file, e.g. configs/error_est/config.yaml")

with open(config_file, "r") as f:
    config = yaml.safe_load(f)


def load_metadata(run_dir):
    with open(os.path.join(run_dir, "metadata.json"), "r") as f:
        return json.load(f)


# MPI
comm = MPI.COMM_WORLD
rank = comm.rank

# Paths
ref_dir = config["reference_solution"]["path"]
coarse_dirs = config["coarse_solutions"]

if not isinstance(coarse_dirs, list) or len(coarse_dirs) == 0:
    raise ValueError("coarse_solutions must be a non-empty list.")

# Load reference solution
domain_ref, V_ref, phi_ref = load_ground_state_from_bp(ref_dir)
ref_meta = load_metadata(ref_dir)

# Parameters
epsilon = ref_meta["epsilon"]
quadrature_degree = config["error"]["quadrature_degree"]
degree = config["error"]["degree"]


# ======================= Precompute reference gradient =======================

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


# ======================= Loop over coarse solutions =======================

all_errors = []

for h_dir in coarse_dirs:

    # Load coarse solution
    domain_coarse, V_coarse, phi_coarse = load_ground_state_from_bp(h_dir)
    coarse_meta = load_metadata(h_dir)

    # ---------- Energy error ----------
    energy_error = abs(coarse_meta["final_energy"] - ref_meta["final_energy"])

    # ---------- Interpolate coarse -> fine ----------
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

    # Phase shift
    phi_shifted = phase_shift(phi_coarse_to_fine, V_ref, phi_ref)
    phi_shifted.x.scatter_forward()

    # ---------- H1 FEM error ----------
    H1_error_fem = scaled_h1_norm(
        epsilon,
        phi_ref - phi_shifted,
        domain_ref,
        quadrature_degree,
    )

    # ================= H1 interpolation error =================

    # Step 2: phi_ref -> coarse (quadrature)
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

    # Step 3: grad(phi_ref) -> coarse
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

    # Step 4: Projection solve
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

    bc_coarse, _ = homogeneous_dirichlet_bc(domain_coarse, V_coarse)
    problem = dolfinx.fem.petsc.LinearProblem(a_coarse, L_coarse, bcs=[bc_coarse])
    Ih_phi_ref = problem.solve()
    Ih_phi_ref.x.scatter_forward()

    # Step 5: back to reference mesh
    Ih_on_ref = fem.Function(V_ref, dtype=ScalarType)

    cells_to_ref = np.arange(
        V_ref.mesh.topology.index_map(V_ref.mesh.topology.dim).size_local,
        dtype=np.int32,
    )

    interp_back = fem.create_interpolation_data(
        V_to=V_ref,
        V_from=Ih_phi_ref.function_space,
        cells=cells_to_ref,
        padding=1e-12,
    )

    Ih_on_ref.interpolate_nonmatching(
        Ih_phi_ref,
        cells=cells_to_ref,
        interpolation_data=interp_back,
    )
    Ih_on_ref.x.scatter_forward()

    # Step 6: error
    H1_interpolation_error = scaled_h1_norm(
        epsilon,
        phi_ref - Ih_on_ref,
        domain_ref,
        quadrature_degree,
    )

    # Store
    all_errors.append({
    "h": coarse_meta["h"],
    "H1_fem_error": float(H1_error_fem),
    "H1_interpolation_error": float(H1_interpolation_error),
    "energy_error": float(energy_error),
    })

    all_errors.sort(key=lambda x: x["h"])
# ======================= Save =======================

# ======================= Save =======================

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
error_dir = os.path.join("results", "error_estimates")
error_file = os.path.join(
    error_dir, f"errors_eps{epsilon}_{run_id}.json"
)
csv_file = os.path.join(
    error_dir, f"errors_eps{epsilon}_{run_id}.csv"
)

# Sort by mesh size
all_errors.sort(key=lambda x: x["h"])

if rank == 0:
    os.makedirs(error_dir, exist_ok=True)

    print(f"Saving error estimates to: {os.path.abspath(error_file)}", flush=True)
    print(f"Saving CSV to: {os.path.abspath(csv_file)}", flush=True)

    error_data = {
        "reference_run": ref_dir,
        "results": all_errors,
    }

    # Save JSON
    with open(error_file, "w") as f:
        json.dump(error_data, f, indent=2)

    # Save CSV
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "epsilon",
            "h",
            "H1_fem_error",
            "H1_interpolation_error",
            "energy_error"
        ])

        for entry in all_errors:
            writer.writerow([
                epsilon,
                entry["h"],
                entry["H1_fem_error"],
                entry["H1_interpolation_error"],
                entry["energy_error"],
            ])

comm.Barrier()