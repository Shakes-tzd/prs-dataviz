"""
Comprehensive testing of prs-dataviz across different plot types and data ranges.
Tests significance indicators, color palettes, and typography across scenarios.
"""
import numpy as np
import matplotlib.pyplot as plt
from prs_dataviz import (
    COMPARISON,
    CLINICAL_DATA,
    STATISTICAL,
    add_significance_indicator,
    apply_prs_style,
)


def test_line_chart_with_confidence():
    """Test line chart with confidence intervals and significance."""
    print("Testing line chart with confidence intervals...")

    apply_prs_style(cycle="comparison")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Time series data with confidence intervals
    time = np.arange(0, 13, 1)
    control_mean = 50 + 2 * time + np.random.normal(0, 2, len(time))
    treatment_mean = 50 + 5 * time + np.random.normal(0, 2, len(time))
    control_ci = 5 + np.random.normal(0, 1, len(time))
    treatment_ci = 4 + np.random.normal(0, 1, len(time))

    # Plot lines
    ax.plot(time, control_mean, marker='o', label='Control',
            color=COMPARISON["Control"], linewidth=2.5, markersize=7)
    ax.plot(time, treatment_mean, marker='s', label='Treatment',
            color=COMPARISON["Treatment"], linewidth=2.5, markersize=7)

    # Confidence intervals
    ax.fill_between(time, control_mean - control_ci, control_mean + control_ci,
                     alpha=0.2, color=COMPARISON["Control"])
    ax.fill_between(time, treatment_mean - treatment_ci, treatment_mean + treatment_ci,
                     alpha=0.2, color=COMPARISON["Treatment"])

    ax.set_xlabel("Time (months)")
    ax.set_ylabel("Recovery Score")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(40, 125)  # Extended to make room for annotation

    # Significance at final timepoint
    final_idx = -1
    add_significance_indicator(
        ax,
        x=time[final_idx] + 0.3,  # Shift right to avoid overlap
        y=115,  # Higher position with more space
        p_value=0.001,
        symbol="***",
        bracket=False,  # No bracket for time series
    )

    plt.tight_layout()
    fig.savefig("test_line_chart_confidence.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: test_line_chart_confidence.png")
    plt.close()


def test_stacked_bar_chart():
    """Test stacked bar chart with multiple categories."""
    print("\nTesting stacked bar chart...")

    apply_prs_style(cycle="clinical")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Stacked bar data
    categories = ['Baseline', '3 Months', '6 Months', '12 Months']
    mild = [30, 25, 20, 15]
    moderate = [40, 35, 30, 25]
    severe = [30, 20, 15, 10]

    x = np.arange(len(categories))
    width = 0.6

    # Stacked bars
    p1 = ax.bar(x, mild, width, label='Mild',
                color=CLINICAL_DATA["Primary"], alpha=0.8)
    p2 = ax.bar(x, moderate, width, bottom=mild, label='Moderate',
                color=CLINICAL_DATA["Secondary"], alpha=0.8)
    p3 = ax.bar(x, severe, width,
                bottom=np.array(mild) + np.array(moderate), label='Severe',
                color=CLINICAL_DATA["Tertiary"], alpha=0.8)

    ax.set_ylabel("Percentage of Patients (%)")
    ax.set_xlabel("Follow-up Time")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(loc="upper right")
    ax.set_ylim(0, 120)
    ax.grid(True, alpha=0.3, axis='y')

    # Significance for total reduction
    total_baseline = mild[0] + moderate[0] + severe[0]
    total_final = mild[-1] + moderate[-1] + severe[-1]
    add_significance_indicator(
        ax,
        x=len(categories) - 1,
        y=total_final + 5,
        p_value=0.001,
        symbol="***",
        bracket=False,
    )

    plt.tight_layout()
    fig.savefig("test_stacked_bar_chart.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: test_stacked_bar_chart.png")
    plt.close()


