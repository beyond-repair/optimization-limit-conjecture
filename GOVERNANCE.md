# Governance lock — optimization-limit-conjecture

**Sweep:** 120  
**Classification:** RESEARCH  
**Claim cap:** Formal conjecture + finite-depth numerical residual. Not a theorem. Not a physical derivation of W*. Not validated research.

## Status

| Field | Value |
|-------|--------|
| Tests | tests/test_residual.py (finite-D formula, int64 overflow regression, CLI) |
| CI | .github/workflows/ci.yml |
| Proofs | Proofs/TheoremA.tex is a draft, not a published proof |
| Residual implementation | experiments/branching_conflict_experiment.py; core.py refuses the removed infinite shortcut |

## Forbidden claims

- Do not claim Theorem A/B/C/D are proved.
- Do not claim W* ≈ 0.08 is derived or measured here.
- Do not promote to ACTIVE without operator review after green CI + SECURITY.md.

`requirements.txt` is the install path. The stray `(requirements.txt` file and the duplicate sweep module were removed so they cannot be installed or imported by mistake.
