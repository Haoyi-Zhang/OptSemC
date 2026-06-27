#!/usr/bin/env python3
"""Verify proof-carrying finite semantics certificates."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.certificates import verify_bundle, read_bundle
from optsemc.io import write_csv
OUT=ART/'evaluation'/'proof_carrying_semantics_check.csv'
path=ART/'evaluation'/'proof_carrying_semantics.json'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
add('certificate_bundle_present', path.exists(), str(path.relative_to(ROOT)))
if path.exists():
    ok, issues = verify_bundle(path)
    data=read_bundle(path)
    add('bundle_hash_valid', ok, ';'.join(issues[:5]))
    add('certificate_count', data.get('certificate_count',0) >= 5, str(data.get('certificate_count')))
    scopes=[c.get('scope') or c.get('projection') for c in data.get('certificates',[])]
    add('headline_projections_present', all(x in scopes for x in ['keyword','yesno','operator_only']), str(scopes))
    add('frontier_and_hitting_set_present', 'all_headline' in scopes and scopes.count('all_headline') >= 2, str(scopes))
else:
    for name in ['bundle_hash_valid','certificate_count','headline_projections_present','frontier_and_hitting_set_present']:
        add(name, False, 'missing')
write_csv(OUT, rows, ['check','passed','details'])
passed=sum(r['passed']=='true' for r in rows)
print(f"Proof-carrying semantics check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)

