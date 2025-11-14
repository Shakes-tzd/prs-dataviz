# Handoff Document: PRS DataViz Package

**Date**: November 14, 2025
**For**: Moreen Njoroge (Plastic Surgery Researcher)
**Project**: PRS-compliant Data Visualization Design System
**Location**: `/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/`

---

## Executive Summary

This package provides a complete solution for creating publication-quality figures that meet Plastic and Reconstructive Surgery (PRS) journal submission requirements. All PRS figure guidelines have been implemented into easy-to-use Python functions.

**Key Benefits**:
- ✅ Automatic PRS compliance (300 DPI, CMYK, proper sizing)
- ✅ Professional medical color palettes
- ✅ Before/after comparison layouts
- ✅ Figure validation before submission
- ✅ Accessibility-focused design

---

## 1. Installation & Setup

### First-Time Setup (One Time Only)

**Important**: This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management (10-100x faster than pip).

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to project folder
cd /Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system

# Install package with uv (preferred)
uv pip install -e .

# Verify installation
uv run python -c "import prs_dataviz; print('✓ Installation successful!')"
```

**Alternative (traditional pip)**:
```bash
pip install -e .
python -c "import prs_dataviz; print('✓ Installation successful!')"
```

### Updating the Package (After Changes)

```bash
cd /Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system

# With uv (preferred)
uv pip install -e . --force-reinstall

# Or sync all dependencies
uv sync

# With pip
pip install -e . --force-reinstall
```

### Why Use uv?

- **10-100x faster** than pip
- **Automatic environment management** (no manual activation)
- **Reproducible** with lockfile support
- **Perfect for research** - ensures consistent package versions

---

## 2. Essential Documentation

### For Daily Use
- **`QUICK_START.md`** - Copy-paste templates for common tasks
- **`README.md`** - Comprehensive examples and API reference
- **`example.py`** - Working code you can run and modify
- **`notebooks/prs_gallery.py`** - Interactive documentation gallery (marimo)

### For Developers/Collaborators
- **`CLAUDE.md`** - Technical architecture and development guide
- **`PROJECT_SUMMARY.md`** - Complete project overview
- **`pyproject.toml`** - Package configuration and dependencies

### Interactive Documentation

View the comprehensive gallery notebook:

```bash
# Using uv (recommended)
uv run marimo edit notebooks/prs_gallery.py

# Run as read-only app
uv run marimo run notebooks/prs_gallery.py

# Or with traditional marimo
marimo edit notebooks/prs_gallery.py
```

The gallery demonstrates:
- All color palettes with visual swatches
- Progressive complexity examples (Ophelia approach)
- PRS compliance features
- Accessibility considerations
- Interactive code examples

---

## 3. Common Use Cases

### Use Case 1: Statistical Bar Chart

**When to use**: Comparing outcomes between groups, showing treatment efficacy

```python
from prs_dataviz import apply_prs_style, save_prs_figure, format_statistical_plot
import matplotlib.pyplot as plt

# Setup
apply_prs_style(cycle="clinical", show_grid=True)
fig, ax = plt.subplots(figsize=(5, 4))

# Your data
groups = ['Control', 'Treatment A', 'Treatment B']
values = [72, 85, 91]
ax.bar(groups, values, color=['#7FA8C9', '#2C5F87', '#5B8F7D'])
ax.set_ylabel('Patient Satisfaction Score (%)')
ax.set_ylim(0, 100)

# Format and save
format_statistical_plot(ax)
save_prs_figure(fig, "satisfaction_scores.tiff", dpi=300, width_inches=5.0, cmyk=True)
```

**Result**: `satisfaction_scores.tiff` ready for PRS submission

---

### Use Case 2: Before/After Patient Photos

**When to use**: Surgical outcome documentation, treatment comparisons

```python
from prs_dataviz import create_before_after_figure, save_prs_figure
from PIL import Image
import numpy as np

# Load images (IMPORTANT: Must be same size, lighting, position)
before_img = np.array(Image.open("patient_001_preop.jpg"))
after_img = np.array(Image.open("patient_001_6mo_postop.jpg"))

# Create comparison
fig, (ax_before, ax_after) = create_before_after_figure(
    before_img,
    after_img,
    labels=("Preoperative", "6 Months Postoperative"),
    title="Patient 001: Rhinoplasty Results"
)

