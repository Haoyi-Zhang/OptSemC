#!/usr/bin/env python3
"""Check finite comparison scaling diagnostics."""
from __future__ import annotations
import csv
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "scalability_regression_check.csv"
rows = []

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})
try:
    fits = read_csv(E / "scalability_regression.csv")
    summary = {row["metric"]: row["value"] for row in read_csv(E / "scalability_regression_summary.csv")}
    add("four_projection_regressions", len(fits) == 4, str(len(fits)))
    add("six_points_per_projection", all(int(row["points"]) == 6 for row in fits), str(fits))
    add("linear_fit_r2_high", min(float(row["r_squared"]) for row in fits) >= 0.95, summary.get("min_r_squared", ""))
    add("positive_scaling_slope", all(float(row["slope_ms_per_comparison"]) > 0 for row in fits), "")
    add("slope_implies_nontrivial_throughput", min(float(row["comparisons_per_ms_from_slope"]) for row in fits) > 50.0, str(fits))
except Exception as exc:
    add("scalability_regression_exception", False, type(exc).__name__ + ":" + str(exc))
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(rows)
passed = sum(row["passed"] == "true" for row in rows)
print(f"Scalability regression check: {passed}/{len(rows)} passed")
for row in rows:
    if row["passed"] != "true":
        print("FAIL", row["check"], row["details"])
if passed != len(rows):
    sys.exit(1)
