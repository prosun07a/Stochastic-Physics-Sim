import pandas as pd
import numpy as np
import os

# --- LOGIC: LOADING THE EXPERIMENT ---
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "decay_simulation_results.csv")

# Load the raw numbers we saved earlier
df = pd.read_csv(data_path)

# --- LOGIC: EXTRACTING THE HALF-LIFE ---
initial_pop = df['nuclei_count'].iloc[0]
target_pop = initial_pop / 2

# Find the first row where the population is <= half
experimental_row = df[df['nuclei_count'] <= target_pop].iloc[0]
exp_half_life = experimental_row['time_s']

# --- LOGIC: SCIENTIFIC VALIDATION ---
lambda_const = 0.03 # Our decay constant
theo_half_life = np.log(2) / lambda_const

# Calculate the "Residual Error" (The difference)
error = abs(exp_half_life - theo_half_life)
accuracy = (1 - (error / theo_half_life)) * 100

print(f"--- KINETICS ANALYSIS REPORT ---")
print(f"Theoretical Half-Life: {theo_half_life:.2f} s")
print(f"Experimental Half-Life: {exp_half_life:.2f} s")
print(f"Simulation Accuracy: {accuracy:.2f}%")
print(f"--------------------------------")