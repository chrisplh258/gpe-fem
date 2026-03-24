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


def homogeneous_dirichlet_bc_mixed(domain, V_mixed):
    """
    Homogeneous Dirichlet BCs on both components of a mixed real-imaginary space.
    """
    topology = domain.topology
    tdim = topology.dim
    fdim = tdim - 1
    topology.create_connectivity(fdim, tdim)

    boundary_facets = mesh.exterior_facet_indices(domain.topology)

    bc_real = fem.dirichletbc(
        ScalarType(0),
        fem.locate_dofs_topological(V_mixed.sub(0), fdim, boundary_facets),
        V_mixed.sub(0),
    )

    bc_imag = fem.dirichletbc(
        ScalarType(0),
        fem.locate_dofs_topological(V_mixed.sub(1), fdim, boundary_facets),
        V_mixed.sub(1),
    )

    return [bc_real, bc_imag]