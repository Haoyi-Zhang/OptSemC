#!/usr/bin/env python3
"""Render baseline and external benchmark crosswalk tables for the paper."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifact"
PAPER_TABLES = ROOT / "Paper" / "latex" / "tables"
ROW_END = r" \\" 


def rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def esc(value: object) -> str:
    s = str(value)
    return (
        s.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("$", r"\$")
        .replace("#", r"\#")
        .replace("_", r"\_")
        .replace("{", r"\{")
        .replace("}", r"\}")
    )


def fmt_int(value: object) -> str:
    return f"{int(value):,}"


def write(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def baseline_table() -> None:
    ordered = [
        "strict",
        "keyword",
        "yesno",
        "operator_only",
        "kind_only",
        "layer_only",
        "placement_only",
        "state_only",
        "operator_kind_surface",
    ]
    labels = {
        "strict": "Exact",
        "keyword": "Keyword",
        "yesno": "Op/action",
        "operator_only": "Operator",
        "kind_only": "Kind-only",
        "layer_only": "Layer-only",
        "placement_only": "Place-only",
        "state_only": "State-only",
        "operator_kind_surface": "Op+kind+surface",
    }
    by_projection = {r["projection"]: r for r in rows(ART / "evaluation" / "grounded" / "baseline_portfolio.csv")}
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Executable projection baselines. False equivalence is conditional on the baseline declaring equivalence; the full baseline portfolio contains 17 projections.}",
        r"\label{tab:baseline-portfolio}",
        r"\scriptsize",
        r"\begin{tabular}{@{}p{0.78in}rrr@{}}",
        r"\toprule",
        "Baseline & Eq. & False & Rate" + ROW_END,
        r"\midrule",
    ]
    for projection in ordered:
        r = by_projection[projection]
        pct = 100.0 * float(r["conditional_false_equivalence_rate"])
        lines.append(
            f"{esc(labels[projection])} & {fmt_int(r['projected_equivalences'])} & {fmt_int(r['false_equivalences'])} & {pct:.1f}\\%" + ROW_END
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    write(PAPER_TABLES / "tab_baseline_portfolio.tex", lines)


def external_table() -> None:
    data = rows(ART / "evaluation" / "grounded" / "external_benchmark_crosswalk.csv")
    labels = {
        "JOB-join-order-sensitivity": "Join-order sensitivity",
        "ExactCardinality-optimizer-testing": "Exact-cardinality testing",
        "CardEst-plan-quality": "CardEst plan quality",
        "AdaptiveJoin-runtime-replanning": "Adaptive replanning",
        "LakeCrossSource-joinability": "Cross-source joinability",
    }
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Crosswalk from published optimizer/benchmark motifs to OptSemBench-C feature requirements.}",
        r"\label{tab:external-crosswalk}",
        r"\small",
        r"\begin{tabular}{lrr}",
        r"\toprule",
        "Motif & Requirements & Covered" + ROW_END,
        r"\midrule",
    ]
    for r in data:
        label = labels.get(r["motif_id"], r["motif_id"])
        lines.append(f"{esc(label)} & {fmt_int(r['total_requirements'])} & {fmt_int(r['covered_requirements'])}" + ROW_END)
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    write(PAPER_TABLES / "tab_external_crosswalk.tex", lines)


def main() -> None:
    PAPER_TABLES.mkdir(parents=True, exist_ok=True)
    baseline_table()
    external_table()
    print("Rendered baseline/external tables")


if __name__ == "__main__":
    main()
