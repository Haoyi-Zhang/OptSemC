#!/usr/bin/env python3
"""Compute projection and repair metamorphic tests."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "artifact"))
from optsemc.corpus import load_contract_maps
from optsemc.projections import false_equivalence_witnesses
from optsemc.metamorphic import run_projection_metamorphic_suite
from optsemc.io import write_csv
E = ROOT / "artifact" / "evaluation"
cm = load_contract_maps(ROOT / "artifact")
witnesses = []
for method in ("keyword", "yesno", "operator_only"):
    witnesses.extend(false_equivalence_witnesses(cm.maps, cm.engines, cm.probes, method))
rows = run_projection_metamorphic_suite(cm.maps, cm.engines, cm.probes, witnesses)
write_csv(E / "metamorphic_projection_tests.csv", [row.as_row() for row in rows], ["test", "projection", "pairs_checked", "violations", "passed", "details"])
print(f"Metamorphic projection tests: {sum(row.passed for row in rows)}/{len(rows)} passed")
