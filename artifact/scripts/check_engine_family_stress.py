#!/usr/bin/env python3
"""Validate engine-family stratification outputs."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "engine_family_stress_check.csv"

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))
rows = []
def add(check, passed, details=""):
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": str(details)})
try:
    stress = read_csv(E / "engine_family_stress.csv")
    summary = {r["projection"]: r for r in read_csv(E / "engine_family_stress_summary.csv")}
    add("family_rows_present", len(stress) >= 20, f"rows={len(stress)}")
    add("seven_engines_family_mapped", len(read_csv(E / "engine_family_map.csv")) == 7, "")
    add("comparison_denominator_all_projections", all(int(r["comparisons"]) == 88536 for r in summary.values()), str(summary))
    add("keyword_count_preserved", int(summary["keyword"]["false_equivalences"]) == 254, summary["keyword"]["false_equivalences"])
    add("yesno_count_preserved", int(summary["yesno"]["false_equivalences"]) == 6, summary["yesno"]["false_equivalences"])
    add("operator_only_count_preserved", int(summary["operator_only"]["false_equivalences"]) == 238, summary["operator_only"]["false_equivalences"])
    add("surface_positive_control_zero", int(summary["operator_kind_surface"]["false_equivalences"]) == 0, summary["operator_kind_surface"]["false_equivalences"])
    add("layer_placement_repairs_headline", all(int(summary[p]["unresolved_after_layer_placement"]) == 0 for p in ("keyword", "yesno", "operator_only")), "")
    add("not_single_family_artifact", int(summary["keyword"]["families_with_false_equivalence"]) >= 2 and int(summary["operator_only"]["families_with_false_equivalence"]) >= 2, str(summary))
except Exception as exc:
    add("engine_family_stress_exception", False, type(exc).__name__ + ":" + str(exc))
with OUT.open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(rows)
passed = sum(r["passed"] == "true" for r in rows)
print(f"Engine-family stress check: {passed}/{len(rows)} passed")
for r in rows:
    if r["passed"] != "true": print("FAIL", r["check"], r["details"])
if passed != len(rows): sys.exit(1)
