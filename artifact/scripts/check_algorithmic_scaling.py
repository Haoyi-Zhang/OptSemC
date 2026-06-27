#!/usr/bin/env python3
"""Check deterministic finite-comparison scaling diagnostics."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "algorithmic_scaling_check.csv"
rows: list[dict[str, str]] = []


def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

try:
    detailed = read_csv(E / "algorithmic_scaling.csv")
    summary = {r["projection"]: r for r in read_csv(E / "algorithmic_scaling_summary.csv")}
    add("required_outputs_present", True, "")
except Exception as exc:
    detailed, summary = [], {}
    add("required_outputs_present", False, type(exc).__name__)
try:
    add("scale_grid_complete", len(detailed) == 16 and {r["scale_factor"] for r in detailed} == {"1", "2", "4", "8"}, f"rows={len(detailed)}")
except Exception as exc:
    add("scale_grid_complete", False, type(exc).__name__)
try:
    for projection, base_false in (("strict", "0"), ("keyword", "254"), ("operator_only", "238"), ("operator_kind_surface", "0")):
        s = summary[projection]
        expected_max = str(int(base_false) * int(s["max_scale_factor"]))
        add(f"{projection}_false_counts_scale_linearly", s["false_equivalences_at_1x"] == base_false and s["false_equivalences_at_max_scale"] == expected_max, str(s))
except Exception as exc:
    add("false_counts_scale_linearly", False, type(exc).__name__)
try:
    min_checks = min(float(r["checks_per_second"]) for r in detailed)
    max_checks = max(int(r["pairwise_checks"]) for r in detailed)
    add("minimum_throughput_reasonable", min_checks >= 10000.0, f"min_checks_per_second={min_checks:.2f}")
    add("max_denominator_reaches_700k_checks", max_checks >= 700000, f"max_checks={max_checks}")
except Exception as exc:
    add("throughput_and_denominator", False, type(exc).__name__)
with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(rows)
passed = sum(1 for r in rows if r["passed"] == "true")
print(f"Algorithmic scaling check: {passed}/{len(rows)} passed")
if passed != len(rows):
    for r in rows:
        if r["passed"] != "true":
            print(f"FAILED {r['check']}: {r['details']}")
    raise SystemExit(1)
