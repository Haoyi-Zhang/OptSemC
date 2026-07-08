#!/usr/bin/env python3
"""Normalize headline engine-pair hotspots by public-source rule opportunity."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifact"
sys.path.insert(0, str(ART))

from optsemc.io import read_csv, write_csv

MATRIX = ART / "evaluation" / "engine_pair_false_equivalence_matrix.csv"
RULE_COUNTS = ART / "evaluation" / "grounded_engine_rule_counts.csv"
OUT = ART / "evaluation" / "source_density_hotspots.csv"
SUMMARY = ART / "evaluation" / "source_density_hotspots_summary.csv"


def fmt(value: float) -> str:
    return f"{value:.6f}"


def main() -> None:
    matrix = read_csv(MATRIX)
    rules = {row["engine"]: int(row["rules"]) for row in read_csv(RULE_COUNTS)}

    rows: list[dict[str, object]] = []
    for row in matrix:
        left = row["engine_left"]
        right = row["engine_right"]
        left_rules = rules[left]
        right_rules = rules[right]
        rule_mass = left_rules + right_rules
        rule_product = left_rules * right_rules
        false_equivalences = int(row["false_equivalences"])
        projected_equivalences = int(row["projected_equivalences"])
        rows.append(
            {
                "projection": row["projection"],
                "engine_left": left,
                "engine_right": right,
                "false_equivalences": false_equivalences,
                "projected_equivalences": projected_equivalences,
                "rules_left": left_rules,
                "rules_right": right_rules,
                "rule_mass": rule_mass,
                "rule_product": rule_product,
                "false_per_rule_mass": fmt(false_equivalences / rule_mass),
                "false_per_rule_product": fmt(false_equivalences / rule_product),
                "projected_per_rule_mass": fmt(projected_equivalences / rule_mass),
            }
        )

    summary_rows: list[dict[str, object]] = []
    projections = sorted({row["projection"] for row in rows})
    for projection in projections:
        group = [row for row in rows if row["projection"] == projection]
        nonzero = [row for row in group if int(row["false_equivalences"]) > 0]
        top_mass = max(group, key=lambda r: (float(r["false_per_rule_mass"]), int(r["false_equivalences"])))
        top_product = max(group, key=lambda r: (float(r["false_per_rule_product"]), int(r["false_equivalences"])))
        summary_rows.append(
            {
                "projection": projection,
                "engine_pairs": len(group),
                "nonzero_pairs": len(nonzero),
                "total_false_equivalences": sum(int(row["false_equivalences"]) for row in group),
                "total_projected_equivalences": sum(int(row["projected_equivalences"]) for row in group),
                "top_pair_by_rule_mass": f"{top_mass['engine_left']}--{top_mass['engine_right']}",
                "top_false_per_rule_mass": top_mass["false_per_rule_mass"],
                "top_pair_by_rule_product": f"{top_product['engine_left']}--{top_product['engine_right']}",
                "top_false_per_rule_product": top_product["false_per_rule_product"],
            }
        )

    write_csv(
        OUT,
        rows,
        [
            "projection",
            "engine_left",
            "engine_right",
            "false_equivalences",
            "projected_equivalences",
            "rules_left",
            "rules_right",
            "rule_mass",
            "rule_product",
            "false_per_rule_mass",
            "false_per_rule_product",
            "projected_per_rule_mass",
        ],
    )
    write_csv(
        SUMMARY,
        summary_rows,
        [
            "projection",
            "engine_pairs",
            "nonzero_pairs",
            "total_false_equivalences",
            "total_projected_equivalences",
            "top_pair_by_rule_mass",
            "top_false_per_rule_mass",
            "top_pair_by_rule_product",
            "top_false_per_rule_product",
        ],
    )
    print(f"Source-density hotspot diagnostics: {len(rows)} pair rows, {len(summary_rows)} summaries")


if __name__ == "__main__":
    main()
