# prs_dataviz API Quick Reference

## Installation

```bash
# Using uv (recommended - 10-100x faster)
uv pip install "prs-dataviz @ git+https://github.com/Shakes-tzd/prs-dataviz.git"

# Or using pip
pip install "git+https://github.com/Shakes-tzd/prs-dataviz.git"

# Verify installation
python -c "import prs_dataviz; print(f'✅ prs_dataviz {prs_dataviz.__version__}')"
```

---

## Core Workflow

```python
import matplotlib.pyplot as plt
from prs_dataviz import apply_prs_style, save_prs_figure, prs_legend

# 1. Apply PRS styling (ALWAYS first)
apply_prs_style(cycle="clinical")

# 2. Create figure
fig, ax = plt.subplots(figsize=(8, 5))
# ... plotting code ...

# 3. Add legend
prs_legend(ax, position="best")

# 4. Export PRS-compliant
save_prs_figure(fig, "figure1.tiff", dpi=300, cmyk=True)

# 5. Validate
from prs_dataviz import validate_figure_file
result = validate_figure_file("figure1.tiff")
```

---

## Color Palettes

### Pre-defined Palettes (All CMYK-safe, Colorblind-friendly)

```python
from prs_dataviz import (
    CLINICAL_BLUE,    # Professional blue family
    TISSUE_TONE,      # Natural tissue/skin tones
    CLINICAL_DATA,    # Muted statistical colors
    COMPARISON,       # Before/after comparisons
    STATISTICAL,      # Significance levels
)

# Color families (dictionaries)
CLINICAL_BLUE = {
    "Dark": "#2C5F87",      # Deep clinical blue
    "Medium": "#4A7BA7",    # Medium blue
    "Light": "#7FA6C9",     # Light blue
    "Accent": "#B8D4E9",    # Accent blue
}

COMPARISON = {
    "Control": "#7A8A99",   # Neutral gray-blue (before/control)
    "Treatment": "#5A8A8A", # Clinical teal (after/treatment)
    "Before": "#7A8A99",    # Alias for control
    "After": "#5A8A8A",     # Alias for treatment
}

CLINICAL_DATA = {
    "Primary": "#4A7BA7",   # Primary data color
    "Secondary": "#7A8A99", # Secondary data color
    "Tertiary": "#9B7357",  # Tertiary data color
    "Accent": "#5A8A8A",    # Accent color
    "Highlight": "#C17D5D", # Highlight color
}

STATISTICAL = {
    "Significant": "#2C5F87",      # p < 0.05
    "VerySignificant": "#1A3A5A",  # p < 0.01
    "NotSignificant": "#CCCCCC",   # p ≥ 0.05
}

TISSUE_TONE = {
    "Light": "#E8C4A8",     # Light skin tone
    "Medium": "#C99876",    # Medium skin tone
    "Dark": "#8B6341",      # Dark skin tone
    "Accent": "#9B7357",    # Accent tone
}
```

### Color Cycles

```python
from prs_dataviz import (
    PRS_DEFAULT_CYCLE,    # 7 colors - general categorical
    PRS_CLINICAL_CYCLE,   # 5 colors - muted clinical
    PRS_COMPARISON_CYCLE, # 2 colors - before/after
)

# Usage:
apply_prs_style(cycle="default")    # Uses PRS_DEFAULT_CYCLE
apply_prs_style(cycle="clinical")   # Uses PRS_CLINICAL_CYCLE
apply_prs_style(cycle="comparison") # Uses PRS_COMPARISON_CYCLE
```

---

## Styling Functions

### `apply_prs_style()`

Apply PRS-compliant global matplotlib styling.

```python
def apply_prs_style(
    *,
    cycle: str = "default",           # "default", "clinical", "comparison"
    font_family: str = "DejaVu Sans", # Font family
    font_size: int = 10,              # Base font size
    show_grid: bool = False,          # Show grid lines
    show_spines: bool = True,         # Show axis spines
    custom_font_paths: list = None,   # Custom font paths
) -> None:
```

**Example**:
```python
# Clinical data with grid
apply_prs_style(cycle="clinical", show_grid=True)

# Before/after comparison
apply_prs_style(cycle="comparison")

# Custom font size
apply_prs_style(cycle="default", font_size=12)
```

### `prs_legend()`

Create professional legend with smart positioning.

```python
def prs_legend(
    ax,
    *args,
    position: str = "best",    # "best", "outside", "top", "top-smart", or matplotlib locations
    compact: bool = False,     # Compact spacing for multi-column
    ncol: int = None,          # Number of columns (auto-calculated if None)
    fontsize: int = None,      # Font size (defaults to 12pt)
    **kwargs                   # Additional matplotlib legend kwargs
) -> None:
```

