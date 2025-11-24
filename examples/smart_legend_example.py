"""
Example: Smart Legend Positioning with Auto-Column Calculation

Demonstrates:
1. Auto-calculation of optimal columns based on label length
2. Smart positioning to avoid data overlap
3. Dynamic bbox_to_anchor adjustment
"""

import matplotlib.pyplot as plt
import numpy as np
from prs_dataviz import apply_prs_style, prs_legend, CLINICAL_DATA

apply_prs_style(cycle="clinical")

# ============================================================================
# Example 1: Short Labels → More Columns (Auto-calculates 2-4 columns)
# ============================================================================
print("Example 1: Short labels - auto-calculates optimal columns")

fig1, ax1 = plt.subplots(figsize=(10, 6))

# Short labels
categories = ["Growth\nDelay", "Speech\nTherapy", "Prenatal\nDiagnosis", "Adopted"]
data1 = [82, 15, 90, 95]
data2 = [18, 85, 10, 5]
data3 = [60, 50, 85, 100]
data4 = [40, 50, 15, 0]

x_pos = np.arange(len(categories))
width = 0.2

ax1.barh(x_pos, data1, width, label="Non-syndromic: No", color=CLINICAL_DATA["Primary"])
ax1.barh(x_pos + width, data2, width, label="Non-syndromic: Yes", color=CLINICAL_DATA["Secondary"])
ax1.barh(x_pos + 2*width, data3, width, label="Syndromic: No", color=CLINICAL_DATA["Tertiary"])
ax1.barh(x_pos + 3*width, data4, width, label="Syndromic: Yes", color=CLINICAL_DATA["Accent"])

ax1.set_yticks(x_pos + 1.5 * width)
ax1.set_yticklabels(categories)
ax1.set_xlabel("Number of Patients")
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Smart top positioning - automatically calculates 2 columns
# (Short labels + 4 items = 2 columns optimal)
prs_legend(ax1, position="top-smart")

plt.tight_layout()
plt.savefig("smart_legend_1_short.png", dpi=150, bbox_inches="tight")
print(f"  Saved: smart_legend_1_short.png")
print(f"  Auto-calculated columns: 2 (short labels)")

# ============================================================================
# Example 2: Long Labels → Fewer Columns (Auto-calculates 1 column)
# ============================================================================
print("\nExample 2: Long labels - auto-calculates fewer columns")

fig2, ax2 = plt.subplots(figsize=(10, 6))

# Long labels (like your second image)
ax2.barh(x_pos, data1, width,
         label="Non-syndromic patients: No complications",
         color=CLINICAL_DATA["Primary"])
ax2.barh(x_pos + width, data2, width,
         label="Non-syndromic patients: With complications",
         color=CLINICAL_DATA["Secondary"])

ax2.set_yticks(x_pos + 0.5 * width)
ax2.set_yticklabels(categories)
ax2.set_xlabel("Number of Patients")
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Smart top positioning - automatically calculates 1 column
# (Long labels → 1 column to avoid clipping)
prs_legend(ax2, position="top-smart")

plt.tight_layout()
plt.savefig("smart_legend_2_long.png", dpi=150, bbox_inches="tight")
print(f"  Saved: smart_legend_2_long.png")
print(f"  Auto-calculated columns: 1 (long labels)")

# ============================================================================
# Example 3: Medium Labels → Balanced (Auto-calculates 2-3 columns)
# ============================================================================
print("\nExample 3: Medium labels - balanced approach")

fig3, ax3 = plt.subplots(figsize=(10, 6))

# Medium-length labels
ax3.barh(x_pos, data1, width, label="Non-syndromic: No", color=CLINICAL_DATA["Primary"])
ax3.barh(x_pos + width, data2, width, label="Non-syndromic: Yes", color=CLINICAL_DATA["Secondary"])
ax3.barh(x_pos + 2*width, data3, width, label="Syndromic: No", color=CLINICAL_DATA["Tertiary"])
ax3.barh(x_pos + 3*width, data4, width, label="Syndromic: Yes", color=CLINICAL_DATA["Accent"])

ax3.set_yticks(x_pos + 1.5 * width)
ax3.set_yticklabels(categories)
ax3.set_xlabel("Number of Patients")
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# Smart top positioning - automatically calculates 2 columns
prs_legend(ax3, position="top-smart")

plt.tight_layout()
plt.savefig("smart_legend_3_medium.png", dpi=150, bbox_inches="tight")
print(f"  Saved: smart_legend_3_medium.png")
print(f"  Auto-calculated columns: 2 (medium labels)")

# ============================================================================
# Example 4: "best" Position - Avoids Overlap (Matplotlib's Smart Algorithm)
# ============================================================================
print("\nExample 4: Smart positioning to avoid data overlap")

fig4, ax4 = plt.subplots(figsize=(8, 6))

