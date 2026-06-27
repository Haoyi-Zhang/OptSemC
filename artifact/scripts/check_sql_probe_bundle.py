#!/usr/bin/env python3
"""Validate the exported SQL bundle and manifest."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evaluation" / "sql_probe_bundle_check.csv"
summary_path = ROOT / "evaluation" / "sql_probe_bundle_summary.csv"
manifest_path = ROOT / "benchmark" / "sql_bundle" / "full_probe_manifest.csv"
bundle_path = ROOT / "benchmark" / "sql_bundle" / "full_probe_bundle.sql"
rep_dir = ROOT / "benchmark" / "sql_bundle" / "representative"
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
summary = {}
if summary_path.exists():
    with summary_path.open(newline='', encoding='utf-8') as f:
        summary = {r['metric']: r['value'] for r in csv.DictReader(f)}
manifest = []
if manifest_path.exists():
    with manifest_path.open(newline='', encoding='utf-8') as f:
        manifest = list(csv.DictReader(f))
add('manifest_has_all_generated_probes', len(manifest) == 4216, f'rows={len(manifest)}')
add('bundle_summary_matches_manifest', summary.get('generated_probe_sql_queries') == str(len(manifest)), summary)
add('representative_sql_cover_present', rep_dir.is_dir() and len(list(rep_dir.glob('*.sql'))) >= 25, f"files={len(list(rep_dir.glob('*.sql'))) if rep_dir.exists() else 0}")
add('shape_check_has_zero_invalid_queries', summary.get('shape_invalid_queries') == '0', f"invalid={summary.get('shape_invalid_queries')}")
try:
    text = bundle_path.read_text(encoding='utf-8')
    add('raw_full_sql_bundle_readable', text.count('OptSemBench-C probe') == 4216 and len(text) > 100000, f"markers={text.count('OptSemBench-C probe')};chars={len(text)}")
except Exception as exc:
    add('raw_full_sql_bundle_readable', False, type(exc).__name__)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"SQL probe bundle check: {passed}/{len(rows)} passed")
if passed != len(rows):
    for r in rows:
        if r['passed'] != 'true': print('FAIL', r)
    sys.exit(1)
