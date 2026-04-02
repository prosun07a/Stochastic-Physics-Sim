import sys
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Path fix to see the analysis folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis.models import run_monte_carlo, get_analytical_solution
from analysis.stats import calculate_half_life, get_accuracy

# --- Configuration: Cobalt-60 (Units in Years) ---
N0 = 50000              # Increased population for higher precision
LAMBDA = 0.1315         # Scientific constant for Cobalt-60 (per year)
TIME = 40               # Simulate for 40 years to see multiple half-lives
DT = 0.1                # Smaller time step for higher resolution

# --- Execution ---
t_axis, n_sim = run_monte_carlo(N0, LAMBDA, TIME, dt=DT)
n_theo = get_analytical_solution(N0, LAMBDA, t_axis)

# --- Analysis ---
t_half_exp = calculate_half_life(t_axis, n_sim)
t_half_theo = 5.27      # Known scientific value for Co-60
acc = get_accuracy(t_half_exp, t_half_theo)

# --- Visualization ---
plt.figure(figsize=(10, 6), dpi=100)
plt.plot(t_axis, n_sim, 'b-', alpha=0.6, label='Monte Carlo ($^{60}Co$ Simulation)')
plt.plot(t_axis, n_theo, 'r--', label='Theoretical Decay Law')

plt.title(f"Isotope Research: Cobalt-60 Decay Validation\n(Accuracy: {acc:.2f}%)")
plt.xlabel("Time (Years)")
plt.ylabel("Atoms Remaining $N(t)$")
plt.legend()
plt.grid(alpha=0.3)

# --- Save with unique ID ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"01_Co60_validation_N{N0}_{timestamp}.png"
plot_path = os.path.join("results", "plots", filename)

os.makedirs(os.path.dirname(plot_path), exist_ok=True)
plt.savefig(plot_path)

print(f"✅ Scientific Validation complete: {plot_path}")
print(f"📊 Experimental Half-life: {t_half_exp:.2f} years (Theory: 5.27 years)")