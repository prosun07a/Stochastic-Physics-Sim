#--------This a performance benchmark between Loops vs Numpy--------/

import sys
import os
import time
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from analysis.models import run_monte_carlo

def legacy_sim_loop(n_initial, decay_constant, max_time):
    """Old style loop-based simulation for comparison"""
    current = n_initial
    for t in range(max_time):
        decayed = 0
        for _ in range(int(current)): # The 'Killer' Loop
            if np.random.random() < decay_constant:
                decayed += 1
        current -= decayed
    return current

N_TEST = 100000 
LAMBDA = 0.1

print(f"🚀 Benchmarking Simulation with N={N_TEST}...")

# Testing Legacy (Loops)
start = time.time()
legacy_sim_loop(N_TEST, LAMBDA, 10)
end_legacy = time.time() - start

# Testing Modern (NumPy Vectorized)
start = time.time()
run_monte_carlo(N_TEST, LAMBDA, 10)
end_modern = time.time() - start

print(f"🐢 Legacy Loop Time: {end_legacy:.4f}s")
print(f"🏎️  Modern NumPy Time: {end_modern:.4f}s")
print(f"📈 Speedup Factor: {end_legacy / end_modern:.1f}x faster!")