# Save
save_prs_figure(fig, "patient_001_comparison.tiff", dpi=300, width_inches=7.0, cmyk=True)
```

**Result**: Professional before/after comparison validated for identical sizing

---

### Use Case 3: Multi-Panel Figure (Separate Files)

**When to use**: Multiple views (frontal/lateral/oblique), multi-part results

```python
from prs_dataviz import save_multi_panel_figure
import matplotlib.pyplot as plt

# Create each panel separately
fig_a, ax_a = plt.subplots(figsize=(3.5, 3.5))
# ... plot frontal view ...

fig_b, ax_b = plt.subplots(figsize=(3.5, 3.5))
# ... plot lateral view ...

fig_c, ax_c = plt.subplots(figsize=(3.5, 3.5))
# ... plot oblique view ...

# Save as separate files (PRS requirement)
saved_files = save_multi_panel_figure(
    {"a": fig_a, "b": fig_b, "c": fig_c},
    "Figure2",  # Base name
    dpi=300,
    width_inches=3.5,
    format="tiff"
)

# Results: Figure2a.tiff, Figure2b.tiff, Figure2c.tiff
for label, filepath in saved_files.items():
    print(f"✓ Saved: {filepath}")
```

**Result**: Three separate TIFF files ready for upload

---

### Use Case 4: Line Graph (Time Series)

**When to use**: Showing changes over time, recovery curves, follow-up data

```python
from prs_dataviz import apply_prs_style, save_prs_figure, prs_legend
import matplotlib.pyplot as plt

apply_prs_style(cycle="clinical")
fig, ax = plt.subplots(figsize=(5, 4))

# Time series data
months = [0, 1, 3, 6, 12]
treatment_scores = [55, 68, 78, 85, 88]
control_scores = [55, 60, 65, 68, 70]

ax.plot(months, treatment_scores, marker='o', linewidth=2, label='Treatment')
ax.plot(months, control_scores, marker='s', linewidth=2, label='Control')
ax.set_xlabel('Follow-up Time (months)')
ax.set_ylabel('Recovery Score')
ax.set_title('Treatment Efficacy Over Time', fontweight='bold')

# Professional legend
prs_legend(ax, outside=True)

save_prs_figure(fig, "recovery_timeline.tiff", dpi=300, width_inches=5.0, cmyk=True)
```

**Result**: Clean time-series visualization with legend

---

### Use Case 5: Box Plot Comparison

**When to use**: Showing distribution and variability, comparing multiple groups

```python
from prs_dataviz import apply_prs_style, save_prs_figure, CLINICAL_DATA
import matplotlib.pyplot as plt
import numpy as np

apply_prs_style(cycle="clinical")
fig, ax = plt.subplots(figsize=(5, 4))

# Generate sample data (replace with your real data)
group_a_data = np.random.normal(70, 10, 50)
group_b_data = np.random.normal(80, 8, 50)
group_c_data = np.random.normal(85, 12, 50)

bp = ax.boxplot(
    [group_a_data, group_b_data, group_c_data],
    labels=['Group A', 'Group B', 'Group C'],
    patch_artist=True,
    widths=0.6
)

# Color the boxes
colors = [CLINICAL_DATA["Primary"], CLINICAL_DATA["Secondary"], CLINICAL_DATA["Tertiary"]]
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_ylabel('Outcome Measurement (mm)')
ax.set_title('Treatment Group Comparison', fontweight='bold')

save_prs_figure(fig, "group_comparison.tiff", dpi=300, width_inches=5.0, cmyk=True)
```

**Result**: Professional box plot ready for publication

---

## 4. Pre-Submission Checklist

Before uploading figures to PRS, validate them:

```python
from prs_dataviz import validate_figure_file

# Check each figure
results = validate_figure_file("satisfaction_scores.tiff")

if results['valid']:
    print("✓ Figure ready for submission!")
    print(f"  DPI: {results['dpi']:.0f}")
    print(f"  Size: {results['width_inches']:.2f}\" × {results['height_inches']:.2f}\"")
    print(f"  Color: {results['color_mode']}")
else:
    print("✗ Issues found:")
    for issue in results['issues']:
        print(f"  - {issue}")
