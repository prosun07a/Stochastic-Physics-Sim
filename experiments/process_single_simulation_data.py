"""
process_single_simulation_data.py

Scientific Data Processing Pipeline for Radioactive Decay Simulations.
This script locates the most recent raw Monte Carlo simulation data, 
computes derived physical quantities (Activity, Logarithmic linearization), 
and exports a clean dataset ready for statistical analysis and plotting.
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

def get_latest_raw_data(raw_dir: Path) -> Path:
    """Finds the most recently modified CSV file in the raw data directory."""
    try:
        # Glob all csv files and find the one with the maximum modification time
        csv_files = list(raw_dir.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {raw_dir}. Run the simulation first.")
        
        latest_file = max(csv_files, key=lambda f: f.stat().st_mtime)
        return latest_file
    except Exception as e:
        print(f"Error locating raw data: {e}")
        sys.exit(1)

def process_decay_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies scientific transformations to raw decay data.
    
    Transforms:
    1. fraction_remaining: N(t) / N0
    2. activity: -dN/dt (computed numerically)
    3. ln_atoms: ln(N(t)) for linear regression of the decay constant
    """
    # 1. Validate required columns exist
    required_cols = ['time_years', 'nuclei_count']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Raw data missing required column: '{col}'")

    # 2. Extract initial population (N0)
    n_0 = df['nuclei_count'].iloc[0]
    
    # 3. Calculate Fraction Remaining
    df['fraction_remaining'] = df['nuclei_count'] / n_0

    # 4. Calculate Activity (Numerical Derivative: -dN/dt)
    # np.gradient provides a more robust central difference derivative than simple pd.Series.diff()
    df['activity'] = -np.gradient(df['nuclei_count'], df['time_years'])

    # 5. Logarithmic Linearization
    # We must mask zero values to prevent log(0) resulting in -inf, which breaks plotting and regression
    valid_atoms = df['nuclei_count'].replace(0, np.nan)
    df['ln_atoms'] = np.log(valid_atoms)

    return df

def main():
    # --- Path Configuration ---
    # Using pathlib for robust, OS-independent path routing
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    
    # Ensure processed directory exists
    processed_dir.mkdir(parents=True, exist_ok=True)

    #Pipeline Execution ---
    print("Initializing Data Processing Pipeline...")
    
    latest_raw_file = get_latest_raw_data(raw_dir)
    print(f"Loading raw data: {latest_raw_file.name}")
    
    # Load raw data
    df_raw = pd.read_csv(latest_raw_file)
    
    # Process data
    print("Computing derived physical quantities (Activity, ln(N))...")
    df_processed = process_decay_data(df_raw)
    
    # --- Data Persistence ---
    # Create output filename based on the input filename
    output_filename = f"Processed-{latest_raw_file.name}"
    output_path = processed_dir / output_filename
    
    # Drop rows where 'ln_atoms' is NaN (i.e., when all atoms decayed) to keep the dataset clean
    df_clean = df_processed.dropna(subset=['ln_atoms'])
    
    df_clean.to_csv(output_path, index=False)
    print(f"Success. Processed dataset saved to: {output_path}")

if __name__ == "__main__":
    main()