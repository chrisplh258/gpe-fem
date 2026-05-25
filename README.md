# Gross-Pitaevskii Ground State Solver

A parallel 2D FEM solver for computing the ground state of a rotating
Bose-Einstein Condensate (BEC) via Riemannian conjugate gradient
optimization, built with FEniCSx and MPI.

---

## Key Features

- **MPI parallel** — scales across multiple cores via PETSc and mpi4py
- **FEM discretization** — conforming Lagrange elements on triangular meshes
  with configurable polynomial degree, built on FEniCSx (DOLFINx)
- **RSCG optimization** — Riemannian Sobolev conjugate gradient with
  energy-adaptive Sobolev metric and Polak–Ribière momentum
- **Flexible initialization** — Gaussian vortex ansatz, precomputed
  solution, or coarse-mesh projection
- **Multi-resolution** — sweep over multiple mesh sizes in a single run
- **YAML-driven** — all parameters via config files, no source edits needed
- **Timestamped output** — ground state, density, and full metadata
  saved automatically per run
- **Docker support** — fully reproducible environments across platforms
- **Three ready-to-use scripts**: `rscg_gs.py` (ground state),
  `error_estimates.py` (error between two solutions),
  `energy_spectrum.py` (constrained energy Hessian spectrum)

---

## Installation

Two Docker images are provided depending on the script you want to run:

| Image | Use for |
|---|---|
| `fem-gpe-complex` | Ground state, error estimates |
| `fem-gpe-real` | Spectrum (requires real-valued PETSc) |

### 1. Build

```bash
docker build -t fem-gpe-complex --build-arg ENV_FILE=environment-complex.yml .
docker build -t fem-gpe-real --build-arg ENV_FILE=environment-real.yml .
```

### 2. Run

Mount the working directory so that results are saved to your machine:

```bash
docker run --rm -it \
  -v "$(pwd):/app" \
  -v "$(pwd)/results:/app/results" \
  fem-gpe-complex
```

> **Note:** without the volume mount, all output files are lost when
> the container exits.

---

## Quick Start

Run all scripts inside the container with `mpirun`.
Adjust `-n` to the number of cores available on your machine.

**Ground state**
```bash
mpirun -n 2 python3 scripts/rscg_gs.py configs/ground_state/config.yaml
```

**Error estimates**
```bash
mpirun -n 2 python3 scripts/error_estimates.py configs/error_est/config.yaml
```

**Spectrum** (use `fem-gpe-real` container)
```bash
mpirun -n 2 python3 scripts/energy_spectrum.py configs/spectrum/config.yaml
```

Results are saved automatically to `results/` with a timestamped folder.

---

## Project Structure

```
fem-gpe/
├── fem_gpe/                    # Core library
│   ├── boundary_conditions.py  # Homogeneous Dirichlet BC
│   ├── domain_setup.py         # Mesh and function space creation
│   ├── gpe_forms.py            # Variational forms (energy, potential, angular momentum)
│   ├── initial_conditions.py   # Initialization modes
│   ├── inner_products.py       # Sobolev inner products
│   ├── norms.py                # L2 and H1 norms
│   ├── phase_shift.py          # Phase correction utilities
│   ├── projection.py           # L2 projection
│   ├── save_results.py         # Output: ground state, density, metadata
│   └── step_size.py            # Line search
│
├── configs/
│   ├── ground_state/           # Config for ground state computation
│   ├── error_est/              # Configs for convergence studies
│   └── spectrum/               # Config for spectral computation
│
├── scripts/
│   ├── rscg_gs.py              # Ground state solver
│   ├── error_estimates.py      # Error estimation between two solutions
│   ├── energy_spectrum.py      # Constrained energy Hessian spectrum
│
├── results/                    # Output directory 
├── Dockerfile
├── environment-complex.yml     # Conda env for ground state and error estimates
├── environment-real.yml        # Conda env for spectrum computation
└── pyproject.toml
```
