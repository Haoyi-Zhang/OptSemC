#!/usr/bin/env python3
"""Validate projection-frontier antichain certificates."""
from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "artifact" / "evaluation"
DETAIL = EVAL / "projection_frontier_antichains.csv"
SUMMARY = EVAL / "projection_frontier_antichain_summary.csv"
OUT = EVAL / "projection_frontier_antichain_check.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def add(rows: list[dict[str, str]], check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})


def main() -> None:
    checks: list[dict[str, str]] = []
    if not DETAIL.exists() or not SUMMARY.exists():
        add(checks, "frontier_files_present", False, f"missing detail={DETAIL.exists()} summary={SUMMARY.exists()}")
    else:
        detail = read_csv(DETAIL)
        summary = {row["universe"]: row for row in read_csv(SUMMARY)}
        add(checks, "frontier_files_present", True, f"detail={len(detail)} summary={len(summary)}")
        add(checks, "both_universes_present", set(summary) == {"all_fields", "semantic_no_variant"}, ";".join(sorted(summary)))
        all_summary = summary.get("all_fields", {})
        sem_summary = summary.get("semantic_no_variant", {})
        add(checks, "all_lattice_counts_match", all_summary.get("subsets") == "256" and all_summary.get("safe_subsets") == "212" and all_summary.get("unsafe_subsets") == "44", str(all_summary))
        add(checks, "semantic_lattice_counts_match", sem_summary.get("subsets") == "128" and sem_summary.get("safe_subsets") == "84" and sem_summary.get("unsafe_subsets") == "44", str(sem_summary))
        add(checks, "variant_is_single_field_minimum", all_summary.get("minimum_safe_size") == "1" and "variant" in all_summary.get("minimum_safe_fields", ""), all_summary.get("minimum_safe_fields", ""))
        sem_min = sem_summary.get("minimum_safe_fields", "")
        add(checks, "semantic_minimum_safe_pairs", sem_summary.get("minimum_safe_size") == "2" and set(sem_min.split(";")) == {"kind+placement", "operator+layer"}, sem_min)
        add(checks, "frontier_monotone", all(row.get("monotone_safe") == "true" and row.get("monotone_unsafe") == "true" for row in summary.values()), str(summary))
        add(checks, "frontier_coverage", all(row.get("every_safe_covered") == "true" and row.get("every_unsafe_covered") == "true" for row in summary.values()), str(summary))
        sem_rows = [row for row in detail if row["universe"] == "semantic_no_variant"]
        min_safe = [row for row in sem_rows if row["frontier"] == "minimal_safe"]
        max_unsafe = [row for row in sem_rows if row["frontier"] == "maximal_unsafe"]
        add(checks, "semantic_frontier_row_counts", len(min_safe) == 14 and len(max_unsafe) == 8, f"min={len(min_safe)} max={len(max_unsafe)}")
        add(checks, "maximal_unsafe_retains_counterexamples", all(int(row["false_equivalences"]) > 0 for row in max_unsafe), "")
        add(checks, "minimal_safe_zero_false", all(int(row["false_equivalences"]) == 0 for row in min_safe), "")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
        writer.writeheader()
        writer.writerows(checks)
    passed = sum(row["passed"] == "true" for row in checks)
    print(f"Projection frontier antichain check: {passed}/{len(checks)} passed")
    for row in checks:
        if row["passed"] != "true":
            print("FAIL", row["check"], row["details"])
    if passed != len(checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
