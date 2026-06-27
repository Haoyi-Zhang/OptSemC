#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'replay_plan_check.csv'
rows=[]
def add(c,o,d=''):
    rows.append({'check':c,'passed':str(bool(o)).lower(),'details':str(d)})
state_file=ART/'evaluation'/'replay_state.csv'
plan=ART/'evaluation'/'replay_plan.csv'
if state_file.exists() and plan.exists():
    r=list(csv.DictReader(state_file.open(newline='', encoding='utf-8'))); p=list(csv.DictReader(plan.open(newline='', encoding='utf-8')))
    add('plan_steps_present', len(p)>=8, len(p))
    add('all_steps_ready', all(x['ready']=='true' for x in r), ';'.join(x['step_id'] for x in r if x['ready']!='true'))
    add('outputs_declared', all(x['outputs'] for x in p), '')
else:
    for c in ['plan_steps_present','all_steps_ready','outputs_declared']: add(c,False,'missing')
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(x['passed']=='true' for x in rows)
print(f'Replay plan check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed!=len(rows): sys.exit(1)
