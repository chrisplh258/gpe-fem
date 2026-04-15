import os
import json
import adios4dolfinx
import ufl
import numpy as np


from datetime import datetime
from dolfinx import fem
from dolfinx.io import XDMFFile
from dolfinx.fem import Function, functionspace, Expression

def save_ground_state(
    domain,
    phi_new,
    epsilon,
    h,
    k,
    omega_unscaled,
    beta_unscaled,
    kappa,
    gamma_x,
    gamma_y,
    omega,
    beta,
    final_energy,
    xmin,
    xmax,
    ymin,
    ymax,
    init_mode,
    comm,
    rank,
):
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"gs_{run_id}_eps{epsilon}_h{h}"
    output_dir = os.path.join("results", folder_name)

    if rank == 0:
        os.makedirs(output_dir, exist_ok=True)

    comm.Barrier()
    ########################### Save the setup ##########################

    metadata = {
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "h": h,
        "k": k,
        "epsilon": epsilon,
        "omega_unscaled": omega_unscaled,
        "beta_unscaled": beta_unscaled,
        "kappa": kappa,
        "gamma_x": gamma_x,
        "gamma_y": gamma_y,
        "omega": omega,
        "beta": beta,
        "final_energy": float(final_energy),
        "initial_condition_mode": init_mode,
        

    }

    if rank == 0:
        with open(os.path.join(output_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)

    ########################### Checkpoint for restart / interpolation ##########################
    V = phi_new.function_space

    phi_real = fem.Function(V, name="phi_real")
    phi_imag = fem.Function(V, name="phi_imag")

    phi_real.x.array[:] = np.real(phi_new.x.array)
    phi_imag.x.array[:] = np.imag(phi_new.x.array)

    phi_real.x.scatter_forward()
    phi_imag.x.scatter_forward()

    checkpoint_file = os.path.join(output_dir, "ground_state.bp")
    adios4dolfinx.write_mesh(checkpoint_file, domain)
    adios4dolfinx.write_function(checkpoint_file, phi_real, time=0.0, name="phi_real")
    adios4dolfinx.write_function(checkpoint_file, phi_imag, time=0.0, name="phi_imag")




    ########################### Density, phase, amplitude for visualization ##########################
    density = fem.Function(V, name="density")
    amplitude = fem.Function(V, name="amplitude")
    phase = fem.Function(V, name="phase")

    density.x.array[:] = np.abs(phi_new.x.array) ** 2
    amplitude.x.array[:] = np.abs(phi_new.x.array)
    phase.x.array[:] = np.angle(phi_new.x.array)

    density.x.scatter_forward()
    amplitude.x.scatter_forward()
    phase.x.scatter_forward()

    # Save separately for ParaView
    density_path = os.path.join(output_dir, "density.xdmf")
    with XDMFFile(comm, density_path, "w") as xdmf:
        xdmf.write_mesh(domain)
        xdmf.write_function(density)

    # amplitude_path = os.path.join(output_dir, "amplitude.xdmf")
    # with XDMFFile(comm, amplitude_path, "w") as xdmf:
    #     xdmf.write_mesh(domain)
    #     xdmf.write_function(amplitude)

    # phase_path = os.path.join(output_dir, "phase.xdmf")
    # with XDMFFile(comm, phase_path, "w") as xdmf:
    #     xdmf.write_mesh(domain)
    #     xdmf.write_function(phase)

        if rank == 0:
            print(f"Saved results in: {output_dir}", flush=True)

        return output_dir