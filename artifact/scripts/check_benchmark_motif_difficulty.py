#!/usr/bin/env python3
"""Check motif difficulty summaries."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evaluation" / "benchmark_motif_difficulty_check.csv"
SRC = ROOT / "evaluation" / "benchmark_motif_difficulty.csv"
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
with SRC.open(newline='', encoding='utf-8') as f:
    data=list(csv.DictReader(f))
add('motif_difficulty_covers_eight_or_more_suites', len(data) >= 8, f'suites={len(data)}')
add('all_suites_have_nonzero_motifs', all(int(r['motifs']) > 0 for r in data), '')
add('difficulty_contains_sparse_motifs', sum(int(r['sparse_motifs_le_5']) for r in data) > 0, '')
add('difficulty_contains_redundant_motifs', any(int(r['max_matching_probes']) >= 100 for r in data), '')
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"Benchmark motif difficulty check: {passed}/{len(rows)} passed")
if passed != len(rows):
    for r in rows:
        if r['passed'] != 'true': print('FAIL', r)
    sys.exit(1)
