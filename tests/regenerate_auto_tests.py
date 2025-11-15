#!/usr/bin/env python3
"""Regenerate automatic positioning test images with updated spacing."""
import sys
sys.path.insert(0, '../src')

import numpy as np
import matplotlib.pyplot as plt
from prs_dataviz import apply_prs_style, add_multiple_comparisons, COMPARISON

print("\n" + "="*70)
print("REGENERATING AUTOMATIC POSITIONING TESTS")
print("="*70)

# Test 1: Large Values (the problematic one)
print("\nTest: Large Values - 3 comparisons")
apply_prs_style(cycle="comparison")
fig, ax = plt.subplots(figsize=(10, 6))

data = [1250, 1680, 2150, 2890]
x = np.arange(len(data))
ax.bar(x, data, width=0.6, color=COMPARISON["Treatment"], alpha=0.8)

ax.set_ylabel("Revenue ($)")
ax.set_xticks(x)
ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
ax.grid(True, alpha=0.3, axis='y')

# Three comparisons - automatic positioning!
comparisons = [
    (2, 3, 0.025),  # Q3 vs Q4
    (1, 3, 0.008),  # Q2 vs Q4
    (0, 3, 0.0002), # Q1 vs Q4
]

print(f"  Comparisons: {len(comparisons)}")
print(f"  Data range: {min(data)} - {max(data)}")

add_multiple_comparisons(ax, comparisons, x)

ylim = ax.get_ylim()
print(f"  Y-limits: {ylim[0]:.1f} - {ylim[1]:.1f}")
print(f"  Y-range: {ylim[1] - ylim[0]:.1f}")
print(f"  Headroom: {((ylim[1] - max(data)) / (ylim[1] - ylim[0]) * 100):.1f}%")

plt.tight_layout()
plt.savefig("visual_tests/test_auto_large_values.png", dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: test_auto_large_values.png")

# Test 2: Many Comparisons (5 comparisons)
print("\nTest: Many Comparisons - 5 comparisons")
apply_prs_style(cycle="comparison")
fig, ax = plt.subplots(figsize=(10, 6))

data = [30, 45, 55, 70, 82, 95]
x = np.arange(len(data))
ax.bar(x, data, width=0.6, color=COMPARISON["Treatment"], alpha=0.8)

ax.set_ylabel("Score (%)")
ax.set_xticks(x)
ax.set_xticklabels(['Baseline', 'Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5'])
ax.grid(True, alpha=0.3, axis='y')

comparisons = [
    (4, 5, 0.001),  # Month 4 vs 5
    (3, 5, 0.005),  # Month 3 vs 5
    (2, 5, 0.01),   # Month 2 vs 5
    (1, 5, 0.02),   # Month 1 vs 5
    (0, 5, 0.04),   # Baseline vs 5
]

print(f"  Comparisons: {len(comparisons)}")
print(f"  Data range: {min(data)} - {max(data)}")

add_multiple_comparisons(ax, comparisons, x)

ylim = ax.get_ylim()
print(f"  Y-limits: {ylim[0]:.1f} - {ylim[1]:.1f}")
print(f"  Headroom: {((ylim[1] - max(data)) / (ylim[1] - ylim[0]) * 100):.1f}%")

plt.tight_layout()
plt.savefig("visual_tests/test_auto_many_comparisons.png", dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Saved: test_auto_many_comparisons.png")

print("\n" + "="*70)
print("TESTS COMPLETE - Check visual_tests/ directory")
print("="*70 + "\n")
