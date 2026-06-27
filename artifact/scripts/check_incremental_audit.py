#!/usr/bin/env python3
"""Validate incremental comparison-maintenance outputs."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "incremental_audit_check.csv"


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

rows = []
def add(check: str, passed: bool, details: str = ""):
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": str(details)})

try:
    audit = read_csv(E / "incremental_audit.csv")
    summary = {r["metric"]: r["value"] for r in read_csv(E / "incremental_audit_summary.csv")}
    deltas = read_csv(E / "incremental_probe_deltas.csv")
    paper = read_csv(E / "incremental_audit_paper.csv")
    add("budget_rows_present", len(audit) == 30, f"rows={len(audit)}")
    add("probe_delta_rows_present", len(deltas) == 4216 * 5, f"rows={len(deltas)}")
    add("zero_incremental_drift", all(int(r["drift"]) == 0 for r in audit), "")
    add("full_denominator_preserved", summary.get("full_incremental_comparisons_per_projection") == "88536", str(summary))
    add("headline_counts_preserved", summary.get("keyword__false_equivalences") == "254" and summary.get("operator_only__false_equivalences") == "238" and summary.get("yesno__false_equivalences") == "6", str(summary))
    add("negative_and_positive_controls_zero", summary.get("strict__false_equivalences") == "0" and summary.get("operator_kind_surface__false_equivalences") == "0", str(summary))
    add("work_reduction_nontrivial", float(summary.get("repeated_prefix_work_reduction_at_full", "0")) >= 2000.0, summary.get("repeated_prefix_work_reduction_at_full"))
    add("paper_rows_match", len(paper) == 4 and all(int(r["drift"]) == 0 for r in paper), str(paper))
except Exception as exc:
    add("incremental_audit_exception", False, type(exc).__name__ + ":" + str(exc))

with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(rows)
passed = sum(r["passed"] == "true" for r in rows)
print(f"Incremental audit check: {passed}/{len(rows)} passed")
for r in rows:
    if r["passed"] != "true":
        print("FAIL", r["check"], r["details"])
if passed != len(rows):
    sys.exit(1)
