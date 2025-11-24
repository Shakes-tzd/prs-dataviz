# Visual Inspection Checklist

## Purpose

This checklist guides **Phase 4: Visual Inspection** in the figure creation pipeline.

After generating a draft figure, **systematically** evaluate it using these criteria.

---

## How to Use This Checklist

1. **Display the figure**: `display(Image("draft_figure.png"))`
2. **Go through each category** below
3. **Mark issues** found
4. **Create refinement plan** based on findings
5. **Iterate** until all checks pass

---

## Category A: Readability

### Text Elements

- [ ] **All text readable** at intended print size (12pt minimum for labels)?
- [ ] **No overlapping text** (tick labels, annotations, legend)?
- [ ] **Labels clear and unambiguous** (include units where appropriate)?
- [ ] **Acronyms explained** (or avoided)?
- [ ] **Font sizes consistent** across elements?

**Common Issues**:
- X-axis labels overlap → rotate 45° or reduce font size
- Y-axis labels too small → increase to 12pt minimum
- Legend text overlaps with data → reposition legend

**Fixes**:
```python
# Rotate x-labels if cramped
ax.set_xticklabels(labels, rotation=45, ha="right")

# Standardize font sizes
from prs_dataviz import set_axis_fontsize
set_axis_fontsize(ax, fontsize=12)
prs_legend(ax, fontsize=12)

# Reposition legend if overlapping
prs_legend(ax, position="outside")  # Safest - never overlaps data

# Or for bar charts without titles:
prs_legend(ax, position="top-smart")  # Standard journal placement
```

### Legend Placement (CRITICAL - Common Problem Area)

