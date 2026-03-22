import dolfinx
import ufl
from ufl import real,imag, grad
from dolfinx import mesh, fem
import numpy as np


def l2_projection(f,V):
    ###L2 projection
    # Set up the projection problem

    u = ufl.TrialFunction(V)
    v = ufl.TestFunction(V)
    f_proj=dolfinx.fem.Function(V)
    a = ufl.inner(u, v) * ufl.dx
    L = ufl.inner(f, v) * ufl.dx # Projecting the coarse solution onto the finer mesh

    # Create a Dirichlet boundary condition for zero values at the boundary
    zero = fem.Constant(V.mesh, 0.0)  # A constant function equal to zero
    bc = fem.dirichletbc(zero, fem.locate_dofs_geometrical(V, lambda x: np.full(x.shape[1], True)))


    # Solve the L2 projection problem
    problem = dolfinx.fem.petsc.LinearProblem(a, L, bc=[bc])
    f_proj=problem.solve()
    return f_proj