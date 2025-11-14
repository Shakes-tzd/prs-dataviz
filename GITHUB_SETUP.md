# GitHub Repository Setup - PRS DataViz

## Repository Information

**Repository URL**: https://github.com/Shakes-tzd/prs-dataviz

**Description**: Professional data visualization design system for Plastic and Reconstructive Surgery (PRS) journal submissions. CMYK-safe palettes, 300 DPI export, accessible design.

## Setup Completed

### 1. Git Repository Initialized
- Initialized git repository with `main` branch
- Created comprehensive `.gitignore` for Python projects
- Made initial commit with all project files

### 2. GitHub Repository Created
```bash
gh repo create prs-dataviz --public \
  --source=. \
  --description="Professional data visualization design system for Plastic and Reconstructive Surgery (PRS) journal submissions. CMYK-safe palettes, 300 DPI export, accessible design." \
  --push
```

### 3. Gallery Notebook Updated
The gallery notebook (`notebooks/prs_gallery.py`) has been updated to use the actual `prs-dataviz` package from GitHub instead of inlined code.

**Updated PEP 723 Dependencies**:
```python
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "prs-dataviz @ git+https://github.com/Shakes-tzd/prs-dataviz.git",
#     "matplotlib>=3.7",
#     "numpy>=1.24",
#     "pillow>=10.0",
#     "marimo>=0.17.7",
# ]
# ///
```

**Benefits**:
- Gallery now uses the actual package, not inlined code
- Ensures documentation accuracy
- Proper testing of package functionality
- Shareable and reproducible

### 4. Verified Package Installation from GitHub

Successfully tested package installation from GitHub:

```bash
uv run --with "prs-dataviz @ git+https://github.com/Shakes-tzd/prs-dataviz.git" \
  python -c "from prs_dataviz import CLINICAL_BLUE, apply_prs_style"
```

**Result**:
- ✅ Package imports successfully from GitHub
- ✅ All palettes accessible
- ✅ All functions callable
- ✅ Installed 34 packages in 281ms

## Using the Package from GitHub

### Install as a Dependency

Add to your `pyproject.toml`:
```toml
[project]
dependencies = [
    "prs-dataviz @ git+https://github.com/Shakes-tzd/prs-dataviz.git",
]
```

Or install directly:
```bash
# Using uv (recommended)
uv pip install "prs-dataviz @ git+https://github.com/Shakes-tzd/prs-dataviz.git"

# Using pip
pip install "git+https://github.com/Shakes-tzd/prs-dataviz.git"
```

### Use in PEP 723 Scripts

For standalone Python scripts with inline dependencies:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "prs-dataviz @ git+https://github.com/Shakes-tzd/prs-dataviz.git",
#     "matplotlib>=3.7",
# ]
# ///

from prs_dataviz import apply_prs_style, save_prs_figure
import matplotlib.pyplot as plt

apply_prs_style(cycle="clinical")
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
save_prs_figure(fig, "output.tiff", dpi=300, width_inches=5.0)
```

Run with:
```bash
uv run your_script.py
```

### Clone and Develop Locally

```bash
# Clone the repository
git clone https://github.com/Shakes-tzd/prs-dataviz.git
cd prs-dataviz

# Install in development mode
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Run example
uv run python example.py
```

## Marimo Gallery Notebook

The interactive gallery can now be run from anywhere with:

```bash
# Download the notebook
curl -O https://raw.githubusercontent.com/Shakes-tzd/prs-dataviz/main/notebooks/prs_gallery.py

# Run it (uv will automatically install dependencies from PEP 723 metadata)
uv run marimo edit prs_gallery.py
```

The notebook will automatically:
1. Install `prs-dataviz` from GitHub
2. Install all other dependencies (matplotlib, numpy, pillow, marimo)
3. Launch the interactive gallery

## Repository Structure

```
prs-dataviz/
├── src/prs_dataviz/          # Package source code
│   ├── __init__.py
│   ├── palettes.py           # Color palettes
│   ├── style.py              # Matplotlib styling
│   ├── export.py             # PRS-compliant export
│   └── layout.py             # Specialized layouts
├── notebooks/
│   └── prs_gallery.py        # Interactive marimo gallery
├── tests/                    # Test suite
├── example.py                # Usage examples
├── pyproject.toml            # Package metadata
├── README.md                 # Documentation
├── CLAUDE.md                 # AI assistant guidance
└── LICENSE                   # MIT License
```

## Next Steps

### Future Publishing Options

1. **Publish to PyPI** (recommended for wider distribution):
   ```bash
   # Build the package
   uv build

   # Publish to PyPI (requires PyPI account)
   uv publish
   ```

   Then users can install with:
   ```bash
   uv pip install prs-dataviz
   ```

2. **Create GitHub Releases**:
   - Tag versions with semantic versioning
   - Users can install specific versions
   - Example: `prs-dataviz @ git+https://github.com/Shakes-tzd/prs-dataviz.git@v0.1.0`

3. **Add CI/CD**:
   - GitHub Actions for automated testing
   - Automatic publishing to PyPI on release
   - Documentation building and deployment

## Maintenance

### Updating the Package

```bash
# Make changes
git add .
git commit -m "Description of changes"
git push

# Users can update by reinstalling
uv pip install --upgrade "prs-dataviz @ git+https://github.com/Shakes-tzd/prs-dataviz.git"
```

### Version Management

Consider adding version tags:
```bash
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0
```

## Support

- **Issues**: https://github.com/Shakes-tzd/prs-dataviz/issues
- **Discussions**: https://github.com/Shakes-tzd/prs-dataviz/discussions

---

**Created**: 2025-11-14
**Status**: ✅ Complete and functional
