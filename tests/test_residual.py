"""Unit tests for residual calculator. Does not prove the conjecture."""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from branching_conflict_experiment import calculate_residual  # noqa: E402


def test_residual_in_unit_interval():
    r = calculate_residual(5, k=3, a=0.8, epsilon=0.05)
    assert 0.0 <= r <= 1.0


def test_depth_zero_no_violation_default_params():
    r = calculate_residual(0, k=3, a=0.8, epsilon=0.05)
    assert r == 0.0


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