def test_grouped_bar_multiple_comparisons():
    """Test grouped bars with multiple significance comparisons."""
    print("\nTesting grouped bars with multiple comparisons...")

    apply_prs_style(cycle="comparison", show_grid=True)
    fig, ax = plt.subplots(figsize=(12, 6))

    # Multiple groups and timepoints
    timepoints = ['Baseline', 'Week 4', 'Week 8', 'Week 12']
    placebo = [50, 52, 54, 55]
    low_dose = [50, 58, 65, 70]
    high_dose = [50, 62, 75, 85]

    x = np.arange(len(timepoints))
    width = 0.25

    bars1 = ax.bar(x - width, placebo, width, label='Placebo',
                   color=CLINICAL_DATA["Primary"], alpha=0.8)
    bars2 = ax.bar(x, low_dose, width, label='Low Dose',
                   color=CLINICAL_DATA["Secondary"], alpha=0.8)
    bars3 = ax.bar(x + width, high_dose, width, label='High Dose',
                   color=CLINICAL_DATA["Tertiary"], alpha=0.8)

    ax.set_ylabel("Efficacy Score")
    ax.set_xlabel("Time Point")
    ax.set_xticks(x)
    ax.set_xticklabels(timepoints)
    ax.legend(loc="upper left")
    ax.set_ylim(0, 105)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    # Multiple comparisons at Week 12
    # Placebo vs High Dose
    add_significance_indicator(
        ax,
        x=x[-1],
        y=92,
        p_value=0.001,
        symbol="***",
        bracket=True,
        x_start=x[-1] - width,
        x_end=x[-1] + width,
    )

    plt.tight_layout()
    fig.savefig("test_grouped_bars_multiple.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: test_grouped_bars_multiple.png")
    plt.close()


def test_violin_plot():
    """Test violin plot with significance."""
    print("\nTesting violin plot...")

    apply_prs_style(cycle="comparison")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Generate distributions
    np.random.seed(42)
    preop = np.random.normal(45, 15, 100)
    postop_3m = np.random.normal(65, 12, 100)
    postop_6m = np.random.normal(75, 10, 100)

    positions = [1, 2, 3]
    data = [preop, postop_3m, postop_6m]

    # Create violin plot
    parts = ax.violinplot(data, positions=positions, widths=0.7,
                          showmeans=True, showmedians=True)

    # Color the violins
    colors = [COMPARISON["Before"], COMPARISON["Control"], COMPARISON["After"]]
    for pc, color in zip(parts['bodies'], colors):
        pc.set_facecolor(color)
        pc.set_alpha(0.7)

    ax.set_ylabel("Outcome Score")
    ax.set_xlabel("Time Point")
    ax.set_xticks(positions)
    ax.set_xticklabels(['Preoperative', '3 Months', '6 Months'])
    ax.set_ylim(0, 115)
    ax.grid(True, alpha=0.3, axis='y')

    # Significance between preop and 6 months
    add_significance_indicator(
        ax,
        x=2,  # Midpoint between positions 1 and 3
        y=100,
        p_value=0.001,
        symbol="***",
        bracket=True,
        x_start=1,
        x_end=3,
    )

    plt.tight_layout()
    fig.savefig("test_violin_plot.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: test_violin_plot.png")
    plt.close()


def test_error_bars():
    """Test bar chart with error bars and significance."""
    print("\nTesting error bars...")

    apply_prs_style(cycle="comparison", show_grid=True)
    fig, ax = plt.subplots(figsize=(10, 6))

    # Data with error bars
    treatments = ['Standard', 'Novel A', 'Novel B', 'Novel C']
    means = [65, 75, 82, 78]
    errors = [8, 6, 5, 7]

    x = np.arange(len(treatments))

    bars = ax.bar(x, means, width=0.6,
                  color=[CLINICAL_DATA["Primary"], CLINICAL_DATA["Secondary"],
                         CLINICAL_DATA["Tertiary"], CLINICAL_DATA["Primary"]],
                  alpha=0.8,
                  yerr=errors,
                  error_kw={'linewidth': 2, 'capsize': 5, 'capthick': 2})

    ax.set_ylabel("Treatment Efficacy (%)")
    ax.set_xlabel("Treatment Type")
    ax.set_xticks(x)
    ax.set_xticklabels(treatments)
    ax.set_ylim(0, 110)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    # Significance: Standard vs Novel B
    add_significance_indicator(
        ax,
        x=1.0,  # Midpoint between 0 and 2
        y=95,
        p_value=0.01,
        symbol="**",
        bracket=True,
        x_start=0,
        x_end=2,
    )

    plt.tight_layout()
    fig.savefig("test_error_bars.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: test_error_bars.png")
    plt.close()


