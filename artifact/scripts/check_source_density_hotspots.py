#!/usr/bin/env python3
"""Check source-density hotspot diagnostics."""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifact"
EVAL = ART / "evaluation"
OUT = EVAL / "source_density_hotspots_check.csv"

EXPECTED_FALSE = {"keyword": 254, "operator_only": 238, "yesno": 6}
EXPECTED_NONZERO = {"keyword": 3, "operator_only": 2, "yesno": 1}
EXPECTED_RULES = {
    "BigQuery": 37,
    "ClickHouse": 26,
    "DuckDB": 21,
    "PostgreSQL": 80,
    "Snowflake": 26,
    "Spark SQL": 36,
    "Trino": 61,
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    checks: list[dict[str, str]] = []

    def add(check: str, ok: bool, details: object = "") -> None:
        checks.append({"check": check, "passed": str(bool(ok)).lower(), "details": str(details)})

    paths = {
        "hotspots": EVAL / "source_density_hotspots.csv",
        "summary": EVAL / "source_density_hotspots_summary.csv",
        "rules": EVAL / "grounded_engine_rule_counts.csv",
    }
    missing = [name for name, path in paths.items() if not path.exists()]
    add("inputs_present", not missing, ",".join(missing))

    if not missing:
        rows = read_rows(paths["hotspots"])
        summary = read_rows(paths["summary"])
        rules = {row["engine"]: int(row["rules"]) for row in read_rows(paths["rules"])}

        add("rule_counts_match_expected", rules == EXPECTED_RULES, rules)
        add("hotspot_rows_match_engine_pairs", len(rows) == 63, len(rows))
        projections = {row["projection"] for row in rows}
        add("headline_projections_present", projections == set(EXPECTED_FALSE), ",".join(sorted(projections)))

        finite = True
        denominator_ok = True
        rate_consistent = True
        for row in rows:
            left_rules = int(row["rules_left"])
            right_rules = int(row["rules_right"])
            mass = int(row["rule_mass"])
            product = int(row["rule_product"])
            false = int(row["false_equivalences"])
            if mass != left_rules + right_rules or product != left_rules * right_rules:
                denominator_ok = False
            for field in ("false_per_rule_mass", "false_per_rule_product", "projected_per_rule_mass"):
                value = float(row[field])
                finite = finite and math.isfinite(value) and value >= 0
            if false == 0 and (
                float(row["false_per_rule_mass"]) != 0.0 or float(row["false_per_rule_product"]) != 0.0
            ):
                rate_consistent = False
        add("opportunity_denominators_consistent", denominator_ok)
        add("normalized_rates_finite_nonnegative", finite)
        add("zero_false_rows_have_zero_false_rates", rate_consistent)

        sums = {
            projection: sum(int(row["false_equivalences"]) for row in rows if row["projection"] == projection)
            for projection in projections
        }
        nonzero = {
            projection: sum(
                1 for row in rows if row["projection"] == projection and int(row["false_equivalences"]) > 0
            )
            for projection in projections
        }
        add("headline_false_counts_preserved", sums == EXPECTED_FALSE, sums)
        add("headline_nonzero_pair_counts_preserved", nonzero == EXPECTED_NONZERO, nonzero)

        summary_by_projection = {row["projection"]: row for row in summary}
        add("summary_rows_match_projections", set(summary_by_projection) == set(EXPECTED_FALSE), sorted(summary_by_projection))
        for projection, expected in EXPECTED_FALSE.items():
            row = summary_by_projection.get(projection, {})
            add(
                f"{projection}_summary_consistent",
                row.get("total_false_equivalences") == str(expected)
                and row.get("nonzero_pairs") == str(EXPECTED_NONZERO[projection]),
                row,
            )

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
        writer.writeheader()
        writer.writerows(checks)

    passed = sum(row["passed"] == "true" for row in checks)
    print(f"Source-density hotspot check: {passed}/{len(checks)} passed")
    for row in checks:
        if row["passed"] != "true":
            print("FAIL", row["check"], row["details"])
    if passed != len(checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
