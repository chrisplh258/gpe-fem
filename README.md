# Gross-Pitaevskii Ground State Solver

A parallel 2D FEM solver for computing the ground state of a rotating
Bose-Einstein Condensate (BEC) via Riemannian conjugate gradient
optimization, built with FEniCSx and MPI.

---

## Key Features

- **MPI parallel** — scales across multiple cores via PETSc and mpi4py
- **FEM discretization** — Lagrange elements on triangular meshes
  with configurable polynomial degree p, built on FEniCSx (DOLFINx)
- **RSCG optimization** — Riemannian Sobolev conjugate gradient with
  energy-adaptive Sobolev metric and Polak–Ribière momentum
- **Flexible initialization** — Gaussian vortex ansatz, precomputed
  solution, or coarse-mesh projection
- **Multi-resolution** — sweep over multiple mesh sizes in a single run
- **YAML-driven** — all parameters via config files, no source edits needed
- **Output** — ground state, density, and full metadata
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

---

## Configuration

All scripts are controlled via YAML config files in `configs/`. No source
code edits are needed.

### Ground state — `configs/ground_state/config.yaml`

```yaml
mesh:
  domain:
    xmin: -0.9   # computational domain boundaries
    xmax: 0.9
    ymin: -1.4
    ymax: 1.4
  resolution:    # mesh size h = 2^{-k}, multiple values for a sweep
      k_values:
      - 5  
          
  element:
    degree: 1      # polynomial degree of Lagrange elements

physics:
  epsilon: 0.45        # scaling parameter (1 = unscaled problem)
  beta_unscaled: 10    # interaction strength
  omega_unscaled: 9    # rotation frequency
  potential_unscaled:
    gamma_x: 1.25      # harmonic trapping potential of the form: V(x)=trap_strength*( gamma_x*x^2 + gamma_y*y^2)
    gamma_y: 0.98
    trap_strength: 26

solver:
  quadrature_degree: 3
  tolerance: 1.0e-11

initial_condition:
  mode: superposition   # superposition | loaded_state | projected_reference
  path: null            # required for loaded_state and projected_reference
```

### Error estimates — `configs/error_est/config.yaml`

```yaml
reference_solution:
  path: results/...    # path to the fine reference solution

coarse_solutions:      # list of coarser solutions to compare against
  - results/...
  - results/...

error:
  quadrature_degree: 3
  degree: 1

output:
  directory: error_estimates
```

### Spectrum — `configs/spectrum/config.yaml`

```yaml
ground_state:
  path: results/...    # path to a precomputed ground state

output:
  directory: spectrum
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
