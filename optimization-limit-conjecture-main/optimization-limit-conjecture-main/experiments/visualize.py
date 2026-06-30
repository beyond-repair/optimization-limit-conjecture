import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Robust import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
try:
    from experiments.core import calculate_residual
except ImportError:
    sys.path.insert(0, os.getcwd())
    from experiments.core import calculate_residual

def plot_surface():
    a_vals = np.linspace(0.1, 0.95, 30)
    res = []
    for a in a_vals:
        try:
            r = calculate_residual(30, k=3, a=a, epsilon=0.05)  # Cap depth to avoid overflow
            res.append(r)
        except:
            res.append(np.nan)
    
    plt.figure(figsize=(8, 5))
    plt.plot(a_vals, res, 'b-', linewidth=2)
    plt.xlabel('Propagation Parameter a')
    plt.ylabel('Residual R_D')
    plt.title('Residual Surface (k=3, ε=0.05)')
    plt.grid(True)
    
    # Ultimate fallback for data dir
    possible_dirs = [
        os.path.join(os.getcwd(), 'data'),
        os.path.join(parent_dir, 'data'),
        os.path.join(os.path.expanduser("~"), 'optimization_data')
    ]
    data_dir = None
    for d in possible_dirs:
        try:
            os.makedirs(d, exist_ok=True)
            data_dir = d
            break
        except:
            continue
    if data_dir:
        save_path = os.path.join(data_dir, 'residual_surface.png')
        plt.savefig(save_path)
        print(f"✅ Plot saved successfully to: {save_path}")
    else:
        print("⚠️ Could not create data dir. Plot shown interactively.")
        plt.show()

if __name__ == "__main__":
    plot_surface()