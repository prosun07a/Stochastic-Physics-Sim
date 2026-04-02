import numpy as np
import matplotlib.pyplot as plt
import os

# --- LOGIC: SETTING THE UNIVERSE 
N_INITIAL = 10000      # Total atoms at t=0
DECAY_CONSTANT = 0.03  # 3% probability per second
MAX_TIME = 150         # Duration of experiment in seconds


# --- LOGIC: THE SIMULATION ENGINE ---
def run_simulation():
    current_atoms = N_INITIAL
    history = [] # To store the population at each second

    for t in range(MAX_TIME):
        history.append(current_atoms)
        
        if current_atoms > 0:
            # MONTE CARLO STEP: Generate a random number [0 to 1] for every atom
            rolls = np.random.random(current_atoms)
            
            # Count how many atoms "rolled" a number less than our probability
            decayed = np.sum(rolls < DECAY_CONSTANT)
            
            # Update the population for the next second
            current_atoms -= decayed
        else:
            history.append(0)
            
    return np.array(history)

# Execute the simulation
data_results = run_simulation()


# --- LOGIC: DATA VISUALIZATION & VALIDATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
results_path = os.path.join(script_dir, "..", "results", "final_decay_model.png")

time_axis = np.arange(len(data_results))

plt.figure(figsize=(10, 6), dpi=300) # High resolution for your CV/Paper
plt.plot(time_axis, data_results, label='Monte Carlo (Simulated)', color='#1f77b4', lw=2)

# Theoretical Line for Comparison
theoretical = N_INITIAL * np.exp(-DECAY_CONSTANT * time_axis)
plt.plot(time_axis, theoretical, 'r--', label='Theoretical (Analytical)', alpha=0.7)

plt.title("Stochastic Decay Simulation: Monte Carlo Validation", fontsize=14)
plt.xlabel("Time (Seconds)")
plt.ylabel("Number of Parent Nuclei (N)")
plt.legend()
plt.grid(alpha=0.3)

plt.savefig(results_path)
print(f"🚀 SUCCESS: Simulation complete. Evidence saved at: {results_path}")

import pandas as pd

# --- LOGIC: DATA PERSISTENCE ---
# Create a table of the results
df = pd.DataFrame({
    'time_s': time_axis,
    'nuclei_count': data_results
})

# Define the data path
data_path = os.path.join(script_dir, "..", "data", "decay_simulation_results.csv")

# Save to CSV (No index needed)
df.to_csv(data_path, index=False)
print(f"📊 DATA LOGGED: Raw results saved to {data_path}")