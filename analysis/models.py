import numpy as np

def run_monte_carlo(n_initial, decay_constant, max_time, dt=1):
    """
    Simulates radioactive decay using Monte Carlo methods.
    Returns: (time_axis, data_results)
    """
    current_atoms = n_initial
    history = []
    time_axis = np.arange(0, max_time, dt)

    # Rigorous Probability: P = 1 - exp(-lambda * dt)
    # This is more accurate than the linear (lambda * dt) approximation
    p_decay = 1 - np.exp(-decay_constant * dt)

    for t in time_axis:
        history.append(current_atoms)
        if current_atoms > 0:
            # Vectorized NumPy roll for efficiency
            rolls = np.random.random(current_atoms)
            decayed = np.sum(rolls < p_decay)
            current_atoms -= decayed
        else:
            current_atoms = 0

    return time_axis, np.array(history)

def get_analytical_solution(n_initial, decay_constant, time_axis):
    """Calculates the theoretical N(t) = N0 * exp(-lambda * t)"""
    return n_initial * np.exp(-decay_constant * time_axis)