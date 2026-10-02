<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║   ATOMIC DREAM LABS  ·  BEYOND-REPAIR                        ║
╚══════════════════════════════════════════════════════════════╝
```

# Optimization-Limit Conjecture

### Research framework for obstruction floors in recursively constrained graphs.

[![Lifecycle](https://img.shields.io/badge/●_RESEARCH-a855f7?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/Claim_≤1-22c55e?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)
[![Governance](https://img.shields.io/badge/ADL--Governance-7c3aed?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)

```
LIFECYCLE   RESEARCH
CLAIM       ≤ 1   framework
NOT CLAIMED proved asymptotic floor
```

</div>

---
## ▌ STATUS

Classification follows [ADL-Governance](https://github.com/beyond-repair/ADL-Governance). A README facelift does not raise claim level. Physics and pharmacology stay at the evidenced cap. CI green is not experimental validation.

---

## ▌ PRESERVED BODY

# optimization-limit-conjecture

A formal **research** framework for investigating whether an asymptotic obstruction floor exists in recursively constrained graph families (the Optimization-Limit Conjecture).

**Classification:** RESEARCH (ADL-Governance Sweep-120)  
**Claim cap:** computational residual on finite k-ary trees. Not a proof. Not a physical constant.

## Abstract
This repository presents the **Optimization-Limit Conjecture**, a mathematical research program investigating whether certain empirical invariants, including the empirical motivator (W* ≈ 0.08), *may* arise as asymptotic obstruction limits in recursively constrained optimization problems. That matching is an **optimization target**, not a result.

## Status
- Current phase: formulation + finite-depth numerics.
- Tests: `pytest` residual bounds (`tests/test_residual.py`).
- CI: GitHub Actions `ci.yml`.
- Theorem drafts live in `Proofs/`; they are **not** established theorems.

## Install

Python 3.10 or newer. There is no compile step and no config file. Parameters are CLI flags.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

Defaults are `--mode experiment --depth 15 --k 3 --a 0.8 --epsilon 0.05 --bar-x 1`.

```bash
python main.py --mode experiment --depth 10
python main.py --mode sweep --depth 20
python main.py --mode theoremA
```

`sweep` writes `data/residual_surface.csv` (columns `a_parameter`, `residual_R_D`). `theoremA` only points at the draft proof; it does not evaluate a residual.

Optional plot (not required for tests):

```bash
python -m pip install -r requirements-viz.txt
python experiments/visualize.py
```

## Test

```bash
pytest -q
```

## Numbers this program prints

These are outputs of the finite-depth residual, not a fit and not a theorem.

- `python main.py --mode experiment --depth 10` prints `Residual R_D = 0.777777` and `|R_D - 0.08| = 0.697777`.
- The depth-10 value is the float of the exact fraction 68890/88573 = 0.7777765233197476. The distance to the external motivator 0.08 is 0.6977765233197476. That is a miss.
- Default `ka = 2.4 >= 1`, so the infinite geometric root does not apply. The old int64 path returned 1.0 at depth 40 because `3**40` overflowed. The repaired depth-40 residual is the float of 14183943035566416934/18236498188585393201, which prints as 0.7777777777777778. That float collides with `7/9`, but the rational is not `7/9`.
- `python main.py --mode sweep --depth 20` (50 values of `a` in [0.1, 0.99]) prints `R_D` from 0.001372 to 1.000000. Closest sample to 0.08: `|R_D - 0.08| = 0.031111` at `a=0.935510`, `R_D=0.111111`. The grid was not refined to chase 0.08.

See [CONJECTURE.md](CONJECTURE.md) for the formal statement. Theorem drafts in `Proofs/` are not established theorems.

**License:** MIT  
**Initial public formulation:** 2026-06-26

---

<div align="center">

**REWRITE · BUILD · TRANSCEND**

**William (Brian) Ware** · [Atomic Dream Labs](https://github.com/beyond-repair)  
Governing source: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) · [Claim levels 0–5](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)

</div>
