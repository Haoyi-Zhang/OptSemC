#!/usr/bin/env python3
"""Compute streaming-vs-full parity for projection comparison counts."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_contract_maps
from optsemc.incremental import incremental_audit
from optsemc.io import write_csv

cm = load_contract_maps(ROOT)
projections = ("strict", "keyword", "yesno", "operator_only", "operator_kind_surface")
budgets = (128, 256, 512, 1024, 2048, len(cm.probes))
rows, deltas = incremental_audit(cm.maps, cm.engines, cm.probes, projections, budgets)
E = ROOT / "evaluation"
write_csv(E / "incremental_audit.csv", [r.as_row() for r in rows], [
    "projection", "probes", "engine_pairs", "comparisons",
    "incremental_projected_equivalences", "full_projected_equivalences",
    "incremental_true_equivalences", "full_true_equivalences",
    "incremental_false_equivalences", "full_false_equivalences", "drift",
    "elapsed_incremental_ms", "elapsed_full_ms", "repeated_prefix_work_units",
    "incremental_work_units", "work_reduction_factor",
])
write_csv(E / "incremental_probe_deltas.csv", [d.as_row() for d in deltas], [
    "projection", "probe_id", "comparisons", "projected_equivalences", "true_equivalences", "false_equivalences",
])
full_rows = [r for r in rows if r.probes == len(cm.probes)]
summary = [
    {"metric": "engine_count", "value": str(len(cm.engines))},
    {"metric": "probe_count", "value": str(len(cm.probes))},
    {"metric": "projection_count", "value": str(len(projections))},
    {"metric": "budget_rows", "value": str(len(rows))},
    {"metric": "delta_rows", "value": str(len(deltas))},
    {"metric": "max_drift", "value": str(max(r.drift for r in rows))},
    {"metric": "full_incremental_comparisons_per_projection", "value": str(len(cm.probes) * 21)},
    {"metric": "repeated_prefix_work_reduction_at_full", "value": f"{max(r.work_reduction_factor for r in full_rows):.1f}"},
]
for r in full_rows:
    summary.append({"metric": f"{r.projection}__false_equivalences", "value": str(r.incremental_false_equivalences)})
write_csv(E / "incremental_audit_summary.csv", summary, ["metric", "value"])
paper_rows = []
for projection in ("strict", "keyword", "operator_only", "operator_kind_surface"):
    r = next(row for row in full_rows if row.projection == projection)
    paper_rows.append({
        "projection": projection.replace("operator_kind_surface", "op+kind+surface").replace("operator_only", "operator-only"),
        "checks": str(r.comparisons),
        "false": str(r.incremental_false_equivalences),
        "drift": str(r.drift),
        "work_factor": f"{r.work_reduction_factor:.1f}x",
    })
write_csv(E / "incremental_audit_paper.csv", paper_rows, ["projection", "checks", "false", "drift", "work_factor"])
# Render a compact LaTeX table used by the paper.
table_path = ROOT.parent / "Paper" / "latex" / "tables" / "tab_incremental_audit.tex"
lines = [
    r"\begin{table}[t]",
    r"\caption{Incremental comparison audit. Each row maintains pairwise projection counts by streaming probes one at a time, then independently recomputes the full prefix. Drift is the absolute count mismatch; work factor is the reduction against recomputing every prefix from scratch.}",
    r"\label{tab:incremental-audit}",
    r"\centering",
    r"\scriptsize",
    r"\begin{tabular}{lrrrr}",
    r"\toprule",
    r"Projection & Checks & False eq. & Drift & Work factor \\",
    r"\midrule",
]
for r in paper_rows:
    row_end = r"\\"
    lines.append(f"{r['projection']} & {int(r['checks']):,} & {int(r['false']):,} & {r['drift']} & {r['work_factor']} {row_end}")
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
table_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Incremental audit: {len(rows)} budget rows, max_drift={summary[5]['value']}")
