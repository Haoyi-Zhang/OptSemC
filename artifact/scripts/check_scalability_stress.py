#!/usr/bin/env python3
"""Check OptSem-C finite comparison scalability outputs."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "scalability_stress_check.csv"

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))
rows = []
def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})
try:
    stress = read_csv(E / "scalability_stress.csv")
    add("stress_rows_present", len(stress) == 24, f"rows={len(stress)}")
    budgets = sorted({int(r["probes"]) for r in stress})
    add("expected_probe_prefixes", budgets == [128, 256, 512, 1024, 2048, 4216], str(budgets))
    projections = sorted({r["projection"] for r in stress})
    add("expected_projection_portfolio", projections == ["keyword", "operator_kind_surface", "operator_only", "strict"], str(projections))
    comparison_ok = all(int(r["comparisons"]) == int(r["probes"]) * 21 for r in stress)
    add("comparison_denominator_matches_engine_pairs", comparison_ok, "")
    full = {(r["projection"], int(r["probes"])): r for r in stress}
    add("full_keyword_count", int(full[("keyword", 4216)]["false_equivalences"]) == 254, full[("keyword", 4216)]["false_equivalences"])
    add("full_operator_only_count", int(full[("operator_only", 4216)]["false_equivalences"]) == 238, full[("operator_only", 4216)]["false_equivalences"])
    add("strict_negative_control", all(int(r["false_equivalences"]) == 0 for r in stress if r["projection"] == "strict"), "")
    add("surface_positive_control", int(full[("operator_kind_surface", 4216)]["false_equivalences"]) == 0, full[("operator_kind_surface", 4216)]["false_equivalences"])
    add("measured_runtime_positive", all(float(r["elapsed_ms"]) > 0.0 and float(r["comparisons_per_second"]) > 0.0 for r in stress), "")
    summary = {r["metric"]: r["value"] for r in read_csv(E / "scalability_stress_summary.csv")}
    add("summary_full_denominator", summary.get("full_pairwise_comparisons_per_projection") == "88536", str(summary))
except Exception as exc:
    add("scalability_stress_exception", False, type(exc).__name__ + ":" + str(exc))
with OUT.open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(rows)
passed = sum(r["passed"] == "true" for r in rows)
print(f"Scalability stress check: {passed}/{len(rows)} passed")
for r in rows:
    if r["passed"] != "true":
        print("FAIL", r["check"], r["details"])
if passed != len(rows):
    sys.exit(1)
