#!/usr/bin/env python3
"""Compute counterfactual repair ablations for headline false witnesses."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.corpus import load_contract_maps
from optsemc.projections import false_equivalence_witnesses
from optsemc.repair import repairs_all
from optsemc.io import write_csv
cm=load_contract_maps(ART)
methods=('keyword','yesno','operator_only')
fields=('operator','kind','variant','layer','placement','decision_time','observability','state')
rows=[]
for method in methods:
    wit=false_equivalence_witnesses(cm.maps, cm.engines, cm.probes, method)
    for field in fields:
        resolved=sum(1 for w in wit if repairs_all([w], cm.maps, (field,)))
        rows.append({'scope':method,'field_set':field,'witnesses':str(len(wit)),'resolved':str(resolved),'unresolved':str(len(wit)-resolved),'resolved_rate':f'{resolved/len(wit) if wit else 1.0:.6f}'})
all_w=[]
for method in methods:
    all_w.extend(false_equivalence_witnesses(cm.maps, cm.engines, cm.probes, method))
for combo in [('layer','placement'),('operator','kind','layer','placement','observability'),('layer',),('placement',)]:
    resolved=sum(1 for w in all_w if repairs_all([w], cm.maps, combo))
    rows.append({'scope':'all_headline','field_set':'+'.join(combo),'witnesses':str(len(all_w)),'resolved':str(resolved),'unresolved':str(len(all_w)-resolved),'resolved_rate':f'{resolved/len(all_w) if all_w else 1.0:.6f}'})
write_csv(ART/'evaluation'/'counterfactual_repair_ablation.csv', rows, ['scope','field_set','witnesses','resolved','unresolved','resolved_rate'])
print(f"Counterfactual repair ablation: {len(rows)} rows")