```

### Manual Checklist

- [ ] Figure is 300+ DPI
- [ ] File format is TIFF (preferred) or PNG/JPEG/PDF
- [ ] Width is 3.25" minimum (5" for graphs with text)
- [ ] Color mode is CMYK (for print)
- [ ] Multi-panel figures saved as separate files
- [ ] Before/after photos have identical size, lighting, position
- [ ] No blurring or eye blocks (patient consent obtained)
- [ ] Professional quality (good lighting, focus, clean background)
- [ ] Figure legend written separately in manuscript text
- [ ] Files named correctly (Figure1.tiff, Figure2a.tiff, etc.)

---

## 5. Color Palette Guide

### When to Use Each Palette

| Palette | Best For | Apply Style |
|---------|----------|-------------|
| **Clinical** | Statistical data, general medical figures | `apply_prs_style(cycle="clinical")` |
| **Comparison** | Before/after, treatment comparisons | `apply_prs_style(cycle="comparison")` |
| **Default** | Multi-category data, versatile use | `apply_prs_style(cycle="default")` |

### Manual Color Selection

```python
from prs_dataviz import CLINICAL_BLUE, TISSUE_TONE, STATISTICAL

# Clinical Blue colors
navy = CLINICAL_BLUE["Navy"]           # Professional, dark
steel = CLINICAL_BLUE["Steel Blue"]    # Mid-tone blue
sky = CLINICAL_BLUE["Sky Blue"]        # Light blue

# Statistical significance colors
sig = STATISTICAL["Significant"]                # p < 0.05
highly_sig = STATISTICAL["Highly Significant"]  # p < 0.01
ns = STATISTICAL["Non-Significant"]             # p ≥ 0.05

# Use in plots
ax.bar(['A', 'B', 'C'], [10, 15, 12], color=[navy, steel, sky])
```

---

## 6. Troubleshooting Common Issues

### Issue 1: "Figure rejected for low DPI"

**Symptom**: Journal rejects figure for insufficient resolution
**Solution**:
```python
# Always use dpi=300 or higher
save_prs_figure(fig, "figure.tiff", dpi=300)  # Correct
# NOT: plt.savefig("figure.png")  # Wrong - no DPI control
```

---

### Issue 2: "Figure too small"

**Symptom**: Figure doesn't meet minimum width requirements
**Solution**:
```python
# For graphs with text: minimum 5"
save_prs_figure(fig, "graph.tiff", width_inches=5.0)

# For simple photos: minimum 3.25"
save_prs_figure(fig, "photo.tiff", width_inches=3.5)
```

---

### Issue 3: "PNG doesn't accept CMYK"

**Symptom**: Warning about PNG not supporting CMYK
**Solution**:
```python
# Use TIFF format for CMYK output
save_prs_figure(fig, "figure.tiff", format="tiff", cmyk=True)  # Correct
# NOT: save_prs_figure(fig, "figure.png", cmyk=True)  # Wrong
```

---

### Issue 4: "Before/after images different sizes"

**Symptom**: ValueError when creating before/after figure
**Solution**:
```python
from PIL import Image

# Resize second image to match first
img1 = Image.open("before.jpg")
img2 = Image.open("after.jpg")

# Match sizes
img2_resized = img2.resize(img1.size, Image.Resampling.LANCZOS)
img2_resized.save("after_resized.jpg")

# Now they match
create_before_after_figure("before.jpg", "after_resized.jpg")
```

---

### Issue 5: "Colors look different in Word/PDF"

**Symptom**: Colors appear washed out or incorrect
**Solution**:
- This is normal - CMYK colors look different than RGB on screen
- Use `cmyk=True` for all journal submissions (print colors)
- View in professional image software (Photoshop, GIMP) to see true CMYK
- Journal will print correctly even if screen looks different

---

## 7. File Management Best Practices

### Naming Convention

Use PRS-standard naming:
```
Figure1.tiff
Figure2a.tiff
Figure2b.tiff
Figure3.tiff
Table1.tiff  (if tables as images)
Supplemental_Figure1.tiff
```

### Directory Structure (Recommended)

```
your_research_project/
├── data/                    # Raw data
├── analysis/               # Analysis scripts
├── figures/               # Generated figures
│   ├── drafts/           # Work-in-progress
│   ├── final/            # PRS-compliant finals
│   └── submission/       # Ready for upload
├── scripts/              # Your plotting scripts
│   ├── figure1_stats.py
│   ├── figure2_photos.py
│   └── figure3_timeline.py
└── manuscript/           # Manuscript files
```

### Version Control

Keep track of figure versions:
```python
# In your script, add version info
VERSION = "v3"  # Increment when making changes
OUTPUT_DIR = "figures/final/"

