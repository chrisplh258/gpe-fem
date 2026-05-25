# Gross-Pitaevskii Ground State Solver

A parallel FEM solver for computing the ground state of a rotating 
Bose-Einstein Condensate (BEC) via Riemannian conjugate gradient 
optimization, built with FEniCSx and MPI.

---

**Key features:**
- Finite Element discretization via [FEniCSx](https://fenicsproject.org/)
- MPI parallelism through PETSc
- YAML-based configuration for parameter sweeps
- Docker support for reproducible environments
- Error estimation and spectral gap utilities

---

## Requirements

- Python 3.11+
- FEniCSx 0.8
- MPI (OpenMPI or MPICH)
- conda or Docker

---

## Installation

### Option 1 — conda

```bash
git clone https://github.com/your-username/fem-gpe.git
cd fem-gpe

# Real-valued problems
conda env create -f environment-real.yml
conda activate fem-gpe-real

# Complex-valued problems
conda env create -f environment-complex.yml
conda activate fem-gpe-complex

pip install -e .
```

### Option 2 — Docker

```bash
docker build -t fem-gpe .
docker run --rm -v $(pwd)/results:/app/results fem-gpe
```

---

## Quick start

```bash
# Single core
python scripts/rscg_gs.py --config configs/ground_state/config.yaml

# Parallel
mpirun -n 4 python scripts/rscg_gs.py --config configs/ground_state/config.yaml
```

Results are saved to `results/` with a timestamped folder.

---

## Project structure
