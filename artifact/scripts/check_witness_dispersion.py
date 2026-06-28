#!/usr/bin/env python3
"""Check false-equivalence witness dispersion outputs."""
from __future__ import annotations
import csv
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "witness_dispersion_check.csv"
rows = []

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})

try:
    summary = {row["metric"]: row["value"] for row in read_csv(E / "witness_dispersion_summary.csv")}
    dispersion = {row["projection"]: row for row in read_csv(E / "witness_dispersion.csv")}
    features = read_csv(E / "witness_feature_coverage.csv")
    cover = read_csv(E / "witness_greedy_probe_cover.csv")
    add("headline_witness_count", summary.get("headline_false_witnesses") == "498", str(summary))
    add("witnesses_not_single_probe", int(summary.get("headline_distinct_probes", "0")) >= 450, summary.get("headline_distinct_probes", ""))
    add("engine_pair_dispersion_present", int(summary.get("headline_distinct_engine_pairs", "0")) >= 4, summary.get("headline_distinct_engine_pairs", ""))
    add("keyword_count_matches_baseline", int(dispersion["keyword"]["false_witnesses"]) == 254, dispersion["keyword"]["false_witnesses"])
    add("operator_only_count_matches_baseline", int(dispersion["operator_only"]["false_witnesses"]) == 238, dispersion["operator_only"]["false_witnesses"])
    add("yesno_count_matches_baseline", int(dispersion["yesno"]["false_witnesses"]) == 6, dispersion["yesno"]["false_witnesses"])
    add("all_feature_dimensions_touched", int(summary.get("feature_dimensions_full_coverage", "0")) >= 10, str(summary))
    add("greedy_cover_reaches_all_witnesses", cover and cover[-1]["cumulative_witnesses"] == summary.get("headline_false_witnesses"), cover[-1] if cover else "empty")
    add("feature_table_has_twelve_dimensions", len(features) == 12, str(len(features)))
except Exception as exc:
    add("witness_dispersion_exception", False, type(exc).__name__ + ":" + str(exc))
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(rows)
passed = sum(row["passed"] == "true" for row in rows)
print(f"Witness dispersion check: {passed}/{len(rows)} passed")
for row in rows:
    if row["passed"] != "true":
        print("FAIL", row["check"], row["details"])
if passed != len(rows):
    sys.exit(1)