**Examples**:
```python
# Auto-optimal positioning (avoids data)
prs_legend(ax, position="best")

# Top position with auto-calculated columns
prs_legend(ax, position="top-smart")

# Outside right side
prs_legend(ax, position="outside")

# Explicit positioning
prs_legend(ax, position="upper left", fontsize=12)

# Compact spacing for many items
prs_legend(ax, position="top", compact=True, ncol=4)
```

**Auto-detection features**:
- Automatically calculates optimal `ncol` based on label lengths
- Automatically detects bar charts and applies larger handles
- Automatically adjusts `bbox_to_anchor` based on `ncol`

### `set_axis_fontsize()`

Standardize font sizes across all text elements.

```python
def set_axis_fontsize(ax, fontsize: int) -> None:
```

**Example**:
```python
# Standardize to 12pt
set_axis_fontsize(ax, fontsize=12)
prs_legend(ax, fontsize=12)

# Result: tick labels, axis labels, title all consistent
```

### `add_significance_indicator()`

Add statistical significance indicators to plots.

```python
def add_significance_indicator(
    ax,
    x: float,                  # X-coordinate (center if bracket=True)
    y: float,                  # Y-coordinate for bracket base
    p_value: float = None,     # P-value for auto-formatting
    symbol: str = "*",         # Symbol ("*", "**", "***", "ns")
    bracket: bool = False,     # Draw horizontal bracket
    x_start: float = None,     # Bracket start x (if bracket=True)
    x_end: float = None,       # Bracket end x (if bracket=True)
    show_p_value: bool = True, # Show exact p-value (default) or symbol
    **kwargs                   # Additional formatting (text_fontsize, line_width, etc.)
) -> None:
```

**Examples**:
```python
# Show exact p-value (default)
add_significance_indicator(
    ax, x=1.5, y=95, p_value=0.03,
    bracket=True, x_start=1, x_end=2
)

# Show symbol only
add_significance_indicator(
    ax, x=1.5, y=95, symbol="**",
    bracket=True, x_start=1, x_end=2,
    show_p_value=False
)

# Auto-select symbol based on p-value
from prs_dataviz import get_significance_symbol
symbol = get_significance_symbol(0.008)  # Returns "**"
add_significance_indicator(
    ax, x=1.5, y=95, symbol=symbol,
    bracket=True, x_start=1, x_end=2,
    show_p_value=False
)
```

### `add_scale_bar()`

Add scale bar to medical images.

```python
def add_scale_bar(
    ax,
    length: float,             # Length in data coordinates
    label: str,                # Label (e.g., "100 μm")
    location: str = "lower right",  # Position
    **kwargs                   # Additional styling
) -> None:
```

**Example**:
```python
# Microscopy image
ax.imshow(microscopy_image)
add_scale_bar(ax, length=100, label="100 μm", location="lower right")
```

---

## Export Functions

### `save_prs_figure()`

Save figure meeting all PRS requirements.

```python
def save_prs_figure(
    fig,                       # Matplotlib figure
    filename: str,             # Output filename
    dpi: int = 300,            # Resolution (minimum 300 for PRS)
    width_inches: float = None,  # Width in inches (validates min requirements)
    cmyk: bool = True,         # Convert to CMYK color mode
    **kwargs                   # Additional savefig kwargs
) -> None:
```

**Examples**:
```python
# Basic export
save_prs_figure(fig, "figure1.tiff", dpi=300, cmyk=True)

# Specify width (validates minimum)
save_prs_figure(fig, "figure1.tiff", dpi=300, width_inches=5.0, cmyk=True)

# High-resolution for text-heavy figures
save_prs_figure(fig, "figure1.tiff", dpi=600, cmyk=True)
```

**Formats supported**: TIFF (preferred), PNG, JPEG, PDF, EPS

### `save_multi_panel_figure()`

Save multi-panel figures as separate files (PRS requirement).

```python
def save_multi_panel_figure(
    figures: dict,             # {"a": fig_a, "b": fig_b, ...}
    base_filename: str,        # "Figure1" → Figure1a.tiff, Figure1b.tiff
    dpi: int = 300,
    width_inches: float = None,
    **kwargs
) -> None:
```

