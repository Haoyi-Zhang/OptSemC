#!/usr/bin/env python3
"""Execute every generated OptSemBench-C SQL skeleton on a deterministic catalog."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_probes
from optsemc.io import write_csv
from optsemc.sql_execution import execute_probe_suite, execution_summary

probes = load_probes(ROOT)
records = execute_probe_suite(probes, rows_per_table=5)
write_csv(ROOT / 'evaluation' / 'sql_probe_execution.csv', [r.as_row() for r in records], ['probe_id','plan_ok','exec_ok','row_count','plan_steps','plan_hash','error'])
write_csv(ROOT / 'evaluation' / 'sql_probe_execution_summary.csv', execution_summary(records), ['metric','value'])
failures = [r for r in records if not r.exec_ok]
print(f"SQL probe execution: {len(records) - len(failures)}/{len(records)} executed; failures={len(failures)}")
if failures:
    for r in failures[:10]:
        print('FAIL', r.probe_id, r.error)
    raise SystemExit(1)
