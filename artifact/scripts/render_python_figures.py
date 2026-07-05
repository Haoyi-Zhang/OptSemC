#!/usr/bin/env python3
"""Render evidence figures from frozen CSV outputs.

Framework and flow diagrams stay in TikZ.  Quantitative evidence figures are
rendered here from checked CSV files and then included by the LaTeX wrappers.
"""
from __future__ import annotations

import csv
import hashlib
import math
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifact"
E = ART / "evaluation"
G = E / "grounded"
LATEX = ROOT / "Paper" / "latex"
OUTDIR = LATEX / "generated_figures"
CHECK = E / "python_figure_renderers.csv"
MANIFEST = E / "paper_figure_manifest.csv"

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "optsemc-mpl"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256_prefix(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:12]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def load_matplotlib():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
        from matplotlib.ticker import FuncFormatter
    except Exception as exc:  # pragma: no cover - environment dependency path
        raise SystemExit(f"matplotlib unavailable for Python figure rendering: {type(exc).__name__}: {exc}")

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": [
                "Linux Libertine O",
                "LinLibertine",
                "Libertinus Serif",
                "Nimbus Roman",
                "Times New Roman",
                "DejaVu Serif",
            ],
            "font.size": 7.2,
            "axes.titlesize": 8.0,
            "axes.labelsize": 7.0,
            "xtick.labelsize": 6.6,
            "ytick.labelsize": 6.7,
            "legend.fontsize": 6.5,
            "pdf.use14corefonts": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.linewidth": 0.45,
        }
    )
    return plt, Rectangle, FuncFormatter


COLORS = {
    "ink": "#1c1f23",
    "blue": "#265684",
    "teal": "#257c74",
    "gold": "#9a6f2b",
    "rose": "#974952",
    "violet": "#57528d",
    "rule": "#bec5c9",
    "gray": "#606971",
    "soft": "#f6f8fa",
}


def save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        path,
        format="pdf",
        bbox_inches="tight",
        pad_inches=0.04,
        metadata={"Creator": "OptSem-C Python figure renderer", "Producer": "OptSem-C"},
    )


def render_projection_information(plt, output: Path) -> None:
    rows = read_csv(E / "projection_information_paper.csv")
    order = ["strict", "keyword", "operator_only", "placement_only", "state_only", "operator_kind_surface"]
    label = {
        "strict": "strict",
        "keyword": "keyword",
        "operator_only": "operator",
        "placement_only": "placement",
        "state_only": "state",
        "operator_kind_surface": "surface",
    }
    data = {row["projection"]: row for row in rows}
    shown = [data[key] for key in order if key in data]
    n = len(shown)
    y = list(range(n))
    false_rates = [float(row["conditional_false_rate"]) for row in shown]
    entropy = [float(row["entropy_retained"]) for row in shown]
    false_counts = [int(float(row["false_equivalences"])) for row in shown]
    colors = [COLORS["teal"] if count == 0 else COLORS["rose"] for count in false_counts]

    fig, (ax1, ax2) = plt.subplots(
        ncols=2,
        figsize=(3.42, 2.05),
        gridspec_kw={"width_ratios": [1.05, 0.95], "wspace": 0.35},
    )
    fig.patch.set_facecolor("white")
    ax1.barh(y, false_rates, color=colors, alpha=0.78, height=0.45, edgecolor="none")
    for yi, rate, count in zip(y, false_rates, false_counts):
        xpos = min(max(rate + 0.025, 0.06), 0.92)
        ax1.text(xpos, yi, f"{count:,}", va="center", ha="left", color=COLORS["gray"], fontsize=6.4)
    ax1.set_yticks(y)
    ax1.set_yticklabels([label[row["projection"]] for row in shown])
    ax1.invert_yaxis()
    ax1.set_xlim(0, 1.0)
    ax1.set_xlabel("collision rate")
    ax1.set_title("projection kernel")
    ax1.grid(axis="x", color=COLORS["rule"], linewidth=0.35, alpha=0.65)
    ax1.spines[["top", "right", "left"]].set_visible(False)
    ax1.tick_params(axis="y", length=0)

    ax2.scatter(entropy, y, s=28, facecolor="white", edgecolor=COLORS["teal"], linewidth=0.9, zorder=3)
    for yi, value, count in zip(y, entropy, false_counts):
        ax2.hlines(yi, 0, value, color=COLORS["teal"] if count == 0 else COLORS["rose"], linewidth=1.3, alpha=0.72)
    ax2.set_yticks([])
    ax2.set_xlim(0, 1.06)
    ax2.set_xlabel("entropy retained")
    ax2.set_title("information kept")
    ax2.grid(axis="x", color=COLORS["rule"], linewidth=0.35, alpha=0.65)
    ax2.spines[["top", "right", "left"]].set_visible(False)
    save(fig, output)
    plt.close(fig)


