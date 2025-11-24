"""
PRS DataViz: Professional Data Visualization for PRS Journal Submissions

A comprehensive design system for creating publication-quality figures for
Plastic and Reconstructive Surgery (PRS) journal submissions.

Features:
- PRS-compliant figure export (300+ DPI, CMYK, proper formats)
- Professional color palettes (CMYK-safe, colorblind-friendly)
- Before/after comparison layouts
- Multi-panel figure utilities
- Accessibility-focused design (Cara Thompson's methodology)

Quick Start:
    >>> from prs_dataviz import apply_prs_style, save_prs_figure
    >>> import matplotlib.pyplot as plt
    >>>
    >>> apply_prs_style(cycle="clinical")
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [1, 4, 9])
    >>> save_prs_figure(fig, "figure1.tiff", dpi=300, width_inches=5.0)

References:
- PRS Figure Guidelines: https://journals.lww.com/plasreconsurg/
- Cara Thompson's Accessibility Methodology:
  https://www.cararthompson.com/talks/on-brand-accessibility/
"""

__version__ = "0.1.0"

# Palette exports
from .palettes import (
    # Color families
    CLINICAL_BLUE,
    TISSUE_TONE,
    CLINICAL_DATA,
    COMPARISON,
    STATISTICAL,
    COLOR_FAMILIES,
    # Categorical palettes
    CATEGORICAL,
    # Sequential palettes
    SEQUENTIAL_BLUES,
    # Diverging palettes
    DIVERGING,
    # Cycles
    PRS_DEFAULT_CYCLE,
    PRS_COMPARISON_CYCLE,
    PRS_CLINICAL_CYCLE,
    # Utilities
    rgb_to_cmyk,
    cmyk_to_rgb,
)

# Style exports
from .style import (
    apply_prs_style,
    format_statistical_plot,
    format_comparison_plot,
    add_significance_indicator,
    add_scale_bar,
    prs_legend,
    set_axis_fontsize,
)

# Export exports
from .export import (
    save_prs_figure,
    save_multi_panel_figure,
    validate_figure_file,
    PRS_MIN_DPI,
    PRS_MIN_WIDTH_SINGLE,
    PRS_MIN_WIDTH_GRAPH,
)

# Layout exports
from .layout import (
    create_before_after_figure,
    create_multi_view_figure,
    create_time_series_figure,
    create_results_panel,
)

# Helper exports
from .helpers import (
    auto_extend_ylim,
    get_data_max_in_range,
    auto_calculate_ylim_for_annotations,
    auto_position_brackets,
    calculate_bracket_position,
    add_comparison_bars,
    add_multiple_comparisons,
    create_comparison_plot,
    create_time_series_plot,
    get_significance_symbol,
    calculate_optimal_ylim,
)

__all__ = [
    # Palettes
    "CLINICAL_BLUE",
    "TISSUE_TONE",
    "CLINICAL_DATA",
    "COMPARISON",
    "STATISTICAL",
    "COLOR_FAMILIES",
    "CATEGORICAL",
    "SEQUENTIAL_BLUES",
    "DIVERGING",
    "PRS_DEFAULT_CYCLE",
    "PRS_COMPARISON_CYCLE",
    "PRS_CLINICAL_CYCLE",
    "rgb_to_cmyk",
    "cmyk_to_rgb",
    # Style
    "apply_prs_style",
    "format_statistical_plot",
    "format_comparison_plot",
    "add_significance_indicator",
    "add_scale_bar",
    "prs_legend",
    "set_axis_fontsize",
    # Export
    "save_prs_figure",
    "save_multi_panel_figure",
    "validate_figure_file",
    "PRS_MIN_DPI",
    "PRS_MIN_WIDTH_SINGLE",
    "PRS_MIN_WIDTH_GRAPH",
    # Layout
    "create_before_after_figure",
    "create_multi_view_figure",
    "create_time_series_figure",
    "create_results_panel",
    # Helpers
    "auto_extend_ylim",
    "get_data_max_in_range",
    "auto_calculate_ylim_for_annotations",
    "auto_position_brackets",
    "calculate_bracket_position",
    "add_comparison_bars",
    "add_multiple_comparisons",
    "create_comparison_plot",
    "create_time_series_plot",
    "get_significance_symbol",
    "calculate_optimal_ylim",
]
