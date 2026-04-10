import os
import sys
import json
import yaml
from pathlib import Path

import numpy as np
import adios4dolfinx
import dolfinx
import ufl

from mpi4py import MPI
from petsc4py import PETSc
from slepc4py import SLEPc

from dolfinx import fem, mesh
from dolfinx.fem import Function
from dolfinx.fem.petsc import assemble_matrix
from dolfinx.mesh import GhostMode
from basix.ufl import mixed_element
from ufl import SpatialCoordinate, grad, inner, dx
from datetime import datetime


########################## LOAD STATE ##########################

def load_ground_state_from_bp(output_dir, element=("Lagrange", 1), engine="BP4"):
    comm = MPI.COMM_WORLD
    checkpoint_file = Path(output_dir) / "ground_state.bp"

    domain = adios4dolfinx.read_mesh(
        checkpoint_file, comm,
        ghost_mode=GhostMode.shared_facet,
        engine=engine,
    )

    V = fem.functionspace(domain, element)

    phi_real = fem.Function(V)
    adios4dolfinx.read_function(checkpoint_file, phi_real, time=0.0, name="phi_real")
    phi_real.x.scatter_forward()

    phi_imag = fem.Function(V)
    adios4dolfinx.read_function(checkpoint_file, phi_imag, time=0.0, name="phi_imag")
    phi_imag.x.scatter_forward()

    return domain, V, phi_real, phi_imag


def load_metadata(run_dir):
    with open(os.path.join(run_dir, "metadata.json"), "r") as f:
        return json.load(f)



########################## OPERATORS ##########################

def Vtr(gamma_x, gamma_y, V, omega, kappa):
    trap = Function(V)
    trap.interpolate(
        lambda x: kappa * (gamma_x**2 * x[0]**2 + gamma_y**2 * x[1]**2)
        - 0.25 * omega**2 * (x[0]**2 + x[1]**2)
    )
    return trap


def Lz_real(phi, domain):
    x = SpatialCoordinate(domain)
    return x[0] * grad(phi)[1] - x[1] * grad(phi)[0]



########################## INPUT ##########################

if len(sys.argv) > 1:
    config_file = sys.argv[1]
else:
    raise ValueError("Provide config file")

with open(config_file, "r") as f:
    config = yaml.safe_load(f)

comm = MPI.COMM_WORLD
rank = comm.rank

run_dir = config["ground_state"]["path"]

domain, V, phi_real, phi_imag = load_ground_state_from_bp(run_dir)
meta = load_metadata(run_dir)

epsilon = meta["epsilon"]
kappa = meta["kappa"]
gamma_x = meta["gamma_x"]
gamma_y = meta["gamma_y"]
omega = meta["omega"]
beta = meta["beta"]
final_energy = meta["final_energy"]

quadrature_degree = 6



########################## SPACES ##########################

mixed_el = mixed_element([V.ufl_element(), V.ufl_element()])
V_mixed = fem.functionspace(domain, mixed_el)



########################## CHEMICAL POTENTIAL ##########################

potential = Vtr(gamma_x, gamma_y, V, 0.0, kappa) / (epsilon**2)

def rot_real(phi_r, phi_i, domain):
    x = SpatialCoordinate(domain)
    return (
        phi_r * (x[0]*grad(phi_i)[1] - x[1]*grad(phi_i)[0]) +
        phi_i * (-x[0]*grad(phi_r)[1] + x[1]*grad(phi_r)[0])
    )

energy = 0.5 * (
    grad(phi_real)**2 + grad(phi_imag)**2 +
    potential * (phi_real**2 + phi_imag**2) +
    0.5 * beta * (phi_real**2 + phi_imag**2)**2 -
    omega * rot_real(phi_real, phi_imag, domain)
) * dx(degree=quadrature_degree)

E = fem.assemble_scalar(fem.form(energy))
E = comm.allreduce(E, op=MPI.SUM)

quartic = (phi_real**2 + phi_imag**2)**2 * dx(degree=quadrature_degree)
Q = fem.assemble_scalar(fem.form(quartic))
Q = comm.allreduce(Q, op=MPI.SUM)

