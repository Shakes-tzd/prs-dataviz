"""
Helper functions to automate common tasks in PRS data visualization.
These functions reduce boilerplate and make it easier to create
publication-quality figures quickly.

Key Features:
- Automatic bracket positioning based on data
- Automatic y-axis limit calculation
- Automatic stacking of multiple comparisons
- Works with any dataset without manual adjustments
"""

from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np

from .palettes import CLINICAL_DATA, COMPARISON
from .style import add_significance_indicator


def auto_extend_ylim(ax, extension_pct: float = 0.15):
    """
    Automatically extend y-axis limits to make room for significance indicators.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to modify.
    extension_pct : float, default 0.15
        Percentage of y-range to add as extension (0.15 = 15%).

    Returns
    -------
    tuple
        New (ymin, ymax) limits.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.bar([1, 2, 3], [10, 15, 12])
    >>> auto_extend_ylim(ax, extension_pct=0.15)  # Add 15% space
    """
    ymin, ymax = ax.get_ylim()
    y_range = ymax - ymin

    # Extend top by percentage
    new_ymax = ymax + (y_range * extension_pct)

    # Keep ymin at 0 for most plots (common in medical data)
    new_ymin = 0 if ymin >= 0 else ymin

    ax.set_ylim(new_ymin, new_ymax)
    return (new_ymin, new_ymax)


def get_data_max_in_range(ax, x_start: float = None, x_end: float = None) -> float:
    """
    Robustly find the maximum data value in a given x-range.

    Works with bars, lines, scatter plots, error bars, and more.
    If no range specified, returns global max.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes containing the plot data.
    x_start : float, optional
        Start of x-range. If None, uses full range.
    x_end : float, optional
        End of x-range. If None, uses full range.

    Returns
    -------
    float
        Maximum y-value in the specified range.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.bar([0, 1, 2, 3], [10, 20, 30, 25])
    >>> max_val = get_data_max_in_range(ax, x_start=1, x_end=3)
    >>> print(max_val)  # Returns 30
    """
    data_max = 0

    # Check bar patches
    for patch in ax.patches:
        x_center = patch.get_x() + patch.get_width() / 2
        # Include patch if no range specified OR if within range
        in_range = (x_start is None and x_end is None) or (x_start <= x_center <= x_end)
        if in_range:
            height = patch.get_height()
            # Accept Python numbers AND numpy numbers (np.int64, np.float64, etc.)
            if isinstance(height, (int, float, np.number)) and not np.isnan(height):
                # Handle stacked bars - get top position
                y_bottom = patch.get_y()
                y_top = y_bottom + height
                data_max = max(data_max, y_top)

    # Check line plots
    for line in ax.get_lines():
        xdata, ydata = line.get_data()
        for x, y in zip(xdata, ydata):
            in_range = (x_start is None and x_end is None) or (x_start <= x <= x_end)
            if in_range:
                if not np.isnan(y):
                    data_max = max(data_max, y)

    # Check scatter plots
    for collection in ax.collections:
        offsets = collection.get_offsets()
        if len(offsets) > 0:
            for x, y in offsets:
                in_range = (x_start is None and x_end is None) or (
                    x_start <= x <= x_end
                )
                if in_range:
                    if not np.isnan(y):
                        data_max = max(data_max, y)

    # If no data found, use current y-limit
    if data_max == 0:
        data_max = ax.get_ylim()[1] * 0.8

    return data_max


