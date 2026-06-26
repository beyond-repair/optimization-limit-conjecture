"""
Parameter Sweep v1.0
Objective: Map W(a) for the 3-ary tree family.
This provides the evidence for Theorem C (Functional Dependence).
"""

import numpy as np
import csv

def run_sweep(k=3, epsilon=0.05, bar_x=1.0, depth=20):
    results = []
    # Sweeping 'a' from 0.1 to 0.99
    for a in np.linspace(0.1, 0.99, 50):
        # ... (Insert the calculate_residual logic from previous script) ...
        # (Assuming the logic is integrated here)
        val = calculate_residual(depth, k=k, a=a, epsilon=epsilon, bar_x=bar_x)
        results.append((a, val))
    return results

# Save to data/
if __name__ == "__main__":
    data = run_sweep()
    with open('data/residual_surface.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["a_parameter", "residual_W"])
        writer.writerows(data)
