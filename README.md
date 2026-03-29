# Stochastic Modeling of Radioactive Decay via Monte Carlo Simulation
**Principal Developer:** Prosun Kanti Datta  
**Research Focus:** Statistical Mechanics & Numerical Methods  
**Platform:** Ubuntu | Python 3.11.2

---

## 1. Physical Problem & System Formulation
This repository contains a discrete-event simulation of isotopic decay. While the analytical solution is trivial ($N(t) = N_0 e^{-\lambda t}$), standard calculus treats the medium as a continuous fluid. This project models the **microscopic reality**: a system of $N$ discrete particles where each decay is a non-deterministic, independent Bernoulli trial.

### Objectives
* To observe the emergence of macroscopic exponential laws from underlying stochastic noise.
* To validate numerical convergence against the theoretical half-life ($t_{1/2}$).
* To implement a vectorized sampling pipeline for high-performance physical modeling.

---

## 2. Computational Methodology
The simulation utilizes a **Direct Monte Carlo (MC)** approach. Unlike iterative subtraction, we utilize vectorized probabilistic thresholding to maintain physical integrity and computational speed.

### Stochastic Algorithm:
1.  **Initialization:** A state vector of $N_0 = 10,000$ active nuclei is defined.
2.  **Sampling:** At each timestep $\Delta t$, a uniform distribution $U(0, 1)$ is sampled for every remaining particle.
3.  **Thresholding:** A particle $i$ decays if $u_i < P$, where $P$ is the decay probability (set at $\lambda = 0.03$).
4.  **Kinetics Logging:** Populations are recorded in a `.csv` format for post-processing and residual analysis.

---

## 3. Results & Statistical Validation
The simulation demonstrates high-fidelity convergence with the analytical model.

| Parameter | Value |
| :--- | :--- |
| **Initial Population ($N_0$)** | 10,000 |
| **Decay Constant ($\lambda$)** | 0.03 |
| **Theoretical Half-Life** | $\approx 23.10$ s |
| **Observed Accuracy** | 92.22%|

### Data Visualization
The generated plots (`results/final_research_plot.png`) contrast the "jagged" stochastic data against the smooth theoretical curve. The overlap confirms that the **Law of Large Numbers** effectively dampens statistical fluctuations as $N \to \infty$.

---

## 4. Repository Structure
* `core/`: Contains the simulation engine and kinetics analysis logic.
* `data/`: Persistent storage for raw CSV simulation logs.
* `results/`: High-DPI (300) scientific visualizations.
* `research_report.py`: Unified pipeline for execution and automated reporting.

---

## 5. Setup & Reproducibility
Ensure you are operating within a virtual environment to avoid dependency conflicts.

```bash
# Activate environment and install scientific stack
source .venv/bin/activate
pip install -r requirements.txt

# Execute the primary research pipeline
python3 research_report.py