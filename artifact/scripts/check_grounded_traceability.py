#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'evaluation/grounded_claim_traceability.csv'
missing=[]
with path.open(newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        for rel in r['artifact_support'].split(';'):
            rel=rel.strip()
            if rel and not (ROOT.parent/rel).exists():
                missing.append((r['claim_id'],rel))
if missing:
    print('Missing grounded traceability targets:')
    for m in missing: print(m)
    sys.exit(1)
print('Grounded traceability check passed')
