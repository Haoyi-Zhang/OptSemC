#!/usr/bin/env python3
"""Validate leave-out projection stability results."""
from __future__ import annotations
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
rows = list(csv.DictReader((E / "leave_out_stability.csv").open()))
summary = list(csv.DictReader((E / "leave_out_stability_summary.csv").open()))
paper = list(csv.DictReader((E / "leave_out_stability_paper.csv").open()))
checks = []
def add(name: str, passed: bool, details: str = "") -> None:
    checks.append({"check": name, "passed": str(bool(passed)).lower(), "details": details})
projections = {r["projection"] for r in rows}
add("four_projection_profiles", projections == {"strict", "keyword", "yesno", "operator_only", "operator_kind_surface"}, ";".join(sorted(projections)))
add("contains_all_engine_scope", sum(1 for r in rows if r["scope_kind"] == "all") == 5)
add("contains_leave_engine_scopes", sum(1 for r in rows if r["scope_kind"] == "leave_engine") >= 28)
add("contains_leave_family_scopes", sum(1 for r in rows if r["scope_kind"] == "leave_family") >= 12)
add("all_repairs_resolved", all(int(r["unresolved_after_layer_placement"]) == 0 for r in rows))
all_false = {(r["projection"], r["scope_kind"]): int(r["false_equivalences"]) for r in rows if r["scope_kind"] == "all"}
add("headline_counts_preserved", all_false.get(("strict", "all")) == 0 and all_false.get(("keyword", "all")) == 254 and all_false.get(("yesno", "all")) == 6 and all_false.get(("operator_only", "all")) == 238)
add("surface_projection_negative_control", all(int(r["false_equivalences"]) == 0 for r in rows if r["projection"] == "operator_kind_surface"))
add("summary_has_scope_groups", len(summary) >= 12)
add("paper_rows_complete", len(paper) == 5)
add("paper_repair_column_zero", all(r["max_unresolved_after_repair"] == "0" for r in paper))
out = E / "leave_out_stability_check.csv"
with out.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(checks)
passed = sum(r["passed"] == "true" for r in checks)
print(f"Leave-out stability check: {passed}/{len(checks)} passed")
for row in checks:
    if row["passed"] != "true":
        print("FAIL", row["check"], row["details"])
if passed != len(checks):
    raise SystemExit(1)
