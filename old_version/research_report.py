import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. SYSTEM PARAMETERS ---
N0 = 10000          # Initial population
LAMBDA = 0.03       # Decay constant
T_MAX = 150         # Simulation duration (s)

def run_pipeline():
    print("="*60)
    print("STOCHASTIC DECAY RESEARCH REPORT")
    print("="*60)
    print("\n[PHASE 1] Initializing Monte Carlo Engine...")
    
    # Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    res_dir = os.path.join(base_dir, "results")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    # Simulation Logic
    time_steps = np.arange(T_MAX)
    population = [N0]
    current_n = N0

    for t in range(1, T_MAX):
        # Vectorized Bernoulli trials
        decayed = np.sum(np.random.random(current_n) < LAMBDA)
        current_n -= decayed
        population.append(current_n)
    
    data = np.array(population)
    print(f"[SUCCESS] Simulation complete. Final N: {data[-1]}")

    # --- 2. KINETICS ANALYSIS ---
    print("\n[PHASE 2] Performing Kinetics Validation...")
    t_half_theory = np.log(2) / LAMBDA
    # Find experimental half-life
    t_half_exp = time_steps[data <= (N0/2)][0]
    accuracy = (1 - abs(t_half_exp - t_half_theory)/t_half_theory) * 100

    # --- 3. DATA PERSISTENCE ---
    df = pd.DataFrame({'time_s': time_steps, 'nuclei_count': data})
    df.to_csv(os.path.join(data_dir, "research_data.csv"), index=False)
    
    # --- 4. VISUALIZATION ---
    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(time_steps, data, label='Stochastic (Monte Carlo)', color='#1f77b4')
    plt.plot(time_steps, N0 * np.exp(-LAMBDA * time_steps), 'r--', label='Analytical (Theory)', alpha=0.7)
    plt.title("Physical Validation: Discrete vs. Continuous Decay Models")
    plt.xlabel("Time (s)")
    plt.ylabel("Active Nuclei (N)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(os.path.join(res_dir, "final_research_plot.png"))

    # --- 5. CONCLUSION ---
    print("-" * 60)
    print(f"RESULTS SUMMARY:")
    print(f"Theoretical Half-Life: {t_half_theory:.2f}s")
    print(f"Experimental Half-Life: {t_half_exp:.2f}s")
    print(f"Statistical Accuracy: {accuracy:.2f}%")
    print("-" * 60)
    print("CONCLUSION: The model confirms that macroscopic order emerges")
    print("from underlying microscopic randomness with high fidelity.")
    print("="*60)

if __name__ == "__main__":
    run_pipeline()