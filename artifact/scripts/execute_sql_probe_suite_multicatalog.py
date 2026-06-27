#!/usr/bin/env python3
"""Execute the full generated SQL corpus across deterministic catalog densities."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_probes
from optsemc.io import write_csv
from optsemc.sql_multicatalog import execute_probe_suite_multicatalog, multicatalog_totals

probes = load_probes(ROOT)
details, summaries = execute_probe_suite_multicatalog(probes, catalog_sizes=(1, 5, 17))
write_csv(ROOT/'evaluation'/'sql_probe_multicatalog_execution.csv', details, ['rows_per_table','probe_id','plan_ok','exec_ok','row_count','plan_steps','plan_hash','error'])
write_csv(ROOT/'evaluation'/'sql_probe_multicatalog_summary.csv', summaries)
totals = multicatalog_totals(summaries)
write_csv(ROOT/'evaluation'/'sql_probe_multicatalog_totals.csv', [{'metric': k, 'value': v} for k, v in totals.items()], ['metric','value'])
print(f"SQL multi-catalog execution: {totals['total_execution_successes']}/{totals['total_probe_catalog_runs']} executed; failures={totals['total_execution_failures']}")
if int(totals['total_execution_failures']) != 0:
    raise SystemExit(1)
