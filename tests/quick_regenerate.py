"""Quick test to regenerate one plot with new spacing."""
import sys
sys.path.insert(0, '/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/src')

import numpy as np
import matplotlib.pyplot as plt
from prs_dataviz import apply_prs_style, add_multiple_comparisons, COMPARISON

print("Testing automatic positioning with reduced text spacing...")

apply_prs_style(cycle="comparison")
fig, ax = plt.subplots(figsize=(10, 6))

# Large values test data
data = [1250, 1680, 2150, 2890]
x = np.arange(len(data))
ax.bar(x, data, width=0.6, color=COMPARISON["Treatment"], alpha=0.8)

ax.set_ylabel("Revenue ($)")
ax.set_xticks(x)
ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
ax.grid(True, alpha=0.3, axis='y')

# Multiple comparisons
comparisons = [
    (2, 3, 0.025),  # Q3 vs Q4
    (1, 3, 0.008),  # Q2 vs Q4
    (0, 3, 0.0002), # Q1 vs Q4
]

add_multiple_comparisons(ax, comparisons, x)

# Print y-limits for verification
ymin, ymax = ax.get_ylim()
print(f"Y-limits: {ymin:.1f} - {ymax:.1f}")
print(f"Data max: {max(data)}")

plt.tight_layout()
plt.savefig("/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/tests/visual_tests/test_auto_large_values.png",
            dpi=150, bbox_inches='tight')
print("✅ Saved: visual_tests/test_auto_large_values.png")
plt.close()

print("Done!")