# Create data with clear space in upper left
x = np.linspace(0, 10, 100)
y1 = np.exp(-x/5) * np.sin(x)  # Data in lower region
y2 = np.exp(-x/5) * np.cos(x)  # Data in lower region

ax4.plot(x, y1, label="Treatment A", linewidth=2)
ax4.plot(x, y2, label="Treatment B", linewidth=2)
ax4.set_xlabel("Time (months)")
ax4.set_ylabel("Response")
ax4.set_title("Matplotlib's 'best' Algorithm Avoids Data", fontweight="bold", pad=15)
ax4.grid(True, alpha=0.3)

# position="best" uses matplotlib's smart algorithm
# It will place the legend where it minimally overlaps with data
prs_legend(ax4, position="best")

plt.tight_layout()
plt.savefig("smart_legend_4_best.png", dpi=150, bbox_inches="tight")
print(f"  Saved: smart_legend_4_best.png")
print(f"  Using matplotlib's 'best' algorithm to avoid overlap")

# ============================================================================
# Example 5: Comparison - Manual vs Auto Columns
# ============================================================================
print("\nExample 5: Comparison - Manual vs Auto columns")

fig5, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(14, 5))

# Same data, different legend approaches
for ax in [ax5a, ax5b]:
    ax.barh(x_pos, data1, width, label="Non-syndromic: No", color=CLINICAL_DATA["Primary"])
    ax.barh(x_pos + width, data2, width, label="Non-syndromic: Yes", color=CLINICAL_DATA["Secondary"])
    ax.barh(x_pos + 2*width, data3, width, label="Syndromic: No", color=CLINICAL_DATA["Tertiary"])
    ax.barh(x_pos + 3*width, data4, width, label="Syndromic: Yes", color=CLINICAL_DATA["Accent"])
    ax.set_yticks(x_pos + 1.5 * width)
    ax.set_yticklabels(categories)
    ax.set_xlabel("Number of Patients")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Manual: Force 4 columns (might be too wide)
ax5a.set_title("Manual: ncol=4", fontweight="bold", pad=20)
prs_legend(ax5a, position="top", ncol=4)

# Auto: Smart calculation (will choose 2)
ax5b.set_title("Auto: Smart Calculation", fontweight="bold", pad=20)
prs_legend(ax5b, position="top-smart")

plt.tight_layout()
plt.savefig("smart_legend_5_comparison.png", dpi=150, bbox_inches="tight")
print(f"  Saved: smart_legend_5_comparison.png")
print(f"  Left: Manual ncol=4 | Right: Auto ncol=2")

# ============================================================================
# Example 6: No Title (Common in PRS) - Adjusted Positioning
# ============================================================================
print("\nExample 6: PRS-style plot without title")

fig6, ax6 = plt.subplots(figsize=(10, 6))

ax6.barh(x_pos, data1, width, label="Non-syndromic: No", color=CLINICAL_DATA["Primary"])
ax6.barh(x_pos + width, data2, width, label="Non-syndromic: Yes", color=CLINICAL_DATA["Secondary"])
ax6.barh(x_pos + 2*width, data3, width, label="Syndromic: No", color=CLINICAL_DATA["Tertiary"])
ax6.barh(x_pos + 3*width, data4, width, label="Syndromic: Yes", color=CLINICAL_DATA["Accent"])

ax6.set_yticks(x_pos + 1.5 * width)
ax6.set_yticklabels(categories)
ax6.set_xlabel("Number of Patients")
ax6.spines['top'].set_visible(False)
ax6.spines['right'].set_visible(False)

# NO TITLE - common in PRS manuscripts
# Legend positioned with smart columns
prs_legend(ax6, position="top-smart")

plt.tight_layout()
plt.savefig("smart_legend_6_notitle.png", dpi=150, bbox_inches="tight")
print(f"  Saved: smart_legend_6_notitle.png")
print(f"  PRS-style: No title, smart legend positioning")

print("\n✅ All examples completed!")
print("\n" + "="*70)
print("SUMMARY: Smart Legend Features")
print("="*70)
print("\n1. AUTO-COLUMN CALCULATION:")
print("   - Short labels (< 15 chars): 2-4 columns")
print("   - Medium labels (15-25 chars): 2-3 columns")
print("   - Long labels (> 25 chars): 1-2 columns")
print("   - Very long labels (> 40 chars): 1 column")
print("\n2. SMART POSITIONING:")
print("   - position='best': Matplotlib avoids data overlap")
print("   - position='top-smart': Auto-columns + optimal centering")
print("   - bbox_to_anchor auto-adjusted based on ncol")
print("\n3. USAGE:")
print("   prs_legend(ax, position='top-smart')     # Full auto")
print("   prs_legend(ax, position='top', ncol=2)   # Manual override")
print("   prs_legend(ax)                           # Smart 'best' position")
print("="*70)
