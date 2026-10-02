"""Sweep the propagation parameter a at fixed depth, branching factor, and tolerance."""

import csv
import os

try:
    from branching_conflict_experiment import calculate_residual
except ImportError:  # imported as experiments.parameter_sweep
    from experiments.branching_conflict_experiment import calculate_residual

import numpy as np


def run_sweep(k=3, epsilon=0.05, bar_x=1.0, depth=20, a_min=0.1, a_max=0.99, count=50):
    """Return (a, R_D) pairs. Does not search for or fit an external target."""
    results = []
    for a in np.linspace(a_min, a_max, count):
        val = calculate_residual(depth, k=k, a=float(a), epsilon=epsilon, bar_x=bar_x)
        results.append((float(a), float(val)))
    return results


def write_sweep_csv(path, rows):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["a_parameter", "residual_R_D"])
        for a, val in rows:
            writer.writerow([f"{a:.10g}", f"{val:.10g}"])
    return path


if __name__ == "__main__":
    data_dir = os.path.join(os.getcwd(), "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, "residual_surface.csv")
    data = run_sweep()
    write_sweep_csv(csv_path, data)
    print("Sweep complete. CSV at:", csv_path)
