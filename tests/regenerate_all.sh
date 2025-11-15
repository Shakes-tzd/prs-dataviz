#!/bin/bash
# Regenerate all test plots with new spacing

cd /Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/tests
export PYTHONPATH=/Users/shakes/DevProjects/moreen_njoroge_dataviz_design_system/src

echo "Regenerating comprehensive plots..."
python3 test_comprehensive_plots.py

echo "Regenerating improved significance plots..."
python3 test_improved_significance.py

echo "Regenerating automatic positioning plots..."
python3 test_automatic_positioning.py

echo "All plots regenerated!"
ls -lh visual_tests/
