import dolfinx
import ufl
from ufl import sqrt
from mpi4py import MPI

#Define L2 norm
def l2_norm(phi, domain, quadrature_degree):
    value = dolfinx.fem.assemble_scalar(
        dolfinx.fem.form(ufl.inner(phi, phi) * ufl.dx(degree=quadrature_degree))
    )
    value = domain.comm.allreduce(value, op=MPI.SUM)
    value = sqrt(value.real)
    return value



# Define scaled H1 norm
def scaled_h1_norm(epsilon, phi, domain, quadrature_degree=3):
    expression_1 = l2_norm(ufl.grad(phi), domain, quadrature_degree)**2
    expression_2 = l2_norm(phi, domain, quadrature_degree)**2

    return sqrt((expression_1 + (1 / epsilon**2) * expression_2).real)