**Example**:
```python
# Create panels
fig_a, ax_a = plt.subplots()
# ... plot panel A ...

fig_b, ax_b = plt.subplots()
# ... plot panel B ...

# Export as separate files (PRS requirement)
save_multi_panel_figure(
    {"a": fig_a, "b": fig_b},
    "Figure1",  # Creates Figure1a.tiff, Figure1b.tiff
    dpi=300,
    width_inches=3.5
)
```

### `validate_figure_file()`

Validate existing figure for PRS compliance.

```python
def validate_figure_file(filename: str) -> dict:
```

**Returns**:
```python
{
    "valid": bool,            # True if all requirements met
    "dpi": int,               # Actual DPI
    "width_inches": float,    # Width in inches
    "height_inches": float,   # Height in inches
    "color_mode": str,        # "RGB", "CMYK", "Grayscale"
    "format": str,            # File format
    "issues": list,           # List of issues found (empty if valid)
}
```

**Example**:
```python
result = validate_figure_file("figure1.tiff")

if result["valid"]:
    print("✅ Figure meets all PRS requirements!")
else:
    print("❌ Issues found:")
    for issue in result["issues"]:
        print(f"  - {issue}")
```

---

## Layout Functions

### `create_before_after_figure()`

Create side-by-side before/after comparison (validates identical sizing).

```python
def create_before_after_figure(
    before_image,              # Numpy array or file path
    after_image,               # Numpy array or file path
    titles: tuple = ("Before", "After"),
    figsize: tuple = (10, 5),
    **kwargs
) -> tuple:  # Returns (fig, (ax_before, ax_after))
```

**Example**:
```python
from prs_dataviz import create_before_after_figure

fig, (ax_before, ax_after) = create_before_after_figure(
    "before.jpg",
    "after.jpg",
    titles=("Preoperative", "6 Months Postoperative")
)

# Package automatically validates identical dimensions
# Will error if images are different sizes
```

### `create_multi_view_figure()`

Create multi-view figure (frontal, lateral, oblique).

```python
def create_multi_view_figure(
    images: list,              # List of images (arrays or paths)
    titles: list,              # List of titles
    layout: str = "row",       # "row", "column", "grid"
    figsize: tuple = None,
    **kwargs
) -> tuple:  # Returns (fig, axes)
```

**Example**:
```python
fig, axes = create_multi_view_figure(
    [frontal_img, lateral_img, oblique_img],
    ["Frontal View", "Lateral View", "Oblique View"],
    layout="row"
)
```

### `create_time_series_figure()`

Create time series progression figure.

```python
def create_time_series_figure(
    images: list,              # List of images at different time points
    timepoints: list,          # List of time labels
    timeline: bool = True,     # Show timeline below images
    **kwargs
) -> tuple:  # Returns (fig, axes)
```

**Example**:
```python
fig, axes = create_time_series_figure(
    [img_preop, img_3mo, img_6mo, img_12mo],
    ["Preoperative", "3 Months", "6 Months", "12 Months"],
    timeline=True
)
```

### `create_results_panel()`

Create multi-panel statistical results figure.

```python
def create_results_panel(
    figures: dict,             # {"A": fig_a, "B": fig_b, ...}
    layout: str = "2x2",       # "1x2", "2x1", "2x2", "2x3", etc.
    figsize: tuple = None,
    **kwargs
) -> tuple:  # Returns (fig, axes_dict)
```

**Example**:
```python
# Create individual plots
fig_a, ax_a = plt.subplots()
# ... plot panel A ...

fig_b, ax_b = plt.subplots()
# ... plot panel B ...

# Combine into results panel
fig, axes = create_results_panel(
    {"A": fig_a, "B": fig_b, "C": fig_c, "D": fig_d},
    layout="2x2"
)
```

---

## Helper Functions

### Auto-Positioning Helpers

#### `add_multiple_comparisons()`

Add multiple significance indicators with automatic bracket positioning.

```python
def add_multiple_comparisons(
    ax,
    comparisons: list,         # [(idx1, idx2, p_value), ...]
    x_positions: array,        # X-positions of bars/points
    **kwargs
) -> None:
```

**Example**:
```python
from prs_dataviz import add_multiple_comparisons

# Define comparisons: (group1_idx, group2_idx, p_value)
comparisons = [
    (0, 1, 0.03),   # Compare groups 0 vs 1, p=0.03
    (1, 2, 0.008),  # Compare groups 1 vs 2, p=0.008
    (0, 2, 0.0001), # Compare groups 0 vs 2, p=0.0001
]

x = np.arange(len(categories))
add_multiple_comparisons(ax, comparisons, x)

# Automatically calculates bracket heights and spacing!
# No manual y-coordinate calculation needed.
```

#### `auto_calculate_ylim_for_annotations()`

