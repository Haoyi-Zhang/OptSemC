#!/usr/bin/env python3
"""Check data-contract validation reports."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
E = ROOT / "artifact" / "evaluation"

def read(path: Path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))
rows = read(E / "data_contracts.csv")
cross = read(E / "data_contract_cross_file.csv")
checks = []
checks.append({"check": "contract_files_present", "passed": str(bool(rows)).lower(), "details": f"contracts={len(rows)}"})
checks.append({"check": "all_data_contracts_pass", "passed": str(bool(rows) and all(r.get('passed') == 'true' for r in rows)).lower(), "details": f"{sum(r.get('passed') == 'true' for r in rows)}/{len(rows)}"})
checks.append({"check": "cross_file_invariants_pass", "passed": str(bool(cross) and all(r.get('passed') == 'true' for r in cross)).lower(), "details": f"{sum(r.get('passed') == 'true' for r in cross)}/{len(cross)}"})
with (E / "data_contracts_check.csv").open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"]); writer.writeheader(); writer.writerows(checks)
print(f"Data contract check: {sum(r['passed']=='true' for r in checks)}/{len(checks)} passed")
if not all(r['passed'] == 'true' for r in checks):
    sys.exit(1)
