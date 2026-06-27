"""External benchmark-motif crosswalk support.

The crosswalk does not import third-party benchmark data.  It imports public,
published workload *motifs* as feature requirements so readers can see which
optimizer-decision surfaces are already exercised by OptSemBench-C and which are
not part of the paper's claim.
"""
from __future__ import annotations

from typing import Mapping, Sequence

from .benchmark import coverage_for_requirements


def motif_coverage(probes: Sequence[Mapping[str, object]], motif: Mapping[str, object]) -> dict[str, object]:
    requirements = motif.get("feature_requirements", {})
    if not isinstance(requirements, Mapping):
        requirements = {}
    covered, total, missing = coverage_for_requirements(probes, {str(k): [str(x) for x in v] for k, v in requirements.items()})
    return {
        "motif_id": motif.get("motif_id", ""),
        "benchmark_family": motif.get("benchmark_family", ""),
        "optimizer_surface": motif.get("optimizer_surface", ""),
        "covered_requirements": covered,
        "total_requirements": total,
        "coverage": f"{covered / total:.6f}" if total else "1.000000",
        "missing_requirements": ";".join(missing),
    }
