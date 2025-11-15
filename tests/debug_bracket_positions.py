#!/usr/bin/env python3
"""Debug bracket positioning calculations."""
import sys
sys.path.insert(0, '../src')

import numpy as np
import matplotlib.pyplot as plt
from prs_dataviz import apply_prs_style, COMPARISON
from prs_dataviz.helpers import auto_position_brackets, auto_calculate_ylim_for_annotations
from prs_dataviz.style import add_significance_indicator

apply_prs_style(cycle="comparison")
fig, ax = plt.subplots(figsize=(10, 6))

# Large values (same as test)
data = [1250, 1680, 2150, 2890]
x = np.arange(len(data))
ax.bar(x, data, width=0.6, color=COMPARISON["Treatment"], alpha=0.8)

ax.set_ylabel("Revenue ($)")
ax.set_xticks(x)
ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
ax.grid(True, alpha=0.3, axis='y')

# Three comparisons
comparisons = [
    (2, 3, 0.025),  # Q3 vs Q4 - indices 2, 3
    (1, 3, 0.008),  # Q2 vs Q4 - indices 1, 3
    (0, 3, 0.0002), # Q1 vs Q4 - indices 0, 3
]

print("\n" + "="*70)
print("BRACKET POSITION DEBUG")
print("="*70)

print(f"\nData: {data}")
print(f"Max data: {max(data)}")

# Step 1: Calculate y-limits
print(f"\nStep 1: Calculate y-limits for {len(comparisons)} comparisons")
ymin_before, ymax_before = ax.get_ylim()
print(f"  Before: ylim = ({ymin_before:.1f}, {ymax_before:.1f})")

auto_calculate_ylim_for_annotations(ax, n_comparisons=len(comparisons))

ymin_after, ymax_after = ax.get_ylim()
y_range = ymax_after - ymin_after
print(f"  After:  ylim = ({ymin_after:.1f}, {ymax_after:.1f})")
print(f"  Y-range: {y_range:.1f}")
print(f"  Headroom: {((ymax_after - max(data)) / y_range * 100):.1f}%")

# Step 2: Calculate bracket positions
print(f"\nStep 2: Calculate bracket positions")
x_ranges = []
for idx1, idx2, _ in comparisons:
    x_start = x[idx1]
    x_end = x[idx2]
    x_ranges.append((x_start, x_end))
    print(f"  Comparison {idx1} vs {idx2}: x_range = ({x_start:.1f}, {x_end:.1f}), span = {abs(x_end - x_start):.1f}")

y_positions = auto_position_brackets(ax, x_ranges)

print(f"\nStep 3: Bracket Y-positions")
for i, ((idx1, idx2, p_val), y_pos) in enumerate(zip(comparisons, y_positions)):
    x_center = (x[idx1] + x[idx2]) / 2
    text_y = y_pos + 0.03 * y_range  # 3% above bracket for text
    print(f"  [{i}] Q{idx1+1} vs Q{idx2+1} (p={p_val}):")
    print(f"      Bracket Y: {y_pos:.1f} ({(y_pos/ymax_after*100):.1f}% of ymax)")
    print(f"      Text Y: {text_y:.1f} ({(text_y/ymax_after*100):.1f}% of ymax)")
    print(f"      X-center: {x_center:.1f}")

    # Check if bracket/text will be visible
    if y_pos > ymax_after:
        print(f"      ⚠️  BRACKET ABOVE YMAX!")
    if text_y > ymax_after:
        print(f"      ⚠️  TEXT ABOVE YMAX!")

# Step 4: Draw brackets manually with debug info
print(f"\nStep 4: Drawing brackets...")
for i, ((idx1, idx2, p_val), y_pos) in enumerate(zip(comparisons, y_positions)):
    print(f"  Drawing bracket {i}: Q{idx1+1} vs Q{idx2+1} at y={y_pos:.1f}")
    add_significance_indicator(
        ax,
        x=(x[idx1] + x[idx2]) / 2,
        y=y_pos,
        p_value=p_val,
        bracket=True,
        x_start=x[idx1],
        x_end=x[idx2]
    )

print(f"\nFinal ylim: {ax.get_ylim()}")
print("="*70 + "\n")

plt.tight_layout()
plt.savefig("visual_tests/debug_bracket_positions.png", dpi=150, bbox_inches='tight')
print("Saved: visual_tests/debug_bracket_positions.png\n")
plt.close()
