#!/usr/bin/env python3
"""Check high-visibility paper numbers against generated result tables.

The goal is not to parse all LaTeX, but to guard the numbers readers see first
against stale table text after an evaluation refresh.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT.parent
E = ROOT / "evaluation"
G = E / "grounded"
OUT = E / "paper_numeric_claims.csv"
ROWS: list[dict[str, str]] = []


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def add(check: str, passed: bool, details: str = "") -> None:
    ROWS.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def contains_all(path: Path, tokens: list[str]) -> tuple[bool, str]:
    t = text(path)
    missing = [tok for tok in tokens if tok not in t]
    return not missing, "|".join(missing)


def fmt_int(value: str | int) -> str:
    return f"{int(value):,}"

try:
    table = PKG / "Paper" / "latex" / "tables" / "tab_scalability_family.tex"
    scale_rows = read_csv(E / "scaling_diversity_paper.csv")
    expected: list[str] = []
    for row in scale_rows:
        expected.extend([
            row["projection"],
            fmt_int(row["false_at_1x"]),
            row["false_probes"],
            row["feature_axes"],
            row["family_regions"],
            row["min_checks_per_second"],
            row["incremental_drift"],
        ])
    ok, detail = contains_all(table, sorted(set(expected)))
    add("scalability_table_matches_scaling_diversity", ok, detail)
except Exception as exc:
    add("scalability_table_matches_scaling_diversity", False, type(exc).__name__ + ":" + str(exc))

try:
    table = PKG / "Paper" / "latex" / "tables" / "tab_witness_dispersion.tex"
    rows = read_csv(E / "witness_dispersion_paper.csv")
    expected = []
    labels = {"keyword": "Keyword", "operator_only": "Operator-only", "yesno": "Yes/No"}
    for row in rows:
        expected.extend([labels.get(row["projection"], row["projection"]), row["witnesses"], row["probes"], row["engine_pairs"], row["feature_values"], row["max_per_probe"]])
    ok, detail = contains_all(table, sorted(set(expected)))
    add("witness_table_matches_dispersion_csv", ok, detail)
except Exception as exc:
    add("witness_table_matches_dispersion_csv", False, type(exc).__name__ + ":" + str(exc))

try:
    intro = text(PKG / "Paper" / "latex" / "paper.tex") + "\n" + text(PKG / "Paper" / "latex" / "sections" / "01_intro.tex")
    baseline = {row["projection"]: row for row in read_csv(G / "baseline_portfolio.csv")}
    required = [
        fmt_int(baseline["keyword"]["projected_equivalences"]),
        fmt_int(baseline["keyword"]["false_equivalences"]),
        fmt_int(baseline["operator_only"]["projected_equivalences"]),
        fmt_int(baseline["operator_only"]["false_equivalences"]),
        "498",
    ]
    missing = [tok for tok in required if tok not in intro]
    add("abstract_and_intro_headline_counts_match", not missing, "|".join(missing))
except Exception as exc:
    add("abstract_and_intro_headline_counts_match", False, type(exc).__name__ + ":" + str(exc))

try:
    section = text(PKG / "Paper" / "latex" / "sections" / "05_evaluation.tex")
    summary = {row["metric"]: row["value"] for row in read_csv(E / "scalability_regression_summary.csv")}
    alg = read_csv(E / "algorithmic_scaling_summary.csv")
    min_cps = min(float(row["min_checks_per_second"]) for row in alg)
    min_r_squared = float(summary["min_r_squared"])
    required = [fmt_int(88536), fmt_int(708288), "70,000", "0.96"]
    missing = [tok for tok in required if tok not in section]
    detail = "|".join(missing)
    if min_cps < 70000.0:
        detail += f";min_cps={min_cps:.0f}"
    if min_r_squared < 0.96:
        detail += f";min_r_squared={min_r_squared:.6f}"
    add("evaluation_scaling_claims_match_outputs", not missing and min_cps >= 70000.0 and min_r_squared >= 0.96, detail)
except Exception as exc:
    add("evaluation_scaling_claims_match_outputs", False, type(exc).__name__ + ":" + str(exc))

try:
    section = text(PKG / "Paper" / "latex" / "sections" / "05_evaluation.tex")
    summary = {row["universe"]: row for row in read_csv(E / "projection_frontier_antichain_summary.csv")}
    sem = summary["semantic_no_variant"]
    required = [sem["minimal_safe_count"], sem["maximal_unsafe_count"], "monotone frontier certificate"]
    missing = [tok for tok in required if tok not in section]
    add("evaluation_frontier_antichain_claims_match_outputs", not missing, "|".join(missing))
except Exception as exc:
    add("evaluation_frontier_antichain_claims_match_outputs", False, type(exc).__name__ + ":" + str(exc))

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader(); writer.writerows(ROWS)
passed = sum(row["passed"] == "true" for row in ROWS)
print(f"Paper numeric claims: {passed}/{len(ROWS)} passed")
for row in ROWS:
    if row["passed"] != "true":
        print("FAIL", row["check"], row["details"])
if passed != len(ROWS):
    raise SystemExit(1)
