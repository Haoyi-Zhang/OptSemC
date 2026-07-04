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


def latex_bold(value: str) -> str:
    return rf"\textbf{{{value}}}"


def latex_underline(value: str) -> str:
    return rf"\underline{{{value}}}"


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
        "operator_kind_surface": "Surface",
    }
    by_projection = {r["projection"]: r for r in rows(ART / "evaluation" / "grounded" / "baseline_portfolio.csv")}
    shown = [by_projection[projection] for projection in ordered]
    worst_false = max(int(r["false_equivalences"]) for r in shown)
    worst_rate = max(float(r["conditional_false_equivalence_rate"]) for r in shown)
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Executable projection baselines. Bold zeros are exact or strengthened controls; underlining marks the worst one-field projection, exposing the shown range.}",
        r"\label{tab:baseline-portfolio}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\begin{tabular}{@{}lrrr@{}}",
        r"\toprule",
        "Baseline & Eq. & False & Rate" + ROW_END,
        r"\midrule",
    ]
    for projection in ordered:
        r = by_projection[projection]
        false_count = int(r["false_equivalences"])
        pct = 100.0 * float(r["conditional_false_equivalence_rate"])
        false_text = fmt_int(false_count)
        rate_text = f"{pct:.1f}\\%"
        if false_count == 0:
            false_text = latex_bold(false_text)
            rate_text = latex_bold(rate_text)
        elif false_count == worst_false:
            false_text = latex_underline(false_text)
            rate_text = latex_underline(rate_text)
        lines.append(
            f"{esc(labels[projection])} & {fmt_int(r['projected_equivalences'])} & {false_text} & {rate_text}" + ROW_END
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    write(PAPER_TABLES / "tab_baseline_portfolio.tex", lines)


def external_table() -> None:
    data = rows(ART / "evaluation" / "grounded" / "external_benchmark_crosswalk.csv")
    labels = {
        "JOB-join-order-sensitivity": "JOB",
        "ExactCardinality-optimizer-testing": "Exact-card.",
        "CardEst-plan-quality": "CardEst",
        "AdaptiveJoin-runtime-replanning": "Adaptive",
        "LakeCrossSource-joinability": "Lake",
    }
    surfaces = {
        "JOB-join-order-sensitivity": "join-order search",
        "ExactCardinality-optimizer-testing": "exact-cardinality testing",
        "CardEst-plan-quality": "plan-quality sensitivity",
        "AdaptiveJoin-runtime-replanning": "runtime replanning",
        "LakeCrossSource-joinability": "cross-source joinability",
    }
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{External vocabulary stress test. Rows are literature/workload motif families, not copied SQL or performance claims; every declared optimizer-surface requirement has executable probe support.}",
        r"\label{tab:external-crosswalk}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{2.5pt}",
        r"\begin{tabular}{@{}p{0.60in}p{1.28in}rr@{}}",
        r"\toprule",
        "Anchor & Surface & Req. & Cov." + ROW_END,
        r"\midrule",
    ]
    for r in data:
        label = labels.get(r["motif_id"], r["motif_id"])
        surface = surfaces.get(r["motif_id"], r["optimizer_surface"])
        lines.append(
            f"{esc(label)} & {esc(surface)} & {fmt_int(r['total_requirements'])} & {fmt_int(r['covered_requirements'])}" + ROW_END
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    write(PAPER_TABLES / "tab_external_crosswalk.tex", lines)


def main() -> None:
    if not (ROOT / "Paper").exists():
        print("Rendered baseline/external tables: skipped (artifact-only package)")
        return
    PAPER_TABLES.mkdir(parents=True, exist_ok=True)
    baseline_table()
    external_table()
    print("Rendered baseline/external tables")


if __name__ == "__main__":
    main()
