"""
Figure export utilities for PRS journal submissions.

Ensures compliance with PRS figure requirements:
- Minimum 300 DPI resolution
- CMYK color mode for print
- Proper file formats (TIFF, PNG, JPEG, PDF, EPS)
- Minimum dimensions (3.25" or 5" width)
- Professional quality output

Reference: PRS Author Guidelines
https://journals.lww.com/plasreconsurg/pages/informationforauthors.aspx
"""

import io
import warnings
from pathlib import Path
from typing import Literal, Optional

import matplotlib.figure
from PIL import Image

# ============================================================================
# PRS Figure Requirements
# ============================================================================

PRS_MIN_DPI = 300
PRS_MIN_WIDTH_SINGLE = 3.25  # inches
PRS_MIN_WIDTH_GRAPH = 5.0  # inches (for graphs or small text)
PRS_COLOR_MODE = "CMYK"

SUPPORTED_FORMATS = ["tiff", "png", "jpeg", "jpg", "pdf", "eps"]


# ============================================================================
# Figure Export Functions
# ============================================================================


def save_prs_figure(
    fig: matplotlib.figure.Figure,
    filename: str | Path,
    dpi: int = 300,
    width_inches: float = 5.0,
    format: Optional[Literal["tiff", "png", "jpeg", "pdf", "eps"]] = None,
    cmyk: bool = True,
    validate: bool = True,
    **kwargs,
) -> Path:
    """
    Save a matplotlib figure in PRS-compliant format.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to save.
    filename : str or Path
        Output filename. Extension determines format if `format` not specified.
    dpi : int, default 300
        Resolution in dots per inch. PRS requires minimum 300 DPI.
    width_inches : float, default 5.0
        Figure width in inches. PRS requires:
        - 3.25" minimum for single images
        - 5.0" minimum for graphs or images with text
    format : str, optional
        File format. If None, inferred from filename extension.
        Supported: tiff, png, jpeg, pdf, eps
    cmyk : bool, default True
        Convert to CMYK color mode (required for PRS print).
    validate : bool, default True
        Validate figure meets PRS requirements before saving.
    **kwargs
        Additional arguments passed to savefig().

    Returns
    -------
    Path
        Path to saved figure.

    Raises
    ------
    ValueError
        If figure doesn't meet PRS requirements and validate=True.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [1, 4, 9])
    >>> save_prs_figure(fig, "figure1.tiff", dpi=300, width_inches=5.0)

    >>> # For a simple photograph
    >>> save_prs_figure(fig, "patient_photo.tiff", width_inches=3.5)

    >>> # Disable CMYK for draft/preview
    >>> save_prs_figure(fig, "draft.png", cmyk=False, validate=False)
    """
    filename = Path(filename)

    # Determine format
    if format is None:
        format = filename.suffix.lstrip(".").lower()
    if format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format '{format}'. "
            f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        )

    # Validation
    if validate:
        _validate_prs_requirements(dpi, width_inches, format)

    # Set figure size
    height_inches = fig.get_figheight()
    aspect_ratio = height_inches / fig.get_figwidth()
    fig.set_size_inches(width_inches, width_inches * aspect_ratio)

    # Save figure
    if format in ["tiff", "png", "jpeg", "jpg"]:
        _save_raster_figure(fig, filename, dpi, format, cmyk, **kwargs)
    elif format == "pdf":
        _save_pdf_figure(fig, filename, dpi, **kwargs)
    elif format == "eps":
        _save_eps_figure(fig, filename, dpi, **kwargs)

    return filename


def _validate_prs_requirements(dpi: int, width_inches: float, format: str) -> None:
    """Validate figure meets PRS requirements."""
    issues = []

    # Check DPI
    if dpi < PRS_MIN_DPI:
        issues.append(
            f"DPI {dpi} is below PRS minimum of {PRS_MIN_DPI}. Figure may be rejected."
        )

    # Check width
    if width_inches < PRS_MIN_WIDTH_SINGLE:
        issues.append(
            f'Width {width_inches}" is below PRS minimum of {PRS_MIN_WIDTH_SINGLE}". '
            f'For graphs or text, use {PRS_MIN_WIDTH_GRAPH}" minimum.'
        )

    # Check format
    if format not in SUPPORTED_FORMATS:
        issues.append(
            f"Format '{format}' may not be accepted by PRS. "
            f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        )

    if issues:
        warning_msg = "PRS validation warnings:\n" + "\n".join(
            f"  - {issue}" for issue in issues
        )
        warnings.warn(warning_msg, UserWarning)


def _save_raster_figure(
    fig: matplotlib.figure.Figure,
    filename: Path,
    dpi: int,
    format: str,
    cmyk: bool,
    **kwargs,
) -> None:
    """Save figure as raster image (TIFF, PNG, JPEG)."""
    # Save to buffer first
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", **kwargs)
    buf.seek(0)

    # Open with PIL for color mode conversion
    img = Image.open(buf)

    # Convert to CMYK if requested
    if cmyk and img.mode != "CMYK":
        # Convert to RGB first if necessary
        if img.mode != "RGB":
            img = img.convert("RGB")
        # Convert to CMYK
        img = img.convert("CMYK")

    # Save in requested format
    save_format = "TIFF" if format == "tiff" else format.upper()
    save_kwargs = {}

    if format == "tiff":
        save_kwargs["compression"] = "tiff_lzw"  # Lossless compression
        save_kwargs["dpi"] = (dpi, dpi)
    elif format in ["jpeg", "jpg"]:
        save_kwargs["quality"] = 95  # High quality
        save_kwargs["dpi"] = (dpi, dpi)
        if cmyk:
            # JPEG can natively support CMYK
            pass
    elif format == "png":
        save_kwargs["dpi"] = (dpi, dpi)
        if cmyk:
            warnings.warn(
                "PNG does not natively support CMYK. "
                "Consider using TIFF format for CMYK output.",
                UserWarning,
            )
            # Convert back to RGB for PNG
            img = img.convert("RGB")

    img.save(filename, format=save_format, **save_kwargs)
    buf.close()


