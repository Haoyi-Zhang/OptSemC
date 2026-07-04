#!/usr/bin/env python3
"""Measure replay/audit resource use for paper-facing scalability evidence.

This script is intended for cloud execution.  It avoids engine ranking and
profiles OptSem-C's own replay stages: loading the frozen denominator,
enumerating projection witnesses, checking the fixed repair basis, validating
SQL over deterministic catalogs, and replay-lift scaling of the finite audit.
"""
from __future__ import annotations

import csv
import os
import resource
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from optsemc.corpus import load_contract_maps, load_probes  # noqa: E402
from optsemc.projections import false_equivalence_witnesses  # noqa: E402
from optsemc.repair_stability import ROBUST_SEMANTIC_BASIS, unresolved_count  # noqa: E402
from optsemc.sql_multicatalog import execute_probe_suite_multicatalog  # noqa: E402

E = ROOT / "evaluation"


@dataclass
class PhaseResult:
    stage: str
    scale: str
    input_rows: int
    output_rows: int
    elapsed_ms: float
    peak_rss_mb: float
    throughput_per_s: float
    note: str


def peak_rss_mb() -> float:
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return rss / (1024 * 1024)
    return rss / 1024


def measure(stage: str, scale: str, input_rows: int, note: str, func: Callable[[], int]) -> PhaseResult:
    start = time.perf_counter()
    output_rows = func()
    elapsed_ms = (time.perf_counter() - start) * 1000
    throughput = 0.0 if elapsed_ms <= 0 else input_rows / (elapsed_ms / 1000)
    return PhaseResult(stage, scale, input_rows, output_rows, elapsed_ms, peak_rss_mb(), throughput, note)


def write_csv(path: Path, data: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def main() -> int:
    cm_cache = {}
    probes_cache = {}

    def load_maps_stage() -> int:
        cm_cache["cm"] = load_contract_maps(ROOT)
        return len(cm_cache["cm"].maps)

    def load_probes_stage() -> int:
        probes_cache["probes"] = load_probes(ROOT)
        return len(probes_cache["probes"])

    phase_results: list[PhaseResult] = []
    phase_results.append(measure("load contract maps", "1x", 1, "frozen source-linked maps", load_maps_stage))
    phase_results.append(measure("load probes", "1x", 1, "generated SQL denominator", load_probes_stage))

    cm = cm_cache["cm"]
    probes = probes_cache["probes"]
    pair_checks = len(cm.probes) * (len(cm.engines) * (len(cm.engines) - 1) // 2)
    methods = ("strict", "keyword", "yesno", "operator_only", "operator_kind_surface")
    witness_cache: dict[str, list] = {}

    def projection_audit_stage() -> int:
        total = 0
        for method in methods:
            witnesses = false_equivalence_witnesses(cm.maps, cm.engines, cm.probes, method)
            witness_cache[method] = witnesses
            total += len(witnesses)
        return total

    phase_results.append(measure("projection audit", "1x", pair_checks * len(methods), "all engine-pair/probe checks", projection_audit_stage))

    def repair_stage() -> int:
        unresolved = 0
        for method in ("keyword", "yesno", "operator_only"):
            unresolved += unresolved_count(cm.maps, witness_cache[method], ROBUST_SEMANTIC_BASIS)
        return unresolved

    phase_results.append(measure("fixed-basis repair", "1x", sum(len(witness_cache[m]) for m in ("keyword", "yesno", "operator_only")), "layer+placement unresolved count", repair_stage))

    sql_catalog_sizes = tuple(int(v) for v in os.environ.get("OPTSEMC_RESOURCE_SQL_SIZES", "1,5,17").split(",") if v.strip())

    def sql_stage() -> int:
        _, summaries = execute_probe_suite_multicatalog(probes, catalog_sizes=sql_catalog_sizes)
        return sum(int(row["execution_successes"]) for row in summaries)

    phase_results.append(measure("SQL catalog validation", "1x", len(probes) * len(sql_catalog_sizes), f"catalog sizes={sql_catalog_sizes}", sql_stage))

    scale_rows = []
    for factor in (1, 2, 4, 8):
        scaled_probes = tuple(probe for _ in range(factor) for probe in cm.probes)
        input_rows = len(scaled_probes) * (len(cm.engines) * (len(cm.engines) - 1) // 2) * 4

        def scaled_audit(probes_for_run=scaled_probes) -> int:
            total = 0
            for method in ("strict", "keyword", "operator_only", "operator_kind_surface"):
                total += len(false_equivalence_witnesses(cm.maps, cm.engines, probes_for_run, method))
            return total

        result = measure("projection replay lift", f"{factor}x", input_rows, "deterministic replay lift, not new corpus", scaled_audit)
        scale_rows.append(result)

    fields = ["stage", "scale", "input_rows", "output_rows", "elapsed_ms", "peak_rss_mb", "throughput_per_s", "note"]
    write_csv(
        E / "resource_profile.csv",
        [
            {
                "stage": r.stage,
                "scale": r.scale,
                "input_rows": r.input_rows,
                "output_rows": r.output_rows,
                "elapsed_ms": f"{r.elapsed_ms:.3f}",
                "peak_rss_mb": f"{r.peak_rss_mb:.3f}",
                "throughput_per_s": f"{r.throughput_per_s:.3f}",
                "note": r.note,
            }
            for r in phase_results
        ],
        fields,
    )
    write_csv(
        E / "resource_profile_scale.csv",
        [
            {
                "stage": r.stage,
                "scale": r.scale,
                "input_rows": r.input_rows,
                "output_rows": r.output_rows,
                "elapsed_ms": f"{r.elapsed_ms:.3f}",
                "peak_rss_mb": f"{r.peak_rss_mb:.3f}",
                "throughput_per_s": f"{r.throughput_per_s:.3f}",
                "note": r.note,
            }
            for r in scale_rows
        ],
        fields,
    )
    print(f"Resource profile: {len(phase_results)} stages, {len(scale_rows)} scale points")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
