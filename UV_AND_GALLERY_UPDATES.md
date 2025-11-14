# UV Integration & Interactive Gallery Updates

**Date**: November 14, 2025
**Updates**: UV package management + Interactive documentation gallery

---

## Summary of Changes

### 1. UV Package Management Integration

Both projects now emphasize using [uv](https://github.com/astral-sh/uv) for Python package management and script execution.

#### Files Updated

**dubois-style project:**
- ✅ `/Users/shakes/DevProjects/dubois-style/CLAUDE.md`

**prs-dataviz project:**
- ✅ `/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/CLAUDE.md`
- ✅ `/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/HANDOFF_DOCUMENT.md`

#### Why UV?

**Performance Benefits:**
- **10-100x faster** than pip for package installation
- Faster resolution algorithm
- Parallel downloads

**Workflow Benefits:**
- **Automatic virtual environment management** - No manual activation needed
- **Script dependencies** - PEP 723 inline metadata support
- **Reproducible builds** - Lockfile support (uv.lock)
- **No configuration** - Just prefix commands with `uv run`

**Research Benefits:**
- **Perfect for medical research** - Ensures reproducible analysis environments
- **Consistent package versions** across collaborators
- **Easy sharing** - Just share pyproject.toml and uv.lock

### 2. Interactive Documentation Gallery

Created comprehensive marimo notebook following the Ophelia approach:

**Location**: `/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/notebooks/prs_gallery.py`

#### Features

**Design Principles:**
- ✅ **Du Bois aesthetic** - Rich, earthy color palettes
- ✅ **Ophelia approach** - Progressive complexity, visual swatches, consistent examples
- ✅ **PRS compliance** - Automatic enforcement of journal requirements

**Content Sections:**

1. **Introduction** - Package overview, design principles, why it matters
2. **Color Palettes** - Visual swatches for all 5 palettes with use cases
3. **Interactive Examples** - Progressive complexity:
   - Basic statistical bar chart
   - Line graph with confidence intervals
   - Before/after comparison
   - Box plot distribution
4. **PRS Compliance** - Feature matrix, code examples
5. **Accessibility** - Cara Thompson's 10-step methodology
6. **Package Usage** - Installation, quick start, examples
7. **Resources** - Documentation links, references, credits

**Ophelia-Inspired Elements:**

- **Visual swatches** - Each palette shown with hex codes
- **Progressive examples** - Simple → Complex
- **Consistent dataset approach** - Mock medical data for reproducibility
- **Code-before-output** - Examples show code then visualization
- **Semantic color usage** - Purpose-built for medical contexts
- **Typography standards** - Professional medical aesthetics

---

## Usage Guide

### Installing UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Using UV with Projects

#### dubois-style Project

```bash
cd /Users/shakes/DevProjects/dubois-style

# Install dependencies
uv sync

# Run example
uv run python example.py

# Edit gallery
uv run marimo edit notebooks/gallery.py

# Export gallery
uv run marimo export html-wasm notebooks/gallery.py -o site --mode run
```

#### prs-dataviz Project

```bash
cd /Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system

# Install package
uv pip install -e .

# Run examples
uv run python example.py

# View interactive gallery
uv run marimo edit notebooks/prs_gallery.py

# Run as app (read-only)
uv run marimo run notebooks/prs_gallery.py
```

### Running Individual Scripts

UV can run standalone Python scripts without project installation:

```bash
# Run a script (uv manages dependencies automatically)
uv run python my_script.py

# Run with inline dependencies (PEP 723)
# Script header example:
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib>=3.7",
#     "numpy>=1.24",
# ]
# ///

uv run my_script.py
```

---

## Interactive Gallery Guide

### Viewing the Gallery

```bash
cd /Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system

# Edit mode (interactive, can modify)
uv run marimo edit notebooks/prs_gallery.py

# App mode (read-only, optimized for viewing)
uv run marimo run notebooks/prs_gallery.py

# Export to static HTML
uv run marimo export html-wasm notebooks/prs_gallery.py -o gallery_export --mode run
```

### Gallery Structure

**Progressive Complexity (Ophelia Approach):**

1. **Start Simple**: Color palette swatches
   - Visual representation of all palettes
   - Hex codes visible
   - Use case descriptions

2. **Basic Examples**: Statistical bar chart
   - Standard medical research visualization
   - PRS-compliant styling
   - Clear annotations

3. **Build Sophistication**: Line graphs, scatter plots
   - Confidence intervals
   - Multiple series
   - Professional styling

4. **Advanced Layouts**: Before/after comparisons
   - Size validation
   - Consistent styling
   - Medical contexts

5. **Distribution Visualization**: Box plots
   - Statistical comparisons
   - Group variability
   - Significance indicators

**Interactive Features:**

- **Live code cells** - Modify and see results
- **Visual outputs** - All figures rendered inline
- **Progressive disclosure** - Information revealed as needed
- **Consistent styling** - Du Bois + Clinical aesthetics
- **WASM export** - Can run entirely in browser (client-side)

### Sharing the Gallery

**Option 1: Share Marimo File**
```bash
# Just share the .py file
# Others can run with:
uv run marimo edit notebooks/prs_gallery.py
```

**Option 2: Export to HTML**
```bash
# Create standalone HTML file
uv run marimo export html-wasm notebooks/prs_gallery.py -o gallery.html --mode run

# Share gallery.html - runs in any browser, no server needed
```

**Option 3: Host on GitHub Pages**
```bash
# Export to directory
uv run marimo export html-wasm notebooks/prs_gallery.py -o _site --mode run

# Push to gh-pages branch or configure GitHub Pages
# Example: https://yourname.github.io/prs-dataviz/
```

---

## Comparison: pip vs uv

| Feature | pip | uv |
|---------|-----|-----|
| Installation speed | Baseline | **10-100x faster** |
| Dependency resolution | Slow, greedy | **Fast, parallel** |
| Virtual env management | Manual | **Automatic** |
| Script execution | Need activation | **`uv run` - instant** |
| Lockfiles | pip-tools needed | **Built-in** |
| PEP 723 support | No | **Yes** |
| Caching | Basic | **Advanced** |
| Best for | Traditional | **Modern workflows** |

**Recommendation**: Use `uv` for all new work. It's backward compatible with pip but significantly faster.

---

## Design System Credits

### Du Bois Aesthetic
- **Inspiration**: W.E.B. Du Bois' 1900 Paris Exposition visualizations
- **Colors**: Rich, earthy tones (warm tans, dusty pinks, ochres, deep greens)
- **Philosophy**: Historical excellence in data visualization

### Ophelia Approach
- **Author**: Cara Thompson
- **URL**: https://cararthompson.github.io/ophelia/
- **Key Elements**:
  - Anchor colors with semantic meaning
  - Progressive complexity in examples
  - Visual color swatches
  - Typography standards
  - Layered accessibility documentation

### Cara Thompson's 10-Step Process
- **Talk**: [On-Brand Accessibility](https://www.cararthompson.com/talks/on-brand-accessibility/)
- **Package**: [monochromeR](https://github.com/cararthompson/monochromeR)
- **Steps**:
  1. Choose intuitive colors
  2. Check colorblind-friendly
  3. Blend brand colors
  4. Mute colors (neurodivergent-friendly)
  5. Check contrast (WCAG 2.1)
  6. Typography
  7. Spacing
  8. Backgrounds
  9. Titles & annotations
  10. Complete system

### PRS Guidelines
- **Journal**: Plastic and Reconstructive Surgery
- **URL**: https://journals.lww.com/plasreconsurg/
- **Requirements**: 300 DPI, CMYK, proper sizing, professional quality

---

## File Summary

### New Files Created

```
moreen_njoroge_dataviz_design_system/
├── notebooks/
│   ├── __init__.py
│   └── prs_gallery.py           ← NEW: Interactive documentation
└── UV_AND_GALLERY_UPDATES.md    ← NEW: This document
```

### Files Updated

```
dubois-style/
└── CLAUDE.md                     ← UPDATED: UV usage added

moreen_njoroge_dataviz_design_system/
├── CLAUDE.md                     ← UPDATED: UV usage added
└── HANDOFF_DOCUMENT.md          ← UPDATED: UV + gallery info added
```

---

## Quick Reference Commands

### UV Commands

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install package
uv pip install -e .

# Sync dependencies
uv sync

# Run script
uv run python script.py

# Run marimo
uv run marimo edit notebook.py
```

### Gallery Commands

```bash
# Edit gallery (interactive)
uv run marimo edit notebooks/prs_gallery.py

# View gallery (read-only)
uv run marimo run notebooks/prs_gallery.py

# Export to HTML
uv run marimo export html-wasm notebooks/prs_gallery.py -o gallery.html --mode run
```

### Validation Commands

```bash
# Validate figure
uv run python -c "from prs_dataviz import validate_figure_file; print(validate_figure_file('figure.tiff'))"

# Run examples
uv run python example.py

# Run tests
uv run pytest
```

---

## Migration Guide

### For Existing Users (Moving from pip to uv)

1. **Install uv**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **No changes to code needed** - Just prefix commands:
   ```bash
   # Before (pip)
   python example.py

   # After (uv)
   uv run python example.py
   ```

3. **Benefits start immediately**:
   - Faster package installation
   - No virtual environment activation
   - Reproducible builds

4. **Optional: Create lockfile**:
   ```bash
   uv sync  # Creates uv.lock
   ```

5. **Share with collaborators**:
   ```bash
   # They just need:
   uv sync   # Installs exact versions from uv.lock
   ```

### For New Users

Just use `uv run` for everything:

```bash
# Install package
uv pip install -e .

# Run anything
uv run python example.py
uv run marimo edit notebooks/prs_gallery.py
uv run pytest
```

No virtual environment management needed!

---

## Next Steps

### For Moreen (Package User)

1. **Install uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. **View gallery**: `uv run marimo edit notebooks/prs_gallery.py`
3. **Create figures**: Use examples from gallery
4. **Share with collaborators**: Send them `prs_gallery.py`

### For Collaborators

1. **Install uv**: One-time setup
2. **Clone/download project**: Get the code
3. **Run**: `uv run marimo edit notebooks/prs_gallery.py`
4. **Learn**: Interactive examples in gallery

### For Developers

1. **Use uv for all commands**: Faster, simpler
2. **Update gallery**: Add new examples to `prs_gallery.py`
3. **Export to HTML**: Share with non-technical users
4. **Deploy**: GitHub Pages for public access

---

## FAQ

**Q: Do I have to use uv?**
A: No, but it's strongly recommended. All commands work with traditional pip/python too.

**Q: Will uv break my existing setup?**
A: No, uv is completely separate from pip. They can coexist.

**Q: Can I share figures created with the gallery?**
A: Yes! The gallery is for learning. Export your code to standalone scripts for production.

**Q: How do I export the gallery for non-Python users?**
A: Use `uv run marimo export html-wasm` to create a standalone HTML file that runs in any browser.

**Q: Does the gallery work offline?**
A: Yes, once exported to HTML-WASM, it runs entirely client-side with no server needed.

---

**Status**: ✅ Complete and Ready to Use

**Package Version**: 0.1.0
**UV Version**: Latest (installed via script)
**Marimo Version**: 0.17.7+

---

For questions or issues, refer to:
- **CLAUDE.md** - Technical details
- **HANDOFF_DOCUMENT.md** - Complete usage guide
- **QUICK_START.md** - Quick templates
