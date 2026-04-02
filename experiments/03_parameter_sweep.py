import os
import matplotlib.pyplot as plt
from analysis.models import run_monte_carlo

# --- Test different decay speeds ---
lambdas = [0.01, 0.03, 0.08]
N0 = 5000
TIME = 150

plt.figure(figsize=(10, 6))

for lam in lambdas:
    t, n = run_monte_carlo(N0, lam, TIME)
    plt.plot(t, n, label=f"$\lambda$ = {lam}")

plt.title("Effect of Decay Constant on Material Stability")
plt.xlabel("Time (s)")
plt.ylabel("Atoms Remaining")
plt.legend()
plt.grid(alpha=0.3)

plot_path = os.path.join("results", "plots", "03_lambda_sweep.png")
plt.savefig(plot_path)
print(f"✅ Parameter sweep saved to {plot_path}")