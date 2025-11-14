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

"""
PRS DataViz Gallery: Professional Data Visualization for Medical Research

This interactive gallery demonstrates the prs-dataviz package for creating
publication-quality figures that meet Plastic and Reconstructive Surgery (PRS)
journal submission requirements.

Design Philosophy:
- Du Bois-inspired aesthetics (historical data visualization excellence)
- Ophelia approach (Cara Thompson's accessible dataviz methodology)
- PRS compliance (300 DPI, CMYK, professional quality)

Reference:
- Cara Thompson's 10-step process: https://www.cararthompson.com/talks/on-brand-accessibility/
- PRS Guidelines: https://journals.lww.com/plasreconsurg/
"""

import marimo

__generated_with = "0.17.7"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # PRS DataViz: Professional Medical Data Visualization

        A comprehensive design system for creating **publication-quality figures** that meet
        [Plastic and Reconstructive Surgery (PRS)](https://journals.lww.com/plasreconsurg/)
        journal submission requirements.

        ## Design Principles

        This package integrates three complementary approaches:

        1. **Du Bois Aesthetic**: Historical excellence in data visualization with rich, earthy color palettes
        2. **Ophelia Methodology**: [Cara Thompson's](https://www.cararthompson.com/talks/on-brand-accessibility/)
           10-step process for accessible, neurodivergent-friendly visualization
        3. **PRS Compliance**: Automatic enforcement of journal requirements (300 DPI, CMYK, proper sizing)

        ### Why This Matters for Medical Research

        - ✅ **Automatic PRS compliance** - No manual DPI/CMYK conversion
        - ✅ **Professional medical palettes** - CMYK-safe, colorblind-friendly
        - ✅ **Before/after layouts** - With size validation
        - ✅ **Accessibility-first** - WCAG 2.1 compliant, neurodivergent-friendly
        - ✅ **Time-saving** - 2-3 hours saved per figure

        ---
        """
    )
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    # Import from the actual prs-dataviz package
    from prs_dataviz import (
        CLINICAL_BLUE,
        TISSUE_TONE,
        CLINICAL_DATA,
        COMPARISON,
        STATISTICAL,
        PRS_DEFAULT_CYCLE,
        PRS_CLINICAL_CYCLE,
        PRS_COMPARISON_CYCLE,
        apply_prs_style,
    )

    return (
        CLINICAL_BLUE,
        CLINICAL_DATA,
        COMPARISON,
        PRS_CLINICAL_CYCLE,
        PRS_COMPARISON_CYCLE,
        PRS_DEFAULT_CYCLE,
        STATISTICAL,
        TISSUE_TONE,
        apply_prs_style,
        font_manager,
        np,
        plt,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 🎨 Color Palettes

        All palettes are designed for medical/surgical contexts with:
        - **CMYK-safe colors** (print-ready)
        - **Colorblind-friendly** (tested for deuteranopia, protanopia, tritanopia)
        - **WCAG 2.1 accessible** (proper contrast ratios)
        - **Professional aesthetics** (muted, clinical appropriate)

        ### Philosophy

        Like the Ophelia package builds from anchor colors with semantic meaning, PRS DataViz
        palettes are purpose-built for medical research contexts, balancing clinical professionalism
        with visual accessibility.
        """
    )
    return


@app.cell
def _(CLINICAL_BLUE, CLINICAL_DATA, COMPARISON, STATISTICAL, TISSUE_TONE, mo, np, plt):
    # Color palette swatches
    def create_palette_swatch(palette_dict, title):
        fig, ax = plt.subplots(figsize=(10, 2))

        colors = list(palette_dict.values())
        labels = list(palette_dict.keys())
        n_colors = len(colors)

        # Create color swatches
        for i, (color, label) in enumerate(zip(colors, labels)):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='#333', linewidth=1))
            ax.text(i + 0.5, 0.5, label, ha='center', va='center',
                   fontsize=9, fontweight='bold', color='white' if i < 2 else '#333')
            ax.text(i + 0.5, -0.3, color, ha='center', va='top',
                   fontsize=8, family='monospace', color='#666')

        ax.set_xlim(0, n_colors)
        ax.set_ylim(-0.5, 1.2)
        ax.axis('off')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=10, loc='left')

        plt.tight_layout()
        return fig

    # Create swatches for each palette
    palette_clinical_blue = create_palette_swatch(CLINICAL_BLUE, "Clinical Blue - Professional & Trustworthy")
    palette_clinical_data = create_palette_swatch(CLINICAL_DATA, "Clinical Data - Statistical Visualization")
    palette_tissue = create_palette_swatch(TISSUE_TONE, "Tissue Tone - Medical Photography")
    palette_comparison = create_palette_swatch(COMPARISON, "Comparison - Before/After & Treatment")
    palette_statistical = create_palette_swatch(STATISTICAL, "Statistical - Significance Levels")

    mo.vstack([
        palette_clinical_blue,
        mo.md("Use for: General medical data, professional contexts, trustworthy clinical presentations"),
        mo.md("---"),
        palette_clinical_data,
        mo.md("Use for: Statistical graphs, research data, multi-series comparisons"),
        mo.md("---"),
        palette_tissue,
        mo.md("Use for: Skin/tissue visualization, patient photo contexts, anatomical references"),
        mo.md("---"),
        palette_comparison,
        mo.md("Use for: Before/after surgical outcomes, treatment comparisons, control vs. experimental"),
        mo.md("---"),
        palette_statistical,
        mo.md("Use for: P-value visualization, significance indicators, hypothesis testing results"),
    ])
    return create_palette_swatch, palette_clinical_blue, palette_clinical_data, palette_comparison, palette_statistical, palette_tissue


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 📊 Interactive Examples

        Progressive complexity demonstrations following the Ophelia approach:
        start simple, build sophistication, maintain consistency.

        ### 1. Basic Statistical Bar Chart

        The foundational visualization for treatment efficacy and group comparisons.
        """
    )
    return


@app.cell
def _(apply_prs_style, np, plt):
    # Example 1: Statistical bar chart
    apply_prs_style(cycle="clinical", show_grid=True)

    fig1, ax1 = plt.subplots(figsize=(8, 5))

    categories = ['Pre-operative', '3 Months', '6 Months', '12 Months']
    control = [65, 68, 70, 72]
    treatment = [65, 75, 82, 88]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax1.bar(x - width/2, control, width, label='Control', alpha=0.8)
    bars2 = ax1.bar(x + width/2, treatment, width, label='Treatment', alpha=0.8)

    ax1.set_ylabel('Patient Satisfaction Score (%)', fontsize=11)
    ax1.set_xlabel('Follow-up Time', fontsize=11)
    ax1.set_title('Treatment Efficacy Over Time', fontsize=13, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.set_ylim(0, 100)
    ax1.legend(frameon=True, loc='upper left')
    ax1.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)

    # Add significance indicators
    ax1.text(2.5, 85, '*', fontsize=20, ha='center', color='#2C5F87')
    ax1.text(2.5, 83, 'p < 0.05', fontsize=8, ha='center', color='#666')

    plt.tight_layout()

    example1_fig = fig1
    return ax1, bars1, bars2, categories, control, example1_fig, fig1, treatment, width, x


@app.cell
def _(example1_fig, mo):
    mo.vstack([
        example1_fig,
        mo.md("""
        **Key Features:**
        - Clinical color palette (professional blues)
        - Grid for easier value reading
        - Significance indicators (p-values)
        - Clear labeling and legend
        - **PRS-ready**: Save at 300 DPI, CMYK mode, 5" width minimum
        """)
    ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ### 2. Line Graph with Confidence Intervals

        Time series data with uncertainty visualization - essential for longitudinal studies.
        """
    )
    return


