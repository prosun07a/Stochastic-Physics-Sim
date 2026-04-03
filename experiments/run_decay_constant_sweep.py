import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Path Fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.analytical_decay_model import run_monte_carlo

# --- Configuration: Comparing Isotopes ---
isotopes = {
    "Isotope A (High Decay)": 0.25,
    "Cobalt-60": 0.1315,
    "Isotope C (Stable)": 0.02
}
N0 = 10000
TIME = 50

plt.figure(figsize=(10, 6))

for name, lam in isotopes.items():
    t, n = run_monte_carlo(N0, lam, TIME)
    plt.plot(t, n, label=f"{name} ($\lambda={lam}$)")

plt.title("Parameter Sweep: Decay Rates Across Different Isotopes", fontweight='bold')
plt.xlabel("Time (Units)")
plt.ylabel("Remaining Nuclei ($N$)")
plt.legend(frameon=False)
plt.grid(True, linestyle=':', alpha=0.6)

# Save to results/plots
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
plt.savefig(os.path.join("results", "plots", f"03_parameter_sweep_{timestamp}.png"), dpi=300)
print("Parameter sweep plot saved to results/plots/")