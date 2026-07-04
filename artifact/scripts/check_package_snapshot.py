#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT.parent
E = ROOT/'evaluation'
OUT = E/'package_snapshot_check.csv'
ARTIFACT_ONLY = not (PKG/'Paper').exists()
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f: return list(csv.DictReader(f))
def cert_pass(path: Path) -> tuple[bool,str]:
    if not path.exists(): return False,'missing'
    try: rows=read_csv(path)
    except Exception as e: return False,type(e).__name__
    passable=[r for r in rows if any(k in r for k in ('passed','status','ok'))]
    def okrow(r):
        if 'passed' in r: return r.get('passed','').lower()=='true'
        if 'status' in r: return r.get('status','').upper()=='PASS'
        if 'ok' in r: return r.get('ok','').lower()=='true'
        return False
    failed=[r for r in passable if not okrow(r)]
    return bool(passable) and not failed, f'{len(passable)-len(failed)}/{len(passable)}'
required = [
 ROOT/'grounded/verified_rules.jsonl', ROOT/'grounded/verified_segments.jsonl', ROOT/'grounded/verified_sources.csv',
 ROOT/'benchmark/generated_probes.jsonl', ROOT/'evaluation/grounded_contract_maps.jsonl',
 E/'grounded/baseline_portfolio.csv', E/'grounded/conditional_trap_rate.csv', E/'grounded/repair_certificate_summary.csv', E/'grounded/repair_basis_stability.csv',
 E/'projection_resolution_lattice.csv', E/'projection_frontier_antichains.csv', E/'side_balanced_witness_support.csv', E/'claim_evidence_graph.csv', E/'repository_audit.csv', E/'repository_quality.csv',
 ROOT/'config/practice_projection_surfaces.csv', E/'practice_projection_surfaces.csv', E/'practice_projection_surface_summary.csv', E/'practice_projection_surfaces_check.csv',
 E/'real_engine_validation_environment.csv', E/'environment.csv', E/'environment_check.csv', E/'git_tree_state.csv', E/'git_tree_porcelain.txt', E/'git_tree_state_check.csv',
 E/'grounded/repair_generalization_folds.csv', E/'grounded/repair_generalization_summary.csv', E/'repair_generalization_check.csv'
]
if not ARTIFACT_ONLY:
    required += [PKG/'Paper/latex/paper.tex', PKG/'Paper/latex/paper.pdf', PKG/'Paper/supplemental/supplement.pdf']
missing=[str(p.relative_to(PKG)) for p in required if not p.exists()]
add('required_outputs_present', not missing, ';'.join(missing[:20]))
try:
    rules=sum(1 for line in (ROOT/'grounded/verified_rules.jsonl').open(encoding='utf-8') if line.strip())
    segs=sum(1 for line in (ROOT/'grounded/verified_segments.jsonl').open(encoding='utf-8') if line.strip())
    srcs=len(read_csv(ROOT/'grounded/verified_sources.csv'))
    add('grounded_counts', rules==287 and segs==287 and srcs==26, f'{rules}/{segs}/{srcs}')
except Exception as e: add('grounded_counts', False, type(e).__name__)
try:
    probes=sum(1 for line in (ROOT/'benchmark/generated_probes.jsonl').open(encoding='utf-8') if line.strip())
    add('probe_count', probes==4216, probes)
except Exception as e: add('probe_count', False, type(e).__name__)
try:
    bp={r['projection']:r for r in read_csv(E/'grounded/baseline_portfolio.csv')}
    add('baseline_headline_counts', int(bp['keyword']['false_equivalences'])==254 and int(bp['operator_only']['false_equivalences'])==238 and int(bp['strict']['false_equivalences'])==0, '')
except Exception as e: add('baseline_headline_counts', False, type(e).__name__)
try:
    sb=read_csv(E/'side_balanced_witness_support_check.csv')
    add('side_balanced_witness_support', bool(sb) and all(r.get('passed')=='true' for r in sb), f'{sum(r.get("passed")=="true" for r in sb)}/{len(sb)}')
except Exception as e: add('side_balanced_witness_support', False, type(e).__name__)
certificate_names = ['package_integrity','claim_evidence_graph_check','data_contracts_check','projection_resolution_check','projection_frontier_antichain_check','package_manifest_check','repository_quality_check','artifact_registry_check','practice_projection_surfaces_check','real_engine_validation_check','environment_check','git_tree_state_check','repair_generalization_check','claim_ledger_check','certificate_freshness_check']
if not ARTIFACT_ONLY:
    certificate_names += ['format_compliance','manuscript_style','latex_compile_check','pdf_integrity','reference_quality','paper_table_source_check']
for name in certificate_names:
    path=E/f'{name}.csv'
    ok, detail=cert_pass(path)
    add(f'certificate:{name}', ok, detail)
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
failed=[r for r in rows if r['passed']!='true']
print(f'Package snapshot check: {len(rows)-len(failed)}/{len(rows)} passed')
for r in failed: print('FAIL', r)
sys.exit(1 if failed else 0)
