# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`prs-dataviz` is a professional data visualization design system for creating publication-quality figures that meet Plastic and Reconstructive Surgery (PRS) journal submission requirements.

**Purpose**: Help medical researchers (specifically plastic surgery researchers) create figures that comply with strict PRS journal guidelines while maintaining accessibility and professional quality.

## Development Commands

### Package Management with uv

**Important**: This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management and script execution.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install package with uv
uv pip install -e .

# With development dependencies
uv pip install -e ".[dev]"

# With documentation dependencies
uv pip install -e ".[docs]"

# Sync all dependencies from pyproject.toml
uv sync
```

### Running Scripts with uv

```bash
# Run Python scripts directly (uv manages environment automatically)
uv run python example.py

# Run validation
uv run python -c "from prs_dataviz import validate_figure_file; print(validate_figure_file('example_figure1.tiff'))"

# Run marimo documentation notebook
uv run marimo edit notebooks/prs_gallery.py
```

### Testing

```bash
# Run example script
uv run python example.py

# Run pytest
uv run pytest

# Validate example figures
uv run python -c "from prs_dataviz import validate_figure_file; print(validate_figure_file('example_figure1.tiff'))"
```

### Code Quality

```bash
# Format code
uv run black src/

# Lint
uv run ruff check src/
```

### Why uv?

- **10-100x faster** than pip for package installation
- **Automatic virtual environment** management
- **Reproducible builds** with lockfile support
- **Script dependencies** via PEP 723 inline metadata
- **No activation needed** - `uv run` handles everything
- **Perfect for medical research** - ensures reproducible analysis environments

## Architecture

### Package Structure

```
src/prs_dataviz/
├── __init__.py       # Public API exports
├── palettes.py       # CMYK-safe color palettes
├── style.py          # Matplotlib rcParams styling
├── export.py         # PRS-compliant figure export (300+ DPI, CMYK)
└── layout.py         # Before/after and multi-panel layouts
```

### Core Modules

#### `palettes.py`

Defines professional, CMYK-safe color palettes for medical visualization:

- **Color Families**: Clinical Blue, Tissue Tone, Clinical Data, Comparison, Statistical
- **CMYK Utilities**: `rgb_to_cmyk()`, `cmyk_to_rgb()` for print-ready colors
- **Pre-defined Cycles**:
  - `PRS_DEFAULT_CYCLE`: General categorical data (7 colors)
  - `PRS_CLINICAL_CYCLE`: Muted clinical data (5 colors)
  - `PRS_COMPARISON_CYCLE`: Before/after comparisons (2 colors)

**Design Principles**:
- All colors tested for CMYK printability
- Colorblind-friendly (deuteranopia, protanopia, tritanopia)
- WCAG 2.1 accessible contrast ratios
- Professional, muted tones for medical contexts

#### `style.py`

Matplotlib styling functions:

- **`apply_prs_style()`**: Apply PRS-compliant global styling
  - Clean, professional aesthetics
  - Configurable color cycles (default, clinical, comparison)
  - Professional fonts (DejaVu Sans default)
  - Optional grid/spines control

- **`format_statistical_plot()`**: Format plots for statistical data
- **`format_comparison_plot()`**: Format before/after comparisons
- **`add_scale_bar()`**: Add scale bars to medical images (PRS prefers scale bars over magnification text)
- **`prs_legend()`**: Create professional legends

#### `export.py`

PRS-compliant figure export:

- **`save_prs_figure()`**: Save figures meeting PRS requirements
  - Minimum 300 DPI
  - CMYK color mode conversion
  - Proper dimensions (3.25" or 5" minimum width)
  - Supported formats: TIFF, PNG, JPEG, PDF, EPS
  - Automatic validation

- **`save_multi_panel_figure()`**: Save multi-panel figures as separate files
  - PRS requires Figure 1a, 1b, 1c as separate files (not composite)

- **`validate_figure_file()`**: Check existing figures for PRS compliance
  - Returns detailed validation report with DPI, dimensions, color mode, issues

**Key Requirements**:
- PRS_MIN_DPI = 300
- PRS_MIN_WIDTH_SINGLE = 3.25 inches (patient photos)
- PRS_MIN_WIDTH_GRAPH = 5.0 inches (graphs with text)
- PRS_COLOR_MODE = "CMYK" (for print)

#### `layout.py`

Specialized layouts for medical research:

- **`create_before_after_figure()`**: Side-by-side before/after comparisons
  - Validates images are identical size (PRS requirement)
  - Consistent labeling

- **`create_multi_view_figure()`**: Multiple views (frontal, lateral, oblique)
  - Flexible layouts: row, column, grid

- **`create_time_series_figure()`**: Healing progression/follow-up
  - Timeline visualization option
  - Consistent sizing across time points

- **`create_results_panel()`**: Multi-panel statistical results
  - Flexible grid layouts (1x2, 2x1, 2x2, etc.)
  - Panel labeling (A, B, C, etc.)

## PRS Journal Requirements

### Critical Compliance Points

From [PRS Author Guidelines](https://journals.lww.com/plasreconsurg/pages/informationforauthors.aspx):

**✅ Required:**
1. **Minimum 300 DPI** resolution
2. **CMYK color mode** for all figures (print-ready)
3. **Minimum dimensions**:
   - 3.25" width for single images/photos
   - 5.0" width for graphs or images with text
4. **Supported formats**: TIFF (preferred), PNG, JPEG, PDF, EPS
5. **Multi-panel figures**: Save as separate files (Figure1a.tiff, Figure1b.tiff)
6. **Before/after photos**: Identical size, position, lighting
7. **Professional quality**: Clean, well-lit, properly focused
8. **Scale bars**: Use scale bars instead of magnification text for microscopy
9. **No modifications**: Only light cropping allowed
10. **Separate legends**: Figure legends in manuscript text, not on images

**❌ Not Accepted:**
- Images below 300 DPI
- Images copied into Word documents
- Blurred patient photos (must obtain consent)
- Substantively modified photographs
- Bar graphs in grayscale (use color)
- Eye blocks to obscure identity (not allowed; use consent)

## Design System Methodology

Implements [Cara Thompson's 10-step process](https://www.cararthompson.com/talks/on-brand-accessibility/) for accessible dataviz:

1. ✅ **Choose Intuitive Colours** - Perceptually-spaced palettes
2. ✅ **Check Colorblind-Friendly** - All palettes tested
3. ✅ **Blend Brand Colors** - Institutional color support (future)
4. ✅ **Mute Colors** - Reduced saturation for neurodivergent audiences
5. ✅ **Check Contrast** - WCAG 2.1 compliant (4.5:1 text, 3:1 UI)
6. ✅ **Typography** - Professional, readable defaults
7. ✅ **Spacing** - Dyslexia-friendly spacing
8. ✅ **Backgrounds** - Subtle, professional backgrounds
9. ✅ **Titles & Annotations** - Clear hierarchical text
10. ✅ **Complete System** - Comprehensive, cohesive design

### Attribution

Always credit Cara Thompson when discussing the design system:
- Link: https://www.cararthompson.com/talks/on-brand-accessibility/
- Reference: monochromeR package (R implementation)

## Common Workflows

### Creating a New Color Palette

1. Define colors in `palettes.py` with CMYK values
2. Test for colorblind accessibility
3. Verify WCAG contrast ratios
4. Add to appropriate cycle
5. Export via `__init__.py`
6. Document in README

### Adding a New Layout Function

1. Implement in `layout.py`
2. Follow PRS requirements (consistent sizing, labeling)
3. Add comprehensive docstring with examples
4. Handle both image arrays and file paths
5. Export via `__init__.py`
6. Add example to `example.py`

### Validating PRS Compliance

When adding new export features:
1. Check against PRS requirements in `export.py`
2. Validate DPI >= 300
3. Validate dimensions meet minimum
4. Verify CMYK conversion works
5. Test with `validate_figure_file()`

## Important Patterns

### CMYK Color Conversion

```python
# Always convert to CMYK for final figures
from prs_dataviz import save_prs_figure

