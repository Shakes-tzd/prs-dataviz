# Visual Test Suite

This directory contains visual validation tests for the prs-dataviz package.

## Significance Annotation Tests

### test_new_significance_design.png
**NEW STANDARD** - Demonstrates improved significance annotation design based on research:

- **Panel 1**: Symbol only (*, **, ***) - Standard for publications
- **Panel 2**: P-value only (p = 0.020) - When precision is needed
- **Panel 3**: Multiple comparisons - Clean stacking

**Key Improvements:**
- Shows EITHER symbols OR p-values (not both)
- 3% spacing between bracket and text (research-based)
- Clean bracket structure with 1% tips
- 14pt symbols, 10pt p-values
- Professional, uncluttered appearance

## Comprehensive Plot Type Tests

These tests validate the package works across different plot types:

### test_line_chart_confidence.png
Line chart with confidence intervals and PRS styling.

### test_stacked_bar_chart.png
Stacked bar chart with CLINICAL_DATA palette.

### test_grouped_bars_multiple.png
Grouped bars with multiple significance comparisons.

### test_violin_plot.png
Violin plot with statistical annotations.

### test_error_bars.png
Error bars with significance indicators.

### test_scatter_regression.png
Scatter plot with regression line.

### test_horizontal_bars.png
Horizontal bar chart layout.

### test_heatmap.png
Heatmap with color-blind friendly palette.

### test_small_values.png
Tests with small value ranges (0-10).

### test_large_values.png
Tests with large value ranges (1000+).

## Design Principles

All tests follow:

1. **PRS Journal Requirements**: 300 DPI, CMYK-safe colors, accessible typography
2. **Cara Thompson's Methodology**: 10-step accessibility framework
3. **Publication Best Practices**: Research-based spacing, clean annotations
4. **Scientific Standards**: Appropriate use of symbols vs p-values

## Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test suite
uv run python tests/test_improved_significance.py
uv run python tests/test_comprehensive_plots.py
uv run python tests/test_helper_functions.py

# Regenerate visual tests
uv run python tests/test_improved_significance.py
uv run python tests/test_comprehensive_plots.py
```

## Interpreting Results

**Visual Validation**: Review generated PNG files to verify:
- Proper spacing and alignment
- Readable typography (10pt minimum)
- Professional appearance
- No overlapping elements
- Correct colors and styling

**Automated Validation**: Test scripts report pass/fail for:
- Function return values
- Positioning calculations
- Typography accessibility
- Color accuracy
