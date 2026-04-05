"""
research_report.py
==================
Master research pipeline for the Stochastic Physics Simulation project.

Runs all seven stages in sequence — simulation, analysis, data processing,
and a final summary dashboard — then prints a complete terminal report.

Usage (from project root):
    python3 research_report.py

Author : Prosun Kanti Datta
GitHub : github.com/prosun07a
"""

import os
import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# 1. ROOT PATH SETUP
# Anchors all imports and file I/O to the project root, regardless of where
# the user invokes the script from.
# ─────────────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "experiments"))

# ─────────────────────────────────────────────────────────────────────────────
# 2. CORE IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
from core.analytical_decay_model    import run_monte_carlo, get_analytical_solution
from core.half_life_analysis        import calculate_half_life, get_accuracy
from process_single_simulation_data import process_decay_data

# ─────────────────────────────────────────────────────────────────────────────
# 3. GLOBAL PLOT STYLE  (matches all experiment scripts)
# ─────────────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "text.usetex"    : False,
    "font.family"    : "serif",
    "font.serif"     : ["Computer Modern Roman"],
    "axes.labelsize" : 12,
    "font.size"      : 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

# ─────────────────────────────────────────────────────────────────────────────
# 4. SHARED CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
TIMESTAMP   = datetime.now().strftime("%Y%m%d_%H%M%S")
CO60_LAMBDA = 0.1315   # Cobalt-60 decay constant (per year)
CO60_THALF  = 5.27     # Known half-life of Co-60 (years)
TIME        = 40       # Simulation duration (years)
DT          = 0.1      # Time step resolution (years)

# Colour palette — identical across every figure in the project
C_BLUE   = "#004488"
C_RED    = "#BB5566"
C_YELLOW = "#CCBB44"
C_TEAL   = "#4477AA"
C_PURPLE = "#BB2DD0"
C_DKRED  = "#CE0000"


# ─────────────────────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def _save_fig(relative_path: str) -> str:
    """Creates parent directories and saves + closes the current figure."""
    os.makedirs(os.path.dirname(relative_path), exist_ok=True)
    plt.savefig(relative_path, dpi=600, bbox_inches="tight", transparent=False)
    plt.close()
    return relative_path


def _header(n: int, title: str) -> None:
    w = 70
    print(f"\n{'═' * w}")
    print(f"  STAGE {n}  │  {title}")
    print(f"{'═' * w}")


def _done(t0: float, outputs: list) -> float:
    elapsed = time.time() - t0
    for path in outputs:
        print(f"   → {path}")
    print(f"   ✓ Completed in {elapsed:.2f}s")
    return elapsed


def _find_latest_sim_csv(raw_dir: Path) -> Path | None:
    """
    Returns the most recently saved Single-Sim CSV from data/raw/.
    Filters by filename prefix so the performance benchmark CSV (which
    has different columns) is never accidentally selected.
    """
    candidates = list(raw_dir.glob("Single-Sim*.csv"))
    if not candidates:
        return None
    return max(candidates, key=lambda f: f.stat().st_mtime)


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 1 — SINGLE SIMULATION VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

