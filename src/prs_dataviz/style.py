"""
Professional matplotlib styling for PRS journal submissions.

Applies clean, professional styling appropriate for medical/surgical publications:
- High contrast for clarity
- Professional fonts
- Clean, minimal design
- Print-friendly defaults

Reference: Cara Thompson's 10-step design system methodology
https://www.cararthompson.com/talks/on-brand-accessibility/
"""

import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib import font_manager

from .palettes import (
    PRS_CLINICAL_CYCLE,
    PRS_COMPARISON_CYCLE,
    PRS_DEFAULT_CYCLE,
)

# ============================================================================
# Style Application
# ============================================================================


def apply_prs_style(
    *,
    cycle: str = "default",
    font_family: str | list[str] = "DejaVu Sans",
    font_size: int = 10,
    show_grid: bool = False,
    show_spines: bool = True,
    custom_font_paths: list[str] | None = None,
) -> None:
    """
    Apply PRS-compliant styling to matplotlib globally.

    Parameters
    ----------
    cycle : str, default "default"
        Color cycle to use:
        - "default": Professional categorical palette
        - "clinical": Muted clinical data palette
        - "comparison": Before/after comparison palette
    font_family : str or list[str], default "DejaVu Sans"
        Font family or fallback chain. DejaVu Sans is recommended for
        professional medical publications.
    font_size : int, default 10
        Base font size in points.
    show_grid : bool, default False
        Whether to show grid lines. Generally False for medical images.
    show_spines : bool, default True
        Whether to show axis spines. Generally True for medical data.
    custom_font_paths : list[str] or None, default None
        Optional paths to custom font files to register.

    Examples
    --------
    >>> apply_prs_style(cycle="default")
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [1, 4, 9])

    >>> # For before/after comparisons
    >>> apply_prs_style(cycle="comparison")

    >>> # For clinical data with grid
    >>> apply_prs_style(cycle="clinical", show_grid=True)
    """
    # Register custom fonts if provided
    if custom_font_paths is not None:
        for font_path in custom_font_paths:
            font_manager.fontManager.addfont(font_path)

    # Select color cycle
    if cycle == "default":
        color_cycle = PRS_DEFAULT_CYCLE
    elif cycle == "clinical":
        color_cycle = PRS_CLINICAL_CYCLE
    elif cycle == "comparison":
        color_cycle = PRS_COMPARISON_CYCLE
    else:
        raise ValueError(
            f"Unknown cycle '{cycle}'. Use 'default', 'clinical', or 'comparison'"
        )

    # Apply rcParams
    plt.rcParams.update(
        {
            # Figure settings
            "figure.facecolor": "white",
            "figure.dpi": 100,  # Screen DPI (use save_prs_figure for print DPI)
            "figure.autolayout": False,
            # Axes settings
            "axes.facecolor": "white",
            "axes.edgecolor": "#333333",
            "axes.linewidth": 1.0,
            "axes.grid": show_grid,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": show_spines,
            "axes.spines.bottom": show_spines,
            "axes.labelcolor": "#333333",
            "axes.labelsize": font_size,
            "axes.titlesize": font_size + 2,
            "axes.titleweight": "bold",
            "axes.titlepad": 10,
            # Color cycle
            "axes.prop_cycle": cycler(color=color_cycle),
            # Grid settings
            "grid.alpha": 0.3,
            "grid.color": "#CCCCCC",
            "grid.linestyle": "-",
            "grid.linewidth": 0.5,
            # Ticks
            "xtick.bottom": show_spines,
            "xtick.top": False,
            "xtick.labelsize": font_size,  # Increased from font_size - 1 for accessibility
            "xtick.color": "#333333",
            "xtick.direction": "out",
            "ytick.left": show_spines,
            "ytick.right": False,
            "ytick.labelsize": font_size,  # Increased from font_size - 1 for accessibility
            "ytick.color": "#333333",
            "ytick.direction": "out",
            # Font settings
            "font.family": [font_family]
            if isinstance(font_family, str)
            else font_family,
            "font.size": font_size,
            "text.color": "#333333",
            # Legend
            "legend.frameon": True,
            "legend.framealpha": 1.0,
            "legend.facecolor": "white",
            "legend.edgecolor": "#CCCCCC",
            "legend.fontsize": font_size,  # Increased from font_size - 1 for accessibility
            "legend.title_fontsize": font_size,
            "legend.borderpad": 0.5,
            "legend.labelspacing": 0.5,
            # Lines
            "lines.linewidth": 1.5,
            "lines.markersize": 6,
            "lines.markeredgewidth": 0.5,
            "lines.markeredgecolor": "auto",
            # Patches (bars, etc.)
            "patch.linewidth": 0.5,
            "patch.edgecolor": "#333333",
            "patch.force_edgecolor": False,
            # Saving figures
            "savefig.dpi": 300,  # High DPI for saving
            "savefig.facecolor": "white",
            "savefig.edgecolor": "white",
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.1,
        }
    )


