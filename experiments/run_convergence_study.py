import sys
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# --- 1. PATH CONFIGURATION ---
# Ensures the script can find the 'analysis' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.analytical_decay_model import run_monte_carlo, get_analytical_solution

# --- 2. PLOT STYLING (Academic Standard) ---
plt.rcParams.update({
    "font.family": "serif",
    "axes.labelsize": 12,
    "font.size": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

# --- 3. EXPERIMENT CONFIGURATION ---
LAMBDA = 0.1315  # Cobalt-60 decay constant
TIME = 40
DT = 0.1
# Comparing three scales of magnitude
populations = [100, 1000, 10000, 50000] 
colors = ['#CCBB44', '#4477AA', "#BB2DD0", "#CE0000"] # Distinct, color-blind friendly palette

# --- 4. EXECUTION & VISUALIZATION ---
plt.figure(figsize=(12, 7), dpi=300)

for N0, col in zip(populations, colors):
    t_axis, n_sim = run_monte_carlo(N0, LAMBDA, TIME, dt=DT)
    
    # NORMALIZATION: Divide by N0 so all curves start at 1.0 for comparison
    n_normalized = n_sim / N0
    
    plt.step(t_axis, n_normalized, where='post', color=col, alpha=0.7, 
             lw=1.5, label=f'Monte Carlo ($N_0={N0}$)')

# Add the Theoretical Baseline
t_theo = np.linspace(0, TIME, 500)
n_theo_norm = np.exp(-LAMBDA * t_theo)
plt.plot(t_theo, n_theo_norm, 'k--', lw=2, label='Analytical Theory (Limit)', zorder=5)

# --- 5. REFINING THE AESTHETICS ---
plt.title("Statistical Convergence: From Stochastic Noise to Physical Law [Law of Large numbers]", fontweight='bold', pad=20)
plt.xlabel("Time (Years)")
plt.ylabel("Normalized Population $N(t)/N_0$")
plt.legend(frameon=False, loc='upper right')
plt.grid(True, linestyle=':', alpha=0.6)

# Add Annotation about the Law of Large Numbers
plt.gca().text(0.05, 0.05, "Note: Larger $N_0$ reduces relative statistical fluctuations.", 
               transform=plt.gca().transAxes, fontsize=9, fontstyle='italic', 
               bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

plt.tight_layout()


#File Save to results / plots
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"Convergence Study-{timestamp}.png"
plot_path = os.path.join("results", "figures","convergence-study", filename)

os.makedirs(os.path.dirname(plot_path), exist_ok=True)
plt.savefig(plot_path, dpi=600)

print(f"Convergence study complete: {plot_path}")