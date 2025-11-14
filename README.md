# PRS DataViz

**Professional Data Visualization Design System for Plastic and Reconstructive Surgery Research**

A comprehensive Python package for creating publication-quality figures that meet [Plastic and Reconstructive Surgery (PRS)](https://journals.lww.com/plasreconsurg/) journal submission requirements.

## Features

### 🎨 PRS-Compliant Figure Export
- **High Resolution**: Automatic 300+ DPI export
- **CMYK Color Mode**: Print-ready color conversion
- **Proper Formats**: TIFF, PNG, JPEG, PDF, EPS support
- **Size Validation**: Ensures minimum dimensions (3.25" or 5" width)
- **Multi-Panel Support**: Separate file export for Figure 1a, 1b, etc.

### 🏥 Medical-Focused Color Palettes
- **Clinical Blue**: Professional, trustworthy palette for medical data
- **Tissue Tone**: Natural skin/tissue tones for medical photography
- **Clinical Data**: Muted, professional colors for statistical visualizations
- **Comparison**: Before/after and treatment comparison palettes
- **Statistical**: Significance-level color coding

All palettes are:
- ✅ CMYK-safe (print-ready)
- ✅ Colorblind-friendly
- ✅ WCAG 2.1 accessible
- ✅ Professional and muted

### 📐 Specialized Layouts
- **Before/After Comparisons**: Side-by-side layouts with consistent sizing
- **Multi-View Figures**: Frontal, lateral, oblique view arrangements
- **Time Series**: Healing progression and follow-up visualization
- **Statistical Panels**: Multi-panel result figures

### ♿ Accessibility-First Design
Implements [Cara Thompson's 10-step methodology](https://www.cararthompson.com/talks/on-brand-accessibility/) for accessible, neurodivergent-friendly data visualization.

## Installation

```bash
# Install from local directory
cd /Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Basic Figure Export

```python
from prs_dataviz import apply_prs_style, save_prs_figure
import matplotlib.pyplot as plt

# Apply PRS styling
apply_prs_style(cycle="clinical")

# Create your plot
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [10, 15, 12], label="Treatment")
ax.plot([1, 2, 3], [8, 10, 9], label="Control")
ax.set_xlabel("Time (months)")
ax.set_ylabel("Outcome Score")
ax.legend()

# Save in PRS-compliant format
save_prs_figure(
    fig,
    "figure1.tiff",
    dpi=300,
    width_inches=5.0,  # Minimum for graphs
    cmyk=True
)
```

### Before/After Comparison

```python
from prs_dataviz import create_before_after_figure, save_multi_panel_figure
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# Load patient photos
before_img = np.array(Image.open("patient_before.jpg"))
after_img = np.array(Image.open("patient_after.jpg"))

# Create comparison figure
fig, (ax_before, ax_after) = create_before_after_figure(
    before_img,
    after_img,
    labels=("Preoperative", "6 Months Postoperative"),
    title="Rhinoplasty Results"
)

# Save as separate panels (PRS requirement)
save_multi_panel_figure(
    {"a": fig},  # If you have multiple views, add them here
    "Figure1",
    dpi=300,
    width_inches=3.5,
    format="tiff"
)
```

### Statistical Results Figure

```python
from prs_dataviz import apply_prs_style, format_statistical_plot, save_prs_figure
import matplotlib.pyplot as plt
import numpy as np

apply_prs_style(cycle="clinical", show_grid=True)

fig, ax = plt.subplots(figsize=(5, 4))

# Example data
categories = ['Pre-op', '3 months', '6 months', '12 months']
control = [65, 68, 70, 72]
treatment = [65, 75, 82, 88]

x = np.arange(len(categories))
width = 0.35

ax.bar(x - width/2, control, width, label='Control')
ax.bar(x + width/2, treatment, width, label='Treatment')

ax.set_ylabel('Patient Satisfaction Score')
ax.set_xlabel('Follow-up Time')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

# Apply statistical formatting
format_statistical_plot(ax, show_significance=True)

save_prs_figure(fig, "results.tiff", dpi=300, width_inches=5.0)
```

### Time Series / Healing Progression

```python
from prs_dataviz import create_time_series_figure, save_prs_figure

# Patient healing progression photos
progression = {
    "preop": "preop.jpg",
    "1wk": "1week_postop.jpg",
    "1mo": "1month_postop.jpg",
    "6mo": "6month_postop.jpg",
}

time_labels = {
    "preop": "Preoperative",
    "1wk": "1 Week",
    "1mo": "1 Month",
    "6mo": "6 Months",
}

fig, axes = create_time_series_figure(
    progression,
    time_labels=time_labels,
    title="Wound Healing Progression",
    show_timeline=True
)

save_prs_figure(fig, "healing_progression.tiff", dpi=300, width_inches=7.0)
```

### Adding Scale Bars to Microscopy Images

```python
from prs_dataviz import apply_prs_style, add_scale_bar, save_prs_figure
import matplotlib.pyplot as plt

apply_prs_style()

fig, ax = plt.subplots()
ax.imshow(microscopy_image)
ax.axis('off')

# PRS prefers scale bars over magnification text
add_scale_bar(
    ax,
    length=100,  # in data coordinates
    label="100 μm",
    location="lower right",
    color='white'
)

save_prs_figure(fig, "microscopy.tiff", dpi=300, width_inches=3.5)
```

## Color Palettes

### Clinical Blue (Professional/Trustworthy)
```python
from prs_dataviz import CLINICAL_BLUE, apply_prs_style

# Use clinical blue palette
apply_prs_style(cycle="clinical")
```

Colors: Navy (#1F4788), Steel Blue (#4A7BA7), Sky Blue (#7FA8C9), Light Blue (#B8D4E8), Pale Blue (#E3F0F7)

### Comparison (Before/After)
```python
from prs_dataviz import COMPARISON, apply_prs_style

apply_prs_style(cycle="comparison")
```

Colors: Before (#8B7A7A), After (#5B8F7D), Control (#7A8A99), Treatment (#9B7357)

### Statistical Significance
```python
from prs_dataviz import STATISTICAL

# Use different colors for significance levels
colors = [
    STATISTICAL["Significant"],        # p < 0.05
    STATISTICAL["Highly Significant"], # p < 0.01
    STATISTICAL["Non-Significant"],    # p ≥ 0.05
]
```

## Validating Existing Figures

```python
from prs_dataviz import validate_figure_file

# Check if an existing figure meets PRS requirements
results = validate_figure_file("my_figure.tiff")

if results['valid']:
    print("✓ Figure meets PRS requirements")
else:
    print("✗ Issues found:")
    for issue in results['issues']:
        print(f"  - {issue}")

print(f"DPI: {results['dpi']}")
print(f"Dimensions: {results['width_inches']:.2f}\" × {results['height_inches']:.2f}\"")
print(f"Color mode: {results['color_mode']}")
```

## PRS Figure Requirements Summary

From [PRS Author Guidelines](https://journals.lww.com/plasreconsurg/pages/informationforauthors.aspx):

### ✅ Required
- **Minimum 300 DPI** resolution
- **Minimum width**: 3.25" (single images) or 5" (graphs/text)
- **CMYK color mode** for print
- **Supported formats**: TIFF, PNG, JPEG, PDF, EPS
- **Separate files** for multi-panel figures (1a, 1b, etc.)
- **Identical sizing** for before/after comparisons
- **High professional quality**

### ❌ Not Accepted
- Images copied into Word documents
- Blurred patient photos (consent required for identifiable photos)
- Substantially modified photographs
- Bar graphs in grayscale (use color)

## Design System Methodology

This package implements **[Cara Thompson's 10-step process](https://www.cararthompson.com/talks/on-brand-accessibility/)** for building accessible, neurodivergent-friendly data visualization design systems:

1. ✅ **Choose Intuitive Colours** - Perceptually-spaced color palettes
2. ✅ **Check Colorblind-Friendly** - All palettes tested for colorblind accessibility
3. ✅ **Blend Brand Colors** - Support for institutional color integration
4. ✅ **Mute Colors** - Reduced saturation for neurodivergent audiences
5. ✅ **Check Contrast** - WCAG 2.1 compliant (4.5:1 for text, 3:1 for UI)
6. ✅ **Typography** - Professional, readable font defaults
7. ✅ **Spacing** - Dyslexia-friendly spacing
8. ✅ **Backgrounds** - Subtle backgrounds to reduce eye strain
9. ✅ **Titles & Annotations** - Clear, hierarchical text
10. ✅ **Complete System** - Comprehensive, cohesive design

## Examples Gallery

See `notebooks/gallery.ipynb` for a comprehensive gallery of examples including:
- Statistical result figures
- Before/after comparisons
- Multi-panel figures
- Time series visualizations
- Microscopy images with scale bars
- Color palette demonstrations

## API Reference

### Style Functions
- `apply_prs_style(cycle, font_family, show_grid, show_spines)` - Apply PRS styling globally
- `format_statistical_plot(ax, show_significance)` - Format statistical plots
- `format_comparison_plot(ax, comparison_type)` - Format before/after plots
- `add_scale_bar(ax, length, label, location)` - Add scale bar to images
- `prs_legend(ax, outside)` - Create professional legend

### Export Functions
- `save_prs_figure(fig, filename, dpi, width_inches, format, cmyk)` - Save PRS-compliant figure
- `save_multi_panel_figure(figures, base_filename, dpi, width_inches)` - Save multi-panel figures
- `validate_figure_file(filename, min_dpi, min_width_inches)` - Validate existing figures

### Layout Functions
- `create_before_after_figure(before_image, after_image, labels, title)` - Before/after layout
- `create_multi_view_figure(images, layout, labels, title)` - Multi-view layout
- `create_time_series_figure(images, time_labels, title, show_timeline)` - Time series layout
- `create_results_panel(plot_data, layout, title)` - Statistical results panel

### Color Utilities
- `rgb_to_cmyk(r, g, b)` - Convert RGB to CMYK
- `cmyk_to_rgb(c, m, y, k)` - Convert CMYK to RGB

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/

# Lint
ruff check src/
```

## Credits

**Design System Methodology**: [Cara Thompson's 10-step process](https://www.cararthompson.com/talks/on-brand-accessibility/) for building accessible, neurodivergent-friendly data visualizations.

**PRS Guidelines**: [Plastic and Reconstructive Surgery Author Guidelines](https://journals.lww.com/plasreconsurg/pages/informationforauthors.aspx)

## License

MIT License - See LICENSE file for details

## Author

Moreen Njoroge, Plastic Surgery Researcher

---

**Note**: This is an independent tool designed to help researchers meet PRS submission requirements. It is not officially affiliated with PRS journal or Wolters Kluwer.
