#!/usr/bin/env python3
"""Check the recoding worksheet exported from grounded source-line evidence."""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSHEET = ROOT / "evaluation" / "recoding_worksheet.csv"
SUMMARY = ROOT / "evaluation" / "recoding_worksheet_summary.csv"
OUT = ROOT / "evaluation" / "recoding_worksheet_check.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


rows: list[dict[str, str]] = []


def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})


worksheet = read_csv(WORKSHEET) if WORKSHEET.exists() else []
summary = {row["metric"]: row["value"] for row in read_csv(SUMMARY)} if SUMMARY.exists() else {}
required_recoder = [
    "recoder_accept",
    "recoder_state",
    "recoder_operator",
    "recoder_action_kind",
    "recoder_optimizer_layer",
    "recoder_execution_placement",
    "recoder_decision_time",
    "recoder_observability",
    "recoder_variant",
    "recoder_notes",
]
HASH_RE = re.compile(r"^[0-9a-f]{64}$")

add("worksheet_present", WORKSHEET.exists(), str(WORKSHEET.relative_to(ROOT)))
add("summary_present", SUMMARY.exists(), str(SUMMARY.relative_to(ROOT)))
add("worksheet_row_count", len(worksheet) == 287, f"rows={len(worksheet)}")
add("worksheet_source_count", len({row.get("source_id", "") for row in worksheet}) == 26, f"sources={len({row.get('source_id', '') for row in worksheet})}")
add("worksheet_engine_count", len({row.get("engine", "") for row in worksheet}) == 7, f"engines={len({row.get('engine', '') for row in worksheet})}")
add("all_rows_have_source_locator", bool(worksheet) and all(row.get("public_locator") for row in worksheet), "")
missing_hash = [row.get("rule_id", "") for row in worksheet if not HASH_RE.match(row.get("segment_hash", ""))]
add("all_rows_have_segment_hash", bool(worksheet) and not missing_hash, f"missing_or_invalid={len(missing_hash)}")
add("all_rows_have_current_fields", bool(worksheet) and all(row.get("state") and row.get("operator") and row.get("action_kind") for row in worksheet), "")
add("recoder_columns_present", bool(worksheet) and all(name in worksheet[0] for name in required_recoder), ",".join(required_recoder))
add("summary_matches_rows", summary.get("worksheet_rows") == "287" and summary.get("distinct_sources") == "26", str(summary))

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader()
    writer.writerows(rows)
passed = sum(row["passed"] == "true" for row in rows)
print(f"Recoding worksheet check: {passed}/{len(rows)} passed")
for row in rows:
    if row["passed"] != "true":
        print("FAIL", row)
if passed != len(rows):
    sys.exit(1)
