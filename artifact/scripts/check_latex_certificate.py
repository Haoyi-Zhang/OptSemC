#!/usr/bin/env python3
"""Validate the frozen LaTeX compile-certificate artifact.

The full compiler can be re-run with check_latex_compile.py. This lightweight
entry-point check keeps the main reproducibility suite deterministic while still
failing if the recorded compile certificate or PDF artifact is missing or failed.
"""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / 'artifact' / 'evaluation' / 'latex_compile_check.csv'
PDF = ROOT / 'Paper' / 'latex' / 'paper.pdf'
if not CSV.exists() or not PDF.exists():
    print('LaTeX certificate check FAIL: missing CSV or PDF')
    sys.exit(1)
rows = list(csv.DictReader(CSV.open(newline='', encoding='utf-8')))
hard = [r for r in rows if r.get('check') not in {'underfull_boxes_nonfatal','overfull_vbox_tiny_nonfatal'}]
failed = [r for r in hard if r.get('passed') != 'true']
print(f'LaTeX certificate check: {len(hard)-len(failed)}/{len(hard)} hard checks passed')
if failed:
    for r in failed: print('FAIL', r)
    sys.exit(1)