def auto_calculate_ylim_for_annotations(
    ax,
    n_comparisons: int = 1,
    base_extension: float = 0.12,
    per_comparison: float = 0.08,
) -> Tuple[float, float]:
    """
    Automatically calculate optimal y-axis limits with space for annotations.

    Analyzes actual data and adds appropriate space based on number of comparisons.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes containing the plot.
    n_comparisons : int, default 1
        Number of significance comparisons to display.
    base_extension : float, default 0.12
        Base extension (12%) for first annotation.
    per_comparison : float, default 0.08
        Additional extension (8%) per extra comparison.

    Returns
    -------
    tuple
        (ymin, ymax) - Optimal limits with space for annotations.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.bar([0, 1, 2], [50, 75, 60])
    >>> ymin, ymax = auto_calculate_ylim_for_annotations(ax, n_comparisons=2)
    >>> ax.set_ylim(ymin, ymax)
    """
    # Get actual data maximum and minimum
    data_max = get_data_max_in_range(ax)
    ymin_data, ymax_data = ax.get_ylim()
    data_min = ymin_data if ymin_data > 0 else 0  # Assume 0 baseline for bar charts

    # Calculate data range (not y-axis range!)
    # This removes circular dependency - we base spacing on actual data, not final axis
    data_range = data_max - data_min

    # Calculate headroom as PERCENTAGE OF DATA RANGE (not y-axis range)
    # Spacing provides clear visual separation without excessive whitespace
    base_offset = 0.05  # 5% of data range above tallest bar (compact clearance)
    stack_spacing = 0.08  # 8% of data range between brackets
    text_spacing = 0.02  # 2% of data range for text height (compact but readable)

    # Calculate total headroom in ABSOLUTE units (data coordinates)
    total_headroom = (
        base_offset + (n_comparisons - 1) * stack_spacing + text_spacing
    ) * data_range

    # Simple addition - no circular math!
    ymin = data_min
    ymax = data_max + total_headroom

    # Set the limits
    ax.set_ylim(ymin, ymax)

    return (ymin, ymax)


def auto_position_brackets(
    ax,
    comparisons: List[Tuple[float, float]],
    base_offset: float = 0.05,
    stack_spacing: float = 0.08,
) -> List[float]:
    """
    Automatically calculate y-positions for multiple stacked brackets.

    Analyzes data and calculates optimal positions with proper spacing.
    No manual calculation needed!

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes containing the plot.
    comparisons : list of tuples
        List of (x_start, x_end) for each comparison.
    base_offset : float, default 0.05
        Base offset (5% of data range) above data for first bracket.
    stack_spacing : float, default 0.08
        Spacing (8% of data range) between stacked brackets.

    Returns
    -------
    list of float
        Y-positions for each bracket, from lowest to highest.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.bar([0, 1, 2, 3], [50, 60, 80, 90])
    >>> comparisons = [(2, 3), (1, 3), (0, 3)]  # x-ranges to compare
    >>> y_positions = auto_position_brackets(ax, comparisons)
    >>> # Returns [y1, y2, y3] with proper spacing
    """
    y_positions = []

    # Get overall data range (not y-axis range!)
    # This ensures spacing is based on data scale, not inflated axis
    overall_data_max = get_data_max_in_range(ax)
    ymin, _ = ax.get_ylim()
    data_min = ymin if ymin > 0 else 0
    data_range = overall_data_max - data_min

    # Sort by span (wider brackets should be higher to avoid crossing)
    sorted_comps = sorted(
        enumerate(comparisons), key=lambda x: abs(x[1][1] - x[1][0]), reverse=True
    )

    for level, (original_idx, (x_start, x_end)) in enumerate(sorted_comps):
        # Find max data in this comparison range
        data_max_in_range = get_data_max_in_range(ax, x_start, x_end)

        # Calculate bracket position based on DATA RANGE (not y-axis range)
        # First bracket: data_max + base_offset% of data_range
        # Subsequent brackets: stack above with spacing% of data_range
        bracket_y = (
            data_max_in_range
            + (base_offset * data_range)
            + (level * stack_spacing * data_range)
        )

        y_positions.append((original_idx, bracket_y))

    # Return in original order
    y_positions.sort(key=lambda x: x[0])
    return [y for _, y in y_positions]


