"""Scalability and stratified robustness utilities for OptSem-C.

These routines intentionally measure the public-contract algorithms rather than
query runtime.  The work units are the finite objects in the formal model:
engine/probe signatures, pairwise projection comparisons, and repair checks.
"""
from __future__ import annotations

import itertools
import time
from dataclasses import dataclass
from typing import Mapping, Sequence

from .projections import project_signature
from .semantics import ContractSignature

EMPTY_SIGNATURE: ContractSignature = frozenset()


def natural_probe_key(probe_id: str) -> tuple[str, int | str]:
    prefix = ''.join(ch for ch in probe_id if not ch.isdigit())
    digits = ''.join(ch for ch in probe_id if ch.isdigit())
    return (prefix, int(digits) if digits else probe_id)


@dataclass(frozen=True)
class ScalingRow:
    projection: str
    probes: int
    engines: int
    engine_pairs: int
    comparisons: int
    projected_equivalences: int
    true_equivalences: int
    false_equivalences: int
    elapsed_ms: float
    comparisons_per_second: float
    mean_signature_atoms: float

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "probes": str(self.probes),
            "engines": str(self.engines),
            "engine_pairs": str(self.engine_pairs),
            "comparisons": str(self.comparisons),
            "projected_equivalences": str(self.projected_equivalences),
            "true_equivalences": str(self.true_equivalences),
            "false_equivalences": str(self.false_equivalences),
            "elapsed_ms": f"{self.elapsed_ms:.3f}",
            "comparisons_per_second": f"{self.comparisons_per_second:.1f}",
            "mean_signature_atoms": f"{self.mean_signature_atoms:.3f}",
        }


@dataclass(frozen=True)
class FamilyRow:
    projection: str
    pair_family: str
    engine_pairs: int
    probes: int
    comparisons: int
    projected_equivalences: int
    true_equivalences: int
    false_equivalences: int
    repaired_by_layer_placement: int
    unresolved_after_layer_placement: int

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "pair_family": self.pair_family,
            "engine_pairs": str(self.engine_pairs),
            "probes": str(self.probes),
            "comparisons": str(self.comparisons),
            "projected_equivalences": str(self.projected_equivalences),
            "true_equivalences": str(self.true_equivalences),
            "false_equivalences": str(self.false_equivalences),
            "repaired_by_layer_placement": str(self.repaired_by_layer_placement),
            "unresolved_after_layer_placement": str(self.unresolved_after_layer_placement),
        }


ENGINE_FAMILIES: Mapping[str, str] = {
    "BigQuery": "cloud_service",
    "Snowflake": "cloud_service",
    "DuckDB": "local_embedded",
    "PostgreSQL": "local_embedded",
    "ClickHouse": "local_embedded",
    "Spark SQL": "distributed_sql",
    "Trino": "distributed_sql",
}


def pair_family(left: str, right: str) -> str:
    lf = ENGINE_FAMILIES.get(left, "other")
    rf = ENGINE_FAMILIES.get(right, "other")
    if lf == rf:
        return f"within_{lf}"
    return "cross_" + "_vs_".join(sorted((lf, rf)))


def projection_counts(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projection: str,
    *,
    extra_fields: Sequence[str] = (),
) -> tuple[int, int, int]:
    """Count projected equivalences without materializing a projection map.

    Earlier versions precomputed a dictionary for every prefix budget.  That is
    fast for one run but creates avoidable allocator pressure when a reader
    replays many budgets/projections in the same Python process.  The streaming
    version below recomputes the two projected signatures needed by each pair;
    it preserves the formal denominator while keeping peak memory bounded by one
    engine-pair comparison.
    """
    projected_equivalences = 0
    true_equivalences = 0
    false_equivalences = 0
    for probe in probes:
        for left, right in itertools.combinations(engines, 2):
            left_key, right_key = (left, probe), (right, probe)
            left_sig = maps.get(left_key, EMPTY_SIGNATURE)
            right_sig = maps.get(right_key, EMPTY_SIGNATURE)
            if project_signature(left_sig, projection, extra_fields) == project_signature(right_sig, projection, extra_fields):
                projected_equivalences += 1
                if left_sig == right_sig:
                    true_equivalences += 1
                else:
                    false_equivalences += 1
    return projected_equivalences, true_equivalences, false_equivalences


