"""
CS475 Project: Evaluation Metrics & Statistics
Computes Mean Performance (P), Aptitude (A90), Unreliability (U10-90), and Answer Bloat.
"""

import numpy as np

def compute_metrics(scores):
    """
    scores: List of float/int numerical scores (0 to 100) across stochastic runs.
    Returns a dictionary containing P_mean, A_90, and U_10_90.
    """
    scores_arr = np.array(scores, dtype=float)
    avg_performance = float(np.mean(scores_arr))
    aptitude_90 = float(np.percentile(scores_arr, 90))
    unreliability = float(np.percentile(scores_arr, 90) - np.percentile(scores_arr, 10))
    
    return {
        "P_mean": round(avg_performance, 2),
        "A_90": round(aptitude_90, 2),
        "U_10_90": round(unreliability, 2)
    }

def measure_bloat(character_lengths_per_turn):
    """
    character_lengths_per_turn: List of average response lengths (in characters or tokens) per turn.
    Example: [420, 680, 950, 1380] across Turns 1 to 4.
    Computes the percentage expansion of answer size over dialogue turns.
    """
    t1 = character_lengths_per_turn[0]
    t_final = character_lengths_per_turn[-1]
    expansion_ratio = ((t_final - t1) / t1) * 100.0
    return round(expansion_ratio, 2)

if __name__ == "__main__":
    # Test suite with mock experimental simulation scores
    mock_scores = [100.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 100.0, 0.0]
    mock_turn_lengths = [450, 720, 1100, 1420]
    
    stats = compute_metrics(mock_scores)
    bloat_rate = measure_bloat(mock_turn_lengths)
    
    print("=== QUANTITATIVE METRICS SUMMARY ===")
    print(f"Mean Performance (P) : {stats['P_mean']}")
    print(f"Aptitude (A90)        : {stats['A_90']}")
    print(f"Unreliability (U)     : {stats['U_10_90']}")
    print(f"Answer Bloat Growth   : +{bloat_rate}% from Turn 1 to Turn 4")
