#!/usr/bin/env python3
"""Check deep provenance audit outputs."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'provenance_deep_audit_check.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
audit=ART/'evaluation'/'provenance_deep_audit.csv'
edges=ART/'evaluation'/'provenance_graph_edges.csv'
if audit.exists():
    data=list(csv.DictReader(audit.open(newline='', encoding='utf-8')))
    add('audit_has_no_issues', len(data)==1 and data[0].get('kind')=='none', str(data[:3]))
else:
    add('audit_has_no_issues', False, 'missing')
if edges.exists():
    e=list(csv.DictReader(edges.open(newline='', encoding='utf-8')))
    add('evidence_dag_edges_present', len(e)==574, str(len(e)))
    add('rule_to_segment_edges_present', sum(1 for r in e if r['edge']=='grounded_by')==287, '')
    add('segment_to_source_edges_present', sum(1 for r in e if r['edge']=='extracted_from')==287, '')
else:
    for name in ['evidence_dag_edges_present','rule_to_segment_edges_present','segment_to_source_edges_present']:
        add(name, False, 'missing')
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"Provenance deep audit check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)