def calculate_bracket_position(
    ax, bar_positions, bar_indices, offset_pct: float = 0.08
):
    """
    Calculate optimal bracket position for significance indicators.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes containing the plot.
    bar_positions : array-like
        X-positions of all bars/groups.
    bar_indices : tuple of int
        Indices of bars to compare (e.g., (0, 1) for first two bars).
    offset_pct : float, default 0.08
        Percentage of y-range above data for bracket (0.08 = 8%).

    Returns
    -------
    dict
        Dictionary with 'x', 'y', 'x_start', 'x_end' for add_significance_indicator.

    Examples
    --------
    >>> x = np.arange(4)
    >>> bracket = calculate_bracket_position(ax, x, (2, 3))
    >>> add_significance_indicator(ax, **bracket, p_value=0.01, bracket=True)
    """
    # Get data max within the comparison range
    lines = ax.get_lines()
    patches = ax.patches

    # Find max y-value in comparison range
    x_start = bar_positions[bar_indices[0]]
    x_end = bar_positions[bar_indices[1]]

    # Get current y-limits
    ymin, ymax = ax.get_ylim()
    y_range = ymax - ymin

    # Calculate bracket y-position (above highest data point)
    # Try to get actual data max in range
    data_max = ymin
    for patch in patches:
        x_center = patch.get_x() + patch.get_width() / 2
        if x_start <= x_center <= x_end:
            height = patch.get_height()
            if isinstance(height, (int, float)) and height > data_max:
                data_max = height

    # Bracket positioned above data with offset
    bracket_y = data_max + (y_range * offset_pct)

    return {
        "x": (x_start + x_end) / 2,
        "y": bracket_y,
        "x_start": x_start,
        "x_end": x_end,
    }


def add_comparison_bars(
    ax,
    data: Dict[str, List[float]],
    categories: List[str],
    colors: Optional[List[str]] = None,
    width: float = 0.35,
    **kwargs,
):
    """
    Create grouped comparison bars with automatic color assignment.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to plot on.
    data : dict
        Dictionary mapping group names to data lists.
        E.g., {'Control': [1, 2, 3], 'Treatment': [2, 3, 4]}
    categories : list of str
        Category labels for x-axis.
    colors : list of str, optional
        Colors for each group. If None, uses COMPARISON palette.
    width : float, default 0.35
        Width of bars.
    **kwargs
        Additional arguments passed to ax.bar().

    Returns
    -------
    tuple
        (x_positions, bar_containers, group_names)

    Examples
    --------
    >>> data = {'Control': [65, 70, 75], 'Treatment': [70, 80, 90]}
    >>> categories = ['Pre-op', '3mo', '6mo']
    >>> x, bars, groups = add_comparison_bars(ax, data, categories)
    """
    groups = list(data.keys())
    n_groups = len(groups)
    n_categories = len(categories)

    # Default colors from COMPARISON palette
    if colors is None:
        color_map = {
            "Control": COMPARISON["Control"],
            "Treatment": COMPARISON["Treatment"],
            "Before": COMPARISON["Before"],
            "After": COMPARISON["After"],
        }
        colors = [color_map.get(g, CLINICAL_DATA["Primary"]) for g in groups]

    # Calculate positions
    x = np.arange(n_categories)
    offsets = np.linspace(
        -(n_groups - 1) * width / 2, (n_groups - 1) * width / 2, n_groups
    )

    # Plot bars
    bar_containers = []
    for i, (group, offset) in enumerate(zip(groups, offsets)):
        bars = ax.bar(
            x + offset,
            data[group],
            width,
            label=group,
            color=colors[i],
            alpha=kwargs.get("alpha", 0.8),
        )
        bar_containers.append(bars)

    ax.set_xticks(x)
    ax.set_xticklabels(categories)

    return x, bar_containers, groups


