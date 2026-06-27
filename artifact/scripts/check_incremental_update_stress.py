#!/usr/bin/env python3
"""Check source-local incremental-update stress outputs."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "incremental_update_check.csv"

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))
rows = []
def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})
try:
    infl = read_csv(E / "source_influence.csv")
    summary = {r["metric"]: r["value"] for r in read_csv(E / "incremental_update_summary.csv")}
    paper = read_csv(E / "incremental_update_paper.csv")
    add("expected_source_count", summary.get("sources") == "26", str(summary))
    add("expected_rule_count", summary.get("rules") == "287", str(summary))
    add("all_sources_have_rules", all(int(r["rules"]) > 0 for r in infl), "")
    add("source_updates_are_map_local", int(summary.get("max_affected_maps", "0")) <= 4216, summary.get("max_affected_maps", ""))
    add("max_source_rule_share_bounded", float(summary.get("max_source_rule_share", "1")) < 0.20, summary.get("max_source_rule_share", ""))
    # A source can touch at most the observed map rows for its engine.  The
    # grounded map table is sparse across engines, so the correct denominator is
    # the observed map relation rather than 7*|probes|.
    add("incremental_share_bounded", float(summary.get("max_affected_map_share", "1")) <= 0.18, summary.get("max_affected_map_share", ""))
    add("paper_rows_present", len(paper) == 5, f"rows={len(paper)}")
    add("applicability_nonzero", int(summary.get("total_applicable_actions", "0")) > 0, summary.get("total_applicable_actions", ""))
except Exception as exc:
    add("incremental_update_exception", False, type(exc).__name__ + ":" + str(exc))
with OUT.open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(rows)
passed = sum(r["passed"] == "true" for r in rows)
print(f"Incremental update stress check: {passed}/{len(rows)} passed")
for r in rows:
    if r["passed"] != "true":
        print("FAIL", r["check"], r["details"])
if passed != len(rows):
    sys.exit(1)
