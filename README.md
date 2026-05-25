# Gross-Pitaevskii Ground State Solver

A parallel 2D-FEM solver for computing the ground state of a rotating 
Bose-Einstein Condensate (BEC) via Riemannian conjugate gradient 
optimization, built with FEniCSx and MPI.

---

## Key Features

- **MPI parallel** — scales across multiple cores via PETSc and mpi4py
- **FEM discretization** — conforming Lagrange elements on triangular
  meshes with configurable polynomial degree, built on FEniCSx (DOLFINx)
- **RSCG optimization** — Riemannian Sobolev conjugate gradient with
  energy-adaptive metric and Polak–Ribière momentum
- **Flexible initialization** — Gaussian vortex ansatz, precomputed
  solution, or coarse-mesh projection
- **Multi-resolution** — sweep over multiple mesh sizes in one run
- **YAML-driven** — all parameters via config files, no source edits needed
- **Timestamped output** — ground state, density, and full metadata
  saved automatically per run
- **Docker support** — fully reproducible environments
- **Three scripts**: `rscg_gs.py` (ground state), `error_estimates.py`
  (error between solutions), `energy_spectrum.py` (constrained energy Hessian
  spectrum)

---

## Installation

Two Docker images are provided depending on the computation:

- **Complex** — ground state and error estimates
- **Real** — spectrum computation (requires real-valued PETSc support)

### Build

```bash
# Mac (Apple Silicon / ARM)
docker build -t fem-gpe-complex --build-arg ENV_FILE=environment-complex.yml .
docker build -t fem-gpe-real --build-arg ENV_FILE=environment-real.yml .

# Linux (AMD64) — build on a Linux machine
docker build -t fem-gpe-complex --build-arg ENV_FILE=environment-complex.yml .
docker build -t fem-gpe-real --build-arg ENV_FILE=environment-real.yml .
```

## Installation

Two Docker images are provided depending on the computation:

- **Complex** — ground state and error estimates
- **Real** — spectrum computation (requires real-valued PETSc support)

### Build

```bash
docker build -t fem-gpe-complex --build-arg ENV_FILE=environment-complex.yml .
docker build -t fem-gpe-real --build-arg ENV_FILE=environment-real.yml .
```

### Run

Mount the working directory to persist results on the host machine:

```bash
docker run --rm -it \
  -v "$(pwd):/app" \
  -v "$(pwd)/results:/app/results" \
  fem-gpe-complex
```

> Without the volume mount, any files written inside the container
> are lost when it exits.
