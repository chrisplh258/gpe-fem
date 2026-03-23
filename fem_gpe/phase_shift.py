import ufl
import dolfinx
import numpy as np

from mpi4py import MPI
from petsc4py.PETSc import ScalarType
from dolfinx.fem import Function


""" Apply a global phase rotation to phi_a so that it is optimally aligned with phi_b.
"""


def phase_shift(phi_a, V, phi_b):
    
    comm = V.mesh.comm
    rank = comm.rank

    # Compute the global L2 inner product of phi_a and phi_b
    alpha_temp = ufl.dot(phi_a, ufl.conj(phi_b)) * ufl.dx
    alpha = dolfinx.fem.assemble_scalar(dolfinx.fem.form(alpha_temp))
    alpha = comm.allreduce(alpha, op=MPI.SUM)

    # if rank == 0:
    #     print("L2 inner product before rotation:", alpha, flush=True)

    r = np.abs(alpha)

    if r == 0:
        shift_phase = 1.0 + 0.0j
    else:
        theta = np.arctan2(np.imag(alpha), np.real(alpha))
        shift_phase = np.cos(theta) - 1j * np.sin(theta)

    phi_shifted = Function(V, dtype=ScalarType)
    phi_shifted.x.array[:] = phi_a.x.array[:] * shift_phase
    phi_shifted.x.scatter_forward()

    alpha_rot_temp = ufl.dot(phi_shifted, ufl.conj(phi_b)) * ufl.dx
    alpha_rot = dolfinx.fem.assemble_scalar(dolfinx.fem.form(alpha_rot_temp))
    alpha_rot = comm.allreduce(alpha_rot, op=MPI.SUM)

    # if rank == 0:
    #     print("L2 inner product after rotation:", alpha_rot, flush=True)

    return phi_shifted