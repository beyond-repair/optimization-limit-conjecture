#!/usr/bin/env python3
"""
Optimization-Limit Conjecture CLI Entry Point
Usage: python main.py --mode [experiment|sweep|theoremA]
"""

import argparse
import os
import sys
sys.path.append('experiments')

from branching_conflict_experiment import calculate_residual
from parameter_sweep import run_sweep

def run_experiment(depth=10, k=3, a=0.8, epsilon=0.05):
    R_D = calculate_residual(depth, k, a, epsilon)
    print(f"Depth {depth}: Residual R_D = {R_D:.6f}")
    return R_D

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimization-Limit Conjecture Framework")
    parser.add_argument('--mode', choices=['experiment', 'sweep', 'theoremA'], default='experiment')
    parser.add_argument('--depth', type=int, default=15)
    parser.add_argument('--k', type=int, default=3)
    parser.add_argument('--a', type=float, default=0.8)
    parser.add_argument('--epsilon', type=float, default=0.05)
    
    args = parser.parse_args()
    
    if args.mode == 'experiment':
        run_experiment(args.depth, args.k, args.a, args.epsilon)
    elif args.mode == 'sweep':
        os.makedirs('data', exist_ok=True)
        data = run_sweep(k=args.k, epsilon=args.epsilon, depth=args.depth)
        print("Sweep completed. Results in data/residual_surface.csv")
    elif args.mode == 'theoremA':
        print("Theorem A: Unique optimizer exists (see Proofs/TheoremA.tex)")
        # Future: symbolic validation hook
