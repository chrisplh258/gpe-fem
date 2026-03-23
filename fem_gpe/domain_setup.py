import math
from dolfinx import mesh, fem



def create_domain_and_space(comm, xmin, ymin, xmax, ymax, h):
    # Compute number of cells
    N_x = math.ceil((xmax - xmin) / h)
    N_y = math.ceil((ymax - ymin) / h)

    dofs_estimate = (N_x + 1) * (N_y + 1)

    # Create mesh
    domain = mesh.create_rectangle(
        comm=comm,
        points=[[xmin, ymin], [xmax, ymax]],
        n=(N_x, N_y),
        cell_type=mesh.CellType.triangle,
    )

    topology = domain.topology

    # Function space
    V = fem.functionspace(domain, ("Lagrange", 1))

    info = {
        "h": h,
        "N_x": N_x,
        "N_y": N_y,
        "dofs_estimate": dofs_estimate,
        "num_nodes_local": topology.index_map(0).size_local,
        "num_nodes_global": topology.index_map(0).size_global,
        "num_dofs_local": V.dofmap.index_map.size_local,
        "num_dofs_global": V.dofmap.index_map.size_global,
    }

    return domain, V, info