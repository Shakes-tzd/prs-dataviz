"""
Basic import tests for prs_dataviz package.
"""

import pytest


def test_import_main_module():
    """Test that main module can be imported."""
    import prs_dataviz
    assert prs_dataviz.__version__ == "0.1.0"


def test_import_palettes():
    """Test palette imports."""
    from prs_dataviz import (
        CLINICAL_BLUE,
        TISSUE_TONE,
        CLINICAL_DATA,
        COMPARISON,
        STATISTICAL,
        PRS_DEFAULT_CYCLE,
        PRS_CLINICAL_CYCLE,
        PRS_COMPARISON_CYCLE,
    )

    # Check palettes are dictionaries
    assert isinstance(CLINICAL_BLUE, dict)
    assert isinstance(TISSUE_TONE, dict)
    assert isinstance(CLINICAL_DATA, dict)
    assert isinstance(COMPARISON, dict)
    assert isinstance(STATISTICAL, dict)

    # Check cycles are lists
    assert isinstance(PRS_DEFAULT_CYCLE, list)
    assert isinstance(PRS_CLINICAL_CYCLE, list)
    assert isinstance(PRS_COMPARISON_CYCLE, list)

    # Check cycles have colors
    assert len(PRS_DEFAULT_CYCLE) > 0
    assert len(PRS_CLINICAL_CYCLE) > 0
    assert len(PRS_COMPARISON_CYCLE) > 0


def test_import_style_functions():
    """Test style function imports."""
    from prs_dataviz import (
        apply_prs_style,
        format_statistical_plot,
        format_comparison_plot,
        add_scale_bar,
        prs_legend,
    )

    # Check functions are callable
    assert callable(apply_prs_style)
    assert callable(format_statistical_plot)
    assert callable(format_comparison_plot)
    assert callable(add_scale_bar)
    assert callable(prs_legend)


def test_import_export_functions():
    """Test export function imports."""
    from prs_dataviz import (
        save_prs_figure,
        save_multi_panel_figure,
        validate_figure_file,
        PRS_MIN_DPI,
        PRS_MIN_WIDTH_SINGLE,
        PRS_MIN_WIDTH_GRAPH,
    )

    # Check functions are callable
    assert callable(save_prs_figure)
    assert callable(save_multi_panel_figure)
    assert callable(validate_figure_file)

    # Check constants
    assert PRS_MIN_DPI == 300
    assert PRS_MIN_WIDTH_SINGLE == 3.25
    assert PRS_MIN_WIDTH_GRAPH == 5.0


def test_import_layout_functions():
    """Test layout function imports."""
    from prs_dataviz import (
        create_before_after_figure,
        create_multi_view_figure,
        create_time_series_figure,
        create_results_panel,
    )

    # Check functions are callable
    assert callable(create_before_after_figure)
    assert callable(create_multi_view_figure)
    assert callable(create_time_series_figure)
    assert callable(create_results_panel)


def test_import_color_utilities():
    """Test color utility function imports."""
    from prs_dataviz import rgb_to_cmyk, cmyk_to_rgb

    assert callable(rgb_to_cmyk)
    assert callable(cmyk_to_rgb)

    # Test round-trip conversion
    r, g, b = 0.5, 0.3, 0.7
    c, m, y, k = rgb_to_cmyk(r, g, b)
    r2, g2, b2 = cmyk_to_rgb(c, m, y, k)

    # Should be approximately equal (allowing for floating point errors)
    assert abs(r - r2) < 0.01
    assert abs(g - g2) < 0.01
    assert abs(b - b2) < 0.01
