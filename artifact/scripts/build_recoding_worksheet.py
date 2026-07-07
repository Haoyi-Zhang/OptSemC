#!/usr/bin/env python3
"""Build a source-line recoding worksheet for the grounded contract corpus."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evaluation" / "recoding_worksheet.csv"
SUMMARY = ROOT / "evaluation" / "recoding_worksheet_summary.csv"

import sys

sys.path.insert(0, str(ROOT))
from optsemc.io import write_csv


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def segment_digest(segment: dict) -> str:
    return str(segment.get("segment_hash") or segment.get("segment_sha256") or "")


segments = {row["segment_id"]: row for row in read_jsonl(ROOT / "grounded" / "verified_segments.jsonl")}
rules = read_jsonl(ROOT / "grounded" / "verified_rules.jsonl")

rows: list[dict[str, str]] = []
for rule in sorted(rules, key=lambda row: row["rule_id"]):
    action = rule.get("action", {})
    evidence = rule.get("evidence", {})
    segment = segments.get(evidence.get("segment_id", ""), {})
    guard = rule.get("guard", {})
    rows.append(
        {
            "rule_id": rule.get("rule_id", ""),
            "engine": rule.get("engine", ""),
            "source_id": evidence.get("source_id", ""),
            "segment_id": evidence.get("segment_id", ""),
            "public_locator": segment.get("public_locator", ""),
            "line_range": evidence.get("line_range", ""),
            "source_title": segment.get("source_title", ""),
            "claim_paraphrase": segment.get("claim_paraphrase", ""),
            "segment_hash": segment_digest(segment),
            "state": rule.get("state", ""),
            "operator": action.get("operator", ""),
            "action_kind": action.get("kind", ""),
            "optimizer_layer": action.get("layer", ""),
            "execution_placement": action.get("placement", ""),
            "decision_time": action.get("decision_time", ""),
            "observability": action.get("observability", ""),
            "variant": action.get("variant", ""),
            "guard_json": json.dumps(guard, sort_keys=True, separators=(",", ":")),
            "recoder_accept": "",
            "recoder_state": "",
            "recoder_operator": "",
            "recoder_action_kind": "",
            "recoder_optimizer_layer": "",
            "recoder_execution_placement": "",
            "recoder_decision_time": "",
            "recoder_observability": "",
            "recoder_variant": "",
            "recoder_notes": "",
        }
    )

fields = [
    "rule_id",
    "engine",
    "source_id",
    "segment_id",
    "public_locator",
    "line_range",
    "source_title",
    "claim_paraphrase",
    "segment_hash",
    "state",
    "operator",
    "action_kind",
    "optimizer_layer",
    "execution_placement",
    "decision_time",
    "observability",
    "variant",
    "guard_json",
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
write_csv(OUT, rows, fields)

summary = [
    {"metric": "worksheet_rows", "value": str(len(rows))},
    {"metric": "distinct_sources", "value": str(len({row["source_id"] for row in rows}))},
    {"metric": "distinct_engines", "value": str(len({row["engine"] for row in rows}))},
    {"metric": "rows_with_locator", "value": str(sum(bool(row["public_locator"]) for row in rows))},
    {"metric": "rows_with_hash", "value": str(sum(bool(row["segment_hash"]) for row in rows))},
    {"metric": "blank_recoder_columns", "value": "10"},
]
write_csv(SUMMARY, summary, ["metric", "value"])
print(f"Recoding worksheet: {len(rows)} rows; sources={summary[1]['value']}")
