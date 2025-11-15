"""Regenerate all automatic positioning tests with reduced text spacing."""
import sys
sys.path.insert(0, '/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/src')

import numpy as np
import matplotlib.pyplot as plt
from prs_dataviz import apply_prs_style, add_multiple_comparisons, COMPARISON

output_dir = "/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/tests/visual_tests"

print("\n" + "="*70)
print("REGENERATING ALL TESTS WITH REDUCED TEXT SPACING")
print("text_spacing: 0.02 (was 0.05)")
print("text_offset: 0.01 (was 0.03)")
print("="*70)

# Test 1: Small values
print("\n[1/5] Regenerating test_auto_small_values.png...")
apply_prs_style(cycle="comparison")
fig, ax = plt.subplots(figsize=(10, 6))
data = [2.5, 3.8, 5.2, 7.1]
x = np.arange(len(data))
ax.bar(x, data, width=0.6, color=COMPARISON["Control"], alpha=0.8)
ax.set_ylabel("Score")
ax.set_xticks(x)
ax.set_xticklabels(['A', 'B', 'C', 'D'])
ax.grid(True, alpha=0.3, axis='y')
comparisons = [(2, 3, 0.04), (1, 3, 0.01), (0, 3, 0.001)]
add_multiple_comparisons(ax, comparisons, x)
ymin, ymax = ax.get_ylim()
print(f"   Y-limits: {ymin:.1f} - {ymax:.1f} (data max: {max(data)})")
plt.tight_layout()
plt.savefig(f"{output_dir}/test_auto_small_values.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Saved")

# Test 2: Large values
print("\n[2/5] Regenerating test_auto_large_values.png...")
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
print(f"   Y-limits: {ymin:.1f} - {ymax:.1f} (data max: {max(data)})")
plt.tight_layout()
plt.savefig(f"{output_dir}/test_auto_large_values.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Saved")

# Test 3: Irregular spacing
print("\n[3/5] Regenerating test_auto_irregular_spacing.png...")
apply_prs_style(cycle="comparison")
fig, ax = plt.subplots(figsize=(10, 6))
x = np.array([0, 1.5, 2.8, 5.0])
data = [45, 62, 78, 91]
ax.bar(x, data, width=0.4, color=COMPARISON["Control"], alpha=0.8)
ax.set_ylabel("Efficacy (%)")
ax.set_xticks(x)
ax.set_xticklabels(['Day 1', 'Day 3', 'Week 1', 'Week 4'])
ax.grid(True, alpha=0.3, axis='y')
comparisons = [(2, 3, 0.04), (1, 3, 0.01), (0, 3, 0.0005)]
add_multiple_comparisons(ax, comparisons, x)
ymin, ymax = ax.get_ylim()
print(f"   Y-limits: {ymin:.1f} - {ymax:.1f} (data max: {max(data)})")
plt.tight_layout()
plt.savefig(f"{output_dir}/test_auto_irregular_spacing.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Saved")

# Test 4: Many comparisons
print("\n[4/5] Regenerating test_auto_many_comparisons.png...")
apply_prs_style(cycle="comparison")
fig, ax = plt.subplots(figsize=(12, 7))
data = [30, 45, 55, 70, 82, 95]
x = np.arange(len(data))
ax.bar(x, data, width=0.6, color=COMPARISON["Treatment"], alpha=0.8)
ax.set_ylabel("Score (%)")
ax.set_xticks(x)
ax.set_xticklabels(['Baseline', 'M1', 'M2', 'M3', 'M4', 'M5'])
ax.grid(True, alpha=0.3, axis='y')
comparisons = [(4, 5, 0.04), (3, 5, 0.02), (2, 5, 0.01), (1, 5, 0.005), (0, 5, 0.001)]
add_multiple_comparisons(ax, comparisons, x)
ymin, ymax = ax.get_ylim()
print(f"   Y-limits: {ymin:.1f} - {ymax:.1f} (data max: {max(data)})")
plt.tight_layout()
plt.savefig(f"{output_dir}/test_auto_many_comparisons.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Saved")

# Test 5: Grouped bars
print("\n[5/5] Regenerating test_auto_grouped_bars.png...")
apply_prs_style(cycle="comparison")
fig, ax = plt.subplots(figsize=(10, 6))
categories = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
control = [50, 52, 54, 55]
treatment = [50, 60, 72, 88]
x = np.arange(len(categories))
width = 0.35
ax.bar(x - width/2, control, width, label='Control',
       color=COMPARISON['Control'], alpha=0.8)
ax.bar(x + width/2, treatment, width, label='Treatment',
       color=COMPARISON['Treatment'], alpha=0.8)
ax.set_ylabel("Recovery Score")
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc="upper left")
ax.grid(True, alpha=0.3, axis='y')
comparisons = [(2, 3, 0.02), (1, 3, 0.005), (0, 3, 0.0001)]
treatment_positions = x + width/2
add_multiple_comparisons(ax, comparisons, treatment_positions)
ymin, ymax = ax.get_ylim()
print(f"   Y-limits: {ymin:.1f} - {ymax:.1f} (data max: {max(treatment)})")
plt.tight_layout()
plt.savefig(f"{output_dir}/test_auto_grouped_bars.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Saved")

print("\n" + "="*70)
print("ALL TESTS REGENERATED SUCCESSFULLY!")
print("="*70)
print("\n✅ Check visual_tests/ directory for updated plots")
print("   - Reduced text spacing from 0.05 to 0.02 (60% reduction)")
print("   - Reduced text offset from 0.03 to 0.01 (67% reduction)")
print("   - Brackets and p-values should be much closer together\n")
