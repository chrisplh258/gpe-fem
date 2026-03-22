import dolfinx
import math
import numpy as np
import ufl
from dolfinx import mesh, fem
from dolfinx.fem import FunctionSpace,Function,petsc
from mpi4py import MPI
from petsc4py.PETSc import ScalarType



def reference_domain(h,dom):
    # Define corners of the rectangle
    xmin,ymin=-dom,-dom
    xmax,ymax=dom,dom

    # Calculate the number of divisions for each axis
    divisions_x=math.ceil((xmax - xmin)/h)
    divisions_y=math.ceil((ymax - ymin)/h)

    # Create the mesh
    domain = mesh.create_rectangle(comm=MPI.COMM_WORLD,
                                points=[[xmin, ymin], [xmax, ymax]],
                                n=(divisions_x, divisions_y),
                                cell_type=mesh.CellType.triangle)

    return domain


def reference_function_space(domain):
    V = fem.functionspace(domain, ("Lagrange", 1))
    return V


def boundary_conditions(domain,V):
    topology=domain.topology

    # Define boundary value
    phi_D=Function(V,dtype=np.complex128)
    phi_D.x.array[:]=ScalarType(0)
    phi_D.x.scatter_forward()

    # Create facet to cell connectivity required to determine boundary facets
    tdim = topology.dim
    fdim = tdim - 1
    topology.create_connectivity(fdim, tdim)
    boundary_facets = mesh.exterior_facet_indices(domain.topology)

    boundary_dofs = fem.locate_dofs_topological(V, fdim, boundary_facets)
    bc = fem.dirichletbc(phi_D, boundary_dofs)
    return bc



