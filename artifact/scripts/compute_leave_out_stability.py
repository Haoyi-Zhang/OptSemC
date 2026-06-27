#!/usr/bin/env python3
"""Compute leave-one-engine/family projection and repair stability."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_contract_maps
from optsemc.io import write_csv
from optsemc.stability import compact_paper_rows, leave_out_stability_profile, summarize_stability

PROJECTIONS = ("strict", "keyword", "yesno", "operator_only", "operator_kind_surface")
cm = load_contract_maps(ROOT)
rows = leave_out_stability_profile(cm.maps, cm.engines, cm.probes, PROJECTIONS)
E = ROOT / "evaluation"
write_csv(E / "leave_out_stability.csv", [r.as_row() for r in rows], [
    "scope_kind", "omitted", "projection", "engines", "engine_pairs", "probes", "comparisons",
    "projected_equivalences", "true_equivalences", "false_equivalences",
    "repaired_by_layer_placement", "unresolved_after_layer_placement",
])
write_csv(E / "leave_out_stability_summary.csv", [r.as_row() for r in summarize_stability(rows)], [
    "projection", "scope_kind", "cases", "all_scope_false_equivalences", "min_false_equivalences",
    "max_false_equivalences", "scopes_with_false_equivalences", "max_unresolved_after_layer_placement",
    "repair_stable",
])
write_csv(E / "leave_out_stability_paper.csv", compact_paper_rows(rows, PROJECTIONS), [
    "projection", "all_false", "leave_engine_false_range", "leave_family_false_range", "max_unresolved_after_repair",
])
print(f"Leave-out stability: {len(rows)} rows over {len(PROJECTIONS)} projections")