# ============================================================================
# Specialized Styling Functions
# ============================================================================


def format_statistical_plot(
    ax,
    show_significance: bool = True,
    p_value_threshold: float = 0.05,
) -> None:
    """
    Format a plot for statistical data with significance indicators.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to format.
    show_significance : bool, default True
        Whether to show significance indicators.
    p_value_threshold : float, default 0.05
        Threshold for statistical significance.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.bar(['Control', 'Treatment'], [10, 15])
    >>> format_statistical_plot(ax)
    """
    # Ensure grid for data reading
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    # Clean up spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def format_comparison_plot(ax, comparison_type: str = "before_after") -> None:
    """
    Format a plot for before/after or treatment comparisons.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to format.
    comparison_type : str, default "before_after"
        Type of comparison: "before_after" or "control_treatment".

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [1, 2, 3], label="Before")
    >>> ax.plot([1, 2, 3], [2, 3, 4], label="After")
    >>> format_comparison_plot(ax, comparison_type="before_after")
    """
    # Set appropriate colors based on comparison type
    if comparison_type == "before_after":
        colors = PRS_COMPARISON_CYCLE
    else:
        colors = PRS_CLINICAL_CYCLE[:2]

    # Update line colors if lines exist
    lines = ax.get_lines()
    for i, line in enumerate(lines[: len(colors)]):
        line.set_color(colors[i])


