"""Optional residual-vs-a plot. Requires matplotlib (not part of the core install)."""

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from branching_conflict_experiment import calculate_residual


def plot_surface(depth=30, k=3, epsilon=0.05, out_dir=None):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    a_vals = np.linspace(0.1, 0.95, 30)
    res = [calculate_residual(depth, k=k, a=float(a), epsilon=epsilon) for a in a_vals]

    plt.figure(figsize=(8, 5))
    plt.plot(a_vals, res, "b-", linewidth=2)
    plt.xlabel("Propagation parameter a")
    plt.ylabel("Residual R_D")
    plt.title(f"Residual surface (k={k}, epsilon={epsilon}, depth={depth})")
    plt.grid(True)

    data_dir = out_dir or os.path.join(os.getcwd(), "data")
    os.makedirs(data_dir, exist_ok=True)
    save_path = os.path.join(data_dir, "residual_surface.png")
    plt.savefig(save_path)
    plt.close()
    print(f"Plot saved to: {save_path}")
    return save_path


if __name__ == "__main__":
    plot_surface()
