import numpy as np
import csv
import os

# --- DEFINE THE CORE LOGIC FIRST ---
def calculate_residual(depth, k=3, a=0.8, epsilon=0.05, bar_x=1.0):
    depths = np.arange(depth + 1)
    nodes_at_depth = k**depths
    
    sum1 = np.sum(nodes_at_depth * (a**depths))
    sum2 = np.sum(nodes_at_depth * (a**(2*depths)))
    
    # Handle edge case where sum2 is 0 to avoid division errors
    if sum2 == 0: return 0.0
    
    x0_opt = bar_x * (sum1 / sum2)
    
    violations = 0
    total_nodes = np.sum(nodes_at_depth)
    
    for d in depths:
        x_i = (a**d) * x0_opt
        if abs(x_i - bar_x) > epsilon:
            violations += nodes_at_depth[d]
            
    return violations / total_nodes

# --- RUN THE SWEEP ---
def run_sweep(k=3, epsilon=0.05, bar_x=1.0, depth=20):
    results = []
    # Sweeping 'a' to observe how the Inconsistency Floor shifts
    for a in np.linspace(0.1, 0.99, 50):
        val = calculate_residual(depth, k=k, a=a, epsilon=epsilon, bar_x=bar_x)
        results.append((a, val))
    return results

if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    data = run_sweep()
    with open('data/residual_surface.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["a_parameter", "residual_W"])
        writer.writerows(data)
    print("Sweep complete. Data saved to data/residual_surface.csv")
