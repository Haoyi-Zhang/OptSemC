#!/usr/bin/env python3
"""Summarize public comparison surfaces that motivate projection baselines."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "practice_projection_surfaces.csv"
SOURCES = ROOT / "grounded" / "verified_sources.csv"
EVAL = ROOT / "evaluation"
OUT = EVAL / "practice_projection_surfaces.csv"
SUMMARY = EVAL / "practice_projection_surface_summary.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def flag(row: dict[str, str], key: str) -> bool:
    return row[key].strip().lower() == "true"


sources = {row["source_id"]: row for row in read_csv(SOURCES)}
rows = read_csv(CONFIG)
missing = sorted(set(sources) - {row["source_id"] for row in rows})
extra = sorted({row["source_id"] for row in rows} - set(sources))
if missing or extra:
    raise SystemExit(f"practice-surface source mismatch: missing={missing}; extra={extra}")

joined: list[dict[str, str]] = []
for row in rows:
    src = sources[row["source_id"]]
    joined.append(
        {
            "source_id": row["source_id"],
            "engine": src["engine"],
            "title": src["title"],
            "url": src["url"],
            "keyword_surface": str(flag(row, "keyword_surface")).lower(),
            "yesno_surface": str(flag(row, "yesno_surface")).lower(),
            "operator_surface": str(flag(row, "operator_surface")).lower(),
            "reference_signature_payload": str(flag(row, "reference_signature_payload")).lower(),
            "observed_surface": row["observed_surface"],
        }
    )

total = len(joined)
summary_rows = [
    {"metric": "public_sources", "value": str(total), "detail": "public source surfaces audited"},
    {
        "metric": "keyword_surfaces",
        "value": str(sum(flag(row, "keyword_surface") for row in rows)),
        "detail": "sources exposing keyword or feature-name labels",
    },
    {
        "metric": "yesno_surfaces",
        "value": str(sum(flag(row, "yesno_surface") for row in rows)),
        "detail": "sources exposing enablement or yes/no controls",
    },
    {
        "metric": "operator_surfaces",
        "value": str(sum(flag(row, "operator_surface") for row in rows)),
        "detail": "sources exposing operator-family labels",
    },
    {
        "metric": "reference_signature_payload_surfaces",
        "value": str(sum(flag(row, "reference_signature_payload") for row in rows)),
        "detail": "sources exposing the full reference-signature field set used by OptSem-C",
    },
]

EVAL.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(joined[0]))
    writer.writeheader()
    writer.writerows(joined)
with SUMMARY.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["metric", "value", "detail"])
    writer.writeheader()
    writer.writerows(summary_rows)
print(
    "Practice projection surfaces: "
    f"{summary_rows[1]['value']} keyword, {summary_rows[2]['value']} yes/no, "
    f"{summary_rows[3]['value']} operator, {summary_rows[4]['value']} reference-signature payload"
)
