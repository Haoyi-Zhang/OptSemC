#!/usr/bin/env python3
"""Compute deterministic finite-comparison scaling diagnostics."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from optsemc.algorithmic_scaling import run_scaling_curve  # noqa: E402
from optsemc.corpus import load_contract_maps  # noqa: E402
from optsemc.io import write_csv  # noqa: E402

OUT = ROOT / "evaluation"
PROJECTIONS = ("strict", "keyword", "operator_only", "operator_kind_surface")
SCALES = (1, 2, 4, 8)


def main() -> int:
    cm = load_contract_maps(ROOT)
    results = run_scaling_curve(cm.maps, cm.engines, cm.probes, PROJECTIONS, SCALES)
    write_csv(OUT / "algorithmic_scaling.csv", [r.as_row() for r in results])
    summary_rows = []
    for projection in PROJECTIONS:
        rows = [r for r in results if r.projection == projection]
        summary_rows.append({
            "projection": projection,
            "max_scale_factor": str(max(r.scale_factor for r in rows)),
            "max_pairwise_checks": str(max(r.pairwise_checks for r in rows)),
            "min_checks_per_second": f"{min(r.checks_per_second for r in rows):.2f}",
            "false_equivalences_at_1x": str(next(r.false_equivalences for r in rows if r.scale_factor == 1)),
            "false_equivalences_at_max_scale": str(next(r.false_equivalences for r in rows if r.scale_factor == max(x.scale_factor for x in rows))),
        })
    write_csv(OUT / "algorithmic_scaling_summary.csv", summary_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
