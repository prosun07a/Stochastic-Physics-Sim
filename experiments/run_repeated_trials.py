import sys
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.labelsize": 12,
    "font.size": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

# Path fix to see the core folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.analytical_decay_model import run_monte_carlo, get_analytical_solution
from core.half_life_analysis import calculate_half_life, get_accuracy

# --- Configuration: Cobalt-60 (Units in Years) ---
N0         = 100       # Initial atom population
LAMBDA     = 0.1315    # Decay constant for Cobalt-60 (per year)
TIME       = 40        # Simulation duration in years
DT         = 0.1       # Time step resolution
NUM_TRIALS = 30        # How many independent Monte Carlo runs to compare
T_HALF_THEO = 5.27     # Known scientific half-life of Co-60 (years)

# --- Run All Trials ---
print(f"Running {NUM_TRIALS} independent Monte Carlo trials...")

all_curves   = []   # Stores N(t) array for each trial
half_lives   = []   # Stores estimated half-life from each trial
accuracies   = []   # Stores accuracy (%) from each trial

for i in range(NUM_TRIALS):
    t_axis, n_sim = run_monte_carlo(N0, LAMBDA, TIME, dt=DT)
    t_half = calculate_half_life(t_axis, n_sim)
    acc    = get_accuracy(t_half, T_HALF_THEO)

    all_curves.append(n_sim)
    half_lives.append(t_half)
    accuracies.append(acc)

    print(f"  Trial {i+1:02d}/{NUM_TRIALS} | Half-life: {t_half:.2f} yrs | Accuracy: {acc:.1f}%")

# --- Compute Ensemble Statistics ---
all_curves_array = np.array(all_curves)           # Shape: (NUM_TRIALS, len(t_axis))
mean_curve       = np.mean(all_curves_array, axis=0)
mean_half_life   = np.mean(half_lives)
std_half_life    = np.std(half_lives)
mean_accuracy    = np.mean(accuracies)

# Analytical reference curve
n_theo = get_analytical_solution(N0, LAMBDA, t_axis)

print(f"\n--- Summary ---")
print(f"  Trials run         : {NUM_TRIALS}")
print(f"  Mean half-life     : {mean_half_life:.2f} ± {std_half_life:.2f} years")
print(f"  Theoretical        : {T_HALF_THEO} years")
print(f"  Mean accuracy      : {mean_accuracy:.1f}%")

# --- Figure: Two-Panel Layout ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle(
    f"Repeated Trials Analysis: Cobalt-60 Monte Carlo ({NUM_TRIALS} runs)",
    fontweight='bold', y=1.01
)

# ── Panel 1: All decay curves + mean + theory ──────────────────────────────

for curve in all_curves_array:
    ax1.step(t_axis, curve, where='post',
             color='#004488', alpha=0.12, lw=0.8)

# Ensemble mean — solid, prominent
ax1.plot(t_axis, mean_curve,
         color='#004488', lw=2.2,
         label=f'Ensemble Mean ({NUM_TRIALS} trials)')

# Analytical theory — contrasting dashed line
ax1.plot(t_axis, n_theo,
         color='#BB5566', linestyle='--', lw=2,
         label=r'Analytical Theory ($N_0 e^{-\lambda t}$)')

# Stats annotation
textstr = (
    f'$N_0 = {N0}$\n'
    f'$\\lambda = {LAMBDA}$\n'
    f'$\\bar{{t_{{1/2}}}}$ = {mean_half_life:.2f} ± {std_half_life:.2f} yrs\n'
    f'Mean Accuracy: {mean_accuracy:.1f}%'
)
props = dict(boxstyle='round', facecolor='white', alpha=0.5)
ax1.text(0.62, 0.95, textstr,
         transform=ax1.transAxes, fontsize=10,
         verticalalignment='top', bbox=props)

ax1.set_title("Decay Curves: All Trials", pad=12)
ax1.set_xlabel("Time (Years)")
ax1.set_ylabel(r"Number of Nuclei ($N$)")
ax1.legend(frameon=False)
ax1.grid(True, linestyle=':', alpha=0.6)

# ── Panel 2: Half-life distribution histogram ──────────────────────────────

ax2.hist(half_lives, bins=10,
         color='#004488', alpha=0.75, edgecolor='white', lw=0.5)

# Theoretical half-life — vertical reference line
ax2.axvline(T_HALF_THEO,
            color='#BB5566', linestyle='--', lw=2,
            label=f'Theory: {T_HALF_THEO} yrs')

# Mean of estimates — vertical solid line
ax2.axvline(mean_half_life,
            color='#004488', linestyle='-', lw=2,
            label=f'Mean estimate: {mean_half_life:.2f} yrs')

ax2.set_title("Half-life Distribution Across Trials", pad=12)
ax2.set_xlabel("Estimated Half-life (Years)")
ax2.set_ylabel("Frequency")
ax2.legend(frameon=False)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()

# --- Save Figure ---
timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
plot_path  = os.path.join("results", "figures", "repeated-trials",
                          f"Repeated-Trials(Co60)-N{N0}-T{NUM_TRIALS}_{timestamp}.png")

os.makedirs(os.path.dirname(plot_path), exist_ok=True)
plt.savefig(plot_path, dpi=600, bbox_inches='tight', transparent=False)

print(f"\n Plot saved: {plot_path}")

# --- Save Summary CSV ---
df_summary = pd.DataFrame({
    'trial':          range(1, NUM_TRIALS + 1),
    'half_life_yrs':  [round(h, 4) for h in half_lives],
    'accuracy_pct':   [round(a, 2) for a in accuracies]
})

csv_path = os.path.join("data", "raw",
                        f"Repeated-Trials(Co60)-N{N0}-T{NUM_TRIALS}_{timestamp}.csv")

os.makedirs(os.path.dirname(csv_path), exist_ok=True)
df_summary.to_csv(csv_path, index=False)

print(f" Data saved : {csv_path}")
print(f"\n Done. {NUM_TRIALS} trials complete.")