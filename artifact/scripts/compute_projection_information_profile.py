#!/usr/bin/env python3
"""Compute finite information-loss diagnostics for projection surfaces."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_contract_maps
from optsemc.information import profiles_for
from optsemc.io import write_csv

PROJECTIONS = [
    "strict", "keyword", "yesno", "operator_only", "kind_only", "layer_only", "placement_only",
    "observability_only", "decision_time_only", "state_only", "operator_kind_surface",
]

def main() -> None:
    cm = load_contract_maps(ROOT)
    rows = [profile.as_row() for profile in profiles_for(PROJECTIONS, cm.maps, cm.engines, cm.probes)]
    write_csv(ROOT / "evaluation" / "projection_information_profile.csv", rows)
    # A compact digest for the paper.
    keep = {"strict", "keyword", "operator_only", "placement_only", "state_only", "operator_kind_surface"}
    paper_rows = [r for r in rows if r["projection"] in keep]
    write_csv(ROOT / "evaluation" / "projection_information_paper.csv", paper_rows)
    print(f"Projection information profile: {len(rows)} projections")

if __name__ == "__main__":
    main()
