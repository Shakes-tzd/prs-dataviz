"""Regenerate the FIXED and FINAL_FIX test files with new spacing."""
import sys
sys.path.insert(0, '/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/src')

import numpy as np
import matplotlib.pyplot as plt
from prs_dataviz import apply_prs_style, add_multiple_comparisons, COMPARISON

output_dir = "/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/tests/visual_tests"

print("Regenerating FIXED test files with reduced spacing...")
print("text_spacing: 0.02, text_offset: 0.01")
print()

# test_auto_large_values_FIXED.png
print("[1/2] Regenerating test_auto_large_values_FIXED.png...")
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
plt.savefig(f"{output_dir}/test_auto_large_values_FIXED.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Saved")

# test_FINAL_FIX.png
print("\n[2/2] Regenerating test_FINAL_FIX.png...")
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
plt.savefig(f"{output_dir}/test_FINAL_FIX.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Saved")

print("\n✅ Both FIXED files regenerated successfully!")
print("   - Reduced text spacing: 0.02 (was 0.05)")
print("   - Reduced text offset: 0.01 (was 0.03)")
print("   - Brackets and p-values now much closer together\n")
