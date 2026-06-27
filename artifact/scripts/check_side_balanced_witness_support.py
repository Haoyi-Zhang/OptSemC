#!/usr/bin/env python3
"""Check side-balanced public-source support certificates."""
from __future__ import annotations
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "side_balanced_witness_support_check.csv"

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))

rows: list[dict[str, str]] = []
def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})

records = read_csv(E / "side_balanced_witness_support.csv")
summary = {row["projection"]: row for row in read_csv(E / "side_balanced_witness_support_summary.csv")}
add("headline_witness_count", len(records) == 498, str(len(records)))
add("projection_set", set(summary) == {"keyword", "operator_only", "yesno"}, ";".join(sorted(summary)))
expected = {"keyword": "254", "operator_only": "238", "yesno": "6"}
for projection, expected_count in expected.items():
    row = summary.get(projection, {})
    add(f"{projection}_false_count", row.get("false_witnesses") == expected_count, str(row))
    add(f"{projection}_both_sides_supported", row.get("both_sides_supported") == expected_count and row.get("both_sides_supported_share") == "1.000000", str(row))
    add(f"{projection}_left_right_minimum_support", int(row.get("min_left_sources", "0") or 0) >= 1 and int(row.get("min_right_sources", "0") or 0) >= 1, str(row))
    add(f"{projection}_distinct_sources", int(row.get("distinct_sources", "0") or 0) >= (3 if projection == "yesno" else 8), str(row))
    add(f"{projection}_zero_shared_sources", row.get("zero_shared_source_witnesses") == row.get("false_witnesses"), str(row))
# Per-record side invariants.
missing = [r for r in records if r.get("both_sides_supported") != "true" or int(r.get("left_source_count", "0")) < 1 or int(r.get("right_source_count", "0")) < 1]
add("record_side_invariants", not missing, str(len(missing)))
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(rows)
passed = sum(r["passed"] == "true" for r in rows)
print(f"Side-balanced witness support check: {passed}/{len(rows)} passed")
for row in rows:
    if row["passed"] != "true":
        print("FAIL", row["check"], row["details"])
if passed != len(rows):
    raise SystemExit(1)
