#!/usr/bin/env python3
"""Compute false-equivalence witness dispersion and diagnostic cover tables."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_contract_maps, load_probes
from optsemc.io import write_csv
from optsemc.witnesses import dispersion_by_projection, feature_coverage_rows, greedy_probe_cover, witness_records

projections = ("keyword", "yesno", "operator_only")
cm = load_contract_maps(ROOT)
probe_rows = load_probes(ROOT)
probe_features = {row["probe_id"]: row["feature_vector"] for row in probe_rows}
records = witness_records(cm.maps, cm.engines, cm.probes, projections)
E = ROOT / "evaluation"
write_csv(
    E / "witness_dispersion.csv",
    [row.as_row() for row in dispersion_by_projection(records, probe_features)],
    [
        "projection",
        "false_witnesses",
        "distinct_probes",
        "distinct_engine_pairs",
        "distinct_feature_values",
        "feature_dimensions_touched",
        "singleton_probe_witnesses",
        "max_witnesses_per_probe",
        "median_witnesses_per_probe",
    ],
)
write_csv(
    E / "witness_feature_coverage.csv",
    feature_coverage_rows(records, probe_features, probe_features),
    ["feature", "touched_values", "total_values", "coverage_fraction", "missing_values"],
)
cover = greedy_probe_cover(records)
write_csv(
    E / "witness_greedy_probe_cover.csv",
    cover,
    ["rank", "probe_id", "new_witnesses", "cumulative_witnesses", "total_witnesses", "coverage_fraction"],
)
# Paper table: keep only compact columns.
paper_rows = []
for row in dispersion_by_projection(records, probe_features):
    paper_rows.append(
        {
            "projection": row.projection,
            "witnesses": str(row.false_witnesses),
            "probes": str(row.distinct_probes),
            "engine_pairs": str(row.distinct_engine_pairs),
            "feature_values": str(row.distinct_feature_values),
            "max_per_probe": str(row.max_witnesses_per_probe),
        }
    )
union_probes = len({record.probe_id for record in records})
union_pairs = len({record.engine_pair for record in records})
feature_rows = feature_coverage_rows(records, probe_features, probe_features)
full_dimensions = sum(1 for row in feature_rows if int(row["touched_values"]) == int(row["total_values"]))
summary = [
    {"metric": "headline_false_witnesses", "value": str(len(records))},
    {"metric": "headline_distinct_probes", "value": str(union_probes)},
    {"metric": "headline_distinct_engine_pairs", "value": str(union_pairs)},
    {"metric": "feature_dimensions_full_coverage", "value": str(full_dimensions)},
    {"metric": "feature_dimensions_total", "value": str(len(feature_rows))},
    {"metric": "greedy_cover_rows", "value": str(len(cover))},
]
write_csv(E / "witness_dispersion_summary.csv", summary, ["metric", "value"])
write_csv(E / "witness_dispersion_paper.csv", paper_rows, ["projection", "witnesses", "probes", "engine_pairs", "feature_values", "max_per_probe"])
print(f"Witness dispersion: {len(records)} witnesses across {union_probes} probes and {union_pairs} engine pairs")