def render_motif_denominator(plt, output: Path) -> None:
    from matplotlib.ticker import FuncFormatter

    rows = read_csv(E / "benchmark_motif_difficulty_paper.csv")
    labels = {
        "CEB-CardEst": "CardEst",
        "Adaptive-Distributed": "Adaptive",
        "Federated-Lakehouse": "Federated",
        "Optimizer-Controls": "Controls",
        "PostgreSQL-Controls": "PostgreSQL",
        "DuckDB-Controls": "DuckDB",
        "ClickHouse-JoinAlgorithms": "ClickHouse",
        "Spark-Trino-Distribution": "Spark/Trino",
    }
    names = [labels.get(row["suite_id"], row["suite_id"]) for row in rows]
    y = list(range(len(rows)))
    mins = [float(row["min_matching_probes"]) for row in rows]
    med = [float(row["median_matching_probes"]) for row in rows]
    maxs = [float(row["max_matching_probes"]) for row in rows]
    motifs = [int(row["motifs"]) for row in rows]
    total_motifs = sum(motifs)
    sparse_motifs = sum(int(row["sparse_motifs_le_5"]) for row in rows)

    fig, ax = plt.subplots(figsize=(3.42, 2.55))
    fig.patch.set_facecolor("white")
    for yi, lo, mid, hi in zip(y, mins, med, maxs):
        ax.hlines(yi, lo, hi, color=COLORS["teal"], linewidth=1.4)
        ax.vlines([lo, hi], yi - 0.09, yi + 0.09, color=COLORS["teal"], linewidth=0.72)
        ax.scatter([mid], [yi], marker="D", s=24, facecolor="#d8eee9", edgecolor=COLORS["teal"], linewidth=0.72, zorder=3)
    ax.set_xscale("log")
    ax.set_xlim(0.8, max(maxs) * 1.18)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{name}  n={count}" for name, count in zip(names, motifs)])
    ax.invert_yaxis()
    ax.set_xlabel("matching probes (log scale)")
    ax.set_title("motif coverage", loc="left")
    ax.grid(axis="x", color=COLORS["rule"], linewidth=0.35, alpha=0.72)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=1.5)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: "1k" if value == 1000 else f"{int(value):g}"))
    ax.text(
        0.99,
        1.02,
        f"{total_motifs} motifs; {sparse_motifs} sparse",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        color=COLORS["teal"],
        fontsize=7.0,
        fontweight="bold",
    )
    ax.text(
        0.01,
        -0.18,
        "ranges are finite matching-probe spans, not population estimates",
        transform=ax.transAxes,
        ha="left",
        va="top",
        color=COLORS["gray"],
        fontsize=6.15,
    )
    save(fig, output)
    plt.close(fig)


def render_semantic_frontier(plt, Rectangle, output: Path) -> None:
    rows = [row for row in read_csv(G / "semantic_frontier.csv") if row["field_universe"] == "core_semantic_state_free"]
    order = ["keyword", "yesno", "operator_only", "all_projections"]
    label = {
        "keyword": "keyword",
        "yesno": "yes/no",
        "operator_only": "operator",
        "all_projections": "all",
    }
    data = {row["scope"]: row for row in rows}
    shown = [data[key] for key in order if key in data]
    depths = ["0", "1", "2+"]

    fig, ax = plt.subplots(figsize=(3.42, 2.02))
    fig.patch.set_facecolor("white")
    ax.set_xlim(-1.90, 4.58)
    ax.set_ylim(-0.28, len(shown) + 0.62)
    ax.axis("off")
    ax.text(-1.84, len(shown) + 0.26, "core state-free repair frontier", fontsize=8.0, weight="bold", color=COLORS["ink"])
    ax.text(0.38, len(shown) - 0.08, "retained depth", fontsize=6.45, color=COLORS["gray"])
    for j, depth in enumerate(depths):
        ax.text(0.35 + j * 0.62, len(shown) - 0.46, depth, ha="center", fontsize=6.4, color=COLORS["gray"])
    ax.text(2.38, len(shown) - 0.46, "basis", fontsize=6.4, color=COLORS["gray"])
    ax.text(4.05, len(shown) - 0.46, "safe/unsafe", ha="center", fontsize=6.4, color=COLORS["gray"])

    for i, row in enumerate(shown):
        y = len(shown) - 1 - i
        min_safe = int(row["minimum_safe_size"])
        ax.text(
            -1.82,
            y,
            f"{label[row['scope']]} ({int(row['false_equivalences']):,})",
            va="center",
            fontsize=6.75,
            weight="bold",
            color=COLORS["ink"],
        )
        for j, depth in enumerate(depths):
            numeric_depth = 2 if depth == "2+" else int(depth)
            if numeric_depth < min_safe:
                txt, fill, edge, fg = "U", "#f3dadd", COLORS["rose"], COLORS["rose"]
            elif numeric_depth == min_safe:
                txt, fill, edge, fg = "S", "#d8eee9", COLORS["teal"], COLORS["teal"]
            else:
                txt, fill, edge, fg = "-", "white", COLORS["rule"], COLORS["gray"]
            x0 = 0.08 + j * 0.62
            ax.add_patch(Rectangle((x0, y - 0.21), 0.52, 0.42, facecolor=fill, edgecolor=edge, linewidth=0.55))
            ax.text(x0 + 0.26, y, txt, ha="center", va="center", fontsize=7.0, weight="bold", color=fg)
        basis = row["representative_minimum_safe_set"].replace("+", " + ")
        basis_count = len([item for item in row["minimum_safe_sets"].split(";") if item])
        compact_basis = basis.replace("placement", "place").replace("operator", "op").replace("decision_time", "time").replace("observability", "obs")
        ax.text(2.38, y, f"{compact_basis} ({basis_count})", va="center", fontsize=6.15, color=COLORS["ink"])
        ax.text(4.05, y, f"{row['safe_subsets']}/{row['unsafe_subsets']}", va="center", ha="center", fontsize=6.35, color=COLORS["gray"])
    save(fig, output)
    plt.close(fig)


