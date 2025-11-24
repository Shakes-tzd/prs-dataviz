# Data Visualization Design Principles

## Research Foundation

This document synthesizes design principles from:
- **Cara Thompson**: [Ophelia design system methodology](https://www.cararthompson.com/talks/nhsr2023-dataviz-design-system/)
- **Draco/Voyager**: [Constraint-based visualization](https://www.domoritz.de/papers/2018-Draco-InfoVis.pdf)
- **Grammar of Graphics**: [Layered compositional approach](https://byrneslab.net/classes/biol607/readings/wickham_layered-grammar.pdf)
- **Claude Code**: [Best practices for iterative refinement](https://www.anthropic.com/engineering/claude-code-best-practices)

---

## Core Principle: Composition Over Enumeration

### ❌ The Enumeration Problem (Doesn't Scale)

```
Plot Type (10) × Colors (5) × Legend Position (6) × Font Size (4) ×
Label Length (4) × Data Density (3) × Title (2) = 14,400 combinations
```

You cannot create templates for all cases.

### ✅ The Compositional Solution (Scales Infinitely)

```
plot = data + aesthetics + geometry + statistics + coordinates + theme

Each component is INDEPENDENT:
- Change data → plot adapts
- Change theme → styling updates
- Change geometry → representation shifts
```

**Key Insight**: Build figures from composable elements, not enumerated templates.

---

## Principle 1: Constraints, Not Templates

### Hard Constraints (MUST follow)

From PRS requirements:
- Resolution ≥ 300 DPI
- Color mode = CMYK
- Dimensions ≥ 3.25" (photos) or 5" (graphs)
- Format = TIFF (preferred)

### Soft Constraints (Preferences with weights)

From design research:
- Legend position: prefer "best" (avoids data) over "fixed"
- Font size: prefer 12pt (readable) over 8pt (too small) or 16pt (too large)
- Color count: prefer 3-5 colors (distinct) over 10+ (confusing)
- Data-ink ratio: prefer minimal decoration over excessive

### Constraint Satisfaction Example

```python
# DON'T enumerate all cases:
if plot_type == "bar" and n_labels == 2 and labels_short:
    legend_position = "top"
elif plot_type == "bar" and n_labels == 2 and labels_long:
    legend_position = "outside"
# ... (infinite more cases)

# DO use constraints:
# Hard constraint: Legend must not obscure data
# Soft preference: Legend near relevant data

# Solution: Use "best" position (matplotlib satisfies both)
prs_legend(ax, position="best")

# OR for bar charts without titles (common in PRS):
# Soft preference: Top position for horizontal layout
prs_legend(ax, position="top-smart")  # Auto-calculates columns
```

---

## Principle 2: Visual Feedback Loop

### Research Finding

From [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices):

> "Claude performs best when it has a clear target to iterate against—a visual mock,
> a test case, or another kind of output... Like humans, Claude's outputs tend to
> improve significantly with iteration. While the first version might be good, after
> 2-3 iterations it will typically look much better."

### Practical Implementation

```python
# Generate initial version
fig, ax = plt.subplots()
# ... plotting code ...
plt.savefig("draft.png", dpi=150)

# INSPECT VISUALLY (critical step!)
display(Image("draft.png"))

# Critique systematically:
# - Readability issues?
# - Balance problems?
# - Aesthetic issues?

# Refine based on visual feedback
# ... adjustments ...
plt.savefig("refined.png", dpi=150)

# Iterate until quality threshold met
```

### Why This Works

1. **Visual inspection** catches issues code logic misses
2. **Iterative refinement** compounds improvements
3. **Feedback signal** guides adjustments
4. **Human-like process** leverages Claude's multimodal capabilities

---

## Principle 3: Data-Driven Design

### Process

```
Step 1: Inspect Data
  ↓
Step 2: Identify Characteristics
  ↓
Step 3: Choose Appropriate Representation
  ↓
Step 4: Apply Design Principles
  ↓
Step 5: Generate + Inspect Visually
  ↓
Step 6: Refine Based on Feedback
```

### Example Decision Tree

```python
# Inspect data characteristics
if data_structure == "categorical" and n_categories <= 7:
    # Bar chart appropriate
    plot_type = "bar"

    if has_groups:
        bar_style = "grouped"
    elif has_parts_to_whole:
        bar_style = "stacked"
    else:
        bar_style = "simple"

elif data_structure == "continuous_over_time":
    # Line plot appropriate
    plot_type = "line"

    if has_uncertainty:
        add_confidence_intervals = True

# This is ADAPTIVE, not ENUMERATED
```

---

## Principle 4: Accessibility First

### WCAG 2.1 Requirements

**Text Contrast**:
- Body text: 4.5:1 minimum
- Large text (14pt+ bold, 18pt+ regular): 3:1 minimum
- UI components: 3:1 minimum

**Color Usage**:
- Don't rely solely on color to convey information
- Provide redundant encoding (color + shape + label)
- Test for colorblindness (prs_dataviz palettes pre-tested)

**Font Sizes**:
- Minimum 10pt for body text
- Minimum 12pt for axis labels (PRS recommendation)
- Prefer 12-14pt for professional medical figures

### Implementation

```python
# All prs_dataviz palettes satisfy:
# - CMYK-safe (printable)
# - Colorblind-friendly (deuteranopia, protanopia, tritanopia)
# - WCAG 2.1 contrast ratios

# Explicit redundant encoding example:
ax.plot(x, y1, color=CLINICAL_DATA["Primary"], marker="o", label="Group A")
ax.plot(x, y2, color=CLINICAL_DATA["Secondary"], marker="s", label="Group B")
#                                                   ↑
#                               Different markers (not just color)
```

---

## Principle 5: Simplicity (Data-Ink Ratio)

### Tufte's Principle

> "Data-ink ratio = (ink used to display data) / (total ink used to print graphic)"

**Maximize** ink showing data.
**Minimize** ink for decoration.

### Practical Rules

✅ **Keep**:
- Data points/bars/lines
- Axis labels with units
- Grid lines (if aid data reading)
- Legend (if necessary)
- Minimal borders

❌ **Remove**:
- Excessive decorations
- 3D effects (distort perception)
- Unnecessary backgrounds
- Redundant labels
- Chartjunk

### Example

```python
# DON'T:
ax.bar(x, y, color="red", edgecolor="black", linewidth=3,
       hatch="///", alpha=0.5)  # Too much decoration
ax.set_facecolor("#F0F0F0")     # Distracting background
ax.spines["top"].set_linewidth(3)
ax.spines["right"].set_linewidth(3)
ax.grid(True, color="blue", linewidth=2, linestyle="--", alpha=0.7)  # Too prominent

# DO:
ax.bar(x, y, color=CLINICAL_DATA["Primary"], alpha=0.85)  # Clean
ax.set_facecolor("white")                                  # Neutral
ax.spines["top"].set_visible(False)                        # Remove unnecessary
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, linestyle="--", alpha=0.3)            # Subtle grid
ax.set_axisbelow(True)                                     # Grid behind data
```

---

## Principle 6: Professional Medical Aesthetics

### Color Psychology in Medical Context

| Color Family | Association | Use Case |
|-------------|-------------|----------|
| Blues | Trust, professionalism, clinical | General medical data |
| Teals/Greens | Healing, clinical environment | Treatment/after states |
| Grays | Neutral, control, baseline | Control groups, before states |
| Warm browns | Natural, tissue | Skin/tissue visualization |
| Muted tones | Professional, accessible | Reduces sensory overwhelm |

### PRS-Specific Standards

**Preferred**:
- Clean, minimal design
- Professional fonts (DejaVu Sans, Arial, Helvetica)
- Muted, accessible colors
- High contrast for readability
- Grid lines for data reading (optional but helpful)

**Avoid**:
- Bright, saturated colors (unprofessional)
- Decorative fonts (Comic Sans, etc.)
- 3D effects (distort perception)
- Excessive gradients
- Colored backgrounds (prefer white/neutral)

---

## Principle 7: Consistent Typography

### The Importance of Font Size Harmony

**Problem**: Inconsistent font sizes look unprofessional.

```python
# DON'T mix random sizes:
ax.set_xlabel("Time", fontsize=10)
ax.set_ylabel("Response", fontsize=14)
ax.set_title("Results", fontsize=11)
ax.tick_params(labelsize=12)
prs_legend(ax, fontsize=9)
# Result: Visually jarring
```

**Solution**: Use consistent sizing with clear hierarchy.

```python
# DO standardize:
base_fontsize = 12  # Base unit

ax.tick_params(labelsize=base_fontsize)
ax.set_xlabel("Time", fontsize=base_fontsize, fontweight="bold")
ax.set_ylabel("Response", fontsize=base_fontsize, fontweight="bold")
ax.set_title("Results", fontsize=base_fontsize + 2, fontweight="bold")  # Slightly larger
prs_legend(ax, fontsize=base_fontsize)

# OR use helper:
from prs_dataviz import set_axis_fontsize
set_axis_fontsize(ax, fontsize=12)
prs_legend(ax, fontsize=12)
```

### Font Size Guidelines

| Element | Size | Weight | Rationale |
|---------|------|--------|-----------|
| Tick labels | 10-12pt | Normal | Readable but subtle |
| Axis labels | 12pt | Bold | Important, prominent |
| Title | 14pt | Bold | Hierarchical emphasis |
| Legend | 10-12pt | Normal | Readable, not dominant |
| Annotations | 10pt | Normal | Informative, not intrusive |

---

## Principle 8: Balance and Composition

### Visual Weight Distribution

```
┌─────────────────────────┐
│  Title (optional)       │
├─────────────────────────┤
│ Y │                     │
│   │   DATA AREA         │
│ L │                     │
│ a │                     │
│ b │                     │
│ e │                     │
│ l │                     │
├───┴─────────────────────┤
│      X Label            │
└─────────────────────────┘
```

**Balance Rules**:
1. **Symmetry**: Avoid lopsided layouts
2. **White space**: Margins proportional to plot size
3. **Alignment**: Elements aligned to grid
4. **Proximity**: Related items close together

### Legend Positioning Heuristics

```python
# Decision heuristic (simplified):

if n_legend_items <= 3 and data_not_dense:
    # Simple case - matplotlib "best" finds good spot
    position = "best"

elif plot_type == "bar" and no_title:
    # PRS common pattern: no title (in caption instead)
    # Top position works well for horizontal layout
    position = "top-smart"

elif plot_type == "line" and data_fills_plot:
    # Data dense - keep legend outside to avoid occlusion
    position = "outside"

elif plot_type == "scatter" and data_sparse_in_corners:
    # Data sparse in corners - can use inside position
    position = "best"  # Matplotlib avoids data automatically

else:
    # Default: trust matplotlib's algorithm
    position = "best"
```

---

## Principle 9: Determinism Through Process

### The Paradox

**Challenge**: Every dataset is unique (infinite variations).
**Solution**: Deterministic *process* produces adaptive *outcomes*.

### Implementation

**Deterministic Pipeline** (always follow these steps):
1. Data Exploration → Understand characteristics
2. Design Decision → Choose representation
3. Initial Generation → Create draft
4. Visual Inspection → Identify issues
5. Iterative Refinement → Fix issues
6. Validation → Ensure compliance

**Adaptive Decisions** (within each step):
- Step 1: Analyze THIS dataset's structure
- Step 2: Choose plot type FOR THIS data
- Step 4: Critique THIS specific figure
- Step 5: Refine THESE specific issues

**Result**: Reproducible process + tailored outcomes.

---

## Principle 10: Fail Fast on Requirements

### Hard Constraint Violation = Immediate Failure

```python
# Example: PRS requires 300+ DPI
if result["dpi"] < 300:
    raise ValueError(
        f"Figure DPI ({result['dpi']}) below PRS minimum (300). "
        "Use save_prs_figure(dpi=300) for export."
    )

# Example: PRS requires minimum width
if result["width_inches"] < 3.25:
    raise ValueError(
        f"Figure width ({result['width_inches']:.2f}\") below PRS minimum (3.25\"). "
        "Use figsize=(5, 4) or larger for graphs."
    )
```

### Soft Preference Violation = Warning

```python
# Example: Excessive colors reduce distinguishability
if n_colors > 7:
    warnings.warn(
        f"Using {n_colors} colors may reduce distinguishability. "
        "Consider grouping categories or using facets."
    )

# Example: Font size very small
if fontsize < 10:
    warnings.warn(
        f"Font size ({fontsize}pt) may be too small for print. "
        "PRS recommends 10-12pt minimum."
    )
```

---

## Summary: Principles → Practice

| Principle | Implementation | Tool/Function |
|-----------|----------------|---------------|
| 1. Constraints not templates | Use constraint satisfaction | `prs_legend(position="best")` |
| 2. Visual feedback loop | Generate → inspect → refine | `display(Image("draft.png"))` |
| 3. Data-driven design | Explore data first | `data.describe()`, `data.dtypes` |
| 4. Accessibility first | WCAG 2.1 compliance | Pre-tested palettes, contrast |
| 5. Simplicity | Maximize data-ink ratio | Remove chartjunk, clean design |
| 6. Professional aesthetics | Medical color psychology | `CLINICAL_DATA`, `COMPARISON` |
| 7. Consistent typography | Standardize font sizes | `set_axis_fontsize(ax, 12)` |
| 8. Balance and composition | Avoid lopsided layouts | `tight_layout()`, `bbox_inches` |
| 9. Determinism through process | 6-phase pipeline | Always follow workflow |
| 10. Fail fast | Validate early | `validate_figure_file()` |

---

## References

- Thompson, C. (2023). [Building dataviz design systems](https://www.cararthompson.com/talks/nhsr2023-dataviz-design-system/). NHS-R Conference.
- Moritz, D., et al. (2018). [Formalizing visualization design knowledge as constraints](https://www.domoritz.de/papers/2018-Draco-InfoVis.pdf). IEEE InfoVis.
- Wickham, H. (2010). [A layered grammar of graphics](https://byrneslab.net/classes/biol607/readings/wickham_layered-grammar.pdf). Journal of Computational and Graphical Statistics.
- Anthropic (2025). [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices).
- World Wide Web Consortium. [Web Content Accessibility Guidelines (WCAG) 2.1](https://www.w3.org/WAI/WCAG21/quickref/).
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.
