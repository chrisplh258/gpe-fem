import numpy as np
import ufl
import basix.ufl
import dolfinx.fem.petsc

from dolfinx import fem
from mpi4py import MPI


def l2_projection(uh, mesh_coarse, V_coarse, bc_coarse, degree=4, padding=1e-8):
    uh.x.scatter_forward()

    Qe = basix.ufl.quadrature_element(mesh_coarse.topology.cell_name(), degree=degree)
    Vq = fem.functionspace(mesh_coarse, Qe)

    tdim = mesh_coarse.topology.dim
    cell_imap = mesh_coarse.topology.index_map(tdim)
    cells = np.arange(cell_imap.size_local + cell_imap.num_ghosts, dtype=np.int32)

    interp_data = fem.create_interpolation_data(
        V_to=Vq,
        V_from=uh.function_space,
        cells=cells,
        padding=padding,
    )

    q_func = fem.Function(Vq, dtype=np.complex128)
    q_func.interpolate_nonmatching(uh, cells=cells, interpolation_data=interp_data)
    q_func.x.scatter_forward()

    u = ufl.TrialFunction(V_coarse)
    v = ufl.TestFunction(V_coarse)

    a = ufl.inner(u, v) * ufl.dx
    L = ufl.inner(q_func, v) * ufl.dx(metadata={"quadrature_degree": degree})

    problem = dolfinx.fem.petsc.LinearProblem(a, L, bcs=[bc_coarse])
    u_coarse = problem.solve()
    u_coarse.x.scatter_forward()

    mass_form = fem.form(ufl.conj(u_coarse) * u_coarse * ufl.dx)
    local_mass = fem.assemble_scalar(mass_form)
    mass = mesh_coarse.comm.allreduce(local_mass, op=MPI.SUM)
    # if mesh_coarse.comm.rank == 0:
    #     print("Projected ||u_coarse||^2 =", mass.real)

    return u_coarse