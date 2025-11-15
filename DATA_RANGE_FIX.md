# Data-Range-Based Spacing Fix

## Problem Identified

**Original approach used circular math:**
```python
# OLD (WRONG):
headroom_fraction = 0.40  # 40% of...?
ymax = data_max / (1 - headroom_fraction)  # Circular dependency!
```

**Result:** Absurdly large gaps
- Data max: 2890
- First bracket: 3275 (gap of **385 units** = 13% of bar height!)
- ymax: 4817

---

## Root Cause

1. **Circular dependency:** We calculate ymax based on percentages of y_range, but y_range depends on ymax!

2. **Wrong reference:** Spacing should be based on **DATA scale** (0-2890), not **AXIS scale** (0-4817 which includes our own spacing)

3. **No physical meaning:** Text height and visual spacing are NOT percentages of an inflated axis

---

## Solution: Base Spacing on DATA RANGE

**New approach (CORRECT):**
```python
# Calculate data range (not y-axis range!)
data_range = data_max - data_min  # e.g., 2890 - 0 = 2890

# Spacing as percentage of DATA, not axis
base_offset = 0.10      # 10% of data range
stack_spacing = 0.08    # 8% of data range per bracket
text_spacing = 0.04     # 4% of data range for text

# Simple addition - no circular math!
total_headroom = (base_offset + (n_comparisons - 1) * stack_spacing + text_spacing) * data_range
ymax = data_max + total_headroom
```

---

## Example Calculation (3 comparisons, data 0-2890)

**Step 1: Calculate headroom**
```
data_range = 2890 - 0 = 2890

total_headroom = (0.10 + 2×0.08 + 0.04) × 2890
               = 0.30 × 2890
               = 867
```

**Step 2: Set y-limits**
```
ymin = 0
ymax = 2890 + 867 = 3757  ✓ (Much better than 4817!)
```

**Step 3: Calculate bracket positions**
```
All comparisons include Q4 (tallest bar at 2890), so data_max_in_range = 2890

Level 0 (Q1→Q4, widest span):
  bracket_y = 2890 + 0.10×2890 = 3179  ✓ (gap of 289, which is 10% of data)

Level 1 (Q2→Q4, medium span):
  bracket_y = 2890 + (0.10 + 0.08)×2890 = 3410  ✓ (18% of data above)

Level 2 (Q3→Q4, narrowest span):
  bracket_y = 2890 + (0.10 + 2×0.08)×2890 = 3641  ✓ (26% of data above)
```

**Step 4: Text positions**
```
Text is 3% of data_range (86.7 units) above each bracket

Level 0 text: 3179 + 87 = 3266
Level 1 text: 3410 + 87 = 3497
Level 2 text: 3641 + 87 = 3728

All fit comfortably within ymax = 3757 ✓
```

---

## Visual Comparison

### OLD (Circular Math):
```
ymax = 4817  ──────────────────────
                (way too high!)
4383  p = 0.03
4239  ━━━━━━━━━━  (Q3→Q4)
3901  p = 0.008
3757  ━━━━━━━━━━━━━━  (Q2→Q4)
3420  p < 0.001
3275  ━━━━━━━━━━━━━━━━━  (Q1→Q4)
      ↑ 385 unit gap (13% of bar!)
2890  █████  (Q4 bar)
```

### NEW (Data-Range Based):
```
ymax = 3757  ──────────────────────
                (perfect fit!)
3728  p = 0.03
3641  ━━━━━━━━━━  (Q3→Q4)
3497  p = 0.008
3410  ━━━━━━━━━━━━━━  (Q2→Q4)
3266  p < 0.001
3179  ━━━━━━━━━━━━━━━━━  (Q1→Q4)
      ↑ 289 unit gap (10% of data ✓)
2890  █████  (Q4 bar)
```

---

## Benefits

1. **No circular dependency:** Data range is independent of axis limits
2. **Consistent across scales:** 10% spacing means 10% of YOUR data, not some inflated axis
3. **Predictable:** Gap above bars is always 10% of data range
4. **Reasonable:** For data 0-2890, first bracket is ~289 units above (not 385!)
5. **Fits better:** ymax = 3757 (not 4817), so matplotlib's autoscaling won't override it

---

## Files Changed

1. **src/prs_dataviz/helpers.py:auto_calculate_ylim_for_annotations()**
   - Changed from `ymax = data_max / (1 - headroom_fraction)`
   - To: `ymax = data_max + total_headroom`
   - Where: `total_headroom = (percentages) * data_range`

2. **src/prs_dataviz/helpers.py:auto_position_brackets()**
   - Changed from using `y_range` for bracket positioning
   - To using `data_range` for bracket positioning
   - Ensures consistency between limit calculation and bracket placement

---

## New Spacing Parameters

- `base_offset`: 0.10 (10% of data range) - space above tallest bar
- `stack_spacing`: 0.08 (8% of data range) - space between stacked brackets
- `text_spacing`: 0.04 (4% of data range) - space for text above bracket

**Total for 3 comparisons:** 30% of data range (was 40% of inflated axis range)
