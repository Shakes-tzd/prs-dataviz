"""Calculate exact spacing between data max and first bracket."""
import sys
sys.path.insert(0, '/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/src')

import numpy as np
import matplotlib.pyplot as plt
from prs_dataviz import apply_prs_style, add_multiple_comparisons, COMPARISON

print("="*70)
print("BRACKET SPACING ANALYSIS")
print("="*70)

# Test with large values (Q1-Q4 example)
apply_prs_style(cycle="comparison")
fig, ax = plt.subplots(figsize=(10, 6))
data = [1250, 1680, 2150, 2890]
x = np.arange(len(data))
ax.bar(x, data, width=0.6, color=COMPARISON["Treatment"], alpha=0.8)
ax.set_ylabel("Revenue ($)")
ax.set_xticks(x)
ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
ax.grid(True, alpha=0.3, axis='y')

comparisons = [(2, 3, 0.025), (1, 3, 0.008), (0, 3, 0.0002)]
add_multiple_comparisons(ax, comparisons, x)

ymin, ymax = ax.get_ylim()
data_max = max(data)
data_min = 0
data_range = data_max - data_min

# Parameters from helpers.py
base_offset = 0.15      # 15% of data range
stack_spacing = 0.08    # 8% of data range
text_spacing = 0.02     # 2% of data range

# Calculate first bracket position
first_bracket_y = data_max + (base_offset * data_range)
height_difference = first_bracket_y - data_max

print(f"\nData Statistics:")
print(f"  Data minimum: {data_min}")
print(f"  Data maximum: {data_max}")
print(f"  Data range:   {data_range}")

print(f"\nSpacing Parameters:")
print(f"  base_offset:   {base_offset:.2f} (15% of data range)")
print(f"  stack_spacing: {stack_spacing:.2f} (8% of data range)")
print(f"  text_spacing:  {text_spacing:.2f} (2% of data range)")

print(f"\nFirst Bracket Position:")
print(f"  Positioned at: {first_bracket_y:.1f}")
print(f"  Height above data max: {height_difference:.1f} units")
print(f"  As percentage of data range: {(height_difference/data_range)*100:.1f}%")
print(f"  As percentage of data max: {(height_difference/data_max)*100:.1f}%")

print(f"\nY-Axis Limits:")
print(f"  Y-min: {ymin:.1f}")
print(f"  Y-max: {ymax:.1f}")
print(f"  Total y-range: {ymax - ymin:.1f}")

print(f"\nTotal Headroom Calculation:")
n_comparisons = len(comparisons)
total_headroom = (base_offset + (n_comparisons - 1) * stack_spacing + text_spacing) * data_range
print(f"  Number of comparisons: {n_comparisons}")
print(f"  Total headroom: {total_headroom:.1f} units")
print(f"  Expected y-max: {data_max + total_headroom:.1f}")

print(f"\nSpacing Breakdown:")
print(f"  Data max to first bracket: {base_offset * data_range:.1f} units (base_offset)")
print(f"  Between brackets: {stack_spacing * data_range:.1f} units each (stack_spacing)")
print(f"  Bracket to text: {text_spacing * data_range:.1f} units (text_spacing, estimated from y-axis)")

# Text offset is calculated from y-axis range, not data range
y_range = ymax - ymin
text_offset_pct = 0.01  # 1% from style.py
text_offset_absolute = text_offset_pct * y_range
print(f"\nText Offset (bracket to p-value):")
print(f"  Y-axis range: {y_range:.1f}")
print(f"  text_offset_pct: {text_offset_pct:.2f} (1% of y-axis range)")
print(f"  Text offset: {text_offset_absolute:.1f} units")

print("\n" + "="*70)

plt.close()
