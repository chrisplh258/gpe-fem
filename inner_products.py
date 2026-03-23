from dolfinx import fem
from ufl import inner,grad,dx
from mpi4py import MPI

def assemble_scalar_parallel(form, domain):
    value = fem.assemble_scalar(fem.form(form))
    value = domain.comm.allreduce(value, op=MPI.SUM)
    return value

def inner_products(search_direction_0,phi_0,Lz,potential,domain,quadrature_degree):

    # Compute gradient inner products
    grad_phi_grad_phi = assemble_scalar_parallel(inner(grad(phi_0), grad(phi_0)) * dx(degree=quadrature_degree), domain)
    grad_phi_grad_d = assemble_scalar_parallel(inner(grad(phi_0), grad(search_direction_0)) * dx(degree=quadrature_degree), domain)
    grad_d_grad_d = assemble_scalar_parallel(inner(grad(search_direction_0), grad(search_direction_0)) * dx(degree=quadrature_degree), domain)
    grad_d_grad_phi = assemble_scalar_parallel(inner(grad(search_direction_0), grad(phi_0)) * dx(degree=quadrature_degree), domain)

    # Compute scalar inner products
    phi_phi = assemble_scalar_parallel(inner(phi_0, phi_0) * dx(degree=quadrature_degree), domain)
    phi_d = assemble_scalar_parallel(inner(phi_0, search_direction_0) * dx(degree=quadrature_degree), domain)
    d_d = assemble_scalar_parallel(inner(search_direction_0, search_direction_0) * dx(degree=quadrature_degree), domain)
    d_phi = assemble_scalar_parallel(inner(search_direction_0, phi_0) * dx(degree=quadrature_degree), domain)

    # Compute pot inner products
    pot_phi_phi = assemble_scalar_parallel(inner(potential * phi_0, phi_0) * dx(degree=quadrature_degree), domain)
    pot_phi_d = assemble_scalar_parallel(inner(potential * phi_0, search_direction_0) * dx(degree=quadrature_degree), domain)
    pot_d_d = assemble_scalar_parallel(inner(potential * search_direction_0, search_direction_0) * dx(degree=quadrature_degree), domain)
    pot_d_phi = assemble_scalar_parallel(inner(potential * search_direction_0, phi_0) * dx(degree=quadrature_degree), domain)

    # Compute Lz operator integrals
    phi_Lz_phi = assemble_scalar_parallel(inner(phi_0, Lz(phi_0, domain)) * dx(degree=quadrature_degree), domain)
    phi_Lz_d = assemble_scalar_parallel(inner(Lz(phi_0, domain), search_direction_0) * dx(degree=quadrature_degree), domain)
    d_Lz_phi = assemble_scalar_parallel(inner(search_direction_0, Lz(phi_0, domain)) * dx(degree=quadrature_degree), domain)
    d_Lz_d = assemble_scalar_parallel(inner(search_direction_0, Lz(search_direction_0, domain)) * dx(degree=quadrature_degree), domain)


    # Additional inner products
    phi_phi_phi_phi = assemble_scalar_parallel(
        inner(phi_0, phi_0) * inner(phi_0, phi_0) * dx(degree=quadrature_degree), domain
    )

    phi_phi_phi_d = assemble_scalar_parallel(
        inner(phi_0, phi_0) * inner(phi_0, search_direction_0) * dx(degree=quadrature_degree), domain
    )
    phi_phi_d_phi = assemble_scalar_parallel(
        inner(phi_0, phi_0) * inner(search_direction_0, phi_0) * dx(degree=quadrature_degree), domain
    )
    phi_d_phi_phi = assemble_scalar_parallel(
        inner(phi_0, search_direction_0) * inner(phi_0, phi_0) * dx(degree=quadrature_degree), domain
    )
    d_phi_phi_phi = assemble_scalar_parallel(
        inner(search_direction_0, phi_0) * inner(phi_0, phi_0) * dx(degree=quadrature_degree), domain
    )

    phi_d_phi_d = assemble_scalar_parallel(
        inner(phi_0, search_direction_0) * inner(phi_0, search_direction_0) * dx(degree=quadrature_degree), domain
    )
    phi_phi_d_d = assemble_scalar_parallel(
        inner(phi_0, phi_0) * inner(search_direction_0, search_direction_0) * dx(degree=quadrature_degree), domain
    )
    phi_d_d_phi = assemble_scalar_parallel(
        inner(phi_0, search_direction_0) * inner(search_direction_0, phi_0) * dx(degree=quadrature_degree), domain
    )
    d_phi_phi_d = assemble_scalar_parallel(
        inner(search_direction_0, phi_0) * inner(phi_0, search_direction_0) * dx(degree=quadrature_degree), domain
    )
    d_phi_d_phi = assemble_scalar_parallel(
        inner(search_direction_0, phi_0) * inner(search_direction_0, phi_0) * dx(degree=quadrature_degree), domain
    )
    d_d_phi_phi = assemble_scalar_parallel(
        inner(search_direction_0, search_direction_0) * inner(phi_0, phi_0) * dx(degree=quadrature_degree), domain
    )

    phi_d_d_d = assemble_scalar_parallel(
        inner(phi_0, search_direction_0) * inner(search_direction_0, search_direction_0) * dx(degree=quadrature_degree), domain
    )
    d_phi_d_d = assemble_scalar_parallel(
        inner(search_direction_0, phi_0) * inner(search_direction_0, search_direction_0) * dx(degree=quadrature_degree), domain
    )
    d_d_phi_d = assemble_scalar_parallel(
        inner(search_direction_0, search_direction_0) * inner(phi_0, search_direction_0) * dx(degree=quadrature_degree), domain
    )
    d_d_d_phi = assemble_scalar_parallel(
        inner(search_direction_0, search_direction_0) * inner(search_direction_0, phi_0) * dx(degree=quadrature_degree), domain
    )

    d_d_d_d = assemble_scalar_parallel(
        inner(search_direction_0, search_direction_0) * inner(search_direction_0, search_direction_0) * dx(degree=quadrature_degree), domain
    )


    return (grad_phi_grad_phi, grad_phi_grad_d, grad_d_grad_d, grad_d_grad_phi,
            phi_phi, phi_d, d_d, d_phi,
            pot_phi_phi, pot_phi_d, pot_d_d, pot_d_phi,
            phi_Lz_phi, phi_Lz_d, d_Lz_phi, d_Lz_d,
            phi_phi_phi_phi,phi_phi_phi_d,phi_phi_d_phi,phi_d_phi_phi,d_phi_phi_phi,
            phi_d_phi_d,phi_phi_d_d,phi_d_d_phi,d_phi_phi_d,d_phi_d_phi,d_d_phi_phi,
            phi_d_d_d,d_phi_d_d,d_d_phi_d,d_d_d_phi,d_d_d_d
            )