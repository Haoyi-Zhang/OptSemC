#!/usr/bin/env python3
"""Validate false-witness diversity diagnostics."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
OUT = E / "witness_diversity_check.csv"
rows: list[dict[str, str]] = []


def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

try:
    summary = {r["projection"]: r for r in read_csv(E / "witness_diversity_summary.csv")}
    features = read_csv(E / "witness_diversity_features.csv")
    pairs = read_csv(E / "witness_diversity_engine_pairs.csv")
    add("required_outputs_present", True, "")
except Exception as exc:
    add("required_outputs_present", False, type(exc).__name__)
    summary, features, pairs = {}, [], []

try:
    add("headline_witness_counts_match", summary.get("keyword", {}).get("witnesses") == "254" and summary.get("operator_only", {}).get("witnesses") == "238" and summary.get("yesno", {}).get("witnesses") == "6", str(summary))
except Exception as exc:
    add("headline_witness_counts_match", False, type(exc).__name__)
try:
    add("keyword_not_single_probe", int(summary["keyword"]["distinct_probes"]) >= 200, summary["keyword"]["distinct_probes"])
    add("operator_not_single_probe", int(summary["operator_only"]["distinct_probes"]) >= 200, summary["operator_only"]["distinct_probes"])
except Exception as exc:
    add("headline_not_single_probe", False, type(exc).__name__)
try:
    add("keyword_feature_diversity", int(summary["keyword"]["feature_axes_with_multiple_values"]) >= 8, summary["keyword"]["feature_axes_with_multiple_values"])
    add("operator_feature_diversity", int(summary["operator_only"]["feature_axes_with_multiple_values"]) >= 6, summary["operator_only"]["feature_axes_with_multiple_values"])
except Exception as exc:
    add("feature_diversity", False, type(exc).__name__)
try:
    surface = summary.get("operator_kind_surface", {})
    add("strengthened_surface_zero_witnesses", surface.get("witnesses") == "0", str(surface))
except Exception as exc:
    add("strengthened_surface_zero_witnesses", False, type(exc).__name__)
try:
    keyword_pairs = [r for r in pairs if r.get("projection") == "keyword"]
    operator_pairs = [r for r in pairs if r.get("projection") == "operator_only"]
    add("headline_engine_pair_coverage", len(keyword_pairs) >= 3 and len(operator_pairs) >= 2, f"keyword={len(keyword_pairs)};operator={len(operator_pairs)}")
except Exception as exc:
    add("headline_engine_pair_coverage", False, type(exc).__name__)
try:
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["check", "passed", "details"])
        writer.writeheader(); writer.writerows(rows)
    passed = sum(1 for r in rows if r["passed"] == "true")
    print(f"Witness diversity check: {passed}/{len(rows)} passed")
    if passed != len(rows):
        for r in rows:
            if r["passed"] != "true":
                print(f"FAILED {r['check']}: {r['details']}")
        raise SystemExit(1)
except Exception:
    raise
