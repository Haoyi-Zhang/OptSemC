#!/usr/bin/env python3
"""Summarize which downstream comparison claims each witness can affect."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from optsemc.corpus import load_contract_maps
from optsemc.io import write_csv
from optsemc.projections import false_equivalence_witnesses
from optsemc.severity import (
    field_value_delta,
    jaccard_distance,
    symmetric_atom_delta,
)

HEADLINE_METHODS = ("keyword", "operator_only", "yesno")


def summarize_projection(method: str) -> dict[str, str]:
    cm = load_contract_maps(ROOT)
    witnesses = false_equivalence_witnesses(cm.maps, cm.engines, cm.probes, method)
    counts = {
        "placement": 0,
        "layer": 0,
        "decision_time": 0,
        "observability": 0,
        "state": 0,
        "taxonomy_only": 0,
        "reference_disjoint": 0,
    }
    atom_deltas: list[int] = []
    for _, _probe, left_key, right_key in witnesses:
        left = cm.maps[left_key]
        right = cm.maps[right_key]
        fields = set(field_value_delta(left, right))
        for field in ("placement", "layer", "decision_time", "observability", "state"):
            if field in fields:
                counts[field] += 1
        if not fields.intersection({"placement", "layer", "decision_time", "observability", "state"}):
            counts["taxonomy_only"] += 1
        if jaccard_distance(left, right) == 1.0:
            counts["reference_disjoint"] += 1
        atom_deltas.append(symmetric_atom_delta(left, right))
    total = len(witnesses)
    mean_delta = sum(atom_deltas) / total if total else 0.0
    return {
        "projection": method,
        "collapsed_witnesses": str(total),
        "placement_claim_risk": str(counts["placement"]),
        "layer_claim_risk": str(counts["layer"]),
        "decision_time_claim_risk": str(counts["decision_time"]),
        "observability_claim_risk": str(counts["observability"]),
        "state_claim_risk": str(counts["state"]),
        "taxonomy_only_witnesses": str(counts["taxonomy_only"]),
        "reference_disjoint_witnesses": str(counts["reference_disjoint"]),
        "mean_atom_delta": f"{mean_delta:.3f}",
    }


def main() -> None:
    rows = [summarize_projection(method) for method in HEADLINE_METHODS]
    write_csv(ROOT / "evaluation" / "claim_severity.csv", rows)
    write_csv(ROOT / "evaluation" / "claim_severity_paper.csv", rows)
    total = sum(int(row["collapsed_witnesses"]) for row in rows)
    print(f"Claim-severity summary: {total} headline witnesses summarized")


if __name__ == "__main__":
    main()
