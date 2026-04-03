import sys
import os
from datetime import datetime
import matplotlib.pyplot as plt

import pandas as pd

plt.rcParams.update({
    "text.usetex": False, # Set to True if you have LaTeX installed, else it uses 'mathtext'
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.labelsize": 12,
    "font.size": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

# Path fix to see the analysis folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.analytical_decay_model import run_monte_carlo, get_analytical_solution
from core.half_life_analysis import calculate_half_life, get_accuracy

# --- Configuration: Cobalt-60 (Units in Years) ---
N0 = 50000              # population / number of atoms 
LAMBDA = 0.1315         # Scientific constant for Cobalt-60 (per year)
TIME = 40               # Simulate for 40 years to see multiple half-lives
DT = 0.1                # Smaller time step for higher resolution

# --- Execution ---
t_axis, n_sim = run_monte_carlo(N0, LAMBDA, TIME, dt=DT)
n_theo = get_analytical_solution(N0, LAMBDA, t_axis)

# --- Analysis ---
t_half_exp = calculate_half_life(t_axis, n_sim)
t_half_theo = 5.27      # scientific value of Co-60
acc = get_accuracy(t_half_exp, t_half_theo)

plt.figure(figsize=(10, 6))

# Use a 'Step' plot to show individual decay events (more scientifically accurate)
plt.step(t_axis, n_sim, where='post', color='#004488', alpha=0.8, lw=1.5, label=r'Monte Carlo Simulation ($^{60}$Co)')

# Fill the area under the curve for a modern aesthetic
plt.fill_between(t_axis, n_sim, step="post", alpha=0.1, color='#004488')

# Theoretical curve as a clean, contrasting dashed line
plt.plot(t_axis, n_theo, color='#BB5566', linestyle='--', lw=2, label=r'Analytical Theory ($N_0 e^{-\lambda t}$)')

# Add a text box with the final accuracy (instead of putting it in the title)
textstr = f'Accuracy: {acc:.2f}%\n$N_0 = {N0}$\n$\lambda = {LAMBDA}$'
props = dict(boxstyle='round', facecolor='white', alpha=0.5)
plt.gca().text(0.65, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=props)

plt.title("Radioactive Decay Validation: Cobalt-60 Statistics", fontweight='bold', pad=20)
plt.xlabel(r"Time (Years)")
plt.ylabel(r"Number of Nuclei or Atoms ($N$)")
plt.legend(frameon=False) 
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout() # Ensures no text is cut off

import pandas as pd

# --- LOGIC: DATA PERSISTENCE ---
# 1. Create a clean DataFrame from your simulation results
df_results = pd.DataFrame({
    'time_years': t_axis,
    'nuclei_count': n_sim
})

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Define time 

#File Save to results / data
data_dir = os.path.join("results", "data")
os.makedirs(data_dir, exist_ok=True) 

csv_filename = f"01_Co60_data_N{N0}_{timestamp}.csv"
csv_path = os.path.join(data_dir, csv_filename)

df_results.to_csv(csv_path, index=False)

print(f" DATA LOGGED: Raw results saved to {csv_path}")

#File Save to results / plots
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"Co60_decay_graph_N{N0}_{timestamp}.png"
plot_path = os.path.join("results", "plots", filename)

os.makedirs(os.path.dirname(plot_path), exist_ok=True)
plt.savefig(plot_path, dpi=600, bbox_inches='tight', transparent=False)

print(f" Scientific Validation complete: {plot_path}")
print(f" Experimental Half-life: {t_half_exp:.2f} years (Theory: 5.2714 years)")