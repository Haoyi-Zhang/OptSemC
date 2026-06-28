#!/usr/bin/env python3
"""Stratify false equivalence by engine-family pair type."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_contract_maps
from optsemc.io import write_csv
from optsemc.scalability import family_stress_profile, ENGINE_FAMILIES

cm = load_contract_maps(ROOT)
projections = ("keyword", "yesno", "operator_only", "operator_kind_surface")
rows = family_stress_profile(cm.maps, cm.engines, cm.probes, projections)
E = ROOT / "evaluation"
write_csv(E / "engine_family_stress.csv", [r.as_row() for r in rows], [
    "projection", "pair_family", "engine_pairs", "probes", "comparisons", "projected_equivalences",
    "true_equivalences", "false_equivalences", "repaired_by_layer_placement", "unresolved_after_layer_placement",
])
summary = []
for projection in projections:
    subset = [r for r in rows if r.projection == projection]
    summary.append({
        "projection": projection,
        "pair_families": str(len(subset)),
        "comparisons": str(sum(r.comparisons for r in subset)),
        "false_equivalences": str(sum(r.false_equivalences for r in subset)),
        "repaired_by_layer_placement": str(sum(r.repaired_by_layer_placement for r in subset)),
        "unresolved_after_layer_placement": str(sum(r.unresolved_after_layer_placement for r in subset)),
        "families_with_false_equivalence": str(sum(1 for r in subset if r.false_equivalences > 0)),
    })
write_csv(E / "engine_family_stress_summary.csv", summary, [
    "projection", "pair_families", "comparisons", "false_equivalences",
    "repaired_by_layer_placement", "unresolved_after_layer_placement", "families_with_false_equivalence",
])
family_rows = [{"engine": engine, "family": family} for engine, family in sorted(ENGINE_FAMILIES.items())]
write_csv(E / "engine_family_map.csv", family_rows, ["engine", "family"])
print(f"Engine-family stress: {len(rows)} rows; families={len(set(r.pair_family for r in rows))}")
