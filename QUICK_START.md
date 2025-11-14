# Quick Start Guide - PRS DataViz

**For: Moreen Njoroge**
**Purpose: Creating PRS journal-compliant figures**

## Installation (One Time)

```bash
cd /Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system
pip install -e .
```

## Basic Template (Copy & Modify)

```python
from prs_dataviz import apply_prs_style, save_prs_figure
import matplotlib.pyplot as plt
import numpy as np

# 1. Apply PRS styling
apply_prs_style(cycle="clinical", show_grid=True)

# 2. Create your figure
fig, ax = plt.subplots(figsize=(5, 4))
# ... your plotting code here ...

# 3. Save in PRS format
save_prs_figure(
    fig,
    "figure1.tiff",      # Filename
    dpi=300,             # Required minimum
    width_inches=5.0,    # 5" for graphs, 3.25" for photos
    cmyk=True            # Required for print
)
```

## Common Scenarios

### Statistical Bar Chart

```python
from prs_dataviz import apply_prs_style, save_prs_figure, format_statistical_plot

apply_prs_style(cycle="clinical", show_grid=True)
fig, ax = plt.subplots(figsize=(5, 4))

# Your data
groups = ['Group A', 'Group B', 'Group C']
values = [75, 82, 88]
ax.bar(groups, values)
ax.set_ylabel('Outcome Score (%)')

# Format & save
format_statistical_plot(ax)
save_prs_figure(fig, "results.tiff", dpi=300, width_inches=5.0)
```

### Before/After Patient Photos

```python
from prs_dataviz import create_before_after_figure, save_prs_figure
from PIL import Image
import numpy as np

# Load photos (must be same size!)
before = np.array(Image.open("before.jpg"))
after = np.array(Image.open("after.jpg"))

# Create comparison
fig, (ax1, ax2) = create_before_after_figure(
    before, after,
    labels=("Preoperative", "6 Months Post-op")
)

# Save
save_prs_figure(fig, "patient_comparison.tiff", dpi=300, width_inches=7.0)
```

### Line Graph with Multiple Series

```python
from prs_dataviz import apply_prs_style, save_prs_figure, prs_legend

apply_prs_style(cycle="clinical")
fig, ax = plt.subplots(figsize=(5, 4))

# Your data
time = [0, 1, 3, 6, 12]  # months
group1 = [50, 60, 70, 80, 85]
group2 = [50, 55, 60, 65, 70]

ax.plot(time, group1, marker='o', label='Treatment')
ax.plot(time, group2, marker='s', label='Control')
ax.set_xlabel('Time (months)')
ax.set_ylabel('Recovery Score')

# Add legend
prs_legend(ax, outside=True)

save_prs_figure(fig, "recovery_curve.tiff", dpi=300, width_inches=5.0)
```

## Check Figure Before Submission

```python
from prs_dataviz import validate_figure_file

results = validate_figure_file("figure1.tiff")

if results['valid']:
    print("✓ Ready for submission!")
else:
    print("✗ Fix these issues:")
    for issue in results['issues']:
        print(f"  - {issue}")
```

## Important PRS Requirements

### ✅ Always Do
- Use `save_prs_figure()` with `dpi=300`, `cmyk=True`
- Width: 5" for graphs, 3.25" for simple photos
- Format: TIFF preferred (best for CMYK)
- Save multi-panel as separate files (Figure1a, Figure1b)
- Before/after: identical size, lighting, position

### ❌ Never Do
- Copy figures into Word (upload separately)
- Use images below 300 DPI
- Blur patient faces (get consent instead)
- Substantially modify photos
- Use grayscale bar charts (use color)

## Color Palette Cheat Sheet

```python
from prs_dataviz import apply_prs_style

# For statistical data (most common)
apply_prs_style(cycle="clinical")

# For before/after comparisons
apply_prs_style(cycle="comparison")

# Default (versatile)
apply_prs_style(cycle="default")
```

## File Size Guide

| Figure Type | Minimum Width | Typical DPI | Example |
|-------------|---------------|-------------|---------|
| Patient photo | 3.25" | 300 | Before/after |
| Graph with text | 5.0" | 300 | Bar chart |
| Microscopy | 3.25" | 300-600 | Histology |
| Multi-panel | 7.0" total | 300 | 3 views |

## Common Errors & Solutions

### Error: "DPI too low"
```python
# Solution: Set dpi=300 or higher
save_prs_figure(fig, "figure.tiff", dpi=300)
```

### Error: "Width too small"
```python
# Solution: Use width_inches=5.0 for graphs
save_prs_figure(fig, "figure.tiff", width_inches=5.0)
```

### Error: "Images not same size" (before/after)
```python
# Solution: Resize one image to match the other
from PIL import Image
img2 = img2.resize(img1.size)
```

### Warning: "PNG doesn't support CMYK"
```python
# Solution: Use TIFF format for CMYK
save_prs_figure(fig, "figure.tiff", format="tiff", cmyk=True)
```

## Workflow Checklist

- [ ] Create figure with matplotlib
- [ ] Apply PRS style (`apply_prs_style()`)
- [ ] Save with `save_prs_figure()` (dpi=300, cmyk=True)
- [ ] Validate with `validate_figure_file()`
- [ ] Check file size (width in inches)
- [ ] Verify CMYK color mode
- [ ] Write figure legend (separate in manuscript)
- [ ] Upload to journal system (not in Word doc)

## Getting Help

1. **Examples**: Run `python example.py` to see working code
2. **Documentation**: See `README.md` for detailed examples
3. **PRS Guidelines**: https://journals.lww.com/plasreconsurg/

## Contact

Package created for Moreen Njoroge (Plastic Surgery Researcher)
Installation location: `/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system`

---

**Pro Tip**: Save this template in your research folder and modify it for each new figure!
