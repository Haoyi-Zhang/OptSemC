#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.registry import validate_registry, registry_summary, registry_rows, registry_for_root
from optsemc.io import write_csv
vals=validate_registry(ART)
specs=registry_for_root(ART)
write_csv(ART/'evaluation'/'artifact_registry.csv', registry_rows(specs), ['path','kind','min_rows','required'])
write_csv(ART/'evaluation'/'artifact_registry_check.csv', [v.as_row() for v in vals], ['path','passed','rows','details'])
write_csv(ART/'evaluation'/'artifact_registry_summary.csv', registry_summary(vals), ['metric','value'])
passed=sum(v.passed for v in vals)
print(f'Artifact registry: {passed}/{len(vals)} passed')
for v in vals:
    if not v.passed: print('FAIL', v.path, v.details)
if passed != len(vals): sys.exit(1)
