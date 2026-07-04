#!/usr/bin/env python3
from __future__ import annotations
import csv, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT/'evaluation'
OUT = E/'integrity_suite.csv'
ARTIFACT_ONLY = not (ROOT.parent/'Paper').exists()
checks = [
 'package_cleanliness','package_manifest_check','package_integrity','format_compliance','visual_latex_style','manuscript_style','latex_compile_check','pdf_integrity','reference_quality','paper_quality','paper_table_renderers','paper_table_source_check',
 'data_contracts_check','claim_evidence_graph_check','projection_resolution_check','projection_frontier_antichain_check','projection_information_profile_check','proof_carrying_semantics_check','formal_obligations_check',
 'side_balanced_witness_support_check','source_witness_support_check','guard_quality_check','feature_holdout_repair_check','repair_generalization_check','statistical_robustness_check','scalability_stress_check','engine_family_stress_check','artifact_registry_check','repository_quality_check','package_snapshot_check',
 'practice_projection_surfaces_check','real_engine_validation_check','environment_check','git_tree_state_check','claim_ledger_check','certificate_freshness_check',
]
paper_checks = {
 'format_compliance','visual_latex_style','manuscript_style','latex_compile_check','pdf_integrity','reference_quality','paper_quality','paper_table_renderers','paper_table_source_check'
}
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
legacy_git_state = E / 'git_tree_status.txt'
if legacy_git_state.exists():
    legacy_git_state.unlink()

def run_refresh(script: str) -> None:
    path = ROOT / 'scripts' / script
    if not path.exists():
        rows.append({'check':f'refresh:{script}','passed':'false','details':'missing'})
        return
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(ROOT) + os.pathsep + str(ROOT / 'scripts') + (os.pathsep + env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
    if script == 'check_real_engine_validation.py' and (
        env.get('RUN_LATEX_COMPILE') == '1'
        or env.get('OPTSEMC_REQUIRE_FRESH_REAL_ENGINE') == '1'
        or (E / 'real_engine_fresh_run.csv').exists()
    ):
        env['OPTSEMC_REQUIRE_FRESH_REAL_ENGINE'] = '1'
    proc = subprocess.run([sys.executable, str(path)], cwd=str(ROOT), env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
    detail = 'ok' if proc.returncode == 0 else proc.stdout[-500:].replace('\n', ' | ')
    rows.append({'check':f'refresh:{script}','passed':str(proc.returncode == 0).lower(),'details':detail})

refresh_scripts = [
    'check_package_integrity.py',
    'compute_practice_projection_surfaces.py',
    'check_practice_projection_surfaces.py',
    'build_environment_report.py',
    'check_environment_report.py',
    'check_real_engine_validation.py',
    'compute_grounded_statistical_robustness.py',
    'check_statistical_robustness.py',
    'compute_repair_generalization.py',
    'check_repair_generalization.py',
    'build_claim_metric_summary.py',
    'build_claim_ledger.py',
    'build_claim_evidence_graph.py',
    'check_claim_evidence_graph.py',
    'run_repository_audit.py',
    'check_repository_quality.py',
    'check_git_tree_state.py',
    'check_artifact_registry.py',
    'build_package_fingerprint.py',
    'build_package_manifest.py',
    'check_package_manifest.py',
    'check_certificate_freshness.py',
    'build_package_fingerprint.py',
    'build_package_manifest.py',
    'check_package_manifest.py',
    'check_package_snapshot.py',
]
if not ARTIFACT_ONLY:
    refresh_scripts[1:1] = [
        'check_manuscript_style.py',
        'check_pdf_integrity.py',
        'check_visual_latex_style.py',
        'check_reference_quality.py',
        'check_paper_quality.py',
    ]
    refresh_scripts[refresh_scripts.index('check_certificate_freshness.py'):refresh_scripts.index('check_certificate_freshness.py')] = [
        'render_paper_tables.py',
        'check_paper_table_sources.py',
    ]

for script in refresh_scripts:
    run_refresh(script)

for name in checks:
    if ARTIFACT_ONLY and name in paper_checks:
        continue
    ok, detail=cert(E/f'{name}.csv')
    rows.append({'check':name,'passed':str(ok).lower(),'details':detail})
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
failed=[r for r in rows if r['passed']!='true']
print(f'Grounded integrity suite: {len(rows)-len(failed)}/{len(rows)} passed')
for r in failed: print('FAIL', r)
sys.exit(1 if failed else 0)
