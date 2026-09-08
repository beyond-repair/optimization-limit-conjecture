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

## Usage

```bash
pip install -r requirements.txt
python main.py --mode experiment --depth 10
pytest -q
```

See [CONJECTURE.md](CONJECTURE.md) for the formal statement.

**License:** MIT  
**Initial public formulation:** 2026-06-26
