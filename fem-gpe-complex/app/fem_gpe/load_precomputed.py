from pathlib import Path
import numpy as np
from mpi4py import MPI
from dolfinx import fem
from petsc4py.PETSc import ScalarType
import adios4dolfinx

def load_ground_state_from_bp(output_dir, element=("Lagrange", 1), engine="BP4"):
    comm = MPI.COMM_WORLD
    output_dir = Path(output_dir)
    checkpoint_file = output_dir / "ground_state.bp"

    domain = adios4dolfinx.read_mesh(checkpoint_file, comm, engine=engine)
    V = fem.functionspace(domain, element)

    phi_real = fem.Function(V)
    phi_real.name = "phi_real"
    adios4dolfinx.read_function(checkpoint_file, phi_real, time=0.0, name="phi_real")
    phi_real.x.scatter_forward()

    phi_imag = fem.Function(V)
    phi_imag.name = "phi_imag"
    adios4dolfinx.read_function(checkpoint_file, phi_imag, time=0.0, name="phi_imag")
    phi_imag.x.scatter_forward()

    phi = fem.Function(V, dtype=ScalarType)
    phi.x.array[:] = phi_real.x.array[:] + 1j * phi_imag.x.array[:]
    phi.x.scatter_forward()
    phi.name = "phi"

    return domain, V, phi