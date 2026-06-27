#!/usr/bin/env python3
"""Check differential reproducibility rows."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
E = ROOT / "artifact" / "evaluation"
with (E / "differential_reproducibility.csv").open(newline='', encoding='utf-8') as handle:
    rows = list(csv.DictReader(handle))
checks = [
    {"check": "differential_rows_present", "passed": str(len(rows) >= 20).lower(), "details": f"rows={len(rows)}"},
    {"check": "all_differential_claims_match", "passed": str(bool(rows) and all(r.get('passed') == 'true' for r in rows)).lower(), "details": f"{sum(r.get('passed') == 'true' for r in rows)}/{len(rows)}"},
]
with (E / "differential_reproducibility_check.csv").open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"]); writer.writeheader(); writer.writerows(checks)
print(f"Differential reproducibility check: {sum(r['passed']=='true' for r in checks)}/{len(checks)} passed")
if not all(r['passed'] == 'true' for r in checks):
    sys.exit(1)
