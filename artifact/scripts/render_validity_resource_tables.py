#!/usr/bin/env python3
"""Render anti-overfit, resource, and SQL-density tables from checked outputs."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifact"
E = ART / "evaluation"
TABLES = ROOT / "Paper" / "latex" / "tables"
ROW = r" \\"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def esc(text: object) -> str:
    out = str(text)
    return (
        out.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("$", r"\$")
        .replace("#", r"\#")
        .replace("_", r"\_")
        .replace("{", r"\{")
        .replace("}", r"\}")
    )


def fmt_int(value: object) -> str:
    return f"{int(float(str(value))):,}"


def fmt_s(ms: str) -> str:
    seconds = float(ms) / 1000.0
    if seconds < 10:
        return f"{seconds:.2f}"
    return f"{seconds:.1f}"


def anti_overfit_table() -> None:
    selected = [
        row
        for row in rows(E / "anti_overfit_audit.csv")
        if row["gate"]
        in {
            "negative control",
            "source removal",
            "probe subsample",
            "feature-family stress",
            "engine-family stress",
            "learned engine-pair repair",
        }
    ]
    labels = {
        "negative control": "Reference ctrl.",
        "source removal": "Source LOO",
        "probe subsample": "Probe 10\\%",
        "feature-family stress": "Feature stress",
        "engine-family stress": "Engine stress",
        "learned engine-pair repair": "Learned split",
    }
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Anti-overfitting audit. Boundary labels separate controls, finite-denominator stress, source sensitivity, overlapping folds, and failed learned transfer; no row is an independent population claim.}",
        r"\label{tab:anti-overfit-audit}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{2.0pt}",
        r"\begin{tabular}{@{}p{0.67in}p{0.73in}p{0.64in}p{1.12in}@{}}",
        r"\toprule",
        "Check & Scope & Evidence & Boundary" + ROW,
        r"\midrule",
    ]
    for row in selected:
        if row["gate"] == "negative control":
            boundary = "control"
        elif row["gate"] == "source removal" and row["scope"] == "yes/no":
            boundary = "sparse; not all LOO nonzero"
        elif row["gate"] == "source removal":
            boundary = "all sources"
        elif row["gate"] == "probe subsample":
            boundary = "within-denom."
        elif row["gate"] == "learned engine-pair repair":
            boundary = "stress exposes non-transfer"
        elif row["gate"] == "engine-family stress":
            boundary = "within-denom."
        elif row["gate"] == "feature-family stress":
            boundary = "overlapping folds"
        else:
            boundary = row["verdict"]
        lines.append(
            f"{labels.get(row['gate'], esc(row['gate']))} & {esc(row['scope'])} & {esc(row['evidence'])} & {esc(boundary)}" + ROW
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    write(TABLES / "tab_anti_overfit_audit.tex", lines)


def resource_table() -> None:
    profile = rows(E / "resource_profile.csv")
    scale = rows(E / "resource_profile_scale.csv")
    stage_labels = {
        "projection audit": "Projection audit",
        "fixed-basis repair": "Repair check",
        "SQL catalog validation": "SQL validation",
    }
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Finite-audit replay cost. Time and RSS are lower-better cloud replay measurements; rows exclude cold-start setup, archive rebuild, and paper regeneration. The 8$\times$ row lifts the same comparison relation.}",
        r"\label{tab:resource-profile}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3.0pt}",
        r"\begin{tabular}{@{}lrrrr@{}}",
        r"\toprule",
        "Stage & Input rows & Output rows & Time (s)$\\downarrow$ & RSS (MB)$\\downarrow$" + ROW,
        r"\midrule",
    ]
    for row in profile:
        if row["stage"] not in stage_labels:
            continue
        lines.append(
            f"{stage_labels[row['stage']]} & {fmt_int(row['input_rows'])} & {fmt_int(row['output_rows'])} & {fmt_s(row['elapsed_ms'])} & {float(row['peak_rss_mb']):.1f}" + ROW
        )
    eight = next(row for row in scale if row["scale"] == "8x")
    lines.append(
        f"8$\\times$ audit lift & {fmt_int(eight['input_rows'])} & {fmt_int(eight['output_rows'])} & {fmt_s(eight['elapsed_ms'])} & {float(eight['peak_rss_mb']):.1f}" + ROW
    )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    write(TABLES / "tab_resource_profile.tex", lines)


def sql_multicatalog_table() -> None:
    data = rows(E / "sql_probe_multicatalog_summary.csv")
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{SQL validation across deterministic catalog densities.  The check repeats the generated corpus over three populations and reports rows returned and plan diversity; it validates query construction and planability, not runtime ranking.}",
        r"\label{tab:sql-multicatalog}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\begin{tabular}{@{}rrrrrr@{}}",
        r"\toprule",
        "Rows/table & Probes & Exec. & Fail & Rows & Plans" + ROW,
        r"\midrule",
    ]
    for row in data:
        lines.append(
            f"{fmt_int(row['rows_per_table'])} & {fmt_int(row['probes'])} & {fmt_int(row['execution_successes'])} & {fmt_int(row['execution_failures'])} & {fmt_int(row['total_result_rows'])} & {fmt_int(row['distinct_plan_hashes'])}" + ROW
        )
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\Description{Multi-catalog SQL validation table with generated probes executed over deterministic catalog sizes, returned-row counts, and distinct plan hashes.}",
        r"\end{table}",
    ]
    write(TABLES / "tab_sql_multicatalog.tex", lines)


def main() -> int:
    if not (ROOT / "Paper").exists():
        print("Rendered validity/resource tables: skipped (artifact-only package)")
        return 0
    TABLES.mkdir(parents=True, exist_ok=True)
    anti_overfit_table()
    resource_table()
    sql_multicatalog_table()
    print("Rendered validity/resource tables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