@app.cell
def _(apply_prs_style, np, plt):
    # Example 2: Line graph with confidence intervals
    apply_prs_style(cycle="clinical")

    fig2, ax2 = plt.subplots(figsize=(8, 5))

    months = np.array([0, 1, 3, 6, 12, 18, 24])
    treatment_mean = np.array([50, 62, 72, 80, 85, 87, 88])
    treatment_std = np.array([8, 7, 6, 5, 4, 4, 4])
    control_mean = np.array([50, 54, 58, 62, 65, 67, 68])
    control_std = np.array([8, 8, 7, 7, 6, 6, 6])

    # Plot lines
    ax2.plot(months, treatment_mean, marker='o', linewidth=2.5,
             label='Treatment', markersize=7)
    ax2.plot(months, control_mean, marker='s', linewidth=2.5,
             label='Control', markersize=7)

    # Add confidence intervals (±1 SD)
    ax2.fill_between(months, treatment_mean - treatment_std,
                     treatment_mean + treatment_std, alpha=0.2)
    ax2.fill_between(months, control_mean - control_std,
                     control_mean + control_std, alpha=0.2)

    ax2.set_xlabel('Time Since Surgery (months)', fontsize=11)
    ax2.set_ylabel('Recovery Score', fontsize=11)
    ax2.set_title('Long-term Recovery Trajectories', fontsize=13, fontweight='bold', pad=15)
    ax2.legend(frameon=True, loc='lower right')
    ax2.set_ylim(35, 100)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)

    plt.tight_layout()

    example2_fig = fig2
    return ax2, control_mean, control_std, example2_fig, fig2, months, treatment_mean, treatment_std