def test_scatter_with_regression():
    """Test scatter plot with regression lines and significance."""
    print("\nTesting scatter plot with regression...")

    apply_prs_style(cycle="comparison")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Generate correlated data
    np.random.seed(42)
    x_data = np.linspace(0, 10, 50)

    # Control: weak correlation
    y_control = 50 + 2 * x_data + np.random.normal(0, 8, len(x_data))

    # Treatment: strong correlation
    y_treatment = 50 + 6 * x_data + np.random.normal(0, 5, len(x_data))

    # Scatter plots
    ax.scatter(x_data, y_control, s=60, alpha=0.6,
              color=COMPARISON["Control"], label='Control', edgecolors='black', linewidth=0.5)
    ax.scatter(x_data, y_treatment, s=60, alpha=0.6,
              color=COMPARISON["Treatment"], label='Treatment', edgecolors='black', linewidth=0.5)

    # Regression lines
    z_control = np.polyfit(x_data, y_control, 1)
    p_control = np.poly1d(z_control)
    ax.plot(x_data, p_control(x_data), "--",
            color=COMPARISON["Control"], linewidth=2, alpha=0.8)

    z_treatment = np.polyfit(x_data, y_treatment, 1)
    p_treatment = np.poly1d(z_treatment)
    ax.plot(x_data, p_treatment(x_data), "--",
            color=COMPARISON["Treatment"], linewidth=2, alpha=0.8)

    ax.set_xlabel("Treatment Duration (months)")
    ax.set_ylabel("Improvement Score")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(30, 125)

    # Significance for slope difference
    ax.text(7, 110, "Slope difference:", fontsize=10, color="#333")
    add_significance_indicator(
        ax,
        x=8.5,
        y=115,
        p_value=0.002,
        symbol="**",
        bracket=False,
    )

    plt.tight_layout()
    fig.savefig("test_scatter_regression.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: test_scatter_regression.png")
    plt.close()


