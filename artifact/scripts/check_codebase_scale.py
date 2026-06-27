#!/usr/bin/env python3
"""Check that the repository has substantial implementation depth without transient bloat."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'artifact'))
from optsemc.repository import python_loc, public_classes_and_functions, python_files
from optsemc.manifest import transient_files
OUT=ROOT/'artifact'/'evaluation'/'codebase_scale_check.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
loc=python_loc(ROOT)
classes, funcs=public_classes_and_functions(ROOT)
files=python_files(ROOT)
add('python_loc_substantial', loc>=20000, f'loc={loc}')
add('public_api_substantial', classes>=55 and funcs>=250, f'classes={classes};functions={funcs}')
add('python_file_surface_substantial', len(files)>=180, f'files={len(files)}')
add('no_transient_bloat', not transient_files(ROOT), ';'.join(transient_files(ROOT)[:5]))
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"Codebase scale check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)

