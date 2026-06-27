#!/usr/bin/env python3
"""Compute engine-pair false-portability matrices for headline projections."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.corpus import load_contract_maps
from optsemc.metrics import engine_pair_matrix
from optsemc.io import write_csv
cm=load_contract_maps(ART)
rows=[]
for method in ('keyword','yesno','operator_only'):
    rows.extend(engine_pair_matrix(cm.maps, cm.engines, cm.probes, method))
write_csv(ART/'evaluation'/'engine_pair_false_portability_matrix.csv', rows, ['projection','engine_left','engine_right','comparisons','true_equivalences','projected_equivalences','false_equivalences','false_differences','conditional_false_equivalence_rate'])
print(f"Engine-pair matrix: {len(rows)} rows")

