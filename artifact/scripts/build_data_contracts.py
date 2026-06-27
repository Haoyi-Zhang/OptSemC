#!/usr/bin/env python3
"""Build executable data-contract validation reports."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "artifact"))
from optsemc.data_contracts import validate_contracts, result_rows, issue_rows, cross_file_invariants
from optsemc.io import write_csv
E = ROOT / "artifact" / "evaluation"
results = validate_contracts(ROOT)
write_csv(E / "data_contracts.csv", result_rows(results), ["contract", "path", "rows", "errors", "warnings", "passed"])
write_csv(E / "data_contract_issues.csv", issue_rows(results), ["contract", "path", "row", "field", "severity", "message"])
write_csv(E / "data_contract_cross_file.csv", cross_file_invariants(ROOT), ["check", "passed", "details"])
print(f"Data contracts: {sum(r.passed for r in results)}/{len(results)} passed")
