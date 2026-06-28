#!/usr/bin/env python3
"""Compute exact-distance severity for projection-induced false equivalence."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_contract_maps
from optsemc.io import write_csv
from optsemc.severity import false_equivalence_severity

METHODS = [
    'keyword', 'yesno', 'operator_only', 'kind_only', 'layer_only',
    'placement_only', 'decision_time_only', 'observability_only',
    'state_only', 'operator_kind_surface'
]
cm = load_contract_maps(ROOT)
rows = [false_equivalence_severity(cm.maps, cm.engines, cm.probes, method).as_row() for method in METHODS]
write_csv(ROOT / 'evaluation' / 'false_equivalence_severity.csv', rows)
# Paper-facing subset.
keep = {'keyword', 'yesno', 'operator_only', 'placement_only', 'state_only', 'operator_kind_surface'}
paper_rows = [row for row in rows if row['projection'] in keep]
write_csv(ROOT / 'evaluation' / 'false_equivalence_severity_paper.csv', paper_rows)
print(f"False-equivalence severity: {sum(int(r['false_equivalences']) for r in rows)} false witnesses summarized over {len(rows)} projections")
