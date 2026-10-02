#!/usr/bin/env python3
"""
Optimization-Limit Conjecture CLI.

Usage (from the repository root):
    python main.py --mode experiment --depth 10
    python main.py --mode sweep --depth 20
    python main.py --mode theoremA
"""

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPERIMENTS = ROOT / "experiments"
if str(EXPERIMENTS) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS))

from branching_conflict_experiment import calculate_residual  # noqa: E402
from parameter_sweep import run_sweep, write_sweep_csv  # noqa: E402


def run_experiment(depth=10, k=3, a=0.8, epsilon=0.05, bar_x=1.0):
    residual = calculate_residual(depth, k, a, epsilon, bar_x)
    miss = abs(residual - 0.08)
    print(
        f"Depth {depth}: Residual R_D = {residual:.6f} "
        f"(k={k}, a={a}, epsilon={epsilon}, bar_x={bar_x})"
    )
    print(f"|R_D - 0.08| = {miss:.6f} (external motivator; not a target this run fits)")
    if k * a >= 1.0:
        print(
            f"ka = {k * a:.6g} >= 1, so the infinite geometric root does not apply. "
            "This is the finite-depth residual only."
        )
    return residual


def main(argv=None):
    parser = argparse.ArgumentParser(description="Optimization-Limit Conjecture finite-depth residual")
    parser.add_argument("--mode", choices=["experiment", "sweep", "theoremA"], default="experiment")
    parser.add_argument("--depth", type=int, default=15)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--a", type=float, default=0.8)
    parser.add_argument("--epsilon", type=float, default=0.05)
    parser.add_argument("--bar-x", type=float, default=1.0, dest="bar_x")
    parser.add_argument(
        "--out",
        default=None,
        help="Sweep CSV path (default: ./data/residual_surface.csv)",
    )
    args = parser.parse_args(argv)

    if args.mode == "experiment":
        run_experiment(args.depth, args.k, args.a, args.epsilon, args.bar_x)
    elif args.mode == "sweep":
        rows = run_sweep(k=args.k, epsilon=args.epsilon, bar_x=args.bar_x, depth=args.depth)
        out = args.out or os.path.join(os.getcwd(), "data", "residual_surface.csv")
        write_sweep_csv(out, rows)
        residuals = [val for _a, val in rows]
        closest = min(rows, key=lambda pair: abs(pair[1] - 0.08))
        print(f"Sweep completed. {len(rows)} rows written to {out}")
        print(f"R_D range at depth {args.depth}: min={min(residuals):.6f} max={max(residuals):.6f}")
        print(
            f"Closest |R_D - 0.08| on this grid: {abs(closest[1] - 0.08):.6f} "
            f"at a={closest[0]:.6f}, R_D={closest[1]:.6f} (not a fit)"
        )
    elif args.mode == "theoremA":
        print("Theorem A is a draft, not a proof. Finite-D root: Proofs/TheoremA.tex.")
        print("The D->infinity factor order in that file was inverted and is corrected there.")
        print("See PROOF_13A_LIMIT_CORRECTION.md. Default (k, a)=(3, 0.8) has ka>1.")
        print("This mode does not evaluate a residual.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