def test_horizontal_bars():
    """Test horizontal bar chart with significance."""
    print("\nTesting horizontal bar chart...")

    apply_prs_style(cycle="clinical")
    fig, ax = plt.subplots(figsize=(10, 8))

    # Complication rates
    complications = ['Infection', 'Hematoma', 'Seroma', 'Dehiscence', 'Revision']
    rates_standard = [5.2, 3.8, 4.1, 2.5, 6.0]
    rates_improved = [2.1, 1.8, 2.0, 1.2, 2.5]

    y = np.arange(len(complications))
    height = 0.35

    bars1 = ax.barh(y - height/2, rates_standard, height, label='Standard Protocol',
                    color=CLINICAL_DATA["Primary"], alpha=0.8)
    bars2 = ax.barh(y + height/2, rates_improved, height, label='Improved Protocol',
                    color=CLINICAL_DATA["Secondary"], alpha=0.8)

    ax.set_xlabel("Complication Rate (%)")
    ax.set_ylabel("Complication Type")
    ax.set_yticks(y)
    ax.set_yticklabels(complications)
    ax.legend(loc="lower right")  # Changed from "upper right" to avoid overlap
    ax.set_xlim(0, 8)
    ax.xaxis.grid(True, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    # Note: For horizontal bars, we'd need a different approach for significance
    # Adding text annotation in upper right area (away from legend)
    ax.text(6.5, 4.3, "p < 0.001", fontsize=10, ha='right', color="#666")
    ax.text(6.5, 4.6, "***", fontsize=16, ha='right', color="#2C5F87", fontweight='bold')

    plt.tight_layout()
    fig.savefig("test_horizontal_bars.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: test_horizontal_bars.png")
    plt.close()


def test_heatmap_style():
    """Test heatmap/correlation matrix visualization."""
    print("\nTesting heatmap visualization...")

    apply_prs_style()
    fig, ax = plt.subplots(figsize=(10, 8))

    # Correlation matrix
    variables = ['Age', 'BMI', 'Duration', 'Severity', 'Outcome']
    np.random.seed(42)
    correlation_matrix = np.random.rand(5, 5)
    # Make symmetric
    correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2
    np.fill_diagonal(correlation_matrix, 1.0)

    # Heatmap
    im = ax.imshow(correlation_matrix, cmap='RdBu_r', aspect='auto',
                   vmin=-1, vmax=1)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Correlation Coefficient', rotation=270, labelpad=20)

    # Labels
    ax.set_xticks(np.arange(len(variables)))
    ax.set_yticks(np.arange(len(variables)))
    ax.set_xticklabels(variables)
    ax.set_yticklabels(variables)

    # Rotate x labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Add correlation values
    for i in range(len(variables)):
        for j in range(len(variables)):
            text = ax.text(j, i, f'{correlation_matrix[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=9)


    plt.tight_layout()
    fig.savefig("test_heatmap.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: test_heatmap.png")
    plt.close()


def test_small_values():
    """Test with small value ranges (< 10)."""
    print("\nTesting small value ranges...")

    apply_prs_style(cycle="comparison", show_grid=True)
    fig, ax = plt.subplots(figsize=(8, 5))

    categories = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    control = [2.1, 2.3, 2.4, 2.5]
    treatment = [2.1, 3.5, 4.8, 6.2]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, control, width, label='Control',
                   color=COMPARISON["Control"], alpha=0.8)
    bars2 = ax.bar(x + width/2, treatment, width, label='Treatment',
                   color=COMPARISON["Treatment"], alpha=0.8)

    ax.set_ylabel("Pain Score (0-10)")
    ax.set_xlabel("Time Point")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 8)
    ax.legend(loc="upper left")
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)

    # Significance at Week 4
    add_significance_indicator(
        ax,
        x=x[-1],
        y=7.0,
        p_value=0.001,
        symbol="***",
        bracket=True,
        x_start=x[-1] - width/2,
        x_end=x[-1] + width/2,
    )

    plt.tight_layout()
    fig.savefig("test_small_values.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: test_small_values.png")
    plt.close()


def test_large_values():
    """Test with large value ranges (> 1000)."""
    print("\nTesting large value ranges...")

    apply_prs_style(cycle="clinical", show_grid=True)
    fig, ax = plt.subplots(figsize=(8, 5))

    years = ['2020', '2021', '2022', '2023']
    procedures = [1200, 1450, 1680, 1920]

    x = np.arange(len(years))

    bars = ax.bar(x, procedures, width=0.6,
                  color=CLINICAL_DATA["Primary"], alpha=0.8)

    ax.set_ylabel("Number of Procedures")
    ax.set_xlabel("Year")
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylim(0, 2200)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)

    # Significance annotation only (trend label removed for clarity)
    add_significance_indicator(
        ax,
        x=1.5,
        y=2050,
        p_value=0.001,
        symbol="***",
        bracket=False,
    )

    plt.tight_layout()
    fig.savefig("test_large_values.png", dpi=150, bbox_inches="tight")
    print("  ✅ Saved: test_large_values.png")
    plt.close()


def main():
    """Run all comprehensive tests."""
    print("=" * 70)
    print("Comprehensive Plot Type Testing - PRS-DataViz")
    print("=" * 70)

    test_line_chart_with_confidence()
    test_stacked_bar_chart()
    test_grouped_bar_multiple_comparisons()
    test_violin_plot()
    test_error_bars()
    test_scatter_with_regression()
    test_horizontal_bars()
    test_heatmap_style()
    test_small_values()
    test_large_values()

    print("\n" + "=" * 70)
    print("All comprehensive tests completed!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  1. test_line_chart_confidence.png")
    print("  2. test_stacked_bar_chart.png")
    print("  3. test_grouped_bars_multiple.png")
    print("  4. test_violin_plot.png")
    print("  5. test_error_bars.png")
    print("  6. test_scatter_regression.png")
    print("  7. test_horizontal_bars.png")
    print("  8. test_heatmap.png")
    print("  9. test_small_values.png")
    print(" 10. test_large_values.png")
    print("\nPlease review all images for visual validation.")


if __name__ == "__main__":
    main()
