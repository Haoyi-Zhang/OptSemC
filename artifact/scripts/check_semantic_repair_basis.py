#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'evaluation/grounded/semantic_repair_basis.csv'
if not path.exists():
    print('missing semantic_repair_basis.csv')
    sys.exit(1)
rows=list(csv.DictReader(path.open()))
by={r['scope']:r for r in rows}
required={'keyword','yesno','operator_only','all_projections'}
missing=required-set(by)
if missing:
    print('missing scopes: '+','.join(sorted(missing)))
    sys.exit(1)
# Regression expectations for the validity-hardened grounded mainline.
if by['keyword']['minimal_semantic_repair_size'] != '1' or 'placement' not in by['keyword']['minimal_semantic_repair_sets']:
    print('keyword semantic repair is not placement-based')
    sys.exit(1)
if by['operator_only']['minimal_semantic_repair_size'] != '1' or 'layer' not in by['operator_only']['minimal_semantic_repair_sets']:
    print('operator-only semantic repair is not layer-based')
    sys.exit(1)
if int(by['all_projections']['minimal_semantic_repair_size']) > 2:
    print('global semantic repair basis exceeds size 2')
    sys.exit(1)

# Engine-pair hotspots should also be repaired by the stable semantic basis.
enginepair = ROOT/'evaluation/grounded/repair_basis_enginepair.csv'
if enginepair.exists():
    erows=list(csv.DictReader(enginepair.open()))
    bad=[r for r in erows if int(r.get('unresolved','1')) != 0 or r.get('basis') != 'layer+placement']
    if bad:
        print('stable semantic basis does not repair all engine-pair hotspots')
        sys.exit(1)
else:
    print('missing repair_basis_enginepair.csv')
    sys.exit(1)
print('Semantic repair basis check passed')
