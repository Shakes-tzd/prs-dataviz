"""Debug script to test bracket rendering."""
import sys
sys.path.insert(0, '../src')

import numpy as np
import matplotlib.pyplot as plt
from prs_dataviz import apply_prs_style, add_multiple_comparisons, COMPARISON

apply_prs_style(cycle="comparison")
fig, ax = plt.subplots(figsize=(10, 6))

# Large values (same as test)
data = [1250, 1680, 2150, 2890]
x = np.arange(len(data))
ax.bar(x, data, width=0.6, color=COMPARISON["Treatment"], alpha=0.8)

ax.set_ylabel("Revenue ($)")
ax.set_title("DEBUG: Large Values - Bracket Test", fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
ax.grid(True, alpha=0.3, axis='y')

# Three comparisons
comparisons = [
    (2, 3, 0.025),  # Q3 vs Q4 - narrow bracket
    (1, 3, 0.008),  # Q2 vs Q4 - medium bracket
    (0, 3, 0.0002), # Q1 vs Q4 - wide bracket
]

print("\nDEBUG INFO:")
print("="*70)
print("Comparisons to draw:")
for i, (idx1, idx2, p_val) in enumerate(comparisons):
    print(f"  {i+1}. {['Q1','Q2','Q3','Q4'][idx1]} vs {['Q1','Q2','Q3','Q4'][idx2]}: p = {p_val}")

# Call the function
print("\nCalling add_multiple_comparisons...")
add_multiple_comparisons(ax, comparisons, x)

print(f"Y-axis limits after: {ax.get_ylim()}")
print("\nPlease check the generated image for bracket visibility.")
print("="*70)

plt.tight_layout()
plt.savefig("visual_tests/debug_brackets.png", dpi=150, bbox_inches='tight')
print("\nSaved: visual_tests/debug_brackets.png")
plt.close()
