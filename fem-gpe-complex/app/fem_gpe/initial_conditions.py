import numpy as np
import ufl



from dolfinx.fem import Function
from petsc4py.PETSc import ScalarType
from fem_gpe.load_precomputed import load_ground_state_from_bp


from fem_gpe.boundary_conditions import homogeneous_dirichlet_bc
from fem_gpe.projection import l2_projection
from fem_gpe.norms import l2_norm



def superposition_ic(domain,V,omega,quadrature_degree):
    phi_00=Function(V,dtype=np.complex128)

    phi_00.interpolate(
        lambda x:
            (1 - omega) * (1/np.sqrt(np.pi)*np.exp(-(x[0]**2+x[1]**2)/2))\
            + omega * (1/ufl.sqrt(np.pi) * (x[0] * np.exp(-(x[0]**2 + x[1]**2)/2) + 1j * x[1] * np.exp(-(x[0]**2 + x[1]**2)/2)))
    )
    phi_00.x.scatter_forward()

    #Normalize
    l2_norm_phi_0=l2_norm(phi_00, domain, quadrature_degree)
    phi_00.x.array[:] /= l2_norm_phi_0
    phi_00.x.scatter_forward()

    return phi_00


def init_projected_reference(reference_dir, domain_coarse, V_coarse, bc_coarse):
    # Load fine/reference state
    domain_ref, V_ref, phi_ref = load_ground_state_from_bp(reference_dir)

    # Get boundary dofs on the reference mesh and enforce zero values strongly
    _, boundary_dofs_ref = homogeneous_dirichlet_bc(domain_ref, V_ref)
    phi_ref.x.array[boundary_dofs_ref] = ScalarType(0)
    phi_ref.x.scatter_forward()

    # Project fine/reference state to the coarse space
    phi_00 = l2_projection(phi_ref, domain_coarse, V_coarse, bc_coarse)
    return phi_00



def init_loaded_state_with_mesh(state_dir, kappa, gamma_x, gamma_y, epsilon, V_pot):
    domain, V, phi_00 = load_ground_state_from_bp(state_dir)

    bc, _ = homogeneous_dirichlet_bc(domain, V)
    potential = V_pot(kappa, gamma_x, gamma_y, V) / (epsilon**2)

    return domain, V, bc, potential, phi_00


def choose_initial_condition(
    init_mode,
    init_path,
    domain,
    V,
    omega,
    quadrature_degree,
    kappa,
    gamma_x,
    gamma_y,
    epsilon,
    V_pot,
):
    if init_mode == "superposition":
        bc, _ = homogeneous_dirichlet_bc(domain, V)
        potential = V_pot(kappa, gamma_x, gamma_y, V) / (epsilon**2)
        phi_00 = superposition_ic(domain, V, omega, quadrature_degree)

    elif init_mode == "projected_reference":
        if init_path is None:
            raise ValueError("init_path must be provided for 'projected_reference'")

        bc, _ = homogeneous_dirichlet_bc(domain, V)
        potential = V_pot(kappa, gamma_x, gamma_y, V) / (epsilon**2)
        phi_00 = init_projected_reference(init_path, domain, V, bc)

    elif init_mode == "loaded_state":
        if init_path is None:
            raise ValueError("init_path must be provided for 'loaded_state'")

        domain, V, bc, potential, phi_00 = init_loaded_state_with_mesh(
            init_path, kappa, gamma_x, gamma_y, epsilon, V_pot
        )

    else:
        raise ValueError(f"Unknown init_mode: {init_mode}")

    return domain, V, bc, potential, phi_00
