import numpy as np
from scipy.optimize import root_scalar

def calculate_residual(depth, k=3, a=0.8, epsilon=0.05, bar_x=1.0, use_analytical_limit=False):
    """
    Computes residual R_D / R_∞. Analytic fallback for large depth.
    """
    if use_analytical_limit and abs(k * a) < 1.0 and depth > 30:
        r1 = k * a
        r2 = k * a**2
        x0_inf = bar_x * (1 - r1) / (1 - r2)
        def viol(d): return abs(a**d * x0_inf - bar_x) - epsilon
        try:
            res = root_scalar(viol, bracket=[0, 200])
            d_star = int(np.floor(res.root))
        except:
            d_star = 0 if viol(0) > 0 else 10000
        if k > 1:
            geom = 1.0 / k
            R_inf = geom ** (d_star + 1) / (1 - geom)
            return R_inf
        return 0.0
    
    # Finite-D original logic
    depths = np.arange(depth + 1)
    nodes = k ** depths
    sum1 = np.sum(nodes * (a**depths))
    sum2 = np.sum(nodes * (a**(2*depths)))
    if sum2 == 0: return 0.0
    x0_opt = bar_x * (sum1 / sum2)
    violations = sum(nodes[d] for d in depths if abs(a**d * x0_opt - bar_x) > epsilon)
    return violations / np.sum(nodes)

def find_optimal_theta(target_w=0.08):
    best, min_dist = None, float('inf')
    for k in range(2, 6):
        for a in np.linspace(0.1, 0.95, 25):
            for eps in np.linspace(0.01, 0.2, 20):
                r = calculate_residual(100, k, a, eps, use_analytical_limit=True)
                dist = abs(r - target_w)
                if dist < min_dist:
                    best, min_dist = (k, a, eps, r), dist
    return best, min_dist