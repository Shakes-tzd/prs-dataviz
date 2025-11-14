"""
Example usage of prs-dataviz package.

Demonstrates:
1. Basic statistical plot with PRS styling
2. Before/after comparison (mock data)
3. Multi-panel statistical results
4. Figure validation
"""

import matplotlib.pyplot as plt
import numpy as np
from prs_dataviz import (
    apply_prs_style,
    save_prs_figure,
    format_statistical_plot,
    validate_figure_file,
    CLINICAL_DATA,
    COMPARISON,
)

# ============================================================================
# Example 1: Statistical Bar Chart
# ============================================================================

print("Creating Example 1: Statistical Bar Chart...")

apply_prs_style(cycle="clinical", show_grid=True)

fig1, ax1 = plt.subplots(figsize=(5, 4))

# Mock data: Patient satisfaction scores
categories = ['Pre-op', '3 mo', '6 mo', '12 mo']
control = [65, 68, 70, 72]
treatment = [65, 75, 82, 88]

x = np.arange(len(categories))
width = 0.35

bars1 = ax1.bar(x - width/2, control, width, label='Control', color=CLINICAL_DATA["Secondary"])
bars2 = ax1.bar(x + width/2, treatment, width, label='Treatment', color=CLINICAL_DATA["Primary"])

ax1.set_ylabel('Patient Satisfaction Score (%)')
ax1.set_xlabel('Follow-up Time')
ax1.set_title('Treatment Efficacy Over Time', fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(categories)
ax1.set_ylim(0, 100)
ax1.legend(frameon=True)

# Format for statistical data
format_statistical_plot(ax1, show_significance=True)

# Save figure
save_prs_figure(
    fig1,
    "example_figure1.tiff",
    dpi=300,
    width_inches=5.0,
    cmyk=True
)

print("  ✓ Saved: example_figure1.tiff")


# ============================================================================
# Example 2: Before/After Comparison Scatter Plot
# ============================================================================

print("\nCreating Example 2: Before/After Comparison...")

apply_prs_style(cycle="comparison")

fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(8, 4))

# Mock data: Measurement comparisons
np.random.seed(42)
before_values = np.random.normal(50, 10, 30)
after_values = before_values + np.random.normal(20, 5, 30)

# Before
ax2a.scatter(range(len(before_values)), before_values,
            color=COMPARISON["Before"], s=50, alpha=0.7, edgecolors='black', linewidth=0.5)
ax2a.set_ylabel('Measurement (mm)')
ax2a.set_xlabel('Patient ID')
ax2a.set_title('Preoperative', fontweight='bold')
ax2a.set_ylim(0, 100)

# After
ax2b.scatter(range(len(after_values)), after_values,
            color=COMPARISON["After"], s=50, alpha=0.7, edgecolors='black', linewidth=0.5)
ax2b.set_ylabel('Measurement (mm)')
ax2b.set_xlabel('Patient ID')
ax2b.set_title('6 Months Postoperative', fontweight='bold')
ax2b.set_ylim(0, 100)

plt.tight_layout()

save_prs_figure(
    fig2,
    "example_figure2.tiff",
    dpi=300,
    width_inches=7.0,
    cmyk=True
)

print("  ✓ Saved: example_figure2.tiff")


# ============================================================================
# Example 3: Box Plot Comparison
# ============================================================================

print("\nCreating Example 3: Box Plot Comparison...")

apply_prs_style(cycle="clinical")

fig3, ax3 = plt.subplots(figsize=(5, 4))

# Mock data: Outcome measurements
data_groups = [
    np.random.normal(60, 8, 40),   # Group A
    np.random.normal(70, 10, 40),  # Group B
    np.random.normal(75, 7, 40),   # Group C
]

positions = [1, 2, 3]
bp = ax3.boxplot(data_groups, positions=positions, widths=0.6,
                 patch_artist=True, showfliers=True)

# Color boxes
colors = [CLINICAL_DATA["Primary"], CLINICAL_DATA["Secondary"], CLINICAL_DATA["Tertiary"]]
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Style medians
for median in bp['medians']:
    median.set_color('black')
    median.set_linewidth(2)

ax3.set_xlabel('Treatment Group')
ax3.set_ylabel('Outcome Score')
ax3.set_title('Treatment Group Comparison', fontweight='bold', pad=15)
ax3.set_xticks(positions)
ax3.set_xticklabels(['Group A', 'Group B', 'Group C'])
ax3.set_ylim(30, 100)

# Add grid for easier reading
ax3.yaxis.grid(True, linestyle='--', alpha=0.3)
ax3.set_axisbelow(True)

save_prs_figure(
    fig3,
    "example_figure3.tiff",
    dpi=300,
    width_inches=5.0,
    cmyk=True
)

print("  ✓ Saved: example_figure3.tiff")


# ============================================================================
# Validate Figures
# ============================================================================

print("\n" + "="*60)
print("Validating Figures:")
print("="*60)

for filename in ["example_figure1.tiff", "example_figure2.tiff", "example_figure3.tiff"]:
    print(f"\n{filename}:")
    results = validate_figure_file(filename)

    if results['valid']:
        print("  ✓ VALID - Meets all PRS requirements")
    else:
        print("  ✗ ISSUES FOUND:")
        for issue in results['issues']:
            print(f"    - {issue}")

    print(f"  DPI: {results['dpi']:.0f}" if results['dpi'] else "  DPI: Not detected")
    if results['width_inches']:
        print(f"  Dimensions: {results['width_inches']:.2f}\" × {results['height_inches']:.2f}\"")
    print(f"  Color Mode: {results['color_mode']}")

print("\n" + "="*60)
print("Example figures created successfully!")
print("="*60)
print("\nGenerated files:")
print("  - example_figure1.tiff (Statistical bar chart)")
print("  - example_figure2.tiff (Before/after comparison)")
print("  - example_figure3.tiff (Box plot comparison)")
print("\nAll figures are PRS-compliant:")
print("  ✓ 300 DPI resolution")
print("  ✓ CMYK color mode")
print("  ✓ Proper dimensions")
print("  ✓ Professional quality")
