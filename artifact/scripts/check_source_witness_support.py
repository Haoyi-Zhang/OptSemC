#!/usr/bin/env python3
"""Validate source-support diagnostics for false-portability witnesses."""
from __future__ import annotations
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "source_witness_support_check.csv"

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

rows: list[dict[str, str]] = []
def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})

try:
    detail = read_csv(E / "source_witness_support.csv")
    summary = {row["projection"]: row for row in read_csv(E / "source_witness_support_summary.csv")}
    paper = read_csv(E / "source_witness_support_paper.csv")
    add("detail_witness_count", len(detail) == 498, f"witnesses={len(detail)}")
    expected = {"keyword": 254, "yesno": 6, "operator_only": 238}
    add("summary_projection_counts", all(int(summary[p]["false_witnesses"]) == v for p, v in expected.items()), str({p: summary.get(p, {}).get("false_witnesses") for p in expected}))
    add("all_witnesses_have_public_sources", all(int(row["source_count"]) >= 2 for row in detail), "")
    add("all_summary_cross_source", all(row["cross_source_witnesses"] == row["false_witnesses"] for row in summary.values()), "")
    add("source_breadth_present", int(summary["keyword"]["distinct_sources"]) >= 10 and int(summary["operator_only"]["distinct_sources"]) >= 8, str(summary))
    add("paper_rows_present", len(paper) == 3 and {row["projection"] for row in paper} == {"Keyword", "Yes/No", "Operator-only"}, "")
except Exception as exc:
    add("source_witness_support_exception", False, type(exc).__name__ + ":" + str(exc))

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(rows)
passed = sum(row["passed"] == "true" for row in rows)
print(f"Source witness support check: {passed}/{len(rows)} passed")
for row in rows:
    if row["passed"] != "true":
        print("FAIL", row["check"], row["details"])
if passed != len(rows):
    raise SystemExit(1)
