# ETN School 2026 — PEPS tutorial

PEPS Tutorial materials for the [European Tensor Network School 2026](https://www.newton.ac.uk/event/mmbw02/).

## Installation

```bash
python -m pip install numpy scipy torch matplotlib jupyterlab
```

For the toric-code and variational optimization notebooks, also install YASTN:

```bash
python -m pip install "git+https://github.com/yastn/yastn.git"
```

## The two-dimensional classical Ising model

[Exercise](notebooks/Ising_exercise.ipynb) · [Solution](notebooks/Ising_sol.ipynb)

- Construct a tensor-network representation of the partition function.
- Approximate the infinite environment using CTMRG.
- Compute the partition function per site and magnetization.
- Use automatic differentiation to obtain magnetization and specific heat.

## Variational optimization

[Notebook](notebooks/Heisenberg_optimization.ipynb)

- Define the Heisenberg energy and optimize an iPEPS with YASTN and PyTorch.

## Toric code

[Exercise](notebooks/Toric_code_exercise.ipynb) · [Solution](notebooks/Toric_code_sol.ipynb)

- Construct $\mathbb Z_2$-symmetric tensors and a toric-code PEPS.
- Measure local stabilizers with the supplied CTMRG setup.
- Extract the topological correction from the second Rényi entropy.
- Explore spin correlations and finite-torus checks in the solution appendices.