def _save_pdf_figure(
    fig: matplotlib.figure.Figure, filename: Path, dpi: int, **kwargs
) -> None:
    """Save figure as PDF (vector format)."""
    fig.savefig(filename, format="pdf", dpi=dpi, bbox_inches="tight", **kwargs)


def _save_eps_figure(
    fig: matplotlib.figure.Figure, filename: Path, dpi: int, **kwargs
) -> None:
    """Save figure as EPS (vector format)."""
    fig.savefig(filename, format="eps", dpi=dpi, bbox_inches="tight", **kwargs)


# ============================================================================
# Multi-Panel Figure Export
# ============================================================================


def save_multi_panel_figure(
    figures: dict[str, matplotlib.figure.Figure],
    base_filename: str | Path,
    dpi: int = 300,
    width_inches: float = 3.5,
    format: str = "tiff",
    **kwargs,
) -> dict[str, Path]:
    """
    Save multiple panels of a figure as separate files.

    PRS requires multi-panel figures to be saved as separate files
    (e.g., Figure1a.tiff, Figure1b.tiff) rather than a single composite image.

    Parameters
    ----------
    figures : dict[str, Figure]
        Dictionary mapping panel labels (e.g., "a", "b", "c") to figures.
    base_filename : str or Path
        Base filename without panel suffix. E.g., "Figure1" will create
        "Figure1a.tiff", "Figure1b.tiff", etc.
    dpi : int, default 300
        Resolution for all panels.
    width_inches : float, default 3.5
        Width for all panels (inches).
    format : str, default "tiff"
        File format for all panels.
    **kwargs
        Additional arguments passed to save_prs_figure().

    Returns
    -------
    dict[str, Path]
        Dictionary mapping panel labels to saved file paths.

    Examples
    --------
    >>> fig_a, ax_a = plt.subplots()
    >>> fig_b, ax_b = plt.subplots()
    >>> ax_a.imshow(preop_image)
    >>> ax_b.imshow(postop_image)
    >>> save_multi_panel_figure(
    ...     {"a": fig_a, "b": fig_b},
    ...     "Figure1",
    ...     dpi=300,
    ...     width_inches=3.5
    ... )
    """
    base_path = Path(base_filename)
    base_name = base_path.stem
    output_dir = base_path.parent if base_path.parent.name else Path.cwd()

    saved_files = {}

    for panel_label, fig in figures.items():
        # Create filename with panel suffix
        panel_filename = output_dir / f"{base_name}{panel_label}.{format}"

        # Save figure
        saved_path = save_prs_figure(
            fig,
            panel_filename,
            dpi=dpi,
            width_inches=width_inches,
            format=format,
            **kwargs,
        )

        saved_files[panel_label] = saved_path

    return saved_files


# ============================================================================
# Figure Validation Utilities
# ============================================================================


def validate_figure_file(
    filename: str | Path, min_dpi: int = 300, min_width_inches: float = 3.25
) -> dict[str, any]:
    """
    Validate an existing figure file meets PRS requirements.

    Parameters
    ----------
    filename : str or Path
        Path to figure file.
    min_dpi : int, default 300
        Minimum required DPI.
    min_width_inches : float, default 3.25
        Minimum required width in inches.

    Returns
    -------
    dict
        Validation results with keys:
        - 'valid': bool, whether file meets requirements
        - 'dpi': int or None, detected DPI
        - 'width_inches': float or None, detected width in inches
        - 'height_inches': float or None, detected height in inches
        - 'color_mode': str or None, detected color mode
        - 'issues': list of str, any issues found

    Examples
    --------
    >>> results = validate_figure_file("figure1.tiff")
    >>> if not results['valid']:
    ...     print("Issues:", results['issues'])
    """
    filename = Path(filename)
    issues = []

    try:
        img = Image.open(filename)

        # Get DPI
        dpi = img.info.get("dpi")
        if dpi:
            dpi_x, dpi_y = dpi
            dpi_avg = (dpi_x + dpi_y) / 2
        else:
            dpi_avg = None
            issues.append("DPI information not found in image metadata")

        # Get dimensions
        width_px, height_px = img.size

        if dpi_avg:
            width_inches = width_px / dpi_avg
            height_inches = height_px / dpi_avg

            # Check DPI
            if dpi_avg < min_dpi:
                issues.append(f"DPI {dpi_avg:.0f} is below minimum {min_dpi}")

            # Check width
            if width_inches < min_width_inches:
                issues.append(
                    f'Width {width_inches:.2f}" is below minimum {min_width_inches}"'
                )
        else:
            width_inches = None
            height_inches = None

        # Get color mode
        color_mode = img.mode

        if color_mode not in ["CMYK", "RGB"]:
            issues.append(
                f"Color mode '{color_mode}' may not be suitable. "
                "PRS recommends CMYK for print."
            )

        valid = len(issues) == 0

        return {
            "valid": valid,
            "dpi": dpi_avg,
            "width_inches": width_inches,
            "height_inches": height_inches,
            "width_pixels": width_px,
            "height_pixels": height_px,
            "color_mode": color_mode,
            "issues": issues,
        }

    except Exception as e:
        return {
            "valid": False,
            "dpi": None,
            "width_inches": None,
            "height_inches": None,
            "width_pixels": None,
            "height_pixels": None,
            "color_mode": None,
            "issues": [f"Error reading file: {str(e)}"],
        }