def add_significance_indicator(
    ax,
    x: float,
    y: float,
    p_value: float = None,
    symbol: str = "*",
    bracket: bool = False,
    x_start: float = None,
    x_end: float = None,
    show_p_value: bool = True,
    **kwargs,
) -> None:
    """
    Add statistical significance indicator to a plot following publication best practices.

    Scientific Standard: Show EITHER symbols (*,**,***) OR exact p-values, not both.
    Based on research from matplotlib best practices, starbars package design,
    and scientific publication conventions.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to add indicator to.
    x : float
        X-coordinate for indicator (center of bracket if bracket=True).
    y : float
        Y-coordinate for bracket base (should be above compared bars).
    p_value : float, optional
        P-value for auto-formatting. Used to show exact value if show_p_value=True.
    symbol : str, default "*"
        Significance symbol (e.g., "*", "**", "***", "ns").
        Ignored if show_p_value=True.
    bracket : bool, default False
        Whether to draw a horizontal bracket line with vertical tips.
    x_start : float, optional
        Starting x-coordinate for bracket (required if bracket=True).
    x_end : float, optional
        Ending x-coordinate for bracket (required if bracket=True).
    show_p_value : bool, default True
        If True, show exact p-value instead of symbol.
        If False, show symbol only.
        Recommendation: p-values for precision (default), symbols for visual clarity.
    **kwargs
        Additional formatting:
        - text_fontsize: Annotation text size (default: 14pt symbols, 10pt p-values)
        - text_color: Annotation color (default: #2C5F87)
        - line_width: Bracket line width (default: 1.5)
        - tip_length: Bracket tip length as % of y-range (default: 0.01 = 1%)
        - text_offset: Bracket-to-text spacing as % of y-range (default: 0.01 = 1%)

    Examples
    --------
    Symbol only (standard):
    >>> fig, ax = plt.subplots()
    >>> ax.bar(['Control', 'Treatment'], [65, 88])
    >>> add_significance_indicator(ax, x=0.5, y=90, symbol="**",
    ...                            bracket=True, x_start=0, x_end=1)

    Exact p-value (when precision needed):
    >>> add_significance_indicator(ax, x=0.5, y=90, p_value=0.023,
    ...                            bracket=True, x_start=0, x_end=1,
    ...                            show_p_value=True)

    Auto-select symbol:
    >>> from prs_dataviz import get_significance_symbol
    >>> symbol = get_significance_symbol(0.008)  # Returns "**"
    >>> add_significance_indicator(ax, x=0.5, y=90, symbol=symbol,
    ...                            bracket=True, x_start=0, x_end=1)
    """
    import matplotlib.pyplot as plt

    # Get current font size from rcParams
    base_fontsize = plt.rcParams.get("font.size", 10)

    # Calculate y-range for relative positioning
    y_range = ax.get_ylim()[1] - ax.get_ylim()[0]

    # Spacing parameters (research-based defaults: 2-3% is standard)
    tip_length_pct = kwargs.get("tip_length", 0.01)  # 1% for bracket tips
    text_offset_pct = kwargs.get(
        "text_offset", 0.01
    )  # 1% between bracket and text (compact)

    # Convert to absolute values
    tip_length = tip_length_pct * y_range
    text_offset = text_offset_pct * y_range

    # Draw bracket if requested
    if bracket and x_start is not None and x_end is not None:
        # Bold, prominent brackets for clear visibility (especially with gridlines)
        line_width = kwargs.get("line_width", 2.5)  # Bold brackets (was 1.5, then 2.0)
        bracket_color = kwargs.get("bracket_color", "#000000")  # Solid black

        # Clean bracket structure: [x1, x1, x2, x2] and [y1, y2, y2, y1]
        # Creates: tip down → horizontal → tip down
        bracket_x = [x_start, x_start, x_end, x_end]
        bracket_y = [y - tip_length, y, y, y - tip_length]

        ax.plot(
            bracket_x,
            bracket_y,
            color=bracket_color,
            linewidth=line_width,
            solid_capstyle="butt",
            zorder=100,
        )

    # Determine display: symbol OR p-value (not both)
    if show_p_value and p_value is not None:
        # Show exact p-value
        if p_value < 0.001:
            display_text = "p < 0.001"
        elif p_value < 0.01:
            display_text = f"p = {p_value:.3f}"
        else:
            display_text = f"p = {p_value:.2f}"

        text_fontsize = kwargs.get("text_fontsize", base_fontsize)  # 10pt
        text_color = kwargs.get("text_color", "#666")
        text_weight = "normal"
    else:
        # Show symbol (standard practice)
        display_text = symbol
        text_fontsize = kwargs.get("text_fontsize", base_fontsize + 4)  # 14pt
        text_color = kwargs.get("text_color", "#2C5F87")
        text_weight = "bold"

    # Position text above bracket
    text_y = y + text_offset

    # Add annotation
    ax.text(
        x,
        text_y,
        display_text,
        fontsize=text_fontsize,
        ha="center",
        va="bottom",
        color=text_color,
        fontweight=text_weight,
    )


def add_scale_bar(
    ax, length: float, label: str, location: str = "lower right", **kwargs
) -> None:
    """
    Add a scale bar to a medical image (PRS prefers scale bars over magnification text).

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes containing the image.
    length : float
        Length of scale bar in data coordinates.
    label : str
        Label for scale bar (e.g., "100 μm", "1 cm").
    location : str, default "lower right"
        Location of scale bar: "lower left", "lower right", "upper left", "upper right".
    **kwargs
        Additional arguments for scale bar appearance.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.imshow(microscopy_image)
    >>> add_scale_bar(ax, length=100, label="100 μm")
    """
    from matplotlib.lines import Line2D

    # Get axes limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Calculate position based on location
    margin = 0.05  # 5% margin from edges
    if "right" in location:
        x_pos = xlim[1] - (xlim[1] - xlim[0]) * margin - length
    else:  # left
        x_pos = xlim[0] + (xlim[1] - xlim[0]) * margin

    if "lower" in location:
        y_pos = ylim[0] + (ylim[1] - ylim[0]) * margin
    else:  # upper
        y_pos = ylim[1] - (ylim[1] - ylim[0]) * margin

    # Scale bar properties
    bar_height = kwargs.get("height", (ylim[1] - ylim[0]) * 0.01)
    bar_color = kwargs.get("color", "white")
    bar_linewidth = kwargs.get("linewidth", 2)

    # Add scale bar
    scale_bar = Line2D(
        [x_pos, x_pos + length],
        [y_pos, y_pos],
        linewidth=bar_linewidth,
        color=bar_color,
        solid_capstyle="butt",
    )
    ax.add_line(scale_bar)

    # Add label
    label_color = kwargs.get("label_color", bar_color)
    label_size = kwargs.get("label_size", 8)

    ax.text(
        x_pos + length / 2,
        y_pos + bar_height * 2,
        label,
        color=label_color,
        fontsize=label_size,
        ha="center",
        va="bottom",
        weight="bold",
    )