Automatically calculate y-axis limits with headroom for annotations.

```python
def auto_calculate_ylim_for_annotations(
    ax,
    extension: float = 0.15    # Extension percentage (0.15 = 15%)
) -> tuple:  # Returns (ymin, ymax)
```

**Example**:
```python
from prs_dataviz import auto_calculate_ylim_for_annotations

# Plot data
ax.bar(x, y)

# Auto-extend y-axis for significance indicators
ymin, ymax = auto_calculate_ylim_for_annotations(ax, extension=0.15)
ax.set_ylim(ymin, ymax)

# Now plenty of room for brackets above data
```

#### `get_significance_symbol()`

Get standard significance symbol for p-value.

```python
def get_significance_symbol(p_value: float) -> str:
```

**Returns**:
- `"***"` if p < 0.001
- `"**"` if p < 0.01
- `"*"` if p < 0.05
- `"ns"` if p ≥ 0.05

**Example**:
```python
from prs_dataviz import get_significance_symbol

symbol = get_significance_symbol(0.008)  # Returns "**"
add_significance_indicator(
    ax, x=1.5, y=95, symbol=symbol,
    bracket=True, x_start=1, x_end=2,
    show_p_value=False
)
```

---

## PRS Requirements Constants

```python
from prs_dataviz import (
    PRS_MIN_DPI,            # 300
    PRS_MIN_WIDTH_SINGLE,   # 3.25 inches (patient photos)
    PRS_MIN_WIDTH_GRAPH,    # 5.0 inches (graphs with text)
)
```

---

## Color Utilities

```python
from prs_dataviz import rgb_to_cmyk, cmyk_to_rgb

# Convert RGB to CMYK
cmyk = rgb_to_cmyk(255, 100, 50)  # Returns (c, m, y, k) tuple

# Convert CMYK to RGB
rgb = cmyk_to_rgb(0.5, 0.3, 0.2, 0.1)  # Returns (r, g, b) tuple
```

---

## Complete Example

```python
import matplotlib.pyplot as plt
import numpy as np
from prs_dataviz import (
    apply_prs_style,
    save_prs_figure,
    prs_legend,
    add_multiple_comparisons,
    validate_figure_file,
    COMPARISON,
)

# 1. Apply PRS styling
apply_prs_style(cycle="comparison", show_grid=True)

# 2. Create figure
fig, ax = plt.subplots(figsize=(8, 5))

# 3. Plot data with explicit colors
categories = ["Pre-op", "3 Months", "6 Months", "12 Months"]
control = [65, 68, 70, 72]
treatment = [65, 75, 82, 88]

x = np.arange(len(categories))
width = 0.35

ax.bar(x - width/2, control, width, label="Control",
       color=COMPARISON["Control"], alpha=0.8)
ax.bar(x + width/2, treatment, width, label="Treatment",
       color=COMPARISON["Treatment"], alpha=0.8)

# 4. Format axes
fontsize = 12
ax.set_ylabel("Satisfaction Score (%)", fontsize=fontsize, fontweight="bold")
ax.set_xlabel("Follow-up Time", fontsize=fontsize, fontweight="bold")
ax.set_title("Treatment Efficacy", fontsize=fontsize + 2, fontweight="bold", pad=15)

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=fontsize)
ax.tick_params(axis="y", labelsize=fontsize)
ax.set_ylim(0, 100)

# 5. Add legend
prs_legend(ax, position="best", fontsize=fontsize)

# 6. Add grid
ax.yaxis.grid(True, linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

# 7. Add significance indicators (auto-positioned)
comparisons = [(2, 3, 0.03)]  # 6mo vs 12mo, p=0.03
add_multiple_comparisons(ax, comparisons, x + width/2)

plt.tight_layout()

# 8. Save draft for inspection
plt.savefig("draft.png", dpi=150)

# 9. Visual inspection (in actual workflow)
# display(Image("draft.png"))
# [Critique and refine as needed]

# 10. Export PRS-compliant
save_prs_figure(fig, "figure1.tiff", dpi=300, width_inches=5.0, cmyk=True)

# 11. Validate
result = validate_figure_file("figure1.tiff")
print(f"Status: {'✅ PASS' if result['valid'] else '❌ FAIL'}")
```

---

## Package Info

- **GitHub**: https://github.com/Shakes-tzd/prs-dataviz
- **Version**: Check with `import prs_dataviz; print(prs_dataviz.__version__)`
- **License**: MIT
- **Python**: Requires 3.11+
- **Dependencies**: matplotlib, numpy, pillow, pandas (optional)