mu = 2 * E + 0.5 * beta * Q

if rank == 0:
    print(f"lambda = {mu}")
    print(f"E = {E}")



########################## HESSIAN ##########################

v = ufl.TrialFunction(V_mixed)
w = ufl.TestFunction(V_mixed)

vr, vi = ufl.split(v)
wr, wi = ufl.split(w)

grad_term = inner(grad(vr), grad(wr)) + inner(grad(vi), grad(wi))

pot_term = (
    potential * (inner(vr, wr) + inner(vi, wi)) +
    beta * (phi_real**2 + phi_imag**2) * (inner(vr, wr) + inner(vi, wi))
)

rot_term = omega * (
    inner(Lz_real(vr, domain), wi) -
    inner(Lz_real(vi, domain), wr)
)

nonlin = 2 * beta * (
    phi_real*phi_real*inner(vr, wr) +
    phi_real*phi_imag*inner(vr, wi) +
    phi_imag*phi_real*inner(vi, wr) +
    phi_imag*phi_imag*inner(vi, wi)
)

a = (grad_term + pot_term + rot_term + nonlin) * dx(degree=quadrature_degree)
m = (inner(vr, wr) + inner(vi, wi)) * dx(degree=quadrature_degree)

A = assemble_matrix(fem.form(a))
A.assemble()

M = assemble_matrix(fem.form(m))
M.assemble()



########################## DOF FILTER ##########################

tdim = domain.topology.dim
fdim = tdim - 1

domain.topology.create_connectivity(fdim, tdim)

facets = mesh.exterior_facet_indices(domain.topology)

dofs_r = fem.locate_dofs_topological(V_mixed.sub(0), fdim, facets)
dofs_i = fem.locate_dofs_topological(V_mixed.sub(1), fdim, facets)

boundary = np.unique(np.concatenate([dofs_r, dofs_i]).astype(np.int32))

local = np.arange(V_mixed.dofmap.index_map.size_local, dtype=np.int32)
interior = np.setdiff1d(local, boundary).astype(np.int32)



########################## GLOBAL MAP ##########################

imap = V_mixed.dofmap.index_map
start, _ = imap.local_range

interior_global = interior + start

is_int = PETSc.IS().createGeneral(interior_global.astype(np.int32), comm=domain.comm)

A = A.createSubMatrix(is_int, is_int)
M = M.createSubMatrix(is_int, is_int)

A.assemble()
M.assemble()



########################## SOLVE ##########################

solver = SLEPc.EPS().create(domain.comm)
solver.setOperators(A, M)
solver.setProblemType(SLEPc.EPS.ProblemType.GHEP)
solver.setDimensions(10)
solver.setTolerances(1e-5, max_it=999999999)
solver.setWhichEigenpairs(SLEPc.EPS.Which.SMALLEST_REAL)

solver.solve()

n = solver.getConverged()

if rank == 0:
    print(f"Number of converged eigenvalues: {n}")

if n < 10:
    raise RuntimeError("Not enough eigenvalues")

for i in range(min(10, n)):
    val = solver.getEigenvalue(i)
    if rank == 0:
        print(val)


########################## SAVE RESULTS ##########################


run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

out_dir = os.path.join("results", "spectrum")
out_file = os.path.join(out_dir, f"spectrum_{run_id}.json")

if rank == 0:
    os.makedirs(out_dir, exist_ok=True)
    print(f"Saving spectrum to: {os.path.abspath(out_file)}", flush=True)

comm.Barrier()

# Collect eigenvalues
eigenvalues = [float(solver.getEigenvalue(i).real) for i in range(min(10, n))]

# Chemical potential
mu_val = float(mu)

# Spectral gap: λ_1 - μ  (second eigenvalue)
spectral_gap = float(eigenvalues[1]-mu_val) if len(eigenvalues) > 1 else None

data = {
    "run_dir": run_dir,
    "epsilon": epsilon,
    "omega": omega,
    "beta": beta,
    "chemical_potential": mu_val,
    "eigenvalues": eigenvalues,
    "spectral_gap": spectral_gap,
}

if rank == 0:
    with open(out_file, "w") as f:
        json.dump(data, f, indent=2)