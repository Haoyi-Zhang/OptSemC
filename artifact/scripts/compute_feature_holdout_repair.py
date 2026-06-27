#!/usr/bin/env python3
"""Compute feature-family held-out repair stability."""
from __future__ import annotations
import csv
import sys
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_contract_maps, load_probe_objects
from optsemc.repair_stability import evaluate_feature_holdout

E = ROOT / 'evaluation'

def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

cm = load_contract_maps(ROOT)
probes = load_probe_objects(ROOT)
rows = evaluate_feature_holdout(cm, probes)
detail = [
    {
        'method': r.method,
        'heldout_feature_family': r.fold,
        'train_false_equivalences': r.train_false,
        'heldout_false_equivalences': r.heldout_false,
        'learned_minimum_repair': '+'.join(r.learned_repair) if r.learned_repair else 'none',
        'learned_minimum_unresolved': r.learned_unresolved,
        'robust_basis': '+'.join(r.robust_repair),
        'robust_basis_unresolved': r.robust_unresolved,
    }
    for r in rows
]
write_csv(E/'feature_holdout_repair.csv', detail, ['method','heldout_feature_family','train_false_equivalences','heldout_false_equivalences','learned_minimum_repair','learned_minimum_unresolved','robust_basis','robust_basis_unresolved'])
by_method = defaultdict(list)
for r in rows: by_method[r.method].append(r)
summary=[]
for method, vals in sorted(by_method.items()):
    summary.append({
        'method': method,
        'folds': len(vals),
        'train_false_equivalences_total': sum(v.train_false for v in vals),
        'heldout_false_equivalences_total': sum(v.heldout_false for v in vals),
        'folds_with_learned_minimum_failure': sum(1 for v in vals if v.learned_unresolved),
        'learned_minimum_unresolved_total': sum(v.learned_unresolved for v in vals),
        'robust_basis': '+'.join(vals[0].robust_repair) if vals else 'layer+placement',
        'robust_basis_unresolved_total': sum(v.robust_unresolved for v in vals),
        'max_heldout_false_equivalences': max((v.heldout_false for v in vals), default=0),
    })
write_csv(E/'feature_holdout_repair_summary.csv', summary, ['method','folds','train_false_equivalences_total','heldout_false_equivalences_total','folds_with_learned_minimum_failure','learned_minimum_unresolved_total','robust_basis','robust_basis_unresolved_total','max_heldout_false_equivalences'])
paper=[]
for row in summary:
    paper.append({
        'projection': row['method'],
        'heldout_folds': row['folds'],
        'heldout_false_equivalences': row['heldout_false_equivalences_total'],
        'point_minimum_unresolved': row['learned_minimum_unresolved_total'],
        'robust_basis': row['robust_basis'],
        'robust_unresolved': row['robust_basis_unresolved_total'],
    })
write_csv(E/'feature_holdout_repair_paper.csv', paper, ['projection','heldout_folds','heldout_false_equivalences','point_minimum_unresolved','robust_basis','robust_unresolved'])
print(f'Feature-holdout repair: {sum(int(r["robust_basis_unresolved_total"]) for r in summary)} unresolved under robust basis across {sum(int(r["folds"]) for r in summary)} folds')
