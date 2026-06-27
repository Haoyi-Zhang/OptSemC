#!/usr/bin/env python3
"""Compatibility entry point for raw-output packages.

The current two-folder package ships raw generated outputs directly and forbids
cache duplicates, so this entry point only verifies that the required raw files
are present.
"""
from __future__ import annotations
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    ROOT / 'artifact/benchmark/generated_probes.jsonl',
    ROOT / 'artifact/evaluation/grounded_applicable_rules.jsonl',
    ROOT / 'artifact/evaluation/grounded_contract_maps.jsonl',
    ROOT / 'artifact/evaluation/grounded_contract_support.jsonl',
]
missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.exists()]
if missing:
    raise SystemExit('Missing raw generated outputs: ' + ', '.join(missing))
print('Large-output hydration: raw generated outputs already present; no cache payloads required')
