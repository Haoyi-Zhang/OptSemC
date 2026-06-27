#!/usr/bin/env python3
"""Validate the current grounded OptSem-C paper artifact.

This validator intentionally ignores quarantined legacy-corpus paths. The
mainline artifact is the verified grounded corpus plus generated probes,
contract maps, evaluation tables, schemas, and scripts.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

REQUIRED = [
    'schema/action_domain.yaml',
    'schema/contract_rule.schema.json',
    'schema/query_probe.schema.json',
    'benchmark/feature_domain.yaml',
    'benchmark/validity_constraints.yaml',
    'benchmark/selected_3wise.yaml',
    'benchmark/generated_probes.jsonl',
    'grounded/verified_sources.csv',
    'grounded/verified_segments.jsonl',
    'grounded/verified_rules.jsonl',
    'grounded/grounded_source_hashes.csv',
    'evaluation/coverage_interactions.csv',
    'evaluation/grounded_applicable_rules.jsonl',
    'evaluation/grounded_contract_maps.jsonl',
    'evaluation/grounded_conflicts.jsonl',
    'evaluation/grounded/conditional_trap_rate.csv',
    'evaluation/grounded/repair_certificate_summary.csv',
    'evaluation/grounded/workload_sensitivity.csv',
    'scripts/generate_probes.py',
    'scripts/match_rules.py',
    'scripts/merge_contracts.py',
    'scripts/compute_metrics.py',
    'scripts/compute_grounded_conditional_traps.py',
    'scripts/compute_grounded_repair_certificates.py',
    'scripts/compute_workload_sensitivity.py',
    'scripts/audit_grounded_core.py',
    'scripts/run_unit_tests.py',
]
JSONL = [
    'benchmark/generated_probes.jsonl',
    'grounded/verified_segments.jsonl',
    'grounded/verified_rules.jsonl',
    'evaluation/grounded_applicable_rules.jsonl',
    'evaluation/grounded_contract_maps.jsonl',
    'evaluation/grounded_conflicts.jsonl',
]

def read_jsonl(path: Path):
    with path.open(encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if line.strip():
                try:
                    json.loads(line)
                except Exception as e:
                    raise ValueError(f'{path}:{i}: {e}') from e

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    missing = [rel for rel in REQUIRED if not (root / rel).exists()]
    errors = []
    for rel in JSONL:
        p = root / rel
        if p.exists():
            try:
                read_jsonl(p)
            except Exception as e:
                errors.append(str(e))
    if missing or errors:
        if missing:
            print('Missing files:', ', '.join(missing))
        for e in errors[:10]:
            print('Invalid JSONL:', e)
        sys.exit(1)
    print(f'Grounded artifact validation passed: {len(REQUIRED)} required files, {len(JSONL)} JSONL files checked')

if __name__ == '__main__':
    main()
