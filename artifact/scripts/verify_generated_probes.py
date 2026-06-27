#!/usr/bin/env python3
"""Validate generated OptSemBench-C probes against the feature-domain constraints.

This check catches benchmark-generation defects that aggregate coverage numbers
can hide. In particular, it rejects probes whose feature vector satisfies an
interaction target but violates global validity constraints such as a non-empty
join shape with join_type=none.
"""
from __future__ import annotations
import csv, importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / 'scripts' / 'generate_probes.py'
spec = importlib.util.spec_from_file_location('generate_probes', GEN)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

def read_jsonl(path: Path):
    with path.open(encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if line.strip():
                yield i, json.loads(line)

def main():
    domain = mod.load_yaml(ROOT / 'benchmark' / 'feature_domain.yaml')
    constraints = mod.load_constraints(ROOT / 'benchmark' / 'validity_constraints.yaml')
    probes_path = ROOT / 'benchmark' / 'generated_probes.jsonl'
    out = ROOT / 'evaluation' / 'probe_validity.csv'
    issues = []
    count = 0
    forced = 0
    sql_sanity_issues = 0
    for line_no, probe in read_jsonl(probes_path):
        count += 1
        fv = probe.get('feature_vector', {})
        sql = probe.get('sql_skeleton', '')
        if probe.get('forced_by_rule_guard'):
            forced += 1
        missing = sorted(set(domain) - set(fv))
        extra = sorted(set(fv) - set(domain))
        if missing or extra:
            issues.append((probe.get('probe_id','?'), 'feature_domain_mismatch', f'missing={missing};extra={extra}'))
            continue
        if not mod.valid_assignment(fv, constraints):
            issues.append((probe.get('probe_id','?'), 'constraint_violation', json.dumps(fv, sort_keys=True)))
        # SQL sanity checks: these are intentionally weaker than semantic parsing.
        if fv.get('join_shape') != 'none' and ' JOIN ' not in sql.upper():
            sql_sanity_issues += 1
            issues.append((probe.get('probe_id','?'), 'sql_missing_join_for_join_shape', fv.get('join_shape')))
        if fv.get('order_limit') == 'topn' and not ('ORDER BY' in sql.upper() and 'LIMIT' in sql.upper()):
            sql_sanity_issues += 1
            issues.append((probe.get('probe_id','?'), 'sql_missing_topn_shape', sql[:80]))
        if fv.get('source_boundary') == 'same_connector' and 'remote_pg.' not in sql:
            sql_sanity_issues += 1
            issues.append((probe.get('probe_id','?'), 'sql_missing_same_connector_marker', sql[:80]))
        if fv.get('source_boundary') == 'cross_connector' and not ('remote_pg.' in sql and 'hive.' in sql):
            sql_sanity_issues += 1
            issues.append((probe.get('probe_id','?'), 'sql_missing_cross_connector_markers', sql[:80]))
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['metric','value'])
        w.writeheader()
        w.writerow({'metric':'probes', 'value': count})
        w.writerow({'metric':'forced_by_rule_guard', 'value': forced})
        w.writerow({'metric':'issues', 'value': len(issues)})
        w.writerow({'metric':'sql_sanity_issues', 'value': sql_sanity_issues})
        w.writerow({'metric':'status', 'value': 'PASS' if not issues else 'FAIL'})
    # Always rewrite the detail file.  This prevents stale issue rows from
    # surviving after regenerated probes pass validation.
    detail = ROOT / 'evaluation' / 'probe_validity_issues.csv'
    with detail.open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['probe_id','issue','details'])
        w.writerows(issues[:1000])
    if issues:
        print(f'Probe validity check FAIL: {len(issues)} issues; see {detail}')
        sys.exit(1)
    print(f'Probe validity check PASS: {count} probes, {forced} rule-forced completions; issue file reset')

if __name__ == '__main__':
    main()
