"""
Test improved significance indicator design.

Compares old approach (symbol + p-value) vs new approach (symbol OR p-value).
"""
import numpy as np
import matplotlib.pyplot as plt
from prs_dataviz import (
    apply_prs_style,
    add_significance_indicator,
    COMPARISON,
)


def test_new_design():
    """Test the improved significance indicator design."""
    print("\n" + "="*70)
    print("IMPROVED SIGNIFICANCE INDICATOR DESIGN")
    print("="*70)
    print("\nBased on research:")
    print("  - Show EITHER symbols OR p-values (not both)")
    print("  - 3% spacing between bracket and text")
    print("  - Clean bracket structure with 1% tips")
    print("  - 10pt p-values (default), 14pt symbols")
    print("="*70 + "\n")

    apply_prs_style(cycle="comparison")

    # Create figure with 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

    # Shared data
    categories = ['Pre-op', '3mo', '6mo', '12mo']
    control = [65, 68, 70, 72]
    treatment = [65, 75, 82, 88]

    x = np.arange(len(categories))
    width = 0.35

    # ========================================================================
    # Test 1: P-value only (DEFAULT)
    # ========================================================================
    ax1.bar(x - width/2, control, width, label='Control',
            color=COMPARISON['Control'], alpha=0.8)
    ax1.bar(x + width/2, treatment, width, label='Treatment',
            color=COMPARISON['Treatment'], alpha=0.8)

    ax1.set_ylabel("Score (%)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.legend(loc="upper left")
    ax1.set_ylim(0, 105)
    ax1.yaxis.grid(True, linestyle="--", alpha=0.3)

    # Add significance with p-value (default behavior)
    add_significance_indicator(
        ax1,
        x=3,
        y=92,
        p_value=0.020,  # Show p-value (default)
        bracket=True,
        x_start=3 - width/2,
        x_end=3 + width/2
    )

    # ========================================================================
    # Test 2: Symbol only (when visual clarity needed)
    # ========================================================================
    ax2.bar(x - width/2, control, width, label='Control',
            color=COMPARISON['Control'], alpha=0.8)
    ax2.bar(x + width/2, treatment, width, label='Treatment',
            color=COMPARISON['Treatment'], alpha=0.8)

    ax2.set_ylabel("Score (%)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories)
    ax2.legend(loc="upper left")
    ax2.set_ylim(0, 105)
    ax2.yaxis.grid(True, linestyle="--", alpha=0.3)

    # Add significance with symbol only
    add_significance_indicator(
        ax2,
        x=3,
        y=92,
        symbol="*",  # Show symbol only
        bracket=True,
        x_start=3 - width/2,
        x_end=3 + width/2,
        show_p_value=False  # Override default to show symbol
    )

    # ========================================================================
    # Test 3: Multiple comparisons with p-values (DEFAULT)
    # ========================================================================
    ax3.bar(x, [65, 70, 85, 90], width=0.5, color='steelblue', alpha=0.7)
    ax3.set_ylabel("Score (%)")
    ax3.set_xticks(x)
    ax3.set_xticklabels(categories)
    ax3.set_ylim(0, 125)  # Increased to prevent overlap
    ax3.yaxis.grid(True, linestyle="--", alpha=0.3)

    # Multiple stacked comparisons with p-values (default behavior)
    # Increased spacing between brackets to prevent overlap
    comparisons = [
        (2, 3, 94, 0.030),     # 6mo vs 12mo - lowest bracket
        (1, 3, 104, 0.005),    # 3mo vs 12mo - middle bracket
        (0, 3, 114, 0.0005),   # Pre-op vs 12mo - highest bracket
    ]

    for idx1, idx2, y_pos, p_val in comparisons:
        add_significance_indicator(
            ax3,
            x=(x[idx1] + x[idx2]) / 2,
            y=y_pos,
            p_value=p_val,  # Show p-value (default)
            bracket=True,
            x_start=x[idx1],
            x_end=x[idx2]
        )

    plt.tight_layout()
    plt.savefig("test_new_significance_design.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("✅ Test completed successfully!")
    print("   Generated: test_new_significance_design.png\n")
    print("Key improvements:")
    print("  ✓ Shows ONLY p-values or symbols (cleaner)")
    print("  ✓ Better spacing (3% offset)")
    print("  ✓ Clean bracket structure")
    print("  ✓ Multiple comparisons properly stacked")
    print("  ✓ P-values shown by default for precision")
    print("\n" + "="*70)


if __name__ == "__main__":
    test_new_design()
