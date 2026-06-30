import numpy as np
import csv
import os

def calculate_residual(depth, k=3, a=0.8, epsilon=0.05, bar_x=1.0):
    depths = np.arange(depth + 1)
    nodes_at_depth = k**depths
    sum1 = np.sum(nodes_at_depth * (a**depths))
    sum2 = np.sum(nodes_at_depth * (a**(2*depths)))
    if sum2 == 0: return 0.0
    x0_opt = bar_x * (sum1 / sum2)
    violations = 0
    total_nodes = np.sum(nodes_at_depth)
    for d in depths:
        x_i = (a**d) * x0_opt
        if abs(x_i - bar_x) > epsilon:
            violations += nodes_at_depth[d]
    return violations / total_nodes

def run_sweep(k=3, epsilon=0.05, bar_x=1.0, depth=20):
    results = []
    for a in np.linspace(0.1, 0.99, 50):
        val = calculate_residual(depth, k=k, a=a, epsilon=epsilon, bar_x=bar_x)
        results.append((a, val))
    return results

if __name__ == "__main__":
    # Handle nested structure
    cwd = os.getcwd()
    if 'optimization-limit-conjecture-main' in cwd:
        project_root = cwd
    else:
        project_root = os.path.dirname(cwd)
    data_dir = os.path.join(project_root, 'data')
    print("Data dir:", data_dir)
    os.makedirs(data_dir, exist_ok=True)
    data = run_sweep()
    csv_path = os.path.join(data_dir, 'residual_surface.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["a_parameter", "residual_W"])
        writer.writerows(data)
    print("✅ Sweep complete.")