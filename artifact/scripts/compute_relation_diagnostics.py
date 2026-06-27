#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.corpus import load_contract_maps
from optsemc.projections import project_signature
from optsemc.relations import quotient_statistics
from optsemc.io import write_csv
cm=load_contract_maps(ART)
items=tuple(sorted(cm.maps))
rows=[]
for method in ('strict','keyword','yesno','operator_only','operator_kind_surface'):
    stats=quotient_statistics(items, lambda k: cm.maps[k], lambda k, m=method: project_signature(cm.maps[k], m))
    stats['projection']=method
    rows.append(stats)
write_csv(ART/'evaluation'/'relation_diagnostics.csv', rows, ['projection','items','exact_classes','projected_classes','nontrivial_projected_classes','false_projected_classes','max_projected_class_size'])
print(f'Relation diagnostics: {len(rows)} projections')