def stage_1_single_simulation() -> dict:
    """
    Runs one complete Co-60 Monte Carlo decay simulation.
    Compares result with the analytical model, estimates half-life,
    and saves both the figure and the raw data CSV.
    """
    _header(1, "Single Simulation — Cobalt-60 Validation")
    N0 = 100
    t0 = time.time()

    t_axis, n_sim = run_monte_carlo(N0, CO60_LAMBDA, TIME, dt=DT)
    n_theo        = get_analytical_solution(N0, CO60_LAMBDA, t_axis)
    t_half_exp    = calculate_half_life(t_axis, n_sim)
    acc           = get_accuracy(t_half_exp, CO60_THALF)

    print(f"   Experimental half-life : {t_half_exp:.2f} yrs  (Theory: {CO60_THALF} yrs)")
    print(f"   Accuracy               : {acc:.2f}%")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.step(t_axis, n_sim, where="post",
            color=C_BLUE, alpha=0.8, lw=1.5,
            label=r"Monte Carlo Simulation ($^{60}$Co)")
    ax.fill_between(t_axis, n_sim, step="post", alpha=0.1, color=C_BLUE)
    ax.plot(t_axis, n_theo,
            color=C_RED, linestyle="--", lw=2,
            label=r"Analytical Theory ($N_0 e^{-\lambda t}$)")

    ax.text(0.65, 0.95,
            f"Accuracy: {acc:.2f}%\n$N_0={N0}$\n$\\lambda={CO60_LAMBDA}$",
            transform=ax.transAxes, fontsize=10, verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.5))

    ax.set_title("Radioactive Decay Validation: Cobalt-60",
                 fontweight="bold", pad=20)
    ax.set_xlabel("Time (Years)")
    ax.set_ylabel(r"Number of Nuclei ($N$)")
    ax.legend(frameon=False)
    ax.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()

    fig_path = os.path.join("results", "figures", "single-sim",
                            f"Single-Sim(Co60)-N{N0}_{TIMESTAMP}.png")
    _save_fig(fig_path)

    # CSV — saved and ACTIVE (required by Stage 6 data processing)
    df = pd.DataFrame({"time_years": t_axis, "nuclei_count": n_sim})
    csv_path = os.path.join("data", "raw",
                            f"Single-Sim(Co60)-N{N0}_{TIMESTAMP}.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)

    elapsed = _done(t0, [fig_path, csv_path])
    return {
        "stage"     : "Single Simulation",
        "duration"  : elapsed,
        "half_life" : t_half_exp,
        "accuracy"  : acc,
        "figure"    : fig_path,
        "csv"       : csv_path,
        # Raw data kept in memory for Stage 7 dashboard
        "_t_axis"   : t_axis,
        "_n_sim"    : n_sim,
        "_n_theo"   : n_theo,
    }


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 2 — CONVERGENCE STUDY
# ─────────────────────────────────────────────────────────────────────────────

def stage_2_convergence_study() -> dict:
    """
    Runs four simulations at increasing population sizes and overlays
    normalised decay curves to demonstrate the Law of Large Numbers.
    """
    _header(2, "Convergence Study — Law of Large Numbers")
    populations = [100, 1000, 10000, 50000]
    colors      = [C_YELLOW, C_TEAL, C_PURPLE, C_DKRED]
    t0          = time.time()

    fig, ax   = plt.subplots(figsize=(12, 7))
    curves_out = {}   # stored for dashboard

    for N0, col in zip(populations, colors):
        t_axis, n_sim = run_monte_carlo(N0, CO60_LAMBDA, TIME, dt=DT)
        n_norm        = n_sim / N0
        curves_out[N0] = (t_axis, n_norm)
        ax.step(t_axis, n_norm, where="post",
                color=col, alpha=0.75, lw=1.5,
                label=f"Monte Carlo ($N_0 = {N0:,}$)")
        print(f"   N₀ = {N0:>6,}  ✓")

    t_ref = np.linspace(0, TIME, 500)
    ax.plot(t_ref, np.exp(-CO60_LAMBDA * t_ref),
            "k--", lw=2, label="Analytical Theory (limit)", zorder=5)

    ax.text(0.05, 0.05,
            "Larger $N_0$ reduces relative statistical fluctuations.",
            transform=ax.transAxes, fontsize=9, fontstyle="italic",
            bbox=dict(facecolor="white", alpha=0.5, edgecolor="none"))

    ax.set_title("Statistical Convergence: From Stochastic Noise to Physical Law",
                 fontweight="bold", pad=20)
    ax.set_xlabel("Time (Years)")
    ax.set_ylabel(r"Normalised Population $N(t)\,/\,N_0$")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()

    fig_path = os.path.join("results", "figures", "convergence-study",
                            f"Convergence-Study_{TIMESTAMP}.png")
    _save_fig(fig_path)

    elapsed = _done(t0, [fig_path])
    return {
        "stage"    : "Convergence Study",
        "duration" : elapsed,
        "figure"   : fig_path,
        "_curves"  : curves_out,   # for dashboard
        "_t_ref"   : t_ref,
    }


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 3 — DECAY CONSTANT PARAMETER SWEEP
# ─────────────────────────────────────────────────────────────────────────────

def stage_3_decay_constant_sweep() -> dict:
    """
    Simulates three isotopes with distinct decay constants and overlays
    their decay curves to illustrate parameter sensitivity.
    """
    _header(3, "Decay Constant Sweep — Isotope Comparison")

    isotopes = {
        "Isotope A  (fast,  λ = 0.25)"   : (0.25,       C_RED),
        "Cobalt-60  (med,   λ = 0.1315)" : (CO60_LAMBDA, C_BLUE),
        "Isotope C  (slow,  λ = 0.02)"   : (0.02,       C_TEAL),
    }
    N0 = 50000
    t0 = time.time()

    fig, ax    = plt.subplots(figsize=(10, 6))
    sweep_out  = {}   # stored for dashboard

    for name, (lam, col) in isotopes.items():
        # BUG FIX: dt=DT passed explicitly (was missing — caused dt=1 default)
        t_axis, n_sim = run_monte_carlo(N0, lam, TIME, dt=DT)
        sweep_out[name] = (t_axis, n_sim, col)
        ax.plot(t_axis, n_sim, color=col, lw=1.8, label=name)
        print(f"   {name}  ✓")

    ax.set_title("Parameter Sweep: Decay Rates Across Different Isotopes",
                 fontweight="bold", pad=20)
    ax.set_xlabel("Time (Years)")
    ax.set_ylabel(r"Remaining Nuclei ($N$)")
    ax.legend(frameon=False)
    ax.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()

    # BUG FIX: makedirs now guaranteed via _save_fig helper
    fig_path = os.path.join("results", "figures", "decay-const-sweep",
                            f"Decay-Const-Sweep-N{N0}_{TIMESTAMP}.png")
    _save_fig(fig_path)

    elapsed = _done(t0, [fig_path])
    return {
        "stage"    : "Decay Constant Sweep",
        "duration" : elapsed,
        "figure"   : fig_path,
        "_sweep"   : sweep_out,   # for dashboard
    }


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 4 — REPEATED TRIALS ENSEMBLE ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

def stage_4_repeated_trials() -> dict:
    """
    Runs 30 independent Monte Carlo trials, computes ensemble statistics,
    and produces a two-panel figure: overlaid decay curves + half-life
    distribution histogram.
    """
    _header(4, "Repeated Trials — Ensemble & Half-life Distribution")

    N0         = 100
    NUM_TRIALS = 30
    t0         = time.time()

    all_curves, half_lives, accuracies = [], [], []

    for i in range(NUM_TRIALS):
        t_axis, n_sim = run_monte_carlo(N0, CO60_LAMBDA, TIME, dt=DT)
        t_half        = calculate_half_life(t_axis, n_sim)
        acc           = get_accuracy(t_half, CO60_THALF)
        all_curves.append(n_sim)
        half_lives.append(t_half)
        accuracies.append(acc)
        print(f"   Trial {i+1:02d}/{NUM_TRIALS}  │  "
              f"t½ = {t_half:.2f} yrs  │  acc = {acc:.1f}%")

    curves_arr    = np.array(all_curves)
    mean_curve    = np.mean(curves_arr, axis=0)
    mean_thalf    = np.mean(half_lives)
    std_thalf     = np.std(half_lives)
    mean_accuracy = np.mean(accuracies)
    n_theo        = get_analytical_solution(N0, CO60_LAMBDA, t_axis)

    print(f"\n   Mean half-life : {mean_thalf:.2f} ± {std_thalf:.2f} yrs")
    print(f"   Mean accuracy  : {mean_accuracy:.1f}%")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle(
        f"Repeated Trials: Cobalt-60 Monte Carlo ({NUM_TRIALS} independent runs)",
        fontweight="bold", y=1.01
    )

    for curve in curves_arr:
        ax1.step(t_axis, curve, where="post",
                 color=C_BLUE, alpha=0.12, lw=0.8)
    ax1.plot(t_axis, mean_curve, color=C_BLUE, lw=2.2,
             label=f"Ensemble Mean ({NUM_TRIALS} trials)")
    ax1.plot(t_axis, n_theo, color=C_RED, linestyle="--", lw=2,
             label=r"Analytical Theory ($N_0 e^{-\lambda t}$)")
    ax1.text(0.62, 0.95,
             f"$N_0={N0}$\n$\\lambda={CO60_LAMBDA}$\n"
             f"$\\bar{{t_{{1/2}}}}$ = {mean_thalf:.2f} ± {std_thalf:.2f} yrs\n"
             f"Mean acc: {mean_accuracy:.1f}%",
             transform=ax1.transAxes, fontsize=10, verticalalignment="top",
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.5))
    ax1.set_title("Decay Curves: All Trials", pad=12)
    ax1.set_xlabel("Time (Years)")
    ax1.set_ylabel(r"Number of Nuclei ($N$)")
    ax1.legend(frameon=False)
    ax1.grid(True, linestyle=":", alpha=0.6)

    ax2.hist(half_lives, bins=10,
             color=C_BLUE, alpha=0.75, edgecolor="white", lw=0.5)
    ax2.axvline(CO60_THALF, color=C_RED, linestyle="--", lw=2,
                label=f"Theory: {CO60_THALF} yrs")
    ax2.axvline(mean_thalf, color=C_BLUE, linestyle="-", lw=2,
                label=f"Mean: {mean_thalf:.2f} yrs")
    ax2.set_title("Half-life Distribution Across Trials", pad=12)
    ax2.set_xlabel("Estimated Half-life (Years)")
    ax2.set_ylabel("Frequency")
    ax2.legend(frameon=False)
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()

    fig_path = os.path.join("results", "figures", "repeated-trials",
                            f"Repeated-Trials(Co60)-N{N0}-T{NUM_TRIALS}_{TIMESTAMP}.png")
    _save_fig(fig_path)

    df_summary = pd.DataFrame({
        "trial"        : range(1, NUM_TRIALS + 1),
        "half_life_yrs": [round(h, 4) for h in half_lives],
        "accuracy_pct" : [round(a, 2)  for a in accuracies],
    })
    csv_path = os.path.join("data", "raw",
                            f"Repeated-Trials(Co60)-N{N0}-T{NUM_TRIALS}_{TIMESTAMP}.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df_summary.to_csv(csv_path, index=False)

    elapsed = _done(t0, [fig_path, csv_path])
    return {
        "stage"        : "Repeated Trials",
        "duration"     : elapsed,
        "mean_thalf"   : mean_thalf,
        "std_thalf"    : std_thalf,
        "mean_accuracy": mean_accuracy,
        "figure"       : fig_path,
        "csv"          : csv_path,
        "_half_lives"  : half_lives,   # for dashboard
        "_mean_curve"  : mean_curve,
        "_t_axis"      : t_axis,
        "_n_theo"      : n_theo,
    }


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 5 — PERFORMANCE BENCHMARK
# ─────────────────────────────────────────────────────────────────────────────

def _legacy_loop(n_initial: int, decay_constant: float, max_time: int) -> int:
    """Pure-Python loop-based decay simulation — the slow baseline."""
    current = n_initial
    for _ in range(max_time):
        decayed = 0
        for _ in range(int(current)):   # the 'killer' inner loop
            if np.random.random() < decay_constant:
                decayed += 1
        current -= decayed
    return current


def stage_5_performance_benchmark() -> dict:
    """
    Times the legacy loop implementation against the vectorised NumPy
    implementation. Saves a bar chart figure and a CSV with timings.
    """
    _header(5, "Performance Benchmark — Loop vs NumPy Vectorisation")

    N_TEST      = 100_000
    LAMBDA_TEST = 0.1
    t0          = time.time()

    print(f"   Benchmarking with N = {N_TEST:,} atoms over 10 time steps...")

    t_start  = time.time()
    _legacy_loop(N_TEST, LAMBDA_TEST, 10)
    t_legacy = time.time() - t_start

    t_start = time.time()
    run_monte_carlo(N_TEST, LAMBDA_TEST, 10)
    t_numpy = time.time() - t_start

    speedup = t_legacy / t_numpy

    print(f"   Legacy loop  : {t_legacy:.4f}s")
    print(f"   NumPy vector : {t_numpy:.4f}s")
    print(f"   Speedup      : {speedup:.1f}×")

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(
        ["Legacy\n(Python loop)", "Vectorised\n(NumPy)"],
        [t_legacy, t_numpy],
        color=[C_RED, C_BLUE],
        width=0.45, edgecolor="white", linewidth=0.8,
    )
    for bar, val in zip(bars, [t_legacy, t_numpy]):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + t_legacy * 0.02,
                f"{val:.4f}s",
                ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.text(0.5, 0.88, f"{speedup:.1f}× faster",
            transform=ax.transAxes, ha="center", fontsize=13,
            color=C_BLUE, fontweight="bold",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.6))

    ax.set_title(f"Simulation Performance: N = {N_TEST:,} atoms",
                 fontweight="bold", pad=16)
    ax.set_ylabel("Wall-clock Time (seconds)")
    ax.set_ylim(0, t_legacy * 1.25)
    ax.grid(True, axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()

    fig_path = os.path.join("results", "figures", "performance",
                            f"Performance-Benchmark-N{N_TEST}_{TIMESTAMP}.png")
    _save_fig(fig_path)

    df_bench = pd.DataFrame([{
        "n_atoms"       : N_TEST,
        "time_steps"    : 10,
        "legacy_loop_s" : round(t_legacy, 6),
        "numpy_vector_s": round(t_numpy,  6),
        "speedup_factor": round(speedup,  2),
    }])
    csv_path = os.path.join("data", "raw",
                            f"Performance-Benchmark-N{N_TEST}_{TIMESTAMP}.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df_bench.to_csv(csv_path, index=False)

    elapsed = _done(t0, [fig_path, csv_path])
    return {
        "stage"   : "Performance Benchmark",
        "duration": elapsed,
        "legacy"  : t_legacy,
        "numpy"   : t_numpy,
        "speedup" : speedup,
        "figure"  : fig_path,
        "csv"     : csv_path,
    }


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 6 — DATA PROCESSING + DERIVED QUANTITIES FIGURE
# ─────────────────────────────────────────────────────────────────────────────

def stage_6_data_processing() -> dict:
    """
    Loads the Single-Sim CSV saved in Stage 1, computes three derived
    physical quantities, saves the processed CSV, and produces a three-panel
    figure: ln(N) linearisation, activity curve, and fraction remaining.

    BUG FIX: Specifically searches for 'Single-Sim*.csv' files so the
    performance benchmark CSV is never accidentally selected.
    """
    _header(6, "Data Processing — Derived Physical Quantities & Visualisation")

    raw_dir       = PROJECT_ROOT / "data" / "raw"
    processed_dir = PROJECT_ROOT / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    # ── Find the right CSV ───────────────────────────────────────────────────
    sim_csv = _find_latest_sim_csv(raw_dir)
    if sim_csv is None:
        print("   ⚠  No Single-Sim CSV found. Stage 1 may not have run correctly.")
        return {"stage": "Data Processing", "duration": 0, "csv": None, "figure": None}

    print(f"   Source file : {sim_csv.name}")
    df_raw      = pd.read_csv(sim_csv)
    df_processed = process_decay_data(df_raw)
    df_clean    = df_processed.dropna(subset=["ln_atoms"])

    output_path = processed_dir / f"Processed-{sim_csv.name}"
    df_clean.to_csv(output_path, index=False)
    print(f"   Rows processed : {len(df_clean)}")
    print(f"   Columns added  : fraction_remaining, activity, ln_atoms")

    # ── Three-panel figure ───────────────────────────────────────────────────
    t  = df_clean["time_years"].values
    N  = df_clean["nuclei_count"].values
    ln_N     = df_clean["ln_atoms"].values
    activity = df_clean["activity"].values
    frac     = df_clean["fraction_remaining"].values

    # Theoretical ln(N) for comparison: ln(N0) - λt
    ln_theo = np.log(N[0]) - CO60_LAMBDA * t

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Processed Data: Derived Physical Quantities — Cobalt-60",
                 fontweight="bold", y=1.02)

    # Panel 1 — Logarithmic linearisation
    # If decay is truly exponential, ln(N) vs time is a straight line
    ax1.scatter(t, ln_N, color=C_BLUE, s=4, alpha=0.6, label="ln(N) simulation")
    ax1.plot(t, ln_theo, color=C_RED, linestyle="--", lw=2,
             label=r"Theory: $\ln N_0 - \lambda t$")
    ax1.set_title("Logarithmic Linearisation", pad=12)
    ax1.set_xlabel("Time (Years)")
    ax1.set_ylabel(r"$\ln\,N(t)$")
    ax1.legend(frameon=False)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.text(0.05, 0.10,
             "Straight line confirms\nexponential decay law",
             transform=ax1.transAxes, fontsize=9, fontstyle="italic",
             bbox=dict(facecolor="white", alpha=0.5, edgecolor="none"))

    # Panel 2 — Activity (-dN/dt)
    ax2.plot(t, activity, color=C_TEAL, lw=1.5, alpha=0.85)
    ax2.fill_between(t, activity, alpha=0.15, color=C_TEAL)
    ax2.set_title("Activity: Rate of Decay $(-dN/dt)$", pad=12)
    ax2.set_xlabel("Time (Years)")
    ax2.set_ylabel("Activity (atoms / year)")
    ax2.grid(True, linestyle=":", alpha=0.6)

    # Panel 3 — Fraction remaining
    ax3.step(t, frac, where="post", color=C_PURPLE, lw=1.5, alpha=0.8,
             label="Simulated fraction")
    t_ref = np.linspace(0, TIME, 500)
    ax3.plot(t_ref, np.exp(-CO60_LAMBDA * t_ref),
             color=C_RED, linestyle="--", lw=2,
             label=r"Theory: $e^{-\lambda t}$")
    ax3.axhline(0.5, color="gray", linestyle=":", lw=1.2, alpha=0.8,
                label="50% threshold")
    ax3.set_title("Fraction Remaining $N(t)/N_0$", pad=12)
    ax3.set_xlabel("Time (Years)")
    ax3.set_ylabel(r"$N(t)\,/\,N_0$")
    ax3.legend(frameon=False)
    ax3.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()

    fig_path = os.path.join("results", "figures", "data-processing",
                            f"Processed-Quantities(Co60)_{TIMESTAMP}.png")
    _save_fig(fig_path)

    elapsed = _done(t0, [str(output_path), fig_path])
    return {
        "stage"   : "Data Processing",
        "duration": elapsed,
        "rows"    : len(df_clean),
        "csv"     : str(output_path),
        "figure"  : fig_path,
        # Raw arrays kept in memory for dashboard
        "_t"      : t,
        "_ln_N"   : ln_N,
        "_ln_theo": ln_theo,
        "_frac"   : frac,
    }


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 7 — MASTER SUMMARY DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────

def stage_7_summary_dashboard(stage_results: list) -> dict:
    """
    Produces a single composite figure — a 2×3 dashboard — pulling one key
    panel from each of the six preceding stages. This is the visual proof
    that the entire research pipeline ran and produced coherent results.
    """
    _header(7, "Summary Dashboard — Master Research Figure")
    t0 = time.time()

    # Pull stored data from each stage result dict
    r1 = next((r for r in stage_results if r["stage"] == "Single Simulation"),    {})
    r2 = next((r for r in stage_results if r["stage"] == "Convergence Study"),    {})
    r3 = next((r for r in stage_results if r["stage"] == "Decay Constant Sweep"), {})
    r4 = next((r for r in stage_results if r["stage"] == "Repeated Trials"),      {})
    r5 = next((r for r in stage_results if r["stage"] == "Performance Benchmark"),{})
    r6 = next((r for r in stage_results if r["stage"] == "Data Processing"),      {})

    fig = plt.figure(figsize=(20, 12))
    fig.suptitle(
        "Stochastic Physics Simulation — Research Pipeline Summary\n"
        "Monte Carlo Validation of Radioactive Decay  │  Prosun Kanti Datta",
        fontweight="bold", fontsize=14, y=0.98
    )
    gs = gridspec.GridSpec(2, 3, figure=fig,
                           hspace=0.42, wspace=0.32)

    # ── Panel 1: Single simulation (Stage 1) ─────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    if r1.get("_t_axis") is not None:
        ax1.step(r1["_t_axis"], r1["_n_sim"], where="post",
                 color=C_BLUE, alpha=0.8, lw=1.2,
                 label="Monte Carlo")
        ax1.plot(r1["_t_axis"], r1["_n_theo"],
                 color=C_RED, linestyle="--", lw=1.5,
                 label="Theory")
        ax1.text(0.60, 0.92,
                 f"Acc: {r1.get('accuracy', 0):.1f}%",
                 transform=ax1.transAxes, fontsize=9,
                 bbox=dict(boxstyle="round", facecolor="white", alpha=0.6))
    ax1.set_title("① Single Simulation", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Time (Years)", fontsize=9)
    ax1.set_ylabel("Nuclei N(t)", fontsize=9)
    ax1.legend(frameon=False, fontsize=8)
    ax1.grid(True, linestyle=":", alpha=0.5)

    # ── Panel 2: Convergence study (Stage 2) ─────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    if r2.get("_curves") is not None:
        pop_colors = [C_YELLOW, C_TEAL, C_PURPLE, C_DKRED]
        for (N0, (t_ax, n_norm)), col in zip(r2["_curves"].items(), pop_colors):
            ax2.step(t_ax, n_norm, where="post",
                     color=col, alpha=0.7, lw=1.0,
                     label=f"$N_0={N0:,}$")
        ax2.plot(r2["_t_ref"],
                 np.exp(-CO60_LAMBDA * r2["_t_ref"]),
                 "k--", lw=1.5, label="Theory")
    ax2.set_title("② Convergence Study", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Time (Years)", fontsize=9)
    ax2.set_ylabel(r"$N(t)/N_0$", fontsize=9)
    ax2.legend(frameon=False, fontsize=7, loc="upper right")
    ax2.grid(True, linestyle=":", alpha=0.5)

    # ── Panel 3: Decay constant sweep (Stage 3) ───────────────────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    if r3.get("_sweep") is not None:
        for name, (t_ax, n_sim, col) in r3["_sweep"].items():
            lam = name.split("λ = ")[-1].rstrip(")")
            ax3.plot(t_ax, n_sim, color=col, lw=1.2,
                     label=f"λ = {lam}")
    ax3.set_title("③ Decay Constant Sweep", fontsize=11, fontweight="bold")
    ax3.set_xlabel("Time (Years)", fontsize=9)
    ax3.set_ylabel("Nuclei N(t)", fontsize=9)
    ax3.legend(frameon=False, fontsize=8)
    ax3.grid(True, linestyle=":", alpha=0.5)

    # ── Panel 4: Half-life distribution (Stage 4) ────────────────────────────
    ax4 = fig.add_subplot(gs[1, 0])
    if r4.get("_half_lives") is not None:
        ax4.hist(r4["_half_lives"], bins=10,
                 color=C_BLUE, alpha=0.75, edgecolor="white", lw=0.5)
        ax4.axvline(CO60_THALF,
                    color=C_RED, linestyle="--", lw=1.8,
                    label=f"Theory: {CO60_THALF} yrs")
        ax4.axvline(r4["mean_thalf"],
                    color=C_BLUE, linestyle="-", lw=1.8,
                    label=f"Mean: {r4['mean_thalf']:.2f} yrs")
    ax4.set_title("④ Half-life Distribution (30 Trials)",
                  fontsize=11, fontweight="bold")
    ax4.set_xlabel("Estimated Half-life (Years)", fontsize=9)
    ax4.set_ylabel("Frequency", fontsize=9)
    ax4.legend(frameon=False, fontsize=8)
    ax4.grid(True, linestyle=":", alpha=0.5)

    # ── Panel 5: Performance benchmark (Stage 5) ─────────────────────────────
    ax5 = fig.add_subplot(gs[1, 1])
    if r5.get("legacy") is not None:
        bars = ax5.bar(
            ["Legacy\n(loop)", "NumPy\n(vector)"],
            [r5["legacy"], r5["numpy"]],
            color=[C_RED, C_BLUE],
            width=0.4, edgecolor="white",
        )
        for bar, val in zip(bars, [r5["legacy"], r5["numpy"]]):
            ax5.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + r5["legacy"] * 0.02,
                     f"{val:.3f}s",
                     ha="center", va="bottom", fontsize=9, fontweight="bold")
        ax5.text(0.5, 0.88, f"{r5['speedup']:.1f}× faster",
                 transform=ax5.transAxes, ha="center", fontsize=11,
                 color=C_BLUE, fontweight="bold",
                 bbox=dict(boxstyle="round", facecolor="white", alpha=0.6))
    ax5.set_title("⑤ Performance Benchmark", fontsize=11, fontweight="bold")
    ax5.set_ylabel("Time (seconds)", fontsize=9)
    ax5.set_ylim(0, (r5.get("legacy", 1)) * 1.3)
    ax5.grid(True, axis="y", linestyle=":", alpha=0.5)

    # ── Panel 6: Logarithmic linearisation (Stage 6) ─────────────────────────
    ax6 = fig.add_subplot(gs[1, 2])
    if r6.get("_t") is not None:
        ax6.scatter(r6["_t"], r6["_ln_N"],
                    color=C_BLUE, s=3, alpha=0.5, label="ln(N) simulation")
        ax6.plot(r6["_t"], r6["_ln_theo"],
                 color=C_RED, linestyle="--", lw=1.8,
                 label=r"Theory: $\ln N_0 - \lambda t$")
        ax6.text(0.05, 0.12,
                 "Linear → confirms\nexponential law",
                 transform=ax6.transAxes, fontsize=8, fontstyle="italic",
                 bbox=dict(facecolor="white", alpha=0.5, edgecolor="none"))
    ax6.set_title("⑥ ln(N) Linearisation", fontsize=11, fontweight="bold")
    ax6.set_xlabel("Time (Years)", fontsize=9)
    ax6.set_ylabel(r"$\ln\,N(t)$", fontsize=9)
    ax6.legend(frameon=False, fontsize=8)
    ax6.grid(True, linestyle=":", alpha=0.5)

    # ── Footer ───────────────────────────────────────────────────────────────
    fig.text(0.5, -0.01,
             f"Generated: {TIMESTAMP}  │  "
             f"github.com/prosun07a/Stochastic-Physics-Sim",
             ha="center", fontsize=9, color="gray")

    fig_path = os.path.join("results", "figures", "summary",
                            f"Research-Summary-Dashboard_{TIMESTAMP}.png")
    _save_fig(fig_path)

    elapsed = _done(t0, [fig_path])
    print(f"   This is the master output figure for the project.")
    return {
        "stage"   : "Summary Dashboard",
        "duration": elapsed,
        "figure"  : fig_path,
    }


# ─────────────────────────────────────────────────────────────────────────────
# TERMINAL SUMMARY REPORT
# ─────────────────────────────────────────────────────────────────────────────

def _print_summary(results: list, total_time: float) -> None:
    w = 70
    print(f"\n\n{'═' * w}")
    print(f"  RESEARCH PIPELINE — COMPLETE SUMMARY")
    print(f"{'═' * w}")
    print(f"  Project   : Stochastic Physics Simulation")
    print(f"  Author    : Prosun Kanti Datta  │  github.com/prosun07a")
    print(f"  Run at    : {TIMESTAMP}")
    print(f"{'─' * w}")

    for r in results:
        status = "✗ FAILED" if "error" in r else "✓"
        print(f"\n  {status}  {r['stage']:<32}  {r.get('duration', 0):.2f}s")

        if "error" in r:
            print(f"       Error: {r['error']}")
            continue

        if "accuracy" in r:
            print(f"       Half-life : {r['half_life']:.2f} yrs  "
                  f"│  Accuracy : {r['accuracy']:.2f}%")
        if "mean_thalf" in r:
            print(f"       Mean t½   : {r['mean_thalf']:.2f} ± "
                  f"{r['std_thalf']:.2f} yrs  "
                  f"│  Mean acc : {r['mean_accuracy']:.1f}%")
        if "speedup" in r:
            print(f"       Speedup   : {r['speedup']:.1f}×  "
                  f"(loop {r['legacy']:.4f}s  →  numpy {r['numpy']:.4f}s)")
        if r.get("rows"):
            print(f"       Rows processed : {r['rows']}")
        if r.get("figure"):
            print(f"       Figure : {r['figure']}")

    print(f"\n{'─' * w}")
    print(f"  Total pipeline time : {total_time:.2f}s")
    print(f"  Figures saved to    : results/figures/")
    print(f"  Data saved to       : data/")
    print(f"{'═' * w}\n")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print()
    print("  ╔══════════════════════════════════════════════════════════════════╗")
    print("  ║       STOCHASTIC PHYSICS SIMULATION — RESEARCH PIPELINE         ║")
    print("  ║          Monte Carlo Validation of Radioactive Decay             ║")
    print("  ║                    Prosun Kanti Datta                            ║")
    print("  ║               github.com/prosun07a  │  MIT License               ║")
    print("  ╚══════════════════════════════════════════════════════════════════╝")

    pipeline_start = time.time()
    results        = []

    experiment_stages = [
        stage_1_single_simulation,
        stage_2_convergence_study,
        stage_3_decay_constant_sweep,
        stage_4_repeated_trials,
        stage_5_performance_benchmark,
        stage_6_data_processing,
    ]

    for stage_fn in experiment_stages:
        try:
            result = stage_fn()
            results.append(result)
        except Exception as exc:
            print(f"\n   ✗ Stage failed: {exc}")
            results.append({
                "stage"   : stage_fn.__name__,
                "duration": 0,
                "error"   : str(exc),
            })

    # Stage 7 always runs last and receives all previous results
    try:
        dashboard_result = stage_7_summary_dashboard(results)
        results.append(dashboard_result)
    except Exception as exc:
        print(f"\n   ✗ Dashboard failed: {exc}")
        results.append({
            "stage"   : "Summary Dashboard",
            "duration": 0,
            "error"   : str(exc),
        })

    total_time = time.time() - pipeline_start
    _print_summary(results, total_time)


if __name__ == "__main__":
    main()