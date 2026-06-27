#!/usr/bin/env python3
"""Compute false-witness diversity over probe features and engine pairs."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from optsemc.corpus import load_contract_maps, load_probes  # noqa: E402
from optsemc.io import write_csv  # noqa: E402
from optsemc.projections import false_equivalence_witnesses  # noqa: E402
from optsemc.witness_diversity import feature_rows, summarize_witness_diversity  # noqa: E402

OUT = ROOT / "evaluation"
METHODS = ("strict", "keyword", "yesno", "operator_only", "operator_kind_surface")


def main() -> int:
    contracts = load_contract_maps(ROOT)
    probe_features = {str(p["probe_id"]): {str(k): str(v) for k, v in p["feature_vector"].items()} for p in load_probes(ROOT)}
    summary_rows = []
    feature_detail_rows = []
    pair_rows = []
    for method in METHODS:
        witnesses = false_equivalence_witnesses(contracts.maps, contracts.engines, contracts.probes, method)
        summary_rows.append(summarize_witness_diversity(method, witnesses, probe_features).as_row())
        feature_detail_rows.extend(row.as_row() for row in feature_rows(method, witnesses, probe_features))
        pair_counts: dict[tuple[str, str], int] = {}
        for _method, _probe, left, right in witnesses:
            pair = tuple(sorted((left[0], right[0])))
            pair_counts[pair] = pair_counts.get(pair, 0) + 1
        for (left, right), count in sorted(pair_counts.items(), key=lambda item: (-item[1], item[0])):
            pair_rows.append({"projection": method, "left_engine": left, "right_engine": right, "false_equivalences": str(count)})
    write_csv(OUT / "witness_diversity_summary.csv", summary_rows)
    write_csv(OUT / "witness_diversity_features.csv", feature_detail_rows)
    write_csv(OUT / "witness_diversity_engine_pairs.csv", pair_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
