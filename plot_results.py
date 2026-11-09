"""
CS475 Project: Visualization Tool
Generates academic publication-ready boxplots comparing information pacing schedules.
"""

import matplotlib.pyplot as plt
import numpy as np

# Mock experimental distributions for pipeline verification
np.random.seed(42)
conditions = ["FULL", "CONCAT", "Uniform", "Early-Burst", "Mid-Burst", "Late-Burst"]
data = [
    np.random.normal(90, 4, 60),   # Upper ceiling baseline
    np.random.normal(87, 5, 60),   # Rephrasing control
    np.random.normal(64, 18, 60),  # Uniform schedule
    np.random.normal(73, 11, 60),  # Early-Burst
    np.random.normal(57, 23, 60),  # Mid-Burst
    np.random.normal(60, 20, 60)   # Late-Burst
]

plt.figure(figsize=(9, 4.5))
box = plt.boxplot(data, tick_labels=conditions, patch_artist=True)

# KAIST primary palette and complementary tones
palette = ["#004191", "#41748D", "#8DA0CB", "#66C2A5", "#FC8D62", "#E78AC3"]
for patch, color in zip(box['boxes'], palette):
    patch.set_facecolor(color)
    patch.set_alpha(0.85)

plt.title("Performance Distribution Across Information Pacing Conditions (T=4)", fontsize=11, fontweight="bold")
plt.ylabel("Accuracy / Score (%)", fontsize=10)
plt.xlabel("Experimental Condition", fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.savefig("pacing_comparison_plot.png", dpi=300, bbox_inches='tight')
print("Successfully generated 'pacing_comparison_plot.png'.")
