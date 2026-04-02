# 📔 Research Lab Log: Stochastic Physics Simulation
**Project Start:** March 26, 2026  
**Primary Investigator:** Prosun Kanti Datta

--------

### **Day 1: March 26, 2026 - Initial Setup & "The Headless Problem"**
* **Goal:** Set up a clean Python environment on Ubuntu and plot a simple decay curve.
* **Problem:** Every time I tried to run `plt.show()`, the terminal crashed with a `Tcl_AsyncDelete` error or a warning about "no display name." 
* **Solution:** Researched the issue and learned that because I am working in a headless/terminal environment, I cannot "show" windows. Switched the logic to `plt.savefig()` and also added`import os ` which specifies the machine to show the windows in this  computer rather than doing the work in void to write files directly to the `/results` folder. This is actually better for reproducibility.

### **Day 2: March 27, 2026 - Vectorization vs. Loops**
* **Goal:** Scale the simulation to 10,000 atoms.
* **Observation:** My initial `for` loop was taking forever. It felt like the computer was hanging.
* **Optimization:** Used AI to help me understand `NumPy` vectorization. Instead of checking each atom, I'm now generating one massive array of random numbers and comparing it to the decay constant in a single CPU cycle. The speed difference is night and day.

### **Day 3: March 28, 2026 - The Data Pipeline**
* **Goal:** Make the data "persistent." 
* **Action:** Added `Pandas` to the project. Created a logic to save the simulation results as a `.csv` in the `/data` folder.
* **Why:** Real physicists don't just look at a graph and walk away. They need the raw numbers for peer review. Now I have a 150-row dataset for every experiment.

### **Day 4: March 29, 2026: Sensitivity & Convergence Test
* **Action:** Created `sensitivity_test.py` to test the effect of population size on model accuracy.
* **Observation:** The simulation with N=50 showed massive fluctuations (stochastic noise). The N=10,000 run converged almost perfectly with the analytical $e^{-\lambda t}$ curve.
* **Conclusion:** This confirms that the "smooth" laws of physics we learn in HSC are actually "Emergent Properties" that only appear when you have a large enough sample size.

--------