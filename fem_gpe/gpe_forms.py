import ufl
from dolfinx import fem
from dolfinx.fem import Function
from petsc4py.PETSc import ScalarType
from mpi4py import MPI
from ufl import SpatialCoordinate,grad, inner, imag, real, dx


# Trapping potential
def V_pot(kappa, gamma_x, gamma_y, V):
    trap_potential = Function(V, dtype=ScalarType)
    trap_potential.interpolate(
        lambda x: kappa * (gamma_x**2 * x[0]**2 + gamma_y**2 * x[1]**2)
    )
    trap_potential.x.scatter_forward()
    return trap_potential

# Effective potential
def Vef(gamma_x, gamma_y,V,omega,kappa ):
    trap_potential = Function(V)
    trap_potential.interpolate(
        lambda x: 
        kappa*((gamma_x**2 * x[0]**2 + gamma_y**2 * x[1]**2))-1/4*(omega**2)*(x[0]**2 +  x[1]**2)
    )    
    return trap_potential


# Angular momentum
def Lz(phi,domain): 
    x = SpatialCoordinate(domain)
    Lz_phi = -1j* (x[0] * grad(phi)[1] - x[1] * grad(phi)[0])
    return Lz_phi

# Energy
def energy(phi, domain, potential, beta, omega, quadrature_degree):
    energy_functional = 0.5 * (
        inner(grad(phi), grad(phi))
        + inner(potential * phi, phi)
        + 0.5 * beta * inner(phi, phi)**2
        - omega * inner(Lz(phi, domain), phi)
    ) * dx(degree=quadrature_degree)

    local_energy = fem.assemble_scalar(fem.form(energy_functional))
    total_energy = domain.comm.allreduce(local_energy, op=MPI.SUM)

    return total_energy.real


### Linearization of E'(u)
def au(v, w, phi, domain, potential, omega, beta, quadrature_degree):
    a_form = (
        inner(grad(v), grad(w))
        + potential * inner(v, w)
        - omega * inner(Lz(v, domain), w)
        + beta * inner((real(phi)**2 + imag(phi)**2) * v, w)
    ) * dx(degree=quadrature_degree)

    return a_form



