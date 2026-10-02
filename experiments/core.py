"""
Compatibility shim.

experiments/core.py previously exposed an infinite-depth shortcut whose root
was the inverted formula x0 = bar_x (1-ka)/(1-ka^2), and a grid search aimed
at 0.08. Both are removed. Finite-depth residuals live in
branching_conflict_experiment.calculate_residual.

See PROOF_13A_LIMIT_CORRECTION.md.
"""

try:
    from branching_conflict_experiment import calculate_residual as _finite_residual
except ImportError:  # imported as experiments.core
    from experiments.branching_conflict_experiment import calculate_residual as _finite_residual


def calculate_residual(*args, use_analytical_limit=False, **kwargs):
    if use_analytical_limit:
        raise ValueError(
            "use_analytical_limit was removed. It used the inverted infinite-depth "
            "root (PROOF_13A_LIMIT_CORRECTION.md). Omit it to compute the finite-depth residual."
        )
    return _finite_residual(*args, **kwargs)


def find_optimal_theta(*_args, **_kwargs):
    raise RuntimeError(
        "find_optimal_theta was removed. It searched for a match to 0.08 with the "
        "inverted infinite-depth formula. This repository does not fit that target."
    )
