#!/usr/bin/env python3
"""Validate task-facing severity summaries for headline projection witnesses."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evaluation"
OUT = EVAL / "claim_severity_check.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


rows: list[dict[str, str]] = []


def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})


try:
    severity = {row["projection"]: row for row in read_csv(EVAL / "claim_severity.csv")}
    add("claim_severity_file_present", bool(severity), f"rows={len(severity)}")
    add(
        "headline_counts_match",
        int(severity["keyword"]["collapsed_witnesses"]) == 254
        and int(severity["operator_only"]["collapsed_witnesses"]) == 238
        and int(severity["yesno"]["collapsed_witnesses"]) == 6,
        "",
    )
    add(
        "keyword_not_taxonomy_only",
        int(severity["keyword"]["placement_claim_risk"]) == 254
        and int(severity["keyword"]["observability_claim_risk"]) >= 240
        and int(severity["keyword"]["taxonomy_only_witnesses"]) == 0,
        str(severity["keyword"]),
    )
    add(
        "operator_not_taxonomy_only",
        int(severity["operator_only"]["layer_claim_risk"]) == 238
        and int(severity["operator_only"]["placement_claim_risk"]) >= 200
        and int(severity["operator_only"]["taxonomy_only_witnesses"]) == 0,
        str(severity["operator_only"]),
    )
    add(
        "yesno_is_narrow_boundary",
        int(severity["yesno"]["collapsed_witnesses"]) == 6
        and int(severity["yesno"]["state_claim_risk"]) == 6
        and int(severity["yesno"]["decision_time_claim_risk"]) == 0,
        str(severity["yesno"]),
    )
    add(
        "all_headline_witnesses_reference_disjoint",
        all(
            row["collapsed_witnesses"] == row["reference_disjoint_witnesses"]
            for row in severity.values()
        ),
        "",
    )
except Exception as exc:
    add("claim_severity_exception_free", False, type(exc).__name__)

with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader()
    writer.writerows(rows)

passed = sum(row["passed"] == "true" for row in rows)
print(f"Claim-severity check: {passed}/{len(rows)} passed")
for row in rows:
    if row["passed"] != "true":
        print("FAIL", row["check"], row["details"])
if passed != len(rows):
    sys.exit(1)