def scaling_profile(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projections: Sequence[str],
    budgets: Sequence[int],
) -> tuple[ScalingRow, ...]:
    ordered_probes = tuple(sorted(probes, key=natural_probe_key))
    engine_pairs = len(tuple(itertools.combinations(engines, 2)))
    rows: list[ScalingRow] = []
    for budget in budgets:
        prefix = ordered_probes[: min(budget, len(ordered_probes))]
        atom_total = sum(len(maps.get((engine, probe), EMPTY_SIGNATURE)) for engine in engines for probe in prefix)
        mean_atoms = atom_total / max(1, len(engines) * len(prefix))
        for projection in projections:
            started = time.perf_counter()
            projected_eq, true_eq, false_eq = projection_counts(maps, engines, prefix, projection)
            elapsed_ms = (time.perf_counter() - started) * 1000.0
            comparisons = len(prefix) * engine_pairs
            throughput = comparisons / max(elapsed_ms / 1000.0, 1e-9)
            rows.append(
                ScalingRow(
                    projection=projection,
                    probes=len(prefix),
                    engines=len(engines),
                    engine_pairs=engine_pairs,
                    comparisons=comparisons,
                    projected_equivalences=projected_eq,
                    true_equivalences=true_eq,
                    false_equivalences=false_eq,
                    elapsed_ms=elapsed_ms,
                    comparisons_per_second=throughput,
                    mean_signature_atoms=mean_atoms,
                )
            )
    return tuple(rows)


def family_stress_profile(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projections: Sequence[str],
) -> tuple[FamilyRow, ...]:
    rows: list[FamilyRow] = []
    pair_groups: dict[str, list[tuple[str, str]]] = {}
    for left, right in itertools.combinations(engines, 2):
        pair_groups.setdefault(pair_family(left, right), []).append((left, right))
    projected_cache: dict[tuple[str, tuple[str, ...]], dict[tuple[str, str], frozenset[tuple[str, ...]]]] = {}
    for projection in projections:
        for group_name, pairs in sorted(pair_groups.items()):
            projected = projected_cache.setdefault(
                (projection, ()),
                {key: project_signature(sig, projection) for key, sig in maps.items()},
            )
            repaired_projected = projected_cache.setdefault(
                (projection, ("layer", "placement")),
                {key: project_signature(sig, projection, ("layer", "placement")) for key, sig in maps.items()},
            )
            projected_eq = true_eq = false_eq = repaired = unresolved = 0
            for probe in probes:
                for left, right in pairs:
                    left_key, right_key = (left, probe), (right, probe)
                    left_sig = maps.get(left_key, EMPTY_SIGNATURE)
                    right_sig = maps.get(right_key, EMPTY_SIGNATURE)
                    if projected.get(left_key, frozenset()) != projected.get(right_key, frozenset()):
                        continue
                    projected_eq += 1
                    if left_sig == right_sig:
                        true_eq += 1
                    else:
                        false_eq += 1
                        if repaired_projected.get(left_key, frozenset()) != repaired_projected.get(right_key, frozenset()):
                            repaired += 1
                        else:
                            unresolved += 1
            rows.append(
                FamilyRow(
                    projection=projection,
                    pair_family=group_name,
                    engine_pairs=len(pairs),
                    probes=len(probes),
                    comparisons=len(probes) * len(pairs),
                    projected_equivalences=projected_eq,
                    true_equivalences=true_eq,
                    false_equivalences=false_eq,
                    repaired_by_layer_placement=repaired,
                    unresolved_after_layer_placement=unresolved,
                )
            )
    return tuple(rows)
