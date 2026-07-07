#!/usr/bin/env python3
"""Fast package verification over frozen OptSem-C certificates."""
from __future__ import annotations
import csv, hashlib, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'artifact'
EVAL = ART / 'evaluation'
OUT = EVAL / 'fast_mainline_results.csv'
sys.path.insert(0, str(ART))
from optsemc.manifest import should_skip as manifest_should_skip
TRANSIENT_SUFFIXES = ('.aux','.log','.out','.toc','.bbl','.blg','.fls','.fdb_latexmk','.pyc','.pyo','.backup')
IGNORED_DIRS = {'.git','.reference_guard_cache','__pycache__','.pytest_cache','.mypy_cache','build','dist','tmp','zenodo_artifact'}
CERT_FILES = [
 'package_cleanliness.csv','package_manifest_check.csv','package_integrity.csv','manuscript_style.csv','format_compliance.csv','visual_latex_style.csv',
 'projection_resolution_check.csv','projection_frontier_antichain_check.csv','architecture_contract.csv','packaging_installability.csv',
 'practice_projection_surfaces_check.csv',
 'scalability_stress_check.csv','algorithmic_scaling_check.csv','guard_quality_check.csv','feature_holdout_repair_check.csv','repair_generalization_check.csv','scalability_regression_check.csv','incremental_audit_check.csv','incremental_update_check.csv',
 'leave_out_stability_check.csv','engine_family_stress_check.csv','witness_diversity_check.csv','witness_dispersion_check.csv','paper_numeric_claims.csv',
 'python_figure_renderers.csv','latex_compile_check.csv','pdf_integrity.csv','reference_quality.csv','paper_quality.csv','paper_table_renderers.csv','paper_table_source_check.csv','repository_quality_check.csv',
 'package_snapshot_check.csv','integrity_suite.csv','source_witness_support_check.csv','side_balanced_witness_support_check.csv','claim_evidence_graph_check.csv'
 ,'anti_overfit_audit_check.csv','real_engine_validation_check.csv','real_engine_noninterference_check.csv','environment_check.csv','git_tree_state_check.csv','claim_ledger_check.csv','certificate_freshness_check.csv','recoding_worksheet_check.csv'
]
PAPER_CERT_FILES = {
 'manuscript_style.csv','format_compliance.csv','visual_latex_style.csv','python_figure_renderers.csv','paper_numeric_claims.csv',
 'latex_compile_check.csv','pdf_integrity.csv','reference_quality.csv','paper_quality.csv',
 'paper_table_renderers.csv','paper_table_source_check.csv'
}

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def skip_path(path: Path) -> bool:
    return manifest_should_skip(path, ROOT)

def read_csv(path: Path) -> list[dict[str,str]]:
    with path.open(newline='', encoding='utf-8') as f: return list(csv.DictReader(f))

def row_ok(row: dict[str,str]) -> bool:
    if 'passed' in row: return row.get('passed','').lower() == 'true'
    if 'status' in row: return row.get('status','').upper() == 'PASS'
    if 'ok' in row: return row.get('ok','').lower() == 'true'
    return False

rows=[]
def add(check, passed, details=''):
    rows.append({'check':check,'passed':str(bool(passed)).lower(),'details':str(details)})

paper_present = (ROOT / 'Paper').exists()
allowed_top_level = {'.github', '.gitattributes', '.gitignore', '.cloudignore', 'Paper', 'README.md', 'artifact'}
top = sorted(p.name for p in ROOT.iterdir() if p.name not in IGNORED_DIRS)
unexpected_top = [name for name in top if name not in allowed_top_level]
required_top = {'artifact'} if not paper_present else {'Paper', 'artifact'}
add('clean_top_level', not unexpected_top and required_top.issubset(set(top)), ','.join(unexpected_top))
required_raw = [ROOT/'artifact/benchmark/generated_probes.jsonl', ROOT/'artifact/evaluation/grounded_applicable_rules.jsonl', ROOT/'artifact/evaluation/grounded_contract_maps.jsonl', ROOT/'artifact/evaluation/grounded_contract_support.jsonl']
missing_raw = [p.relative_to(ROOT).as_posix() for p in required_raw if not p.exists()]
add('raw_generated_outputs_present', not missing_raw, ';'.join(missing_raw))
trans=[]
for path in ROOT.rglob('*'):
    if any(part in IGNORED_DIRS or part.endswith('.egg-info') for part in path.relative_to(ROOT).parts): continue
    if path.is_file() and (path.name.startswith('paper_build') or path.name.endswith(TRANSIENT_SUFFIXES)):
        trans.append(path.relative_to(ROOT).as_posix())
add('no_transient_products', not trans, ';'.join(trans[:20]))

manifest = EVAL/'package_manifest.csv'
if manifest.exists():
    old = {r['path']:r['sha256'] for r in read_csv(manifest)}
    cur = {p.relative_to(ROOT).as_posix():sha256_file(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and not skip_path(p)}
    missing=sorted(set(cur)-set(old)); stale=sorted(set(old)-set(cur)); changed=sorted(k for k in set(old)&set(cur) if old[k]!=cur[k])
    add('manifest_complete', not missing, ';'.join(missing[:10]))
    add('manifest_no_stale', not stale, ';'.join(stale[:10]))
    add('manifest_hashes_current', not changed, ';'.join(changed[:10]))
else:
    add('manifest_complete', False, 'missing'); add('manifest_no_stale', False, 'missing'); add('manifest_hashes_current', False, 'missing')

for name in CERT_FILES:
    if not paper_present and name in PAPER_CERT_FILES:
        continue
    path=EVAL/name
    if not path.exists():
        add(f'certificate_present:{name}', False, 'missing'); continue
    cert=read_csv(path); passable=[r for r in cert if any(k in r for k in ('passed','status','ok'))]
    failed=[r for r in passable if not row_ok(r)]
    add(f'certificate_pass:{name}', bool(passable) and not failed, f'{len(passable)-len(failed)}/{len(passable)}')

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'Fast mainline package verification: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): raise SystemExit(1)
