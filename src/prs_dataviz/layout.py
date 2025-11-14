"""
Figure layout utilities for PRS journal submissions.

Specialized layouts for medical/surgical research:
- Before/after comparisons
- Multi-panel figures
- Patient photo grids
- Consistent sizing and alignment

Reference: PRS Figure Guidelines
https://journals.lww.com/plasreconsurg/pages/informationforauthors.aspx
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure
import numpy as np
from typing import Optional, Literal, Tuple
from PIL import Image


# ============================================================================
# Before/After Comparison Layouts
# ============================================================================

def create_before_after_figure(
    before_image: np.ndarray | str,
    after_image: np.ndarray | str,
    labels: tuple[str, str] = ("Before", "After"),
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
    **kwargs
) -> Tuple[Figure, tuple]:
    """
    Create a side-by-side before/after comparison figure.

    PRS requires before/after photos to be:
    - Identical in size
    - Identical in position
    - Identical in lighting

    Parameters
    ----------
    before_image : ndarray or str
        Before image as numpy array or path to image file.
    after_image : ndarray or str
        After image as numpy array or path to image file.
    labels : tuple of str, default ("Before", "After")
        Labels for each panel.
    figsize : tuple of float, optional
        Figure size in inches. If None, auto-calculated based on image aspect ratio.
    title : str, optional
        Overall figure title.
    **kwargs
        Additional styling arguments.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure.
    axes : tuple of matplotlib.axes.Axes
        Tuple of (ax_before, ax_after).

    Examples
    --------
    >>> before_img = plt.imread("patient_before.jpg")
    >>> after_img = plt.imread("patient_after.jpg")
    >>> fig, (ax1, ax2) = create_before_after_figure(
    ...     before_img, after_img,
    ...     title="6-Month Postoperative Results"
    ... )
    >>> save_prs_figure(fig, "figure1.tiff", width_inches=7.0)
    """
    # Load images if paths provided
    if isinstance(before_image, str):
        before_image = np.array(Image.open(before_image))
    if isinstance(after_image, str):
        after_image = np.array(Image.open(after_image))

    # Validate images are same size
    if before_image.shape != after_image.shape:
        raise ValueError(
            f"Before and after images must be identical size. "
            f"Got {before_image.shape} and {after_image.shape}"
        )

    # Calculate figure size if not provided
    if figsize is None:
        aspect_ratio = before_image.shape[0] / before_image.shape[1]
        figsize = (7.0, 7.0 * aspect_ratio / 2)  # Side by side

    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Display images
    ax1.imshow(before_image)
    ax2.imshow(after_image)

    # Remove axes
    ax1.axis('off')
    ax2.axis('off')

    # Add labels
    label_size = kwargs.get('label_size', 12)
    label_weight = kwargs.get('label_weight', 'bold')
    label_y = kwargs.get('label_y', -0.05)

    ax1.text(
        0.5, label_y, labels[0],
        transform=ax1.transAxes,
        ha='center', va='top',
        fontsize=label_size,
        fontweight=label_weight,
    )
    ax2.text(
        0.5, label_y, labels[1],
        transform=ax2.transAxes,
        ha='center', va='top',
        fontsize=label_size,
        fontweight=label_weight,
    )

    # Add overall title if provided
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold', y=0.98)

    # Adjust layout
    plt.tight_layout()

    return fig, (ax1, ax2)


def create_multi_view_figure(
    images: dict[str, np.ndarray | str],
    layout: Literal["row", "column", "grid"] = "row",
    labels: dict[str, str] | None = None,
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
    **kwargs
) -> Tuple[Figure, dict]:
    """
    Create a multi-view figure (e.g., frontal, lateral, oblique views).

    Parameters
    ----------
    images : dict of {str: ndarray or str}
        Dictionary mapping view names to images.
    layout : {"row", "column", "grid"}, default "row"
        Layout arrangement for multiple views.
    labels : dict of {str: str}, optional
        Custom labels for each view. If None, uses view names.
    figsize : tuple of float, optional
        Figure size in inches.
    title : str, optional
        Overall figure title.
    **kwargs
        Additional styling arguments.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure.
    axes : dict of {str: matplotlib.axes.Axes}
        Dictionary mapping view names to axes.

    Examples
    --------
    >>> views = {
    ...     "frontal": "frontal_view.jpg",
    ...     "lateral": "lateral_view.jpg",
    ...     "oblique": "oblique_view.jpg",
    ... }
    >>> fig, axes = create_multi_view_figure(
    ...     views, layout="row",
    ...     title="Preoperative Views"
    ... )
    """
    n_images = len(images)

    # Determine grid layout
    if layout == "row":
        nrows, ncols = 1, n_images
    elif layout == "column":
        nrows, ncols = n_images, 1
    elif layout == "grid":
        ncols = int(np.ceil(np.sqrt(n_images)))
        nrows = int(np.ceil(n_images / ncols))
    else:
        raise ValueError(f"Unknown layout '{layout}'")

    # Create figure
    if figsize is None:
        fig_width = 3.5 * ncols
        fig_height = 3.5 * nrows
        figsize = (fig_width, fig_height)

    fig, axes_array = plt.subplots(nrows, ncols, figsize=figsize)

    # Ensure axes_array is iterable
    if n_images == 1:
        axes_array = [axes_array]
    else:
        axes_array = axes_array.flatten() if isinstance(axes_array, np.ndarray) else [axes_array]

    # Load and display images
    axes_dict = {}
    for idx, (view_name, img) in enumerate(images.items()):
        if idx >= len(axes_array):
            break

        ax = axes_array[idx]

        # Load image if path
        if isinstance(img, str):
            img = np.array(Image.open(img))

        # Display
        ax.imshow(img)
        ax.axis('off')

        # Add label
        label = labels.get(view_name, view_name) if labels else view_name
        label_size = kwargs.get('label_size', 11)
        label_weight = kwargs.get('label_weight', 'bold')

        ax.text(
            0.5, -0.05, label,
            transform=ax.transAxes,
            ha='center', va='top',
            fontsize=label_size,
            fontweight=label_weight,
        )

        axes_dict[view_name] = ax

    # Hide unused axes
    for idx in range(n_images, len(axes_array)):
        axes_array[idx].axis('off')

    # Add overall title
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold', y=0.98)

    plt.tight_layout()

    return fig, axes_dict


# ============================================================================
# Time Series / Progression Layouts
# ============================================================================

def create_time_series_figure(
    images: dict[str, np.ndarray | str],
    time_labels: dict[str, str] | None = None,
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
    show_timeline: bool = True,
    **kwargs
) -> Tuple[Figure, dict]:
    """
    Create a time-series figure showing progression (e.g., healing progression).

    Parameters
    ----------
    images : dict of {str: ndarray or str}
        Dictionary mapping time points to images (e.g., {"preop": img1, "6mo": img2}).
    time_labels : dict of {str: str}, optional
        Human-readable labels for time points.
    figsize : tuple of float, optional
        Figure size in inches.
    title : str, optional
        Overall figure title.
    show_timeline : bool, default True
        Whether to show a timeline connecting the images.
    **kwargs
        Additional styling arguments.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure.
    axes : dict of {str: matplotlib.axes.Axes}
        Dictionary mapping time points to axes.

    Examples
    --------
    >>> progression = {
    ...     "preop": "preop.jpg",
    ...     "1wk": "1week.jpg",
    ...     "1mo": "1month.jpg",
    ...     "6mo": "6month.jpg",
    ... }
    >>> labels = {
    ...     "preop": "Preoperative",
    ...     "1wk": "1 Week",
    ...     "1mo": "1 Month",
    ...     "6mo": "6 Months",
    ... }
    >>> fig, axes = create_time_series_figure(
    ...     progression, time_labels=labels,
    ...     title="Healing Progression"
    ... )
    """
    n_images = len(images)

    # Create figure with extra space for timeline
    if figsize is None:
        figsize = (3.5 * n_images, 4.0)

    fig = plt.figure(figsize=figsize)

    # Create grid: main row for images, small row for timeline
    if show_timeline:
        gs = gridspec.GridSpec(2, n_images, height_ratios=[10, 1], hspace=0.3)
    else:
        gs = gridspec.GridSpec(1, n_images)

    # Display images
    axes_dict = {}
    for idx, (time_point, img) in enumerate(images.items()):
        ax = fig.add_subplot(gs[0, idx])

        # Load image if path
        if isinstance(img, str):
            img = np.array(Image.open(img))

        # Display
        ax.imshow(img)
        ax.axis('off')

        # Add label
        label = time_labels.get(time_point, time_point) if time_labels else time_point
        label_size = kwargs.get('label_size', 11)
        label_weight = kwargs.get('label_weight', 'bold')

        ax.text(
            0.5, -0.05, label,
            transform=ax.transAxes,
            ha='center', va='top',
            fontsize=label_size,
            fontweight=label_weight,
        )

        axes_dict[time_point] = ax

    # Add timeline if requested
    if show_timeline:
        ax_timeline = fig.add_subplot(gs[1, :])
        ax_timeline.plot([0, 1], [0.5, 0.5], 'k-', linewidth=2)

        # Add time point markers
        for idx in range(n_images):
            x_pos = idx / (n_images - 1) if n_images > 1 else 0.5
            ax_timeline.plot(x_pos, 0.5, 'ko', markersize=8)

        ax_timeline.set_xlim(-0.05, 1.05)
        ax_timeline.set_ylim(0, 1)
        ax_timeline.axis('off')

    # Add overall title
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold', y=0.98)

    plt.tight_layout()

    return fig, axes_dict


# ============================================================================
# Statistical Figure Layouts
# ============================================================================

def create_results_panel(
    plot_data: dict,
    layout: Literal["1x1", "1x2", "2x1", "2x2"] = "1x2",
    figsize: tuple[float, float] | None = None,
    title: str | None = None,
) -> Tuple[Figure, dict]:
    """
    Create a multi-panel figure for statistical results.

    Parameters
    ----------
    plot_data : dict
        Dictionary mapping panel labels to plot configuration dicts.
        Each config dict should have 'type' and 'data' keys.
    layout : {"1x1", "1x2", "2x1", "2x2"}, default "1x2"
        Grid layout for panels.
    figsize : tuple of float, optional
        Figure size in inches.
    title : str, optional
        Overall figure title.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure.
    axes : dict of {str: matplotlib.axes.Axes}
        Dictionary mapping panel labels to axes.

    Examples
    --------
    >>> plot_data = {
    ...     "A": {"type": "bar", "data": ([1, 2, 3], [10, 15, 12])},
    ...     "B": {"type": "scatter", "data": ([1, 2, 3], [10, 15, 12])},
    ... }
    >>> fig, axes = create_results_panel(plot_data, layout="1x2")
    """
    # Parse layout
    nrows, ncols = map(int, layout.split('x'))

    # Create figure
    if figsize is None:
        figsize = (5.0 * ncols, 4.0 * nrows)

    fig, axes_array = plt.subplots(nrows, ncols, figsize=figsize, squeeze=False)

    # Create axes dictionary
    axes_dict = {}
    panel_labels = list(plot_data.keys())

    for idx, label in enumerate(panel_labels):
        row = idx // ncols
        col = idx % ncols

        if row >= nrows:
            break

        ax = axes_array[row, col]
        axes_dict[label] = ax

        # Add panel label
        ax.text(
            -0.1, 1.05, label,
            transform=ax.transAxes,
            fontsize=12,
            fontweight='bold',
            va='bottom',
        )

    # Hide unused axes
    for row in range(nrows):
        for col in range(ncols):
            idx = row * ncols + col
            if idx >= len(panel_labels):
                axes_array[row, col].axis('off')

    # Add overall title
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold', y=0.98)

    plt.tight_layout()

    return fig, axes_dict
