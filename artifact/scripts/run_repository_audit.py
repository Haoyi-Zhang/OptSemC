#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'artifact'))
from optsemc.repository import repository_audit, score_row
EVAL = ROOT/'artifact'/'evaluation'
checks = repository_audit(ROOT)
EVAL.mkdir(parents=True, exist_ok=True)
with (EVAL/'repository_audit.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','score','weight','details']); w.writeheader(); w.writerows([c.as_row() for c in checks])
with (EVAL/'repository_quality.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['metric','score','max_score','percent','passed']); w.writeheader(); w.writerow(score_row(checks))
print('Repository audit: generated')
