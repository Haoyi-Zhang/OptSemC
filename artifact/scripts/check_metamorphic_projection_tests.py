#!/usr/bin/env python3
"""Check metamorphic projection tests."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
E = ROOT / "artifact" / "evaluation"
with (E / "metamorphic_projection_tests.csv").open(newline='', encoding='utf-8') as handle:
    rows = list(csv.DictReader(handle))
checks = [
    {"check": "metamorphic_suite_nonempty", "passed": str(len(rows) >= 40).lower(), "details": f"rows={len(rows)}"},
    {"check": "metamorphic_suite_all_pass", "passed": str(bool(rows) and all(r.get('passed') == 'true' for r in rows)).lower(), "details": f"{sum(r.get('passed') == 'true' for r in rows)}/{len(rows)}"},
    {"check": "separator_soundness_checked", "passed": str(any(r.get('test') == 'repair_separator_soundness' for r in rows)).lower(), "details": ""},
]
with (E / "metamorphic_projection_check.csv").open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"]); writer.writeheader(); writer.writerows(checks)
print(f"Metamorphic projection check: {sum(r['passed']=='true' for r in checks)}/{len(checks)} passed")
if not all(r['passed'] == 'true' for r in checks):
    sys.exit(1)