def render_sql_execution(plt, output: Path) -> None:
    summary = {row["metric"]: int(float(row["value"])) for row in read_csv(E / "sql_probe_execution_summary.csv")}
    labels = ["planned", "executed", "failures"]
    values = [summary["plan_successes"], summary["execution_successes"], summary["execution_failures"]]
    denom = max(summary["executed_sql_probes"], 1)
    colors = [COLORS["blue"], COLORS["teal"], COLORS["rose"]]

    fig, ax = plt.subplots(figsize=(3.2, 1.45))
    y = list(range(len(labels)))
    ax.barh(y, [v / denom for v in values], color=colors, alpha=0.78, height=0.42)
    for yi, value in zip(y, values):
        xpos = min(value / denom + 0.02, 0.95) if value else 0.035
        ax.text(xpos, yi, f"{value:,}", va="center", fontsize=6.5, color=COLORS["gray"])
        if value == 0:
            ax.plot([0.008], [yi], marker="o", markersize=3.2, markerfacecolor="white", markeredgecolor=COLORS["rose"], zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("share of generated probes")
    ax.set_title("SQL validation: all generated probes execute")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=COLORS["rule"], linewidth=0.35, alpha=0.65)
    ax.text(
        0.0,
        -0.55,
        f"deterministic catalog, n={denom:,}; distinct plans: {summary['distinct_plan_hashes']}; rows: {summary['total_result_rows']:,}",
        fontsize=6.2,
        color=COLORS["gray"],
    )
    save(fig, output)
    plt.close(fig)


def main() -> int:
    if not LATEX.exists():
        print("Python figure rendering: skipped (paper tree absent)")
        return 0
    plt, Rectangle, _ = load_matplotlib()
    OUTDIR.mkdir(parents=True, exist_ok=True)
    specs = [
        ("projection_information", OUTDIR / "fig_projection_information.pdf", "artifact/evaluation/projection_information_paper.csv", render_projection_information),
        ("external_motifs", OUTDIR / "fig_external_motifs.pdf", "artifact/evaluation/benchmark_motif_difficulty_paper.csv", render_motif_denominator),
        ("semantic_frontier", OUTDIR / "fig_semantic_frontier.pdf", "artifact/evaluation/grounded/semantic_frontier.csv", lambda p, o: render_semantic_frontier(p, Rectangle, o)),
        ("sql_execution", OUTDIR / "fig_sql_execution.pdf", "artifact/evaluation/sql_probe_execution_summary.csv", render_sql_execution),
    ]
    checks: list[dict[str, str]] = []
    manifest: list[dict[str, str]] = []
    for figure_id, output, source_rel, renderer in specs:
        source = ROOT / source_rel
        try:
            renderer(plt, output)
            ok = output.exists() and output.stat().st_size > 1_000
            detail = f"{output.relative_to(ROOT).as_posix()} bytes={output.stat().st_size if output.exists() else 0}"
        except Exception as exc:
            ok = False
            detail = f"{type(exc).__name__}: {exc}"
        checks.append({"figure": figure_id, "passed": str(ok).lower(), "details": detail})
        if ok:
            manifest.append(
                {
                    "figure": figure_id,
                    "latex_file": f"Paper/latex/figures/fig_{figure_id}_plot.tex",
                    "output_file": output.relative_to(ROOT).as_posix(),
                    "source_files": source_rel,
                    "output_sha256_12": sha256_prefix(output),
                    "source_sha256_12": sha256_prefix(source),
                }
            )
    write_csv(CHECK, checks, ["figure", "passed", "details"])
    write_csv(MANIFEST, manifest, ["figure", "latex_file", "output_file", "source_files", "output_sha256_12", "source_sha256_12"])
    passed = sum(row["passed"] == "true" for row in checks)
    print(f"Python figure rendering: {passed}/{len(checks)} passed")
    for row in checks:
        if row["passed"] != "true":
            print("FAIL", row)
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