def add_multiple_comparisons(
    ax,
    comparisons: List[Tuple[int, int, float]],
    x_positions: np.ndarray,
    bar_width: float = 0.35,
    auto_adjust_ylim: bool = True,
):
    """
    Add multiple significance comparisons with AUTOMATIC positioning.

    NEW: Automatically calculates optimal y-positions and extends y-axis!
    No manual calculations needed - works with any dataset.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to annotate.
    comparisons : list of tuples
        Each tuple is (index1, index2, p_value) for comparison.
    x_positions : array
        X-positions of groups/bars.
    bar_width : float, default 0.35
        Width of bars (for calculating bracket endpoints).
    auto_adjust_ylim : bool, default True
        If True, automatically extends y-axis to fit all annotations.

    Examples
    --------
    Automatic positioning (recommended):
    >>> comparisons = [(0, 1, 0.05), (1, 2, 0.01), (0, 2, 0.001)]
    >>> add_multiple_comparisons(ax, comparisons, x)
    # Automatically positions all brackets with proper spacing!

    Manual positioning (old way):
    >>> add_multiple_comparisons(ax, comparisons, x, auto_adjust_ylim=False)
    # User must set ylim manually
    """
    # Step 1: Automatically extend y-axis if needed
    if auto_adjust_ylim:
        auto_calculate_ylim_for_annotations(ax, n_comparisons=len(comparisons))

    # Step 2: Build list of (x_start, x_end) pairs for positioning
    x_ranges = []
    for idx1, idx2, _ in comparisons:
        x_start = x_positions[idx1]
        x_end = x_positions[idx2]
        x_ranges.append((x_start, x_end))

    # Step 3: Automatically calculate optimal y-positions
    y_positions = auto_position_brackets(ax, x_ranges)

    # Step 4: Add all significance indicators
    for (idx1, idx2, p_val), y_pos in zip(comparisons, y_positions):
        add_significance_indicator(
            ax,
            x=(x_positions[idx1] + x_positions[idx2]) / 2,
            y=y_pos,
            p_value=p_val,  # Show p-value (default behavior)
            bracket=True,
            x_start=x_positions[idx1],
            x_end=x_positions[idx2],
        )


def create_comparison_plot(
    data: Dict[str, List[float]],
    categories: List[str],
    ylabel: str,
    xlabel: Optional[str] = None,
    title: Optional[str] = None,
    comparisons: Optional[List[Tuple[int, int, float]]] = None,
    figsize: Tuple[float, float] = (10, 6),
    **kwargs,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Create a complete comparison bar plot with significance indicators.

    This is a high-level convenience function that sets up everything:
    - PRS styling
    - Comparison colors
    - Grouped bars
    - Significance indicators
    - Proper spacing

    Parameters
    ----------
    data : dict
        Dictionary mapping group names to data lists.
    categories : list of str
        Category labels for x-axis.
    ylabel : str
        Y-axis label.
    xlabel : str, optional
        X-axis label. Default is None (no xlabel).
    title : str, optional
        Plot title. Default is None (no title).
    comparisons : list of tuples, optional
        List of (index1, index2, p_value) for significance.
    figsize : tuple, default (10, 6)
        Figure size.
    **kwargs
        Additional styling options (show_grid, bar_width, etc.).

    Returns
    -------
    fig, ax
        Matplotlib figure and axes objects.

    Examples
    --------
    >>> data = {
    ...     'Control': [65, 68, 70, 72],
    ...     'Treatment': [65, 75, 82, 88]
    ... }
    >>> categories = ['Pre-op', '3mo', '6mo', '12mo']
    >>> comparisons = [(2, 3, 0.05)]  # Compare at 12mo
    >>> fig, ax = create_comparison_plot(
    ...     data, categories,
    ...     ylabel='Score (%)',
    ...     title='Treatment Efficacy',
    ...     comparisons=comparisons
    ... )
    """
    from .style import apply_prs_style

    # Apply PRS styling
    apply_prs_style(cycle="comparison", show_grid=kwargs.get("show_grid", True))

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Add bars
    bar_width = kwargs.get("bar_width", 0.35)
    x, bars, groups = add_comparison_bars(ax, data, categories, width=bar_width)

    # Labels
    ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    if title:
        ax.set_title(title, fontweight="bold", pad=15)

    ax.legend(loc="best")
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    # Add comparisons if provided
    if comparisons:
        # Extend y-limit for significance indicators
        auto_extend_ylim(ax, extension_pct=0.15)
        add_multiple_comparisons(ax, comparisons, x, bar_width=bar_width)

    plt.tight_layout()

    return fig, ax


def create_time_series_plot(
    data: Dict[str, np.ndarray],
    time: np.ndarray,
    ylabel: str,
    xlabel: str = "Time",
    title: Optional[str] = None,
    confidence_intervals: Optional[Dict[str, np.ndarray]] = None,
    figsize: Tuple[float, float] = (10, 6),
    **kwargs,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Create a time series plot with optional confidence intervals.

    Parameters
    ----------
    data : dict
        Dictionary mapping group names to time series arrays.
    time : array
        Time points.
    ylabel : str
        Y-axis label.
    xlabel : str, default "Time"
        X-axis label.
    title : str, optional
        Plot title. Default is None (no title).
    confidence_intervals : dict, optional
        Dictionary mapping group names to CI width arrays.
    figsize : tuple, default (10, 6)
        Figure size.
    **kwargs
        Additional options (markers, linewidth, etc.).

    Returns
    -------
    fig, ax
        Matplotlib figure and axes objects.

    Examples
    --------
    >>> time = np.arange(0, 13)
    >>> data = {
    ...     'Control': np.linspace(50, 70, 13),
    ...     'Treatment': np.linspace(50, 90, 13)
    ... }
    >>> ci = {
    ...     'Control': np.full(13, 5),
    ...     'Treatment': np.full(13, 4)
    ... }
    >>> fig, ax = create_time_series_plot(
    ...     data, time,
    ...     ylabel='Recovery Score',
    ...     confidence_intervals=ci
    ... )
    """
    from .style import apply_prs_style

    apply_prs_style(cycle="comparison")

    fig, ax = plt.subplots(figsize=figsize)

    # Colors
    groups = list(data.keys())
    color_map = {
        "Control": COMPARISON["Control"],
        "Treatment": COMPARISON["Treatment"],
        "Before": COMPARISON["Before"],
        "After": COMPARISON["After"],
    }

    # Plot lines
    markers = kwargs.get("markers", ["o", "s", "^", "D"])
    linewidth = kwargs.get("linewidth", 2.5)
    markersize = kwargs.get("markersize", 7)

    for i, group in enumerate(groups):
        color = color_map.get(group, CLINICAL_DATA["Primary"])
        marker = markers[i % len(markers)]

        ax.plot(
            time,
            data[group],
            marker=marker,
            linewidth=linewidth,
            markersize=markersize,
            label=group,
            color=color,
        )

        # Add confidence intervals if provided
        if confidence_intervals and group in confidence_intervals:
            ci = confidence_intervals[group]
            ax.fill_between(
                time, data[group] - ci, data[group] + ci, alpha=0.2, color=color
            )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontweight="bold", pad=15)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    return fig, ax


