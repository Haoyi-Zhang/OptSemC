#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT/'evaluation'
OUT = E/'integrity_suite.csv'
checks = [
 'package_cleanliness','package_manifest_check','package_integrity','format_compliance','visual_latex_style','manuscript_style','latex_compile_check','pdf_integrity','reference_quality','paper_quality','paper_table_renderers','paper_table_source_check',
 'data_contracts_check','claim_evidence_graph_check','projection_resolution_check','projection_frontier_antichain_check','projection_information_profile_check','proof_carrying_semantics_check','formal_obligations_check',
 'side_balanced_witness_support_check','source_witness_support_check','guard_quality_check','feature_holdout_repair_check','scalability_stress_check','engine_family_stress_check','artifact_registry_check','repository_quality_check','package_snapshot_check'
]
def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f: return list(csv.DictReader(f))
def cert(path: Path):
    if not path.exists(): return False,'missing'
    rows=read_csv(path); passable=[r for r in rows if 'passed' in r or 'status' in r or 'ok' in r]
    def ok(r):
        return r.get('passed','').lower()=='true' or r.get('status','').upper()=='PASS' or r.get('ok','').lower()=='true'
    failed=[r for r in passable if not ok(r)]
    return bool(passable) and not failed, f'{len(passable)-len(failed)}/{len(passable)}'
rows=[]
for name in checks:
    ok, detail=cert(E/f'{name}.csv')
    rows.append({'check':name,'passed':str(ok).lower(),'details':detail})
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
failed=[r for r in rows if r['passed']!='true']
print(f'Grounded integrity suite: {len(rows)-len(failed)}/{len(rows)} passed')
for r in failed: print('FAIL', r)
sys.exit(1 if failed else 0)
