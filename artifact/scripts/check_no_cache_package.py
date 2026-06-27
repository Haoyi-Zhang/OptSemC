#!/usr/bin/env python3
"""Ensure the two-folder package has no duplicate gzip cache payloads."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evaluation' / 'no_cache_package_check.csv'
gz = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*.gz'))
required_raw = [
    ROOT/'benchmark/generated_probes.jsonl',
    ROOT/'benchmark/sql_bundle/full_probe_bundle.sql',
    ROOT/'evaluation/grounded_applicable_rules.jsonl',
    ROOT/'evaluation/grounded_contract_maps.jsonl',
    ROOT/'evaluation/grounded_contract_support.jsonl',
]
rows=[
    {'check':'no_gzip_cache_payloads', 'passed':str(len(gz)==0).lower(), 'details':'|'.join(gz[:10])},
    {'check':'required_raw_outputs_present', 'passed':str(all(p.exists() for p in required_raw)).lower(), 'details':'|'.join(str(p.relative_to(ROOT)) for p in required_raw if not p.exists())},
]
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"No-cache package check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r)
if passed != len(rows): sys.exit(1)
