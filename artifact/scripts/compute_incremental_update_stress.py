#!/usr/bin/env python3
"""Compute source-local incremental-update and influence diagnostics."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.incremental import source_influence
from optsemc.io import write_csv
rows, summary = source_influence(ROOT)
E = ROOT / "evaluation"
write_csv(E / "source_influence.csv", [r.as_row() for r in rows], [
    "source_id", "engine", "source_class", "rules", "rule_share", "affected_maps", "affected_map_share",
    "affected_probes", "applicable_actions", "max_actions_per_map",
])
write_csv(E / "incremental_update_summary.csv", summary.as_rows(), ["metric", "value"])
paper_rows = []
for row in sorted(rows, key=lambda r: (-r.affected_maps, -r.rules, r.source_id))[:5]:
    paper_rows.append({
        "source": row.source_id.replace("-001", ""),
        "engine": row.engine,
        "rules": str(row.rules),
        "affected_maps": str(row.affected_maps),
        "affected_map_share": f"{100.0 * row.affected_map_share:.1f}\\%",
        "actions": str(row.applicable_actions),
    })
write_csv(E / "incremental_update_paper.csv", paper_rows, ["source", "engine", "rules", "affected_maps", "affected_map_share", "actions"])
print(f"Incremental update stress: sources={summary.sources}; max_affected_maps={summary.max_affected_maps}")
