# ⚛️ Stochastic Physics Simulation
### *What happens when you simulate 10,000 radioactive atoms — one random decision at a time.*

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Ubuntu%2024.04-orange?style=flat-square&logo=ubuntu)
![Status](https://img.shields.io/badge/Status-Independent%20Research-success?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

There is a question that bothered me for a long time.

Radioactive decay is *random*. Each atom decays whenever it feels like it — there is no timer, no schedule, no reason. And yet, when you observe thousands of atoms together, they always follow the same smooth mathematical curve. Always. Without fail.

How does that happen? How does randomness produce a law?

I couldn't find a satisfying answer just by reading about it. So I built a simulation to see it for myself.

---

## What This Is

A Monte Carlo simulation of radioactive decay, written in Python.

Each atom gets a random "coin flip" every second. If it lands a certain way, the atom decays. I run this for 10,000 atoms, log everything, and then compare what the simulation produced with what the physics equation predicts.

The equation I was testing against:

$$N(t) = N_0 \cdot e^{λ}$$

$N(t)$ is how many atoms are left at time $t$. $N_0$ is how many you started with. λ is the decay constant — it controls how fast they disappear.

The simulation doesn't *use* this equation to generate results. It just uses probability. Then we check at the end whether the results match the equation anyway.

They do. That's the point.

---

## Results

I ran the main simulation with N_0 = 10000 atoms and λ = 0.03

| | Theoretical | Simulated |
|---|---|---|
| **Half-life** | 23.10 seconds | 22 – 24 seconds |
| **Accuracy** | — | ~98% |

98% accuracy from pure probability. No equation forced into the code. Just atoms flipping coins.

The result that actually stopped me was a different one. When I dropped the atom count to just **50**, the decay curve looked like noise — jagged, unpredictable, nothing like the smooth law. Then I brought it back to 10,000 and the noise disappeared. The law came back.

That is the Law of Large Numbers. I had read that phrase in a textbook. But seeing it happen in a graph I produced myself — that hit differently.

---

## Repository Structure

```
Stochastic-Physics-Sim/
│
├── core/
│   ├── analytical_decay_model.py   # Monte Carlo engine + theoretical curve
│   ├── half_life_analysis.py       # Estimates half-life, calculates accuracy
│   └── __init__.py
│
├── experiments/
│   ├── run_single_simulation.py            # Start here — the main experiment
│   ├── run_repeated_trials.py              # Same sim, many runs — see variance
│   ├── run_convergence_study.py            # N₀=100 vs N₀=50,000 — the key test
│   ├── run_decay_constant_sweep.py         # What changes when λ changes
│   ├── run_performance_comparison.py       # Loop vs NumPy — the speed gap is real
│   └── process_single_simulation_data.py   # Cleans the raw data and get it ready for analysis
│
├── prototypes/
│   ├── early_loop_based_version.py      # Where this project actually started
│   └── early_monte_carlo_simulation.py  # Messy. Slow. Kept on purpose.
│
├── data/
│   ├── raw/          # CSV output straight from the simulation
│   └── processed/    # Cleaned up, ready for analysis
│
├── results/
│   └── figures/      # All plots saved here at 300 DPI
│
├── docs/
│   ├── explanation_book.md   # Plain-language walkthrough of the physics and code
│   ├── LAB_LOG.md            # Day-by-day research log — the honest version
│   ├── experiments.md        # Experiment tracker with parameters and outcomes
│   └── research_notes.md     # Open questions, limitations, technical notes
│
├── research_report.py    # Runs the full pipeline end-to-end (all in one)
├── requirements.txt
└── README.md
```

The `prototypes/` folder is there for a reason. The early code is inefficient and a bit embarrassing. But it shows where I actually started — before I understood vectorization, before I had a folder structure, before I knew what I was doing. I think hiding that would be dishonest.

---

## Setup

```bash
git clone https://github.com/prosun07a/Stochastic-Physics-Sim.git
cd Stochastic-Physics-Sim

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

**Dependencies:** `numpy >= 1.24`, `pandas >= 2.0`, `matplotlib >= 3.7`

Quick note: if you are on a headless Linux terminal and get a `FigureCanvasAgg` warning from matplotlib — that is normal. All plots are saved directly to `results/figures/` using `savefig()`. Nothing needs a display window to open.

---

## Running the Experiments

**Start with the main simulation:**

```bash
python3 experiments/run_single_simulation.py
# → data/raw/decay_simulation.csv
# → results/figures/single-sim/decay_curve.png
```

**Then run the one that shows the Law of Large Numbers:**

```bash
python3 experiments/run_convergence_study.py
# Compares N₀ = 100, 1000, 10000, 50000
# → results/figures/convergence/
```

**Other experiments:**

```bash
# Randomness across multiple runs
python3 experiments/run_repeated_trials.py

# Change λ, watch the decay speed shift
python3 experiments/run_decay_constant_sweep.py

# The speed difference between loops and NumPy
python3 experiments/run_performance_comparison.py

# Clean up raw CSV into processed data
python3 experiments/process_single_simulation_data.py
```

**Or run everything at once:**

```bash
python3 research_report.py
```

---

## Documentation

| File | What it contains |
|---|---|
| [`docs/explanation_book.md`](docs/explanation_book.md) | Plain-language walkthrough — physics and code together |
| [`docs/LAB_LOG.md`](docs/LAB_LOG.md) | Chronological log of what I did, what broke, and what I learned |
| [`docs/experiments.md`](docs/experiments.md) | Parameters, outcomes, and notes for each experiment |
| [`docs/research_notes.md`](docs/research_notes.md) | Technical notes, limitations, open questions |

---

## Why I Built This

I'm an class 11 student in Bangladesh.

I don't have a physics lab. I don't have a CS or Physics Professor or a research supervisor. I don't have institutional access to journals or equipment or anyone to check my work.

What I have is a laptop running Ubuntu, a Python interpreter, and a habit of asking questions I can't leave alone.

This project started the way most of mine do — I was studying something for an exam, something stopped making sense, and I couldn't move on until I understood it properly. The textbook gave me the decay equation and told me to use it. It didn't explain *why* randomness at the atomic level becomes order at the population level. That gap bothered me more than I expected.

So I spent a few weeks building this. I ran into the usual problems — broken file paths, a matplotlib error I wasted an embarrassing amount of time on, virtual environment confusion, not knowing how to structure a project bigger than two files. None of that was in the textbook either.


But also that is exactly the kind of thing you only learn by doing it wrong first. 

I'm not sharing this because I think it's groundbreaking research. I'm sharing it because I believe students in places like Bangladesh — without labs, without mentors, without resources — can still build things that are scientifically honest and worth taking seriously. You don't need a university affiliation to care about doing good work. In this era you just need a good knowledge of using AI and different resources from the Internet. But learning, understanding and implementing is the most.

This is me caring about doing good work.

---

## What's Next

This project is the foundation for something I'm working toward: **Physics-Informed Machine Learning (PIML)** — training neural networks that don't just learn patterns from data, but also respect physical laws as hard constraints during training.

The jump from Monte Carlo decay simulation to PIML is not small. But learning how to model a physical system computationally, validate it against theory, and document it honestly — that is exactly the preparation I needed.

---

## Author

**Prosun Kanti Datta**
Class 11 · Independent Researcher · Bangladesh

[GitHub](https://github.com/prosun07a) · [LinkedIn](https://linkedin.com/in/prosun07a) · [Medium](https://medium.com/@prosun07a) · [Website](https://prosun07a.github.io)

---

## License

MIT. Use it freely — just keep the attribution.
See [`LICENSE`](LICENSE) for details.