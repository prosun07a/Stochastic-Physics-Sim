import os
import matplotlib.pyplot as plt
from analysis.models import run_monte_carlo

# --- Compare Small vs Large Population ---
samples = [50, 50000]
colors = ['orange', 'green']
TIME = 40
LAMBDA = 0.1315 
DT = 0.1

fig, axes = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

for i, N in enumerate(samples):
    t, n = run_monte_carlo(N, LAMBDA, TIME)
    # Normalize by N so we can compare the "shape" of the curve
    axes[i].step(t, n/N, color=colors[i], label=f"Population: {N}")
    axes[i].set_ylabel("Fraction Remaining $N(t)/N_0$")
    axes[i].legend()
    axes[i].grid(alpha=0.2)

axes[0].set_title("Stochastic Noise in Small Samples")
axes[1].set_title("Statistical Convergence in Large Samples")
plt.xlabel("Time (s)")

plot_path = os.path.join("results", "plots", "02_convergence_study.png")
plt.savefig(plot_path)
print(f"✅ Convergence study saved to {plot_path}")