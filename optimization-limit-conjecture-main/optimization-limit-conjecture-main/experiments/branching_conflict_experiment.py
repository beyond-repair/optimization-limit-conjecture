"""
Branching Conflict Experiment v1.0
Objective: Calculate the asymptotic residual R_D for a recursive 3-ary tree.
This experiment provides the numerical evidence for Theorem A (Existence of Limit).
"""

import numpy as np

def calculate_residual(depth, k=3, a=0.8, epsilon=0.05, bar_x=1.0):
    """
    Computes the residual R_D for a k-ary tree of depth D.
    Global constraint: x_i = a^d * x_0
    Local constraint: |x_i - bar_x| > epsilon
    """
    # 1. Determine optimal root x_0 by minimizing sum of squared errors
    # Cost = sum_{d=0}^{D} (k^d) * (a^d * x_0 - bar_x)^2
    # Solving d(Cost)/dx_0 = 0 gives x_0 = bar_x * sum(k^d * a^d) / sum(k^d * a^{2d})
    
    depths = np.arange(depth + 1)
    nodes_at_depth = k**depths
    
    sum1 = np.sum(nodes_at_depth * (a**depths))
    sum2 = np.sum(nodes_at_depth * (a**(2*depths)))
    
    x0_opt = bar_x * (sum1 / sum2)
    
    # 2. Identify violated nodes
    violations = 0
    total_nodes = np.sum(nodes_at_depth)
    
    for d in depths:
        x_i = (a**d) * x0_opt
        if abs(x_i - bar_x) > epsilon:
            violations += nodes_at_depth[d]
            
    return violations / total_nodes

# Execution
if __name__ == "__main__":
    print("Depth | Residual (R_D)")
    for D in range(15):
        R_D = calculate_residual(D)
        print(f"{D:5d} | {R_D:.6f}")
