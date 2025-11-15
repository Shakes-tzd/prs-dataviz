#!/usr/bin/env python3
"""Test data-range-based spacing fix."""
import sys
sys.path.insert(0, '../src')

import numpy as np
import matplotlib.pyplot as plt
from prs_dataviz import apply_prs_style, add_multiple_comparisons, COMPARISON

print("\n" + "="*70)
print("TESTING DATA-RANGE-BASED SPACING")
print("="*70)

apply_prs_style(cycle="comparison")
fig, ax = plt.subplots(figsize=(10, 6))

# Test data
data = [1250, 1680, 2150, 2890]
x = np.arange(len(data))
ax.bar(x, data, width=0.6, color=COMPARISON["Treatment"], alpha=0.8)

ax.set_ylabel("Revenue ($)")
ax.set_xticks(x)
ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
ax.grid(True, alpha=0.3, axis='y')

# Three comparisons
comparisons = [
    (2, 3, 0.025),  # Q3 vs Q4
    (1, 3, 0.008),  # Q2 vs Q4
    (0, 3, 0.0002), # Q1 vs Q4
]

print(f"\nData: {data}")
print(f"Data range: {max(data) - 0} = {max(data)}")
print(f"Comparisons: {len(comparisons)}")

# Get ylim before
ymin_before, ymax_before = ax.get_ylim()
print(f"\nBefore: ylim = ({ymin_before:.1f}, {ymax_before:.1f})")

# Add comparisons (this calls auto_calculate_ylim_for_annotations internally)
add_multiple_comparisons(ax, comparisons, x)

# Get ylim after
ymin_after, ymax_after = ax.get_ylim()
y_range_after = ymax_after - ymin_after

print(f"After:  ylim = ({ymin_after:.1f}, {ymax_after:.1f})")
print(f"Y-range: {y_range_after:.1f}")

# Calculate expected values
data_range = max(data) - 0
expected_headroom = (0.10 + 2*0.08 + 0.04) * data_range
expected_ymax = max(data) + expected_headroom

print(f"\n Expected ymax: {expected_ymax:.1f}")
print(f"  Actual ymax: {ymax_after:.1f}")
print(f"  Match: {'✅ YES' if abs(expected_ymax - ymax_after) < 1 else '❌ NO'}")

# Calculate expected bracket positions
print(f"\nExpected bracket positions (data-range-based):")
print(f"  Level 0 (Q1→Q4): {max(data) + 0.10*data_range:.1f}")
print(f"  Level 1 (Q2→Q4): {max(data) + (0.10 + 1*0.08)*data_range:.1f}")
print(f"  Level 2 (Q3→Q4): {max(data) + (0.10 + 2*0.08)*data_range:.1f}")

print(f"\nHeadroom: {((ymax_after - max(data)) / data_range * 100):.1f}% of DATA range")
print(f"Gap above tallest bar: {ymax_after - max(data):.1f} units")

plt.tight_layout()
plt.savefig("visual_tests/test_data_range_fix.png", dpi=150, bbox_inches='tight')
plt.close()

print(f"\n✅ Saved: visual_tests/test_data_range_fix.png")
print("="*70 + "\n")
