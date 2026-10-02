"""
Branching Conflict Experiment v1.0
Objective: Calculate the finite-depth residual R_D for a recursive k-ary tree.

Node counts use Python integers so k**d is not cut off at int64. The minimizer
is the original finite-D critical point

    x0* = bar_x * sum_{d=0}^{D} (k a)^d / sum_{d=0}^{D} (k a^2)^d

with R_D the fraction of nodes whose level state misses bar_x by more than epsilon.
It is not a proof of an asymptotic floor and it is not a fit to 0.08.
"""

import math


def _geom_log_sum(ratio, depth):
    """log(sum_{d=0}^{depth} ratio^d). ratio must be >= 0."""
    depth = int(depth)
    if depth < 0:
        raise ValueError("depth must be non-negative")
    ratio = float(ratio)
    if ratio < 0.0:
        raise ValueError("ratio must be non-negative")
    if ratio == 0.0:
        return 0.0  # only the d=0 term, which is 1
    if ratio == 1.0:
        return math.log(depth + 1.0)
    n = depth + 1
    if ratio < 1.0:
        log_rn = n * math.log(ratio)
        rn = math.exp(log_rn) if log_rn > -700.0 else 0.0
        return math.log(1.0 - rn) - math.log(1.0 - ratio)
    log_rn = n * math.log(ratio)
    inv = math.exp(-log_rn) if log_rn < 700.0 else 0.0
    return log_rn + math.log1p(-inv) - math.log(ratio - 1.0)


def _as_depth(depth):
    if isinstance(depth, bool) or not isinstance(depth, (int, float)):
        raise TypeError("depth must be an integer")
    if int(depth) != depth or depth < 0:
        raise ValueError("depth must be a non-negative integer")
    return int(depth)


def _as_branching(k):
    if isinstance(k, bool) or not isinstance(k, (int, float)):
        raise TypeError("k must be an integer branching factor")
    if int(k) != k or k < 1:
        raise ValueError("k must be an integer >= 1")
    return int(k)


def optimal_root(depth, k=3, a=0.8, bar_x=1.0):
    """Unique minimizer of sum_d k^d (a^d x0 - bar_x)^2 on a depth-D k-ary tree."""
    depth = _as_depth(depth)
    k = _as_branching(k)
    a = float(a)
    bar_x = float(bar_x)
    if not math.isfinite(a) or a <= 0.0:
        raise ValueError("a must be finite and > 0")
    if not math.isfinite(bar_x):
        raise ValueError("bar_x must be finite")
    log_s1 = _geom_log_sum(k * a, depth)
    log_s2 = _geom_log_sum(k * (a * a), depth)
    return bar_x * math.exp(log_s1 - log_s2)


def level_state(depth_index, x0, a):
    """State at graph distance depth_index from the root, x = a^d x0."""
    d = _as_depth(depth_index)
    a = float(a)
    x0 = float(x0)
    if a <= 0.0:
        raise ValueError("a must be > 0")
    if d == 0 or a == 1.0 or x0 == 0.0:
        return x0 if d == 0 or a == 1.0 else 0.0
    return x0 * math.exp(d * math.log(a))


def calculate_residual(depth, k=3, a=0.8, epsilon=0.05, bar_x=1.0):
    """
    Residual R_D: fraction of nodes with |a^d x0* - bar_x| > epsilon.

    Node counts are Python integers, so depths past the int64 overflow of
    numpy's k**d (for example k=3, D=40) stay exact until the final division.
    """
    depth = _as_depth(depth)
    k = _as_branching(k)
    a = float(a)
    epsilon = float(epsilon)
    bar_x = float(bar_x)
    if not math.isfinite(epsilon):
        raise ValueError("epsilon must be finite")
    x0 = optimal_root(depth, k=k, a=a, bar_x=bar_x)
    # Python ints, not numpy int64: k**d overflows signed 64-bit at modest depth
    # (k=3, d=40) and the old sum then returned a wrong residual.
    violated = 0
    total = 0
    nodes = 1
    for d in range(depth + 1):
        if abs(level_state(d, x0, a) - bar_x) > epsilon:
            violated += nodes
        total += nodes
        nodes *= k
    return violated / total


if __name__ == "__main__":
    print("Depth | Residual (R_D)")
    for D in range(16):
        R_D = calculate_residual(D)
        print(f"{D:5d} | {R_D:.6f}")
