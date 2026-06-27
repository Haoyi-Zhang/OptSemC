#!/usr/bin/env python3
"""Compute differential reproducibility rows."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "artifact"))
from optsemc.differential import run_differential_reproducibility
from optsemc.io import write_csv
E = ROOT / "artifact" / "evaluation"
rows = run_differential_reproducibility(ROOT)
write_csv(E / "differential_reproducibility.csv", [row.as_row() for row in rows], ["claim", "frozen_value", "recomputed_value", "method", "passed", "details"])
print(f"Differential reproducibility: {sum(row.passed for row in rows)}/{len(rows)} passed")
