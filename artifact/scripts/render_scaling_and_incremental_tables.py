#!/usr/bin/env python3
"""Render compact scalability/dispersion table from executable outputs."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT.parent
E = ROOT / "evaluation"
TABLES = PKG / "Paper" / "latex" / "tables"
ROW = r" \\" 


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, table: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(table)


def label(projection: str) -> str:
    return {
        "strict": "strict",
        "keyword": "keyword",
        "operator_only": "operator-only",
        "operator_kind_surface": "surface",
    }.get(projection, projection)


def bold_if(text: str, condition: bool) -> str:
    return rf"\textbf{{{text}}}" if condition else text


def main() -> int:
    alg = {r["projection"]: r for r in rows(E / "algorithmic_scaling_summary.csv")}
    disp = {r["projection"]: r for r in rows(E / "witness_diversity_summary.csv")}
    fam = {r["projection"]: r for r in rows(E / "engine_family_stress_summary.csv")}
    inc = {r["projection"].replace("operator-only", "operator_only").replace("op+kind+surface", "operator_kind_surface"): r for r in rows(E / "incremental_audit_paper.csv")}
    ordered = ["strict", "keyword", "operator_only", "operator_kind_surface"]
    paper_rows: list[dict[str, str]] = []
    for projection in ordered:
        false_count = alg[projection]["false_equivalences_at_1x"]
        probes = disp.get(projection, {}).get("distinct_probes", "0")
        axes = disp.get(projection, {}).get("feature_axes_with_multiple_values", "0")
        fam_row = fam.get(projection, {})
        family_regions = f"{fam_row.get('families_with_false_equivalence', '0')}/{fam_row.get('pair_families', '6')}"
        paper_rows.append({
            "projection": label(projection),
            "false_at_1x": false_count,
            "false_probes": "--" if false_count == "0" else probes,
            "feature_axes": "--" if false_count == "0" else axes,
            "family_regions": family_regions,
            "checks_at_8x": f"{int(alg[projection]['max_pairwise_checks']):,}",
            "min_checks_per_second": f"{float(alg[projection]['min_checks_per_second']):,.0f}",
            "incremental_drift": inc.get(projection, {}).get("drift", "0"),
        })
    fields = ["projection", "false_at_1x", "false_probes", "feature_axes", "family_regions", "checks_at_8x", "min_checks_per_second", "incremental_drift"]
    write_csv(E / "scaling_diversity_paper.csv", paper_rows, fields)
    if not (PKG / "Paper").exists():
        print("Rendered scalability/family table: skipped TeX output (artifact-only package)")
        return 0
    false_values = [int(row["false_at_1x"]) for row in paper_rows]
    checks_values = [float(row["min_checks_per_second"].replace(",", "")) for row in paper_rows]
    drift_values = [float(row["incremental_drift"]) for row in paper_rows]
    best_false = min(false_values)
    best_checks = max(checks_values)
    best_drift = min(drift_values)
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\footnotesize",
        r"\caption{Finite-comparison replay and dispersion. False and Drift are lower-better; Checks/s is higher-better for the projection inner loop, not end-to-end construction. Bold marks per-column best values.}",
        r"\label{tab:scalability-family}",
        r"\setlength{\tabcolsep}{2.5pt}",
        r"\begin{tabular}{@{}lrrrrrr@{}}",
        r"\toprule",
        "Proj. & False$\\downarrow$ & Probes & Axes & Fam. & Checks/s$\\uparrow$ & Drift$\\downarrow$" + ROW,
        r"\midrule",
    ]
    for r in paper_rows:
        false_text = f"{int(r['false_at_1x']):,}"
        checks_text = r["min_checks_per_second"]
        drift_text = r["incremental_drift"]
        lines.append(
            f"{r['projection']} & "
            f"{bold_if(false_text, int(r['false_at_1x']) == best_false)} & "
            f"{r['false_probes']} & {r['feature_axes']} & {r['family_regions']} & "
            f"{bold_if(checks_text, float(checks_text.replace(',', '')) == best_checks)} & "
            f"{bold_if(drift_text, float(drift_text) == best_drift)}" + ROW
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (TABLES / "tab_scalability_family.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
