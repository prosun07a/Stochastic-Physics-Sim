import numpy as np
import matplotlib.pyplot as plt
import os

# --- LOGIC: THE EXPERIMENT ---
# We want to see how "Noise" disappears as we add more atoms.
populations = [50, 500, 10000]
lam = 0.03
t_max = 150
time_axis = np.arange(t_max)

plt.figure(figsize=(12, 7), dpi=300)

for N in populations:
    current_n = N
    history = [current_n]
    
    for t in range(1, t_max):
        # Stochastic trial
        decayed = np.sum(np.random.random(current_n) < lam)
        current_n -= decayed
        history.append(current_n)
    
    # Normalizing to 1.0 (Percentage) so we can compare them on one graph
    plt.plot(time_axis, np.array(history)/N, label=f'N = {N} atoms', alpha=0.8)

# Add the smooth theoretical line for reference
plt.plot(time_axis, np.exp(-lam * time_axis), 'k--', label='Theoretical Limit', lw=2)

plt.title("Sensitivity Analysis: Convergence and the Law of Large Numbers", fontsize=14)
plt.xlabel("Time (s)")
plt.ylabel("Remaining Fraction (N/N0)")
plt.legend()
plt.grid(alpha=0.2)

# Save the proof of your investigation
script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, "results", "sensitivity_analysis.png")
plt.savefig(save_path)

print(f"✅ ANALYSIS COMPLETE: View the convergence at {save_path}")