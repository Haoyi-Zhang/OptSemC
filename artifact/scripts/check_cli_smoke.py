#!/usr/bin/env python3
"""Smoke-test the public optsemc command-line interface."""
from __future__ import annotations
import subprocess, sys, csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifact'/'evaluation'/'cli_smoke_check.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':details})
def run(args):
    return subprocess.run([sys.executable,'-m','optsemc.cli','--root',str(ROOT),*args], cwd=ROOT/'artifact', text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
for name,args,needle in [('summary',['summary'],'engines'),('metrics',['metrics','--projection','keyword'],'false_equivalences'),('manifest',['manifest','--summary'],'fingerprint'),('contracts',['contracts'],'grounded_rules'),('claim_graph',['claim-graph'],'claims')]:
    try:
        p=run(args)
        add(f'{name}_command', p.returncode==0 and needle in p.stdout, p.stdout.splitlines()[0] if p.stdout else '')
    except Exception as exc:
        add(f'{name}_command', False, type(exc).__name__)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"CLI smoke check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)