**Based on [visualization standards](https://xdgov.github.io/data-design-standards/components/legends) and research:**

- [ ] **Legend doesn't obscure ANY data points**?
- [ ] **Legend position follows journal standards** (outside/below/top preferred)?
- [ ] **Legend proximity appropriate** (not too far from relevant data)?
- [ ] **Could direct labeling eliminate legend entirely**?

**Journal Standard Positions (in order of preference)**:
1. **Outside right** (safest, never overlaps, professional standard)
2. **Top center** (for bar charts without titles, horizontal layout)
3. **Below plot** (for titled figures, doesn't interrupt visual flow)
4. **Upper right** (only if data sparse in that corner)

**RED FLAGS** (requires immediate fix):
- ❌ Legend using `position="best"` (non-standard, often poor choice)
- ❌ Legend overlaps with any data points/bars/lines
- ❌ Legend in middle of plot (interrupts data reading)
- ❌ Legend too far from plot (breaks visual connection)
- ❌ Legend could be replaced with direct labeling (simpler)

**Evaluation Questions**:
1. **Occlusion Check**: Does legend cover ANY data? → If yes, move to "outside"
2. **Standard Check**: Is position outside/below/top? → If no, reconsider
3. **Simplicity Check**: Could we label data directly? → If yes, prefer that
4. **Proximity Check**: Is legend reasonably close to data? → Should be

**Fixes for Common Legend Placement Errors**:

```python
# ERROR 1: Legend using "best" (non-standard)
# BEFORE:
prs_legend(ax, position="best")  # ❌ Avoid for publications

# FIX:
prs_legend(ax, position="outside")  # ✅ Journal standard

# ERROR 2: Legend overlaps data points
# BEFORE:
prs_legend(ax, position="upper right")  # ❌ Data exists there

# FIX:
prs_legend(ax, position="outside")  # ✅ Never overlaps

# ERROR 3: Bar chart with title + legend inside
# BEFORE:
prs_legend(ax, position="upper left")  # ❌ Non-standard

# FIX:
prs_legend(ax, position="outside")  # ✅ Professional standard

# ERROR 4: Legend could be eliminated (3 or fewer series)
# BEFORE:
ax.bar(x, y1, label="Control")
ax.bar(x, y2, label="Treatment")
prs_legend(ax, position="outside")  # ❌ Unnecessary complexity

# FIX - Direct labeling (BEST):
ax.bar(x, y1, color=COMPARISON["Control"])
ax.bar(x, y2, color=COMPARISON["Treatment"])
# Add text labels directly on or near bars
ax.text(x1, y1 + 1, "Control", ha='center', fontweight='bold')
ax.text(x2, y2 + 1, "Treatment", ha='center', fontweight='bold')
# ✅ No legend needed - cleaner, more direct
```

**Decision Flowchart**:
```
Can we use direct labeling (≤3 series, space allows)?
├─ YES → Use direct text labels, NO LEGEND ✅ (Best option)
└─ NO → Proceed to positioning decision

Is this a bar chart without a title?
├─ YES → position="top-smart" ✅ (Standard for PRS)
└─ NO → Proceed to next check

Is there dense data throughout the plot?
├─ YES → position="outside" ✅ (Safest, never overlaps)
└─ NO → Check for empty corners

Is upper right corner empty (no data there)?
├─ YES → position="upper right" ⚠️  (Acceptable, but outside preferred)
└─ NO → position="outside" ✅ (Safest)

AVOID: position="best" ❌ (Not optimized for publication standards)
```

---

## Category B: Data Visibility

### Data Elements

- [ ] **All data points/bars/lines visible** (not occluded)?
- [ ] **No data hidden** behind legend or annotations?
- [ ] **Colors sufficiently distinct** (not too similar)?
- [ ] **Error bars visible** (if present)?
- [ ] **Markers distinguishable** (if multiple series)?

**Common Issues**:
- Legend covers data points → move legend or use "best" position
- Colors too similar (e.g., two shades of blue) → use different color families
- Error bars too small/thin → increase linewidth
- Data extends beyond axis limits → adjust xlim/ylim

**Fixes**:
```python
# Let matplotlib find optimal legend position
prs_legend(ax, position="best")  # Avoids data automatically

# Use explicit, distinct colors
from prs_dataviz import COMPARISON
ax.bar(x1, y1, color=COMPARISON["Before"])   # Gray
ax.bar(x2, y2, color=COMPARISON["After"])    # Teal (very distinct)

# Make error bars more visible
ax.errorbar(x, y, yerr=std, capsize=5, capthick=2, linewidth=1.5)

# Extend axis limits if data clipped
ax.set_ylim(0, max_value * 1.15)  # 15% headroom
```

---

## Category C: Balance & Composition

### Visual Weight

- [ ] **No lopsided appearance** (visually balanced)?
- [ ] **Appropriate white space** (not cramped, not excessive)?
- [ ] **Elements properly aligned** (labels, ticks, legend)?
- [ ] **Margins proportional** to plot size?

**Common Issues**:
- Too much white space above data → reduce y-axis max
- Plot area cramped → increase figure size
- Legend far from related data → reposition closer
- Uneven spacing between bars/points → adjust width parameter

**Fixes**:
```python
# Adjust y-axis limits to reduce excessive white space
data_max = max(values)
ax.set_ylim(0, data_max * 1.1)  # 10% headroom (not 50%)

# Increase figure size if cramped
fig, ax = plt.subplots(figsize=(10, 6))  # Was (6, 4), now larger

# Ensure tight layout (removes excess margins)
plt.tight_layout()

# Adjust bar width for better spacing
width = 0.35  # Adjust as needed (try 0.25 to 0.5)
ax.bar(x, y, width=width)
```

---

## Category D: Accessibility

### Color & Contrast

- [ ] **Colorblind-friendly** (prs_dataviz palettes are pre-tested)?
- [ ] **Sufficient contrast** (text vs. background ≥ 4.5:1)?
- [ ] **Not relying solely on color** (use shapes/patterns too)?
- [ ] **Markers/lines distinguishable** without color?

**Common Issues**:
- Only color differentiates series → add different markers
- Text low contrast → use darker colors or white background
- Too many colors (7+) → reduce categories or use faceting

**Fixes**:
```python
# Add redundant encoding (color + marker shape)
ax.plot(x, y1, color=CLINICAL_DATA["Primary"], marker="o", label="Group A")
ax.plot(x, y2, color=CLINICAL_DATA["Secondary"], marker="s", label="Group B")
#                                                        ↑ Square vs circle

# Ensure white background (not gray)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Use pre-tested colorblind-friendly palettes
from prs_dataviz import COMPARISON, CLINICAL_DATA, PRS_DEFAULT_CYCLE
# All palettes tested for deuteranopia, protanopia, tritanopia
```

---

## Category E: Data-Ink Ratio (Tufte)

### Simplicity

- [ ] **No unnecessary decorations** (chartjunk removed)?
- [ ] **Grid helpful** (aids reading) or distracting?
- [ ] **Borders minimal** (top/right spines removed)?
- [ ] **Background plain** (white or subtle)?
- [ ] **Maximize data, minimize ink**?

**Common Issues**:
- 3D effects (never use) → switch to 2D
- Excessive grid lines → make subtle or remove
- Colored background → use white
- Heavy borders → remove or thin
- Unnecessary decorative elements → remove all

**Fixes**:
```python
# Remove top/right spines (cleaner look)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Subtle grid (if helpful for data reading)
ax.yaxis.grid(True, linestyle="--", alpha=0.3)  # Very subtle
ax.set_axisbelow(True)  # Grid behind data

# Plain white background
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# No 3D effects (distort perception)
# Never use: ax.bar3d(), mpl_toolkits.mplot3d, etc.
```

---

## Category F: PRS-Specific Standards

### Professional Medical Appearance

- [ ] **Professional appearance** suitable for medical journal?
- [ ] **Clean, clinical aesthetic** (not flashy)?
- [ ] **Font sizes appropriate** (10pt+ body, 12pt+ labels)?
- [ ] **Muted, professional colors** (not bright/saturated)?
- [ ] **Proper scientific notation** (if applicable)?

**Common Issues**:
- Bright, saturated colors → use prs_dataviz muted palettes
- Decorative fonts → use DejaVu Sans, Arial, or Helvetica
- Font sizes too small (<10pt) → increase to 12pt
- Flashy design → simplify and use clinical colors

**Fixes**:
```python
# Use muted, professional palettes
from prs_dataviz import CLINICAL_DATA, COMPARISON
apply_prs_style(cycle="clinical")  # Sets professional defaults

# Ensure readable font sizes
fontsize = 12  # Minimum for medical journals
ax.tick_params(labelsize=fontsize)
ax.set_xlabel("Label", fontsize=fontsize, fontweight="bold")
ax.set_ylabel("Label", fontsize=fontsize, fontweight="bold")

# Professional color selection
colors = [CLINICAL_DATA["Primary"], CLINICAL_DATA["Secondary"]]
# Not: colors = ["red", "green", "blue", "yellow"]  # Too saturated
```

---

## Category G: Scientific Accuracy

### Integrity

- [ ] **Axes start at zero** (for bar charts)?
- [ ] **No misleading visual effects** (e.g., truncated axes)?
- [ ] **Error bars visible and labeled** (mean ± SD? 95% CI?)?
- [ ] **Statistical indicators clear** (p-values, significance)?
- [ ] **Units included** in axis labels?

**Common Issues**:
- Bar chart doesn't start at zero → creates misleading visual
- Broken axis without clear indication → confusing
- Error bar type unclear → specify in legend or caption
- P-values shown without context → add brackets showing comparison

**Fixes**:
```python
# Bar charts should start at zero
ax.set_ylim(0, max_value * 1.15)  # Not (50, 100) if data is 60-90

# Clearly label error bar type
ax.errorbar(x, y, yerr=std, label="Mean ± SD", capsize=5)

# Add significance indicators with clarity
from prs_dataviz import add_significance_indicator
add_significance_indicator(
    ax, x=1.5, y=95, p_value=0.03,
    bracket=True, x_start=1, x_end=2
)

# Include units in labels
ax.set_ylabel("Recovery Time (days)")  # Not just "Recovery Time"
ax.set_xlabel("Treatment Group")
```

---

## Systematic Inspection Workflow

### Step 1: Initial Viewing (30 seconds)

**First impression**:
- Does it look professional?
- Is the message immediately clear?
- Any obvious problems?

### Step 2: Detailed Checklist (2-3 minutes)

Go through all 7 categories (A-G) above systematically.

### Step 3: Document Findings

**Template**:
```
VISUAL INSPECTION RESULTS

✅ GOOD:
  - [List what works well]
  - [E.g., "Colors distinct and professional"]
  - [E.g., "Font sizes consistent"]

⚠️  NEEDS REFINEMENT:
  - [List specific issues found]
  - [E.g., "Legend overlaps with rightmost data point"]
  - [E.g., "Y-axis max too high (excessive white space)"]
  - [E.g., "X-axis labels slightly cramped"]

REFINEMENT PLAN:
  1. [Specific action to fix issue 1]
  2. [Specific action to fix issue 2]
  3. [Specific action to fix issue 3]
```

### Step 4: Prioritize Issues

**High priority** (must fix):
- Readability issues (can't read text)
- Data visibility (data occluded)
- Scientific accuracy (misleading)

**Medium priority** (should fix):
- Balance/composition (unprofessional appearance)
- Accessibility (colorblind issues)

**Low priority** (nice to fix):
- Minor aesthetic improvements
- Small optimization opportunities

### Step 5: Implement Refinements

Make targeted changes based on refinement plan.

### Step 6: Re-inspect

After refinements:
- Display refined figure
- Check if issues resolved
- Identify any new issues introduced
- Iterate if needed (typically 1-2 iterations)

---

## Example Inspection

### Draft Figure Issues

```
VISUAL INSPECTION: draft_complication_figure.png

✅ GOOD:
  - Colors professional (clinical blue)
  - Data clearly visible
  - Font sizes mostly consistent (12pt)
  - Grid aids data reading

⚠️  NEEDS REFINEMENT:
  1. Legend position "best" put it in upper right, but data exists there
     → Overlaps with "Rhinoplasty" bar
  2. Y-axis extends to 20%, but max data is 12.5%
     → Excessive white space above (40% wasted)
  3. X-axis labels cramped (long procedure names)
     → "Blepharoplasty" overlaps with "Otoplasty"
  4. No data labels on bars
     → User must estimate values from grid (less precise)

REFINEMENT PLAN:
  1. Move legend to "upper left" (data sparse there)
  2. Reduce y-axis max to 15% (10% headroom above max)
  3. Rotate x-labels 30° to right-align
  4. Add value labels on top of bars (e.g., "12.5%")
```

### After Refinement

```
VISUAL INSPECTION: refined_complication_figure.png

✅ ALL ISSUES RESOLVED:
  - Legend now in upper left (no data overlap)
  - Y-axis max reduced to 15% (appropriate headroom)
  - X-labels rotated and readable
  - Data labels added (precise values visible)
  - Professional appearance maintained

🎯 READY FOR PRS EXPORT
```

---

## Quick Reference: Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Text overlap | Labels touch/overwrite | Rotate labels, reduce font size |
| Legend obscures data | Legend covers points/bars | Use `position="best"` or move explicitly |
| Cramped appearance | Elements too close | Increase `figsize`, use `tight_layout()` |
| Excessive white space | Large empty areas | Adjust `xlim`/`ylim` to data range + 10-15% |
| Colors too similar | Hard to distinguish series | Use different color families (COMPARISON) |
| Font sizes inconsistent | Unprofessional look | Use `set_axis_fontsize(ax, 12)` |
| Grid too prominent | Distracts from data | Reduce alpha to 0.3, use `linestyle="--"` |
| Bar chart doesn't start at zero | Misleading visual | `ax.set_ylim(0, max_value * 1.15)` |
| Error bars invisible | Too thin/small | Increase `capsize`, `capthick`, `linewidth` |
| Too many colors (7+) | Confusing | Reduce categories or use faceting |

---

## When to Iterate vs. Accept

### Iterate If:
- ❌ Critical readability issue (can't read text)
- ❌ Data occluded or misleading
- ❌ Unprofessional appearance
- ❌ Accessibility failure (contrast, colorblind)

### Accept If:
- ✅ All checklist items pass
- ✅ Minor aesthetic preferences only
- ✅ "Good enough" for context (draft vs. publication)

**Guideline**: 2-3 iterations typically sufficient to reach publication quality.

---

## Summary

1. **Display** draft figure
2. **Inspect** systematically (A-G categories)
3. **Document** findings (Good / Needs Refinement)
4. **Prioritize** issues (High / Medium / Low)
5. **Refine** with targeted changes
6. **Re-inspect** to verify improvements
7. **Iterate** until quality threshold met (1-3 cycles)

**Remember**: Visual inspection is **critical**. Code logic alone cannot ensure quality—you must look at the figure!