# ============================================================================
# Legend Helpers
# ============================================================================


def _calculate_optimal_ncol(labels, max_label_length=20, max_cols=4):
    """
    Calculate optimal number of columns for legend based on label lengths.

    Parameters
    ----------
    labels : list of str
        Legend labels.
    max_label_length : int, default 20
        Maximum characters before preferring fewer columns.
    max_cols : int, default 4
        Maximum number of columns to use.

    Returns
    -------
    int
        Optimal number of columns (1-max_cols).

    Examples
    --------
    >>> labels = ["Short", "A bit longer"]
    >>> _calculate_optimal_ncol(labels)
    2

    >>> labels = ["Very long description text", "Another long one"]
    >>> _calculate_optimal_ncol(labels)
    1
    """
    if not labels:
        return 1

    n_labels = len(labels)
    avg_length = sum(len(str(label)) for label in labels) / n_labels
    max_length = max(len(str(label)) for label in labels)

    # Decision logic:
    # - Short labels (avg < 15 chars): Use more columns
    # - Medium labels (15-25 chars): Use 2-3 columns
    # - Long labels (> 25 chars): Use 1-2 columns

    if max_length > 40:
        # Very long labels - force single column
        return 1
    elif avg_length > 25:
        # Long labels - prefer 1-2 columns
        return min(2, n_labels)
    elif avg_length > 15:
        # Medium labels - prefer 2-3 columns
        return min(3, max(2, n_labels // 2))
    else:
        # Short labels - can use more columns
        # Use sqrt rule for small counts, otherwise max_cols
        if n_labels <= 4:
            return min(max_cols, n_labels)
        else:
            import math
            return min(max_cols, int(math.ceil(math.sqrt(n_labels))))


def _get_legend_labels(ax):
    """
    Extract legend labels from axes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to extract labels from.

    Returns
    -------
    list of str
        Legend labels.
    """
    handles, labels = ax.get_legend_handles_labels()
    return labels


def _is_bar_chart(ax):
    """
    Detect if axes contains bar chart (bar or barh plot).

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to check.

    Returns
    -------
    bool
        True if axes contains bar patches (bar chart).
    """
    from matplotlib.patches import Rectangle

    # Check if any patches are bar-like (rectangles)
    for patch in ax.patches:
        if isinstance(patch, Rectangle):
            return True

    # Also check containers (grouped/stacked bars)
    if hasattr(ax, "containers") and ax.containers:
        return True

    return False


def set_axis_fontsize(ax, fontsize: int) -> None:
    """
    Standardize font size across all text elements in axes.

    Applies consistent font size to:
    - Axis labels (xlabel, ylabel)
    - Tick labels (x and y)
    - Title (if present, uses fontsize + 2)

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to standardize.
    fontsize : int
        Font size in points (e.g., 12, 14, 16).

    Examples
    --------
    Standardize entire figure typography:
    >>> fig, ax = plt.subplots()
    >>> ax.bar([1, 2], [3, 4], label="Data")
    >>> ax.set_xlabel("Category")
    >>> ax.set_ylabel("Value")
    >>> ax.set_title("Results")
    >>> set_axis_fontsize(ax, fontsize=14)
    >>> prs_legend(ax, position="top", fontsize=14)

    Multiple subplots with consistent sizing:
    >>> fig, (ax1, ax2) = plt.subplots(1, 2)
    >>> # ... plotting ...
    >>> for ax in [ax1, ax2]:
    ...     set_axis_fontsize(ax, fontsize=14)
    ...     prs_legend(ax, fontsize=14)

    Notes
    -----
    This function modifies existing labels. For best results:
    1. Create plot and set labels
    2. Call set_axis_fontsize()
    3. Call prs_legend() with same fontsize

    The title receives fontsize + 2 for visual hierarchy.
    """
    # Update tick label sizes
    ax.tick_params(axis="both", labelsize=fontsize)

    # Update axis labels if they exist
    if ax.get_xlabel():
        current_xlabel = ax.get_xlabel()
        ax.set_xlabel(current_xlabel, fontsize=fontsize, fontweight="bold")

    if ax.get_ylabel():
        current_ylabel = ax.get_ylabel()
        ax.set_ylabel(current_ylabel, fontsize=fontsize, fontweight="bold")

    # Update title if it exists (slightly larger)
    if ax.get_title():
        current_title = ax.get_title()
        ax.set_title(current_title, fontsize=fontsize + 2, fontweight="bold")


def prs_legend(
    ax,
    *args,
    position: str = "best",
    compact: bool = False,
    ncol: int | None = None,
    fontsize: int | None = None,
    **kwargs
) -> None:
    """
    Create a PRS-style legend with professional formatting and smart positioning.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to add legend to.
    position : str, default "best"
        Legend position. Options:
        - "best": Automatic optimal placement avoiding data overlap (recommended)
        - "outside": Right side, outside plot area
        - "top": Above plot, compact horizontal layout
        - "top-smart": Above plot with auto-calculated columns and positioning
        - Any matplotlib location string: "upper left", "lower right", etc.
    compact : bool, default False
        If True, use compact spacing optimized for multi-column legends.
        Recommended for 2+ columns.
    ncol : int, optional
        Number of columns. If None, automatically calculated based on:
        - Number of labels
        - Label text length
        - Position type (more columns for "top", fewer for vertical positions)
    fontsize : int, optional
        Font size for legend text. If None, uses matplotlib default (usually 10-12).
        Recommended: Use same fontsize for axes labels, tick labels, and legend
        for consistent professional appearance.
    *args, **kwargs
        Additional arguments passed to ax.legend().
        Common options: title, markerscale, bbox_to_anchor

    Examples
    --------
    Smart auto-positioning (avoids overlap with data):
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], label="Before")
    >>> ax.plot([1, 2, 3], label="After")
    >>> prs_legend(ax)  # Uses position="best"

    Smart top positioning (auto-calculates columns):
    >>> prs_legend(ax, position="top-smart")

    Standardized font size across figure:
    >>> fontsize = 14
    >>> ax.tick_params(labelsize=fontsize)
    >>> ax.set_xlabel("Time", fontsize=fontsize)
    >>> ax.set_ylabel("Response", fontsize=fontsize)
    >>> prs_legend(ax, position="top", fontsize=fontsize)

    Bar chart with prominent legend (auto-detected):
    >>> fig, ax = plt.subplots()
    >>> ax.bar([1, 2, 3], [4, 5, 6], label="Treatment")
    >>> prs_legend(ax, position="top")  # Auto-applies large handles for bars

    Notes
    -----
    **Smart Column Calculation:**
    When `ncol=None`, the function automatically determines optimal columns:
    - Short labels (< 15 chars avg): 2-4 columns
    - Medium labels (15-25 chars): 2-3 columns
    - Long labels (> 25 chars): 1-2 columns
    - Very long labels (> 40 chars): 1 column

    **Smart Positioning:**
    - `position="best"` uses matplotlib's algorithm to avoid data overlap
    - `position="top-smart"` auto-positions above plot with optimal column count
    - Works best for plots WITHOUT titles (common in PRS manuscripts)

    **Auto-Detection for Bar Charts:**
    When the axes contains bar charts (bar/barh), automatically applies:
    - `markerscale=4` (4× larger handles for visibility)
    - `handleheight=2` (taller color boxes)
    - `handlelength=2` (standard width)
    These make bar chart legends more prominent and professional.

    **Font Size Standardization:**
    Use the same `fontsize` parameter for axes labels and legend:
    ```python
    fontsize = 14
    ax.tick_params(labelsize=fontsize)
    ax.set_xlabel("Label", fontsize=fontsize)
    prs_legend(ax, position="top", fontsize=fontsize)
    ```

    **Position-Specific Defaults:**
    - "top": Frameless, bbox_to_anchor adjusted based on ncol, compact spacing
    - "outside": Framed, right side, vertically centered
    - "best": Framed, automatic placement inside plot, avoids overlap
    """
    # Auto-calculate ncol if not provided
    if ncol is None:
        labels = _get_legend_labels(ax)

        if position in ["top", "top-smart"]:
            # Top position: prefer more columns (horizontal layout)
            ncol = _calculate_optimal_ncol(labels, max_label_length=20, max_cols=4)
        elif position == "outside":
            # Outside position: prefer fewer columns (vertical layout)
            ncol = _calculate_optimal_ncol(labels, max_label_length=30, max_cols=2)
        else:
            # Other positions: balanced approach
            ncol = _calculate_optimal_ncol(labels, max_label_length=25, max_cols=3)

    # Auto-detect bar charts and apply prominent handle settings
    is_bar = _is_bar_chart(ax)
    if is_bar:
        # Bar charts need larger, more visible legend handles
        kwargs.setdefault("markerscale", 4)
        kwargs.setdefault("handleheight", 2)
        kwargs.setdefault("handlelength", 2)

    # Position-specific defaults
    if position == "outside":
        kwargs.setdefault("loc", "center left")
        kwargs.setdefault("bbox_to_anchor", (1.02, 0.5))
        kwargs.setdefault("frameon", True)
        kwargs.setdefault("framealpha", 1.0)
        kwargs.setdefault("edgecolor", "#CCCCCC")
        kwargs.setdefault("ncol", ncol)

    elif position in ["top", "top-smart"]:
        # Professional top-aligned legend (frameless, compact)
        # Adjust x position based on ncol for better centering
        if ncol == 1:
            x_anchor = 0.5  # Centered
        elif ncol == 2:
            x_anchor = 0.35  # Slightly left for 2 columns
        elif ncol == 3:
            x_anchor = 0.4   # Balanced for 3 columns
        else:  # ncol >= 4
            x_anchor = 0.45  # Nearly centered for 4+ columns

        kwargs.setdefault("loc", "upper center")
        kwargs.setdefault("bbox_to_anchor", (x_anchor, 1.12))
        kwargs.setdefault("frameon", False)
        kwargs.setdefault("ncol", ncol)
        kwargs.setdefault("markerscale", 4)
        kwargs.setdefault("labelspacing", 0.25)
        kwargs.setdefault("handleheight", 2)
        kwargs.setdefault("handlelength", 2)
        kwargs.setdefault("columnspacing", 0.75)

    elif position == "best":
        # Smart positioning - matplotlib avoids data overlap
        kwargs.setdefault("loc", "best")
        kwargs.setdefault("frameon", True)
        kwargs.setdefault("framealpha", 1.0)
        kwargs.setdefault("edgecolor", "#CCCCCC")
        kwargs.setdefault("ncol", ncol)
 

    else:
        # Custom position (use matplotlib location string)
        kwargs.setdefault("loc", position)
        kwargs.setdefault("frameon", True)
        kwargs.setdefault("framealpha", 1.0)
        kwargs.setdefault("edgecolor", "#CCCCCC")
        kwargs.setdefault("ncol", ncol)


    # Apply compact spacing if requested
    if compact:
        kwargs.setdefault("labelspacing", 0.25)
        kwargs.setdefault("handleheight", 2)
        kwargs.setdefault("handlelength", 2)
        kwargs.setdefault("columnspacing", 0.75)


    # Common defaults (can be overridden by kwargs)
    if fontsize is not None:
        kwargs.setdefault("fontsize", fontsize)
    else:
        kwargs.setdefault("fontsize", 12)

    kwargs.setdefault("title", "")

    ax.legend(*args, **kwargs)