def get_significance_symbol(p_value: float) -> str:
    """
    Get appropriate significance symbol based on p-value.

    Parameters
    ----------
    p_value : float
        Statistical p-value.

    Returns
    -------
    str
        Significance symbol: "***", "**", "*", or "ns".

    Examples
    --------
    >>> get_significance_symbol(0.0005)
    '***'
    >>> get_significance_symbol(0.03)
    '*'
    >>> get_significance_symbol(0.12)
    'ns'
    """
    if p_value < 0.001:
        return "***"
    elif p_value < 0.01:
        return "**"
    elif p_value < 0.05:
        return "*"
    else:
        return "ns"


def calculate_optimal_ylim(
    ax, data_max: Optional[float] = None, n_comparisons: int = 1
) -> Tuple[float, float]:
    """
    Calculate optimal y-axis limits with space for significance indicators.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes containing the plot.
    data_max : float, optional
        Maximum data value. If None, automatically detected.
    n_comparisons : int, default 1
        Number of significance comparisons (affects spacing).

    Returns
    -------
    tuple
        (ymin, ymax) for optimal display.

    Examples
    --------
    >>> ymin, ymax = calculate_optimal_ylim(ax, data_max=95, n_comparisons=2)
    >>> ax.set_ylim(ymin, ymax)
    """
    # Detect data max if not provided
    if data_max is None:
        data_max = 0
        for patch in ax.patches:
            height = patch.get_height()
            if isinstance(height, (int, float)) and height > data_max:
                data_max = height

    # Calculate extension based on number of comparisons
    base_extension = 0.12  # 12% for one comparison
    additional_per_comp = 0.06  # 6% for each additional

    total_extension = base_extension + (n_comparisons - 1) * additional_per_comp

    # Calculate new limits
    ymin = 0 if data_max >= 0 else data_max * 1.1
    ymax = data_max * (1 + total_extension)

    return (ymin, ymax)