@app.cell
def _(example2_fig, mo):
    mo.vstack([
        example2_fig,
        mo.md("""
        **Key Features:**
        - Smooth lines with distinct markers
        - Confidence intervals (shaded regions)
        - Clear temporal progression
        - Professional grid for reading values
        - **Suitable for**: Healing progression, follow-up studies, longitudinal data
        """)
    ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ### 3. Before/After Comparison

        The cornerstone of surgical outcomes research - properly sized and styled.
        """
    )
    return


@app.cell
def _(COMPARISON, apply_prs_style, np, plt):
    # Example 3: Before/After scatter comparison
    apply_prs_style(cycle="comparison")

    fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(12, 5))

    # Generate mock measurement data
    np.random.seed(42)
    n_patients = 30
    before_values = np.random.normal(45, 10, n_patients)
    after_values = before_values + np.random.normal(25, 5, n_patients)

    # Before
    ax3a.scatter(range(n_patients), before_values,
                s=60, alpha=0.7, edgecolors='black', linewidth=0.5,
                color=COMPARISON["Before"])
    ax3a.axhline(y=np.mean(before_values), color='#333', linestyle='--',
                linewidth=1.5, alpha=0.7, label=f'Mean: {np.mean(before_values):.1f}')
    ax3a.set_ylabel('Measurement (mm)', fontsize=11)
    ax3a.set_xlabel('Patient ID', fontsize=11)
    ax3a.set_title('Preoperative', fontsize=12, fontweight='bold', pad=10)
    ax3a.set_ylim(20, 90)
    ax3a.legend(frameon=True, loc='upper right', fontsize=8)
    ax3a.grid(True, alpha=0.3, axis='y')

    # After
    ax3b.scatter(range(n_patients), after_values,
                s=60, alpha=0.7, edgecolors='black', linewidth=0.5,
                color=COMPARISON["After"])
    ax3b.axhline(y=np.mean(after_values), color='#333', linestyle='--',
                linewidth=1.5, alpha=0.7, label=f'Mean: {np.mean(after_values):.1f}')
    ax3b.set_ylabel('Measurement (mm)', fontsize=11)
    ax3b.set_xlabel('Patient ID', fontsize=11)
    ax3b.set_title('6 Months Postoperative', fontsize=12, fontweight='bold', pad=10)
    ax3b.set_ylim(20, 90)
    ax3b.legend(frameon=True, loc='upper right', fontsize=8)
    ax3b.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    example3_fig = fig3
    return after_values, ax3a, ax3b, before_values, example3_fig, fig3, n_patients


@app.cell
def _(example3_fig, mo):
    mo.vstack([
        example3_fig,
        mo.md("""
        **Key Features:**
        - Comparison color palette (warm gray vs. clinical teal)
        - Identical y-axis scales (PRS requirement)
        - Mean lines with values
        - Individual data points visible
        - **PRS Requirement**: When using patient photos, ensure identical size, lighting, and position
        """)
    ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ### 4. Box Plot Distribution

        Showing variability and central tendency across treatment groups.
        """
    )
    return


@app.cell
def _(CLINICAL_DATA, apply_prs_style, np, plt):
    # Example 4: Box plots
    apply_prs_style(cycle="clinical")

    fig4, ax4 = plt.subplots(figsize=(8, 6))

    # Generate sample data
    np.random.seed(123)
    group_a = np.random.normal(68, 12, 50)
    group_b = np.random.normal(78, 10, 50)
    group_c = np.random.normal(85, 8, 50)

    data_groups = [group_a, group_b, group_c]
    positions = [1, 2, 3]

    bp = ax4.boxplot(data_groups, positions=positions, widths=0.6,
                     patch_artist=True, showfliers=True,
                     boxprops=dict(linewidth=1.5),
                     medianprops=dict(color='black', linewidth=2),
                     whiskerprops=dict(linewidth=1.5),
                     capprops=dict(linewidth=1.5))

    # Color boxes
    colors = [CLINICAL_DATA["Primary"], CLINICAL_DATA["Secondary"], CLINICAL_DATA["Tertiary"]]
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax4.set_xlabel('Treatment Group', fontsize=11)
    ax4.set_ylabel('Outcome Score', fontsize=11)
    ax4.set_title('Treatment Group Comparison', fontsize=13, fontweight='bold', pad=15)
    ax4.set_xticks(positions)
    ax4.set_xticklabels(['Group A\n(n=50)', 'Group B\n(n=50)', 'Group C\n(n=50)'])
    ax4.set_ylim(35, 110)
    ax4.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax4.set_axisbelow(True)

    # Add statistical annotation
    y_max = 100
    ax4.plot([1, 2], [y_max, y_max], 'k-', linewidth=1.5)
    ax4.text(1.5, y_max + 2, '**', ha='center', fontsize=14)
    ax4.text(1.5, y_max + 5, 'p < 0.01', ha='center', fontsize=8, style='italic')

    plt.tight_layout()

    example4_fig = fig4
    return ax4, bp, colors, data_groups, example4_fig, fig4, group_a, group_b, group_c, patch, positions, y_max


@app.cell
def _(example4_fig, mo):
    mo.vstack([
        example4_fig,
        mo.md("""
        **Key Features:**
        - Box plots show distribution (median, quartiles, outliers)
        - Clinical data palette (professional blues/tans)
        - Statistical comparison brackets
        - Sample sizes clearly labeled
        - **Interpretation**: Box = IQR (25th-75th percentile), Line = Median, Whiskers = 1.5×IQR
        """)
    ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 🎯 PRS Compliance Features

        ### Automatic Enforcement

        The package automatically ensures your figures meet all PRS requirements:
        """
    )
    return


@app.cell
def _(mo):
    # Create compliance table
    compliance_data = {
        "Requirement": [
            "Resolution",
            "Color Mode",
            "Minimum Width",
            "File Formats",
            "Multi-Panel",
            "Before/After Sizing",
            "Professional Quality"
        ],
        "PRS Standard": [
            "300 DPI minimum",
            "CMYK for print",
            "3.25\" (photos) / 5\" (graphs)",
            "TIFF, PNG, JPEG, PDF, EPS",
            "Separate files (1a, 1b, 1c)",
            "Identical dimensions",
            "High quality, proper lighting"
        ],
        "How Package Handles It": [
            "`save_prs_figure(dpi=300)` - automatic",
            "`save_prs_figure(cmyk=True)` - automatic",
            "Validated automatically",
            "All supported",
            "`save_multi_panel_figure()` creates separate files",
            "`create_before_after_figure()` validates sizing",
            "Professional styling defaults"
        ],
        "Status": [
            "✅ Automatic",
            "✅ Automatic",
            "✅ Validated",
            "✅ Supported",
            "✅ Automatic",
            "✅ Validated",
            "⚠️ User ensures quality"
        ]
    }

    compliance_df = mo.ui.table(
        compliance_data,
        selection=None,
        label="PRS Compliance Matrix"
    )

    mo.vstack([
        mo.md("### PRS Requirements Compliance Matrix"),
        compliance_df,
        mo.md("""
        **Legend:**
        - ✅ **Automatic**: Package enforces automatically
        - ⚠️ **User**: User responsible (package provides guidance)
        """)
    ])
    return (compliance_data,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ### Code Example: Saving PRS-Compliant Figure

        ```python
        from prs_dataviz import apply_prs_style, save_prs_figure
        import matplotlib.pyplot as plt

        # 1. Apply styling
        apply_prs_style(cycle="clinical", show_grid=True)

        # 2. Create figure
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(['A', 'B', 'C'], [75, 82, 88])
        ax.set_ylabel('Outcome Score (%)')

        # 3. Save PRS-compliant
        save_prs_figure(
            fig,
            "figure1.tiff",
            dpi=300,              # PRS minimum
            width_inches=5.0,     # 5" for graphs, 3.25" for photos
            cmyk=True             # Print-ready
        )

        # 4. Validate before submission
        from prs_dataviz import validate_figure_file
        results = validate_figure_file("figure1.tiff")
        print("✓ Valid!" if results['valid'] else "Issues:", results['issues'])
        ```

        **Result**: A TIFF file meeting all PRS requirements, ready for journal submission.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## ♿ Accessibility Features

        Following [Cara Thompson's 10-step methodology](https://www.cararthompson.com/talks/on-brand-accessibility/):

        ### 1. Colorblind-Friendly Palettes

        All palettes tested for:
        - **Deuteranopia** (most common, red-green)
        - **Protanopia** (red-green)
        - **Tritanopia** (blue-yellow)

        ### 2. WCAG 2.1 Contrast Compliance

        - **Text**: 4.5:1 minimum contrast ratio
        - **Graphics**: 3:1 minimum contrast ratio
        - **Large text**: 3:1 minimum contrast ratio

        ### 3. Neurodivergent-Friendly Design

        - **Muted colors** reduce sensory overwhelm
        - **Clear hierarchy** aids comprehension
        - **Consistent spacing** reduces cognitive load
        - **Professional fonts** optimize readability

        ### 4. Universal Design

        - **High contrast** for low vision
        - **Clear labels** for screen readers
        - **Alternative text** support
        - **Semantic color use** (not color-only information)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 📦 Package Usage

        ### Installation

        ```bash
        # Using uv (recommended - 10-100x faster)
        uv pip install -e .

        # Or using pip
        pip install -e .
        ```

        ### Quick Start

        ```python
        from prs_dataviz import (
            apply_prs_style,
            save_prs_figure,
            create_before_after_figure,
            validate_figure_file,
        )

        # Apply professional medical styling
        apply_prs_style(cycle="clinical")

        # Create your figure
        fig, ax = plt.subplots()
        # ... your plotting code ...

        # Save PRS-compliant
        save_prs_figure(fig, "figure1.tiff", dpi=300, width_inches=5.0, cmyk=True)

        # Validate before submission
        results = validate_figure_file("figure1.tiff")
        ```

        ### Color Palette Selection

        ```python
        # For statistical data
        apply_prs_style(cycle="clinical")

        # For before/after comparisons
        apply_prs_style(cycle="comparison")

        # For general multi-category data
        apply_prs_style(cycle="default")
        ```

        ### Multi-Panel Figures (PRS Requirement)

        ```python
        from prs_dataviz import save_multi_panel_figure

        # Create panels
        fig_a, ax_a = plt.subplots()
        # ... plot panel a ...

        fig_b, ax_b = plt.subplots()
        # ... plot panel b ...

        # Save as separate files (PRS requirement)
        save_multi_panel_figure(
            {"a": fig_a, "b": fig_b},
            "Figure1",  # Creates Figure1a.tiff, Figure1b.tiff
            dpi=300,
            width_inches=3.5
        )
        ```
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## 📚 Resources

        ### Package Documentation
        - **Quick Start**: `QUICK_START.md` - Copy-paste templates
        - **Handoff Document**: `HANDOFF_DOCUMENT.md` - Complete usage guide
        - **README**: `README.md` - Comprehensive reference
        - **Examples**: `example.py` - Working code

        ### External References
        - [PRS Author Guidelines](https://journals.lww.com/plasreconsurg/pages/informationforauthors.aspx)
        - [PRS Digital Artwork Guide](http://links.lww.com/ES/A42)
        - [Cara Thompson: On-Brand Accessibility](https://www.cararthompson.com/talks/on-brand-accessibility/)
        - [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

        ### Design System Credits
        - **Methodology**: Cara Thompson's 10-step accessible dataviz process
        - **Aesthetic**: Du Bois-inspired color palettes and styling
        - **Approach**: Ophelia package's progressive documentation model

        ---

        ## 🎉 Summary

        This package streamlines the journey from data to publication-quality figures while ensuring:

        - ✅ **Automatic PRS compliance** (300 DPI, CMYK, proper sizing)
        - ✅ **Professional medical aesthetics** (clinical color palettes)
        - ✅ **Accessibility** (colorblind-friendly, WCAG 2.1 compliant)
        - ✅ **Time savings** (2-3 hours per figure)
        - ✅ **Reproducibility** (code-based figures)

        **Start creating professional medical visualizations today!**

        ```bash
        uv run python example.py  # See it in action
        ```
        """
    )
    return


if __name__ == "__main__":
    app.run()
