# 13A correction (2026-09-23)

Full writeup: https://github.com/beyond-repair/-ware-constant-derivation/blob/main/PROOF_13A_RECURSIVE_LIMIT.md

Theorem A finite-D formula is correct.

The D→∞ line in Proofs/TheoremA.tex is **wrong**:

    written: x0^∞ = x̄ (1-ka)/(1-ka^2)
    correct, when a<1/k: x0^∞ = x̄ (1-ka^2)/(1-ka)

Default (k,a)=(3,0.8) lies **outside** the convergence domain (ka=2.4>1).

R_D in CONJECTURE.md is a node-violation fraction, depends on ε/|x̄|, and is not a spectral coupling. min_Θ |W(Θ)-0.08| is matching, not a theorem.

The invariant object is ρ(k,a)=(1-ka^2)/(1-ka), with (k,a) FREE.
