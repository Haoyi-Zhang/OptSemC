#!/usr/bin/env python3
"""Validate packaged JSONL records against lightweight schemas."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.io import read_jsonl, write_csv
from optsemc.schemas import validate_rule_record, validate_probe_record, validate_contract_map_record
issues=[]
for row in read_jsonl(ART/'grounded'/'verified_rules.jsonl'):
    issues.extend(validate_rule_record(row))
for row in read_jsonl(ART/'benchmark'/'generated_probes.jsonl'):
    issues.extend(validate_probe_record(row))
for row in read_jsonl(ART/'evaluation'/'grounded_contract_maps.jsonl'):
    issues.extend(validate_contract_map_record(row))
write_csv(ART/'evaluation'/'schema_coverage_check.csv', [i.as_row() for i in issues] or [{'object_type':'none','object_id':'none','field':'none','detail':'no issues'}], ['object_type','object_id','field','detail'])
print(f"Schema coverage: issues={len(issues)}")
if issues:
    for issue in issues[:10]: print('FAIL', issue)
    sys.exit(1)

