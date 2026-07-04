#!/usr/bin/env python3
"""Check the practice-surface audit used to justify projection baselines."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evaluation"
SURFACES = EVAL / "practice_projection_surfaces.csv"
SUMMARY = EVAL / "practice_projection_surface_summary.csv"
SOURCES = ROOT / "grounded" / "verified_sources.csv"
OUT = EVAL / "practice_projection_surfaces_check.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def yes(row: dict[str, str], key: str) -> bool:
    return row.get(key, "").lower() == "true"


rows = read_csv(SURFACES) if SURFACES.exists() else []
summary = {row["metric"]: int(row["value"]) for row in read_csv(SUMMARY)} if SUMMARY.exists() else {}
source_count = len(read_csv(SOURCES)) if SOURCES.exists() else 0
checks: list[dict[str, str]] = []


def add(check: str, passed: bool, details: str = "") -> None:
    checks.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})


keyword = sum(yes(row, "keyword_surface") for row in rows)
yesno = sum(yes(row, "yesno_surface") for row in rows)
operator = sum(yes(row, "operator_surface") for row in rows)
reference_signature_payload = sum(yes(row, "reference_signature_payload") for row in rows)
urls = [row.get("url", "") for row in rows]

add("all_public_sources_audited", len(rows) == source_count and source_count == 26, f"{len(rows)}/{source_count}")
add("keyword_baseline_observed", keyword == 26 and summary.get("keyword_surfaces") == 26, str(keyword))
add("yesno_baseline_observed", yesno == 12 and summary.get("yesno_surfaces") == 12, str(yesno))
add("operator_baseline_observed", operator == 26 and summary.get("operator_surfaces") == 26, str(operator))
add(
    "reference_signature_payload_not_public_surface",
    reference_signature_payload == 0 and summary.get("reference_signature_payload_surfaces") == 0,
    str(reference_signature_payload),
)
add("stable_public_urls", all(url.startswith("https://") for url in urls), "checked")

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader()
    writer.writerows(checks)
passed = sum(row["passed"] == "true" for row in checks)
print(f"Practice projection-surface check: {passed}/{len(checks)} passed")
for row in checks:
    if row["passed"] != "true":
        print("FAIL", row)
sys.exit(0 if passed == len(checks) else 1)
