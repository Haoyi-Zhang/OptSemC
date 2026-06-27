#!/usr/bin/env python3
"""Compute a mutation suite over projection vocabularies.

For baseline projections we reuse the canonical baseline portfolio. For singleton
repair mutations, false equivalence under a refined projection is exactly the set
of original false witnesses not separated by the restored field; refinement
cannot introduce false equivalences or false differences.
"""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.corpus import load_contract_maps
from optsemc.projections import false_equivalence_witnesses
from optsemc.repair import repairs_all
from optsemc.io import write_csv, read_csv
FIELDNAMES=['projection','comparisons','projected_equivalences','true_equivalences','false_equivalences','false_differences','projected_equivalence_rate','conditional_false_equivalence_rate','exact_equivalence_rate','mutation_class']
base_rows=[]
for row in read_csv(ART/'evaluation'/'grounded'/'baseline_portfolio.csv'):
    base_rows.append({
        'projection': row['projection'],
        'comparisons': row['comparisons'],
        'projected_equivalences': row['projected_equivalences'],
        'true_equivalences': row['true_equivalences'],
        'false_equivalences': row['false_equivalences'],
        'false_differences': row.get('false_differences','0'),
        'projected_equivalence_rate': row['projected_equivalence_rate'],
        'conditional_false_equivalence_rate': row['conditional_false_equivalence_rate'],
        'exact_equivalence_rate': f"{int(row['true_equivalences'])/int(row['comparisons']) if int(row['comparisons']) else 0.0:.6f}",
        'mutation_class': 'projection_baseline',
    })
cm=load_contract_maps(ART)
comparisons=int(base_rows[0]['comparisons']) if base_rows else 0
true_eq=int(next(r['true_equivalences'] for r in base_rows if r['projection']=='strict'))
rows=list(base_rows)
for base in ('keyword','yesno','operator_only'):
    witnesses=false_equivalence_witnesses(cm.maps, cm.engines, cm.probes, base)
    for field in ('operator','kind','variant','layer','placement','decision_time','observability','state'):
        false_eq=sum(1 for w in witnesses if not repairs_all([w], cm.maps, (field,)))
        projected=true_eq+false_eq
        rows.append({
            'projection': f'{base}+{field}',
            'comparisons': str(comparisons),
            'projected_equivalences': str(projected),
            'true_equivalences': str(true_eq),
            'false_equivalences': str(false_eq),
            'false_differences': '0',
            'projected_equivalence_rate': f'{projected/comparisons if comparisons else 0.0:.6f}',
            'conditional_false_equivalence_rate': f'{false_eq/projected if projected else 0.0:.6f}',
            'exact_equivalence_rate': f'{true_eq/comparisons if comparisons else 0.0:.6f}',
            'mutation_class': 'singleton_repair',
        })
write_csv(ART/'evaluation'/'projection_mutation_suite.csv', rows, FIELDNAMES)
print(f"Projection mutation suite: {len(rows)} projections")
