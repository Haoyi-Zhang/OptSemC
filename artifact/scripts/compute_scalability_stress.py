#!/usr/bin/env python3
"""Measure finite OptSem-C comparison scalability over increasing probe prefixes."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_contract_maps
from optsemc.io import write_csv
from optsemc.scalability import scaling_profile

cm = load_contract_maps(ROOT)
projections = ("strict", "keyword", "operator_only", "operator_kind_surface")
budgets = (128, 256, 512, 1024, 2048, len(cm.probes))
rows = scaling_profile(cm.maps, cm.engines, cm.probes, projections, budgets)
E = ROOT / "evaluation"
write_csv(E / "scalability_stress.csv", [r.as_row() for r in rows], [
    "projection", "probes", "engines", "engine_pairs", "comparisons", "projected_equivalences",
    "true_equivalences", "false_equivalences", "elapsed_ms", "comparisons_per_second", "mean_signature_atoms",
])
full = [r for r in rows if r.probes == len(cm.probes)]
summary = [
    {"metric": "engine_count", "value": str(len(cm.engines))},
    {"metric": "probe_count", "value": str(len(cm.probes))},
    {"metric": "full_pairwise_comparisons_per_projection", "value": str(len(cm.probes) * 21)},
    {"metric": "full_rows", "value": str(len(full))},
    {"metric": "full_elapsed_ms_total", "value": f"{sum(r.elapsed_ms for r in full):.3f}"},
    {"metric": "full_min_comparisons_per_second", "value": f"{min(r.comparisons_per_second for r in full):.1f}"},
    {"metric": "full_max_comparisons_per_second", "value": f"{max(r.comparisons_per_second for r in full):.1f}"},
]
write_csv(E / "scalability_stress_summary.csv", summary, ["metric", "value"])
paper_rows = []
for projection in projections:
    r = next(row for row in full if row.projection == projection)
    paper_rows.append({
        "projection": projection,
        "comparisons": str(r.comparisons),
        "false_equivalences": str(r.false_equivalences),
        "elapsed_ms": f"{r.elapsed_ms:.1f}",
        "comparisons_per_second": f"{r.comparisons_per_second:.0f}",
    })
write_csv(E / "scalability_stress_paper.csv", paper_rows, ["projection", "comparisons", "false_equivalences", "elapsed_ms", "comparisons_per_second"])
print(f"Scalability stress: {len(rows)} rows; full projections={len(full)}")
