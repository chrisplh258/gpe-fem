import numpy as np
from dolfinx import mesh, fem
from dolfinx.fem import Function
from petsc4py.PETSc import ScalarType


def homogeneous_dirichlet_bc(domain, V):
    
    phi_D = Function(V, dtype=np.complex128)
    phi_D.x.array[:] = ScalarType(0)
    phi_D.x.scatter_forward()

    topology = domain.topology
    tdim = topology.dim
    fdim = tdim - 1
    topology.create_connectivity(fdim, tdim)

    boundary_facets = mesh.exterior_facet_indices(domain.topology)
    boundary_dofs = fem.locate_dofs_topological(V, fdim, boundary_facets)

    bc = fem.dirichletbc(phi_D, boundary_dofs)
    return bc, boundary_dofs
