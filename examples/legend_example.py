"""
Example: Using prs_legend() for professional legend styling

Demonstrates the enhanced prs_legend() function with various positioning
and styling options.
"""

import matplotlib.pyplot as plt
import numpy as np
from prs_dataviz import apply_prs_style, prs_legend, CLINICAL_DATA

# Apply PRS styling
apply_prs_style(cycle="clinical")

# Create sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.exp(-x / 10)

# ============================================================================
# Example 1: Top-positioned compact legend (horizontal, 2 columns)
# ============================================================================
print("Example 1: Top-positioned compact legend")

fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(x, y1, label="Treatment A", linewidth=2)
ax1.plot(x, y2, label="Treatment B", linewidth=2)
ax1.set_xlabel("Time (months)")
ax1.set_ylabel("Response")
ax1.set_title("Clinical Response Over Time", fontweight="bold", pad=20)

# Professional top-aligned legend (matches your requirements)
prs_legend(ax1, position="top", ncol=2)

plt.tight_layout()
plt.savefig("legend_example1_top.png", dpi=150, bbox_inches="tight")
print("  Saved: legend_example1_top.png")

# ============================================================================
# Example 2: Compact legend with custom positioning
# ============================================================================
print("\nExample 2: Custom position with compact spacing")

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.plot(x, y1, label="Non-syndromic", linewidth=2, color=CLINICAL_DATA["Primary"])
ax2.plot(x, y2, label="Syndromic", linewidth=2, color=CLINICAL_DATA["Secondary"])
ax2.plot(x, y3, label="Combined", linewidth=2, color=CLINICAL_DATA["Tertiary"])
ax2.set_xlabel("Time (months)")
ax2.set_ylabel("Response")
ax2.set_title("Treatment Response by Group", fontweight="bold")

# Compact legend in upper left with 3 columns
prs_legend(ax2, position="upper left", ncol=3, compact=True)

plt.tight_layout()
plt.savefig("legend_example2_compact.png", dpi=150, bbox_inches="tight")
print("  Saved: legend_example2_compact.png")

# ============================================================================
# Example 3: Outside legend (right side)
# ============================================================================
print("\nExample 3: Outside legend (right side)")

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.plot(x, y1, label="Before Treatment", linewidth=2)
ax3.plot(x, y2, label="After Treatment", linewidth=2)
ax3.plot(x, y3, label="Follow-up", linewidth=2)
ax3.set_xlabel("Time (months)")
ax3.set_ylabel("Measurement")
ax3.set_title("Treatment Progression", fontweight="bold")

# Legend outside plot area (right side)
prs_legend(ax3, position="outside")

plt.tight_layout()
plt.savefig("legend_example3_outside.png", dpi=150, bbox_inches="tight")
print("  Saved: legend_example3_outside.png")

# ============================================================================
# Example 4: Auto-positioned legend (matplotlib "best")
# ============================================================================
print("\nExample 4: Auto-positioned legend")

fig4, ax4 = plt.subplots(figsize=(8, 5))
ax4.plot(x, y1, label="Group A", linewidth=2)
ax4.plot(x, y2, label="Group B", linewidth=2)
ax4.set_xlabel("Time (months)")
ax4.set_ylabel("Outcome Score")
ax4.set_title("Treatment Outcomes", fontweight="bold")

# Automatic optimal positioning
prs_legend(ax4)  # Uses position="best" by default

plt.tight_layout()
plt.savefig("legend_example4_auto.png", dpi=150, bbox_inches="tight")
print("  Saved: legend_example4_auto.png")

# ============================================================================
# Example 5: Bar chart with top legend (your exact use case)
# ============================================================================
print("\nExample 5: Bar chart with top legend (your use case)")

fig5, ax5 = plt.subplots(figsize=(10, 6))

categories = ["Growth\nDelay", "Speech\nTherapy", "Prenatal\nDiagnosis", "Adopted"]
non_syndromic = [18, 85, 10, 5]
syndromic = [40, 50, 15, 0]

x_pos = np.arange(len(categories))
width = 0.35

ax5.bar(
    x_pos - width / 2,
    non_syndromic,
    width,
    label="Non-syndromic",
    color=CLINICAL_DATA["Primary"],
    alpha=0.9,
)
ax5.bar(
    x_pos + width / 2,
    syndromic,
    width,
    label="Syndromic",
    color=CLINICAL_DATA["Secondary"],
    alpha=0.9,
)

ax5.set_ylabel("Number of Patients")
ax5.set_xticks(x_pos)
ax5.set_xticklabels(categories)
ax5.spines["top"].set_visible(False)
ax5.spines["right"].set_visible(False)

# Professional top legend with exact parameters you wanted
prs_legend(
    ax5,
    position="top",
    ncol=2,
    fontsize=12,
    # All your parameters are now defaults for position="top"!
)

plt.tight_layout()
plt.savefig("legend_example5_barchart.png", dpi=150, bbox_inches="tight")
print("  Saved: legend_example5_barchart.png")

print("\n✅ All examples completed!")
print("\nUsage Summary:")
print("  prs_legend(ax, position='top', ncol=2)  # Top, compact, 2 columns")
print("  prs_legend(ax, position='outside')      # Right side, outside")
print("  prs_legend(ax)                          # Auto-positioned")
print("  prs_legend(ax, compact=True, ncol=3)    # Compact spacing, any position")