save_prs_figure(
    fig,
    f"{OUTPUT_DIR}Figure1_{VERSION}.tiff",
    dpi=300,
    width_inches=5.0
)
```

---

## 8. Integration with Research Workflow

### Step-by-Step Workflow

1. **Data Analysis**
   ```python
   # Analyze your data (pandas, numpy, etc.)
   import pandas as pd
   data = pd.read_csv("results.csv")
   # ... analysis ...
   ```

2. **Create Figure**
   ```python
   from prs_dataviz import apply_prs_style, save_prs_figure

   apply_prs_style(cycle="clinical")
   fig, ax = plt.subplots(figsize=(5, 4))
   # ... plotting ...
   ```

3. **Save PRS-Compliant**
   ```python
   save_prs_figure(fig, "figures/final/Figure1.tiff", dpi=300, width_inches=5.0, cmyk=True)
   ```

4. **Validate**
   ```python
   from prs_dataviz import validate_figure_file
   results = validate_figure_file("figures/final/Figure1.tiff")
   print(results)
   ```

5. **Write Legend**
   ```
   Figure 1. Patient satisfaction scores across treatment groups.
   Control group (n=30) shown in blue, Treatment A (n=28) in teal,
   Treatment B (n=32) in green. Error bars represent standard deviation.
   *p < 0.05, **p < 0.01.
   ```

6. **Upload to Journal System**
   - Upload each figure separately (not in Word)
   - Match filenames to figure callouts
   - Verify CMYK color mode on upload

---

## 9. Package Maintenance

### Updating Colors/Styles

To modify color palettes:

1. Open `src/prs_dataviz/palettes.py`
2. Edit color values (use CMYK-safe colors)
3. Test colorblind accessibility
4. Reinstall: `pip install -e . --force-reinstall`

### Adding New Features

To add new layout functions:

1. Open `src/prs_dataviz/layout.py`
2. Add your function following existing patterns
3. Export in `src/prs_dataviz/__init__.py`
4. Test thoroughly
5. Update documentation

### Reporting Issues

If you encounter bugs or have feature requests:

1. Document the issue with example code
2. Note expected vs actual behavior
3. Include figure samples if relevant
4. Contact: [Your contact info]

---

## 10. FAQ

### Q: Can I use this for other journals?

**A**: Yes! Most journals have similar requirements. You may need to adjust:
- DPI (some require 600+ for certain image types)
- File format preferences
- Color mode (some prefer RGB for online-only)

Just modify the parameters in `save_prs_figure()`.

---

### Q: What if my institution has brand colors?

**A**: The package supports institutional colors:

```python
# Future feature - brand color blending
from prs_dataviz import blend_with_brand, CLINICAL_DATA

institutional_blue = "#003366"  # Your institution's color
blended_colors = blend_with_brand(
    list(CLINICAL_DATA.values()),
    institutional_blue,
    blend_amount=0.2
)
```

---

### Q: Can I create figures in Jupyter notebooks?

**A**: Yes! The package works seamlessly in Jupyter:

```python
# In Jupyter cell
%matplotlib inline
from prs_dataviz import apply_prs_style, save_prs_figure
import matplotlib.pyplot as plt

apply_prs_style(cycle="clinical")
fig, ax = plt.subplots(figsize=(5, 4))
# ... plotting ...
plt.show()

# Save when ready
save_prs_figure(fig, "output/figure1.tiff", dpi=300, width_inches=5.0)
```

---

### Q: How do I handle large datasets?

**A**: The package handles large datasets efficiently:

```python
import numpy as np
import matplotlib.pyplot as plt
from prs_dataviz import apply_prs_style, save_prs_figure

apply_prs_style(cycle="clinical")

# Large dataset example
n_points = 10000
x = np.random.randn(n_points)
y = np.random.randn(n_points)

fig, ax = plt.subplots(figsize=(5, 4))
ax.scatter(x, y, s=1, alpha=0.5)  # Small points, transparency

