# confidence_validator.py

import statistics

def should_stop(conf_values, threshold):
    """
    Stop if at least two values exist and last two are within threshold.
    """
    if len(conf_values) < 2:
        return False

    return abs(conf_values[-1] - conf_values[-2]) < threshold


def compute_variance_score(conf_values):
    """
    Convert variance into a penalty factor between 0 and 1.
    Lower variance → closer to 1.
    Higher variance → closer to 0.
    """
    if len(conf_values) == 1:
        return 1.0

    try:
        var = statistics.variance(conf_values)
    except:
        var = 0.0

    # reasonable LLM confidence variance cap
    normalized = min(var / 0.05, 1.0)

    stability = 1 - normalized
    return stability


def validate_confidence(conf_values):
    """
    Combine mean confidence with variance penalty.
    """
    base = sum(conf_values) / len(conf_values)
    stability = compute_variance_score(conf_values)

    final = base * stability
    return round(max(0.0, min(1.0, final)), 4)
