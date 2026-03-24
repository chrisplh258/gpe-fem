import os
import json
from datetime import datetime

import adios4dolfinx
from dolfinx.io import XDMFFile


def save_ground_state(
    domain,
    phi_real,
    phi_imag,
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

    # Checkpoint for restart / interpolation
    checkpoint_file = os.path.join(output_dir, "ground_state.bp")
    adios4dolfinx.write_mesh(checkpoint_file, domain)
    adios4dolfinx.write_function(checkpoint_file, phi_real, time=0.0, name="phi_real")
    adios4dolfinx.write_function(checkpoint_file, phi_imag, time=0.0, name="phi_imag")

    # XDMF export for postprocessing (visualization)
    xdmf_path = os.path.join(output_dir, "ground_state.xdmf")
    with XDMFFile(comm, xdmf_path, "w") as xdmf:
        xdmf.write_mesh(domain)
        xdmf.write_function(phi_real)
        xdmf.write_function(phi_imag)

    if rank == 0:
        print(f"Saved results in: {output_dir}", flush=True)

    return output_dir