save_prs_figure(fig, "large_scatter.tiff", dpi=300, width_inches=5.0)
```

---

### Q: Can collaborators use this without Python knowledge?

**A**: Collaborators can use saved templates:

1. Create a template script for them
2. Mark clearly where to input their data
3. Provide step-by-step instructions
4. Have them run: `python make_figure.py`

Example template provided in `templates/` directory.

---

## 11. Contact & Support

### Package Information
- **Version**: 0.1.0
- **Location**: `/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/`
- **License**: MIT
- **Author**: Moreen Njoroge

### Resources
- **PRS Guidelines**: https://journals.lww.com/plasreconsurg/pages/informationforauthors.aspx
- **Digital Artwork Guide**: http://links.lww.com/ES/A42
- **Cara Thompson's Methodology**: https://www.cararthompson.com/talks/on-brand-accessibility/
- **Python Documentation**: https://docs.python.org/3/
- **Matplotlib Documentation**: https://matplotlib.org/stable/contents.html

### Getting Help

1. **Check documentation first**: `README.md`, `QUICK_START.md`
2. **Run examples**: `python example.py`
3. **Test with sample data** before using real research data
4. **Validate figures** before submission
5. **Consult PRS guidelines** for journal-specific requirements

---

## 12. Handoff Checklist

### For Moreen (Package User)

- [ ] Package installed: `pip install -e .`
- [ ] Ran example.py successfully
- [ ] Read QUICK_START.md
- [ ] Understands color palette options
- [ ] Knows how to validate figures
- [ ] Has template scripts ready
- [ ] Bookmarked PRS guidelines
- [ ] Tested with sample data

### For Future Developers

- [ ] Reviewed CLAUDE.md (technical architecture)
- [ ] Understands package structure
- [ ] Knows how to add new features
- [ ] Can run tests: `pytest`
- [ ] Familiar with PRS requirements
- [ ] Understands CMYK color conversion
- [ ] Can modify palettes safely

### For Collaborators

- [ ] Received template scripts
- [ ] Knows where to find documentation
- [ ] Understands file naming conventions
- [ ] Can validate figures independently
- [ ] Knows PRS submission requirements
- [ ] Has contact for questions

---

## 13. Next Steps

### Immediate (This Week)
1. Install package: `pip install -e .`
2. Run examples: `python example.py`
3. Create first figure with real data
4. Validate output
5. Get familiar with color palettes

### Short-Term (This Month)
1. Create figures for current manuscript
2. Validate all figures before submission
3. Customize scripts for your specific needs
4. Build library of reusable templates

### Long-Term (Ongoing)
1. Share with lab colleagues
2. Contribute improvements
3. Report issues/requests
4. Keep package updated
5. Maintain figure archive

---

## Appendix A: Complete API Reference

### Style Functions

```python
apply_prs_style(
    cycle="default",           # or "clinical", "comparison"
    font_family="DejaVu Sans",
    font_size=10,
    show_grid=False,
    show_spines=True
)

format_statistical_plot(ax, show_significance=True)
format_comparison_plot(ax, comparison_type="before_after")
add_scale_bar(ax, length, label, location="lower right")
prs_legend(ax, outside=False)
```

### Export Functions

```python
save_prs_figure(
    fig,
    filename,
    dpi=300,
    width_inches=5.0,
    format=None,          # Auto-detected from filename
    cmyk=True,
    validate=True
)

save_multi_panel_figure(
    figures,              # Dict: {"a": fig_a, "b": fig_b}
    base_filename,
    dpi=300,
    width_inches=3.5,
    format="tiff"
)

validate_figure_file(
    filename,
    min_dpi=300,
    min_width_inches=3.25
)
```

### Layout Functions

```python
create_before_after_figure(
    before_image,        # ndarray or path
    after_image,
    labels=("Before", "After"),
    figsize=None,
    title=None
)

create_multi_view_figure(
    images,             # Dict: {"frontal": img1, "lateral": img2}
    layout="row",       # or "column", "grid"
    labels=None,
    figsize=None,
    title=None
)

create_time_series_figure(
    images,             # Dict: {"preop": img1, "6mo": img2}
    time_labels=None,
    figsize=None,
    title=None,
    show_timeline=True
)

create_results_panel(
    plot_data,          # Dict of panel configurations
    layout="1x2",       # or "2x1", "2x2"
    figsize=None,
    title=None
)
```

---

## Appendix B: PRS Requirements Summary

### File Requirements
- **Resolution**: Minimum 300 DPI
- **Color Mode**: CMYK for print
- **Formats**: TIFF (preferred), PNG, JPEG, PDF, EPS
- **Dimensions**: 3.25" minimum (photos), 5.0" minimum (graphs with text)

### Multi-Panel Requirements
- Save each panel as separate file
- Label as Figure1a.tiff, Figure1b.tiff, etc.
- No composite images with superimposed letters

### Photo Requirements
- Before/after: identical size, position, lighting
- No blurring or eye blocks (consent required)
- Professional quality (good lighting, focus, clean background)
- Minimal modification (light cropping only)

### Submission Requirements
- Upload figures separately (not embedded in Word)
- Filename matches figure callouts in manuscript
- Legends in manuscript text (not on images)
- Scale bars preferred over magnification text

---

**Document Version**: 1.0
**Last Updated**: November 14, 2025
**Status**: Ready for Use

---

✅ **Package is fully functional and ready for PRS submissions!**
