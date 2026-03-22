##### Energy at tau
def energy_at_tau(tau, grad_phi_grad_phi, grad_phi_grad_d, grad_d_grad_d, grad_d_grad_phi,
            phi_phi, phi_d, d_d, d_phi,
            pot_phi_phi, pot_phi_d, pot_d_d, pot_d_phi,
            phi_Lz_phi, phi_Lz_d, d_Lz_phi, d_Lz_d,
            phi_phi_phi_phi,phi_phi_phi_d,phi_phi_d_phi,phi_d_phi_phi,d_phi_phi_phi,
            phi_d_phi_d,phi_phi_d_d,phi_d_d_phi,d_phi_phi_d,d_phi_d_phi,d_d_phi_phi,
            phi_d_d_d,d_phi_d_d,d_d_phi_d,d_d_d_phi,d_d_d_d, beta,omega):
   
    
    E_kin = grad_phi_grad_phi+ tau*grad_phi_grad_d+ tau**2*grad_d_grad_d+ tau*grad_d_grad_phi
    E_pot = pot_phi_phi + tau*pot_phi_d + tau**2*pot_d_d + tau*pot_d_phi
    E_rot = omega*(phi_Lz_phi+ tau*phi_Lz_d+ tau*d_Lz_phi+ tau**2*d_Lz_d)
   
   
   
    E_non = beta *( phi_phi_phi_phi
     + tau * (phi_phi_phi_d + phi_phi_d_phi +phi_d_phi_phi +d_phi_phi_phi)
     + tau**2 *(phi_d_phi_d + phi_phi_d_d +phi_d_d_phi +d_phi_phi_d+d_phi_d_phi + d_d_phi_phi )
     + tau**3 * (phi_d_d_d + d_phi_d_d + d_d_phi_d +d_d_d_phi)
     + tau**4 * d_d_d_d)

    
   
    #Compute normalization linear term
    N_lin = 2* (1 + tau * (phi_d+d_phi) + tau**2 * d_d)

    # Compute normalization nonlinear term
    
    N_nonlin= 4 *( 1 
        + tau * (2*phi_d + 2*d_phi)
        + tau**2 *(2*d_d + phi_d *phi_d + phi_d*d_phi + d_phi * phi_d +d_phi*d_phi)
        + tau**3 * (phi_d*d_d + d_phi *d_d + d_d*phi_d + d_d*d_phi)
        + tau**4 * d_d*d_d)
    
    # Compute the total energy in respect of tau
    E_total = (E_kin.real + E_pot.real - E_rot.real)/N_lin.real  + E_non.real /N_nonlin.real

    return E_total

    
   