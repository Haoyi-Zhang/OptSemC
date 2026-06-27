"""Algorithmic scaling diagnostics for finite contract comparison.

The scaling experiment uses a deterministic lift that repeats the probe
sequence.  Repetition preserves the empirical contract signatures while growing
only the pairwise-comparison denominator.  The implementation deliberately avoids
materializing copied contract maps: it streams the lifted probes and reuses the
base projected signatures, which is the same optimization a reader would
expect from a scalable finite-contract comparator.
"""
from __future__ import annotations

import itertools
import time
from dataclasses import dataclass
from typing import Mapping, Sequence

from .projections import project_signature
from .scalability import EMPTY_SIGNATURE
from .semantics import ContractSignature


@dataclass(frozen=True)
class ScalingResult:
    """One projection run over a deterministic lifted denominator."""

    scale_factor: int
    projection: str
    engines: int
    probes: int
    engine_pairs: int
    pairwise_checks: int
    false_equivalences: int
    elapsed_seconds: float
    checks_per_second: float

    def as_row(self) -> dict[str, str]:
        return {
            "scale_factor": str(self.scale_factor),
            "projection": self.projection,
            "engines": str(self.engines),
            "probes": str(self.probes),
            "engine_pairs": str(self.engine_pairs),
            "pairwise_checks": str(self.pairwise_checks),
            "false_equivalences": str(self.false_equivalences),
            "elapsed_seconds": f"{self.elapsed_seconds:.6f}",
            "checks_per_second": f"{self.checks_per_second:.2f}",
        }


def lifted_false_equivalence_count(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projection: str,
    scale_factor: int,
) -> int:
    """Count false equivalences over a virtual repeated-probe lift.

    This is an actual full-denominator count: every copied probe contributes the
    same pairwise checks as its base probe.  The function avoids building copied
    keys, so memory grows with the base corpus rather than the lift factor.
    """
    if scale_factor < 1:
        raise ValueError("scale_factor must be positive")
    projected = {key: project_signature(sig, projection) for key, sig in maps.items()}
    pairs = tuple(itertools.combinations(engines, 2))
    false_count = 0
    empty_projected: frozenset[tuple[str, ...]] = frozenset()
    for _copy in range(scale_factor):
        for probe in probes:
            for left, right in pairs:
                left_key, right_key = (left, probe), (right, probe)
                left_sig = maps.get(left_key, EMPTY_SIGNATURE)
                right_sig = maps.get(right_key, EMPTY_SIGNATURE)
                if left_sig != right_sig and projected.get(left_key, empty_projected) == projected.get(right_key, empty_projected):
                    false_count += 1
    return false_count


def run_scaling_curve(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projections: Sequence[str],
    scale_factors: Sequence[int],
) -> tuple[ScalingResult, ...]:
    """Measure finite-comparison throughput over deterministic lifted denominators."""
    results: list[ScalingResult] = []
    engine_pairs = len(engines) * (len(engines) - 1) // 2
    for scale in scale_factors:
        checks = engine_pairs * len(probes) * scale
        for projection in projections:
            start = time.perf_counter()
            false_equivalences = lifted_false_equivalence_count(maps, engines, probes, projection, scale)
            elapsed = max(time.perf_counter() - start, 1e-9)
            results.append(
                ScalingResult(
                    scale_factor=scale,
                    projection=projection,
                    engines=len(engines),
                    probes=len(probes) * scale,
                    engine_pairs=engine_pairs,
                    pairwise_checks=checks,
                    false_equivalences=false_equivalences,
                    elapsed_seconds=elapsed,
                    checks_per_second=checks / elapsed,
                )
            )
    return tuple(results)
