#!/usr/bin/env python3
"""Compute finite algebra/projection proof obligations from the reusable library."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.corpus import load_contract_maps
from optsemc.formal import all_formal_obligations
from optsemc.projections import METHODS
from optsemc.repair import CORE_SEMANTIC_STATE_FREE
from optsemc.io import write_csv
cm=load_contract_maps(ART)
rows=[r.as_row() for r in all_formal_obligations(tuple(cm.maps.values()), METHODS, CORE_SEMANTIC_STATE_FREE)]
write_csv(ART/'evaluation'/'formal_obligations.csv', rows, ['theorem','obligation','passed','details'])
print(f"Formal obligations: {sum(r['passed']=='true' for r in rows)}/{len(rows)} passed")

