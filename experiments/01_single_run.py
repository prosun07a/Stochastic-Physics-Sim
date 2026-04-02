import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
from analysis.models import run_monte_carlo, get_analytical_solution
from analysis.stats import calculate_half_life, get_accuracy


#Configuration of decay 
N0 = 50000
LAMBDA = 0.03
TIME = 150

#Execution 
t_axis, n_sim = run_monte_carlo(N0, LAMBDA, TIME)
n_theo = get_analytical_solution(N0, LAMBDA, t_axis)

# Analysis 
t_half_exp = calculate_half_life(t_axis, n_sim)
t_half_theo = 0.693 / LAMBDA  # Simplified ln(2)/lambda
acc = get_accuracy(t_half_exp, t_half_theo)

#Visualization 
plt.figure(figsize=(10, 6), dpi=100)
plt.plot(t_axis, n_sim, 'b-', label='Monte Carlo Simulation')
plt.plot(t_axis, n_theo, 'r--', label='Analytical Theory')

plt.title(f"Radioactive Decay Validation (Accuracy: {acc:.2f}%)")
plt.xlabel("Time (s)")
plt.ylabel("Atoms Remaining $N(t)$")
plt.legend()
plt.grid(alpha=0.3)

# Save results

import os
from datetime import datetime

# ... (rest of your existing simulation code) ...

# --- LOGIC: DYNAMIC FILENAME GENERATION ---
# Creates a unique string based on current date and time
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"01_validation_N{N0}_{timestamp}.png"

# Ensure the directory exists
plot_dir = os.path.join("results", "plots")
os.makedirs(plot_dir, exist_ok=True)

# Define the full path
plot_path = os.path.join(plot_dir, filename)

# Save the plot
plt.savefig(plot_path)
print(f"✅ Validation plot saved as: {plot_path}")