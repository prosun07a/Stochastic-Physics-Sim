import numpy as np

def calculate_half_life(time_axis, population):
    """Finds the experimental half-life point."""
    n0 = population[0]
    target = n0 / 2
    
    # Find the index where population first drops below half
    idx = np.where(population <= target)[0]
    if len(idx) > 0:
        return time_axis[idx[0]]
    return None

def get_accuracy(experimental, theoretical):
    """Calculates percentage accuracy between two values."""
    error = abs(experimental - theoretical)
    return (1 - (error / theoretical)) * 100