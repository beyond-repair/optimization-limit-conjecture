"""Unit tests for the finite-depth residual. They do not prove the conjecture."""

import csv
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from branching_conflict_experiment import calculate_residual, level_state, optimal_root  # noqa: E402
from core import calculate_residual as core_residual  # noqa: E402
from core import find_optimal_theta  # noqa: E402
from parameter_sweep import run_sweep, write_sweep_csv  # noqa: E402


def test_residual_in_unit_interval():
    r = calculate_residual(5, k=3, a=0.8, epsilon=0.05)
    assert 0.0 <= r <= 1.0


def test_depth_zero_no_violation_default_params():
    r = calculate_residual(0, k=3, a=0.8, epsilon=0.05)
    assert r == 0.0


def test_depth_one_default_all_nodes_violate():
    # Hand check: x0 = 3.4/2.92, both levels miss bar_x=1 by more than 0.05.
    r = calculate_residual(1, k=3, a=0.8, epsilon=0.05, bar_x=1.0)
    assert r == 1.0


def test_root_matches_finite_geometric_formula():
    k, a, depth, bar_x = 3, 0.8, 2, 1.0
    r1 = k * a
    r2 = k * a * a
    sum1 = (r1 ** (depth + 1) - 1.0) / (r1 - 1.0)
    sum2 = (r2 ** (depth + 1) - 1.0) / (r2 - 1.0)
    assert math.isclose(
        optimal_root(depth, k=k, a=a, bar_x=bar_x),
        bar_x * sum1 / sum2,
        rel_tol=0,
        abs_tol=1e-12,
    )


def test_pre_overflow_depth_matches_direct_sum():
    """Depth 15 fits in int64; lock the value the original power-sum printed."""
    r = calculate_residual(15, k=3, a=0.8, epsilon=0.05, bar_x=1.0)
    assert math.isclose(r, 0.777777772615428, rel_tol=0, abs_tol=1e-12)


def test_depth_40_is_not_the_int64_overflow_value():
    """k**40 overflows int64 and the old code returned 1. The finite-D value does not."""
    r = calculate_residual(40, k=3, a=0.8, epsilon=0.05, bar_x=1.0)
    assert r != 1.0
    assert 0.7 < r < 0.8
    assert math.isfinite(r)


def test_monotonic_node_count_increases_depth():
    r3 = calculate_residual(3)
    r8 = calculate_residual(8)
    assert 0.0 <= r3 <= 1.0
    assert 0.0 <= r8 <= 1.0


def test_large_epsilon_zero_residual():
    r = calculate_residual(4, k=2, a=0.5, epsilon=10.0)
    assert r == 0.0


def test_finite_and_numeric():
    r = calculate_residual(6, k=2, a=0.9, epsilon=0.1)
    assert np.isfinite(r)


def test_infinite_root_inside_convergence_domain():
    """Correct limit is bar_x (1-ka^2)/(1-ka), only when ka<1. Not the inverted draft."""
    k, a = 2, 0.4
    assert k * a < 1.0
    x_inf = (1.0 - k * a * a) / (1.0 - k * a)
    x_wrong = (1.0 - k * a) / (1.0 - k * a * a)
    x_big = optimal_root(200, k=k, a=a, bar_x=1.0)
    assert math.isclose(x_big, x_inf, rel_tol=0, abs_tol=1e-8)
    assert not math.isclose(x_big, x_wrong, rel_tol=0, abs_tol=1e-3)


def test_core_shim_matches_and_refuses_removed_paths():
    assert core_residual(5, k=3, a=0.8, epsilon=0.05) == calculate_residual(5)
    try:
        core_residual(5, use_analytical_limit=True)
    except ValueError as exc:
        assert "inverted" in str(exc)
    else:
        raise AssertionError("analytical shortcut should fail closed")
    try:
        find_optimal_theta()
    except RuntimeError as exc:
        assert "0.08" in str(exc)
    else:
        raise AssertionError("0.08 search should fail closed")


def test_sweep_writes_csv(tmp_path):
    rows = run_sweep(k=3, epsilon=0.05, depth=4, count=5)
    assert len(rows) == 5
    path = write_sweep_csv(str(tmp_path / "residual_surface.csv"), rows)
    with open(path, newline="") as handle:
        parsed = list(csv.reader(handle))
    assert parsed[0] == ["a_parameter", "residual_R_D"]
    assert len(parsed) == 6
    for row in parsed[1:]:
        value = float(row[1])
        assert 0.0 <= value <= 1.0


def test_cli_experiment_and_sweep(tmp_path):
    experiment = subprocess.run(
        [sys.executable, str(ROOT / "main.py"), "--mode", "experiment", "--depth", "10"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Residual R_D = 0.777777" in experiment.stdout
    assert "|R_D - 0.08|" in experiment.stdout
    out = tmp_path / "residual_surface.csv"
    sweep = subprocess.run(
        [
            sys.executable,
            str(ROOT / "main.py"),
            "--mode",
            "sweep",
            "--depth",
            "6",
            "--out",
            str(out),
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    assert out.is_file()
    assert "Closest |R_D - 0.08|" in sweep.stdout
    theorem = subprocess.run(
        [sys.executable, str(ROOT / "main.py"), "--mode", "theoremA"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "not a proof" in theorem.stdout

def test_depth_10_exact_fraction_documented_in_readme():
    """README quotes this rational. It is not 0.08."""
    from fractions import Fraction

    depth, k, a, epsilon, bar_x = 10, 3, 0.8, 0.05, 1.0
    x0 = optimal_root(depth, k=k, a=a, bar_x=bar_x)
    violated = 0
    total = 0
    nodes = 1
    for d in range(depth + 1):
        if abs(level_state(d, x0, a) - bar_x) > epsilon:
            violated += nodes
        total += nodes
        nodes *= k
    assert Fraction(violated, total) == Fraction(68890, 88573)
    residual = calculate_residual(depth, k=k, a=a, epsilon=epsilon, bar_x=bar_x)
    assert residual == 68890 / 88573
    assert abs(residual - 0.08) > 0.6