save_prs_figure(fig, "figure1.tiff", dpi=300, cmyk=True)
```

### Before/After Consistency

```python
# PRS requires identical sizing
from prs_dataviz import create_before_after_figure

# This validates images are same size
fig, (ax1, ax2) = create_before_after_figure(before_img, after_img)
```

### Multi-Panel Export

```python
# PRS requires separate files for panels
from prs_dataviz import save_multi_panel_figure

save_multi_panel_figure(
    {"a": fig_a, "b": fig_b},
    "Figure1",  # Creates Figure1a.tiff, Figure1b.tiff
    dpi=300
)
```

## Dependencies

Core:
- `matplotlib>=3.7` - Plotting
- `numpy>=1.24` - Array operations
- `pillow>=10.0` - Image processing and CMYK conversion
- `colorspacious>=1.1.2` - Colorspace conversions (optional)
- `marimo>=0.17.7` - Interactive notebooks

Dev:
- `pytest>=7.0` - Testing
- `black>=23.0` - Code formatting
- `ruff>=0.1.0` - Linting

## File Conventions

- Source code: `src/prs_dataviz/`
- Examples: `example.py`
- Tests: `tests/` (pytest)
- Documentation: `README.md`, `CLAUDE.md`
- Notebooks: `notebooks/` (marimo format)

## Special Considerations

### CMYK vs RGB

- **Display (screen)**: RGB
- **Print (journal)**: CMYK
- PIL Image: Use `.convert('CMYK')` for print-ready
- PNG does not support CMYK natively → use TIFF for CMYK output
- JPEG supports CMYK but with quality loss

### Image Resolution

- **Screen**: 100-150 DPI sufficient
- **Print**: 300 DPI minimum (PRS requirement)
- **High-quality**: 600 DPI for images with text overlays
- Use `save_prs_figure(dpi=300)` for all journal submissions

### Medical Image Ethics

- Always obtain patient consent for identifiable photos
- No blurring or eye blocks allowed by PRS
- Only light cropping permitted
- Before/after must be identical in size, position, lighting
- Professional quality required (no messy backgrounds, proper lighting)

### Accessibility

- All palettes tested for colorblind viewers
- Contrast ratios meet WCAG 2.1 (4.5:1 text, 3:1 UI)
- Muted colors reduce cognitive load
- Professional typography for readability

## Testing Strategy

When adding new features, test:
1. **CMYK conversion**: Verify colors look correct in CMYK
2. **DPI validation**: Check files meet 300 DPI minimum
3. **Dimension validation**: Verify minimum widths (3.25" or 5")
4. **Format support**: Test TIFF, PNG, JPEG, PDF, EPS
5. **Multi-panel export**: Verify separate files created correctly
6. **Validation function**: Ensure `validate_figure_file()` catches issues

## Future Enhancements

Potential improvements:
- [ ] Interactive figure builder (marimo notebook)
- [ ] Batch figure validation CLI tool
- [ ] Institutional brand color blending
- [ ] Automated figure numbering/labeling
- [ ] Before/after alignment checker
- [ ] Figure quality scorer
- [ ] Export to PRS-specific templates

## Support Resources

- **PRS Guidelines**: https://journals.lww.com/plasreconsurg/pages/informationforauthors.aspx
- **Digital Artwork Guidelines**: http://links.lww.com/ES/A42
- **Cara Thompson's Methodology**: https://www.cararthompson.com/talks/on-brand-accessibility/
- **WCAG 2.1**: https://www.w3.org/WAI/WCAG21/quickref/

## Notes for Claude

- **Primary user**: Plastic surgery researcher (Moreen Njoroge)
- **Context**: Creating figures for journal submission, not general dataviz
- **Critical**: PRS compliance is non-negotiable (300 DPI, CMYK, dimensions)
- **Accessibility**: Always maintain Cara Thompson's methodology
- **Professional quality**: Medical/surgical context requires highest standards
- **No modifications**: Respect PRS guidelines on photo modification
