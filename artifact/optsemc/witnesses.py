"""False-portability witness dispersion utilities.

The core evaluation counts false equivalences.  These helpers ask a different
reader question: are the witnesses concentrated in one hand-picked query, or
are they dispersed across probes, feature values, and engine-pair regions?  The
answer is computed from the same finite contract maps used by the projection
kernel checks.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Mapping, Sequence

from .projections import false_equivalence_witnesses
from .semantics import ContractSignature

ProbeFeatures = Mapping[str, Mapping[str, str]]


@dataclass(frozen=True)
class WitnessRecord:
    """One false-equivalence witness after a lossy projection."""

    projection: str
    probe_id: str
    left_engine: str
    right_engine: str

    @property
    def engine_pair(self) -> str:
        return "::".join(sorted((self.left_engine, self.right_engine)))

    def key(self) -> tuple[str, str, str, str]:
        left, right = sorted((self.left_engine, self.right_engine))
        return (self.projection, self.probe_id, left, right)


@dataclass(frozen=True)
class ProjectionDispersion:
    """Summary of how widely one projection's false witnesses are dispersed."""

    projection: str
    false_witnesses: int
    distinct_probes: int
    distinct_engine_pairs: int
    distinct_feature_values: int
    feature_dimensions_touched: int
    singleton_probe_witnesses: int
    max_witnesses_per_probe: int
    median_witnesses_per_probe: float

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "false_witnesses": str(self.false_witnesses),
            "distinct_probes": str(self.distinct_probes),
            "distinct_engine_pairs": str(self.distinct_engine_pairs),
            "distinct_feature_values": str(self.distinct_feature_values),
            "feature_dimensions_touched": str(self.feature_dimensions_touched),
            "singleton_probe_witnesses": str(self.singleton_probe_witnesses),
            "max_witnesses_per_probe": str(self.max_witnesses_per_probe),
            "median_witnesses_per_probe": f"{self.median_witnesses_per_probe:.1f}",
        }


def witness_records(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projections: Sequence[str],
) -> tuple[WitnessRecord, ...]:
    """Return all headline false-equivalence witnesses as typed records."""
    rows: list[WitnessRecord] = []
    for projection in projections:
        for method, probe_id, left_key, right_key in false_equivalence_witnesses(maps, engines, probes, projection):
            rows.append(WitnessRecord(method, probe_id, left_key[0], right_key[0]))
    return tuple(sorted(rows, key=lambda r: r.key()))


def median(values: Sequence[int]) -> float:
    """Return the median of a non-empty integer sequence."""
    ordered = sorted(values)
    if not ordered:
        return 0.0
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def feature_values_for(probe_ids: set[str], probe_features: ProbeFeatures) -> dict[str, set[str]]:
    """Collect feature values touched by a set of probes."""
    values: dict[str, set[str]] = defaultdict(set)
    for probe_id in probe_ids:
        for name, value in probe_features.get(probe_id, {}).items():
            values[name].add(str(value))
    return dict(values)


def dispersion_by_projection(records: Sequence[WitnessRecord], probe_features: ProbeFeatures) -> tuple[ProjectionDispersion, ...]:
    """Summarize witness dispersion for every projection present in records."""
    by_projection: dict[str, list[WitnessRecord]] = defaultdict(list)
    for record in records:
        by_projection[record.projection].append(record)
    rows: list[ProjectionDispersion] = []
    for projection, witnesses in sorted(by_projection.items()):
        probe_counts = Counter(w.probe_id for w in witnesses)
        probes = set(probe_counts)
        pairs = {w.engine_pair for w in witnesses}
        feature_values = feature_values_for(probes, probe_features)
        counts = list(probe_counts.values())
        rows.append(
            ProjectionDispersion(
                projection=projection,
                false_witnesses=len(witnesses),
                distinct_probes=len(probes),
                distinct_engine_pairs=len(pairs),
                distinct_feature_values=sum(len(v) for v in feature_values.values()),
                feature_dimensions_touched=sum(1 for v in feature_values.values() if v),
                singleton_probe_witnesses=sum(1 for c in counts if c == 1),
                max_witnesses_per_probe=max(counts) if counts else 0,
                median_witnesses_per_probe=median(counts),
            )
        )
    return tuple(rows)


def feature_coverage_rows(records: Sequence[WitnessRecord], probe_features: ProbeFeatures, all_features: ProbeFeatures) -> tuple[dict[str, str], ...]:
    """Compare feature values touched by witnesses with the full probe domain."""
    false_probes = {record.probe_id for record in records}
    false_values = feature_values_for(false_probes, probe_features)
    all_values: dict[str, set[str]] = defaultdict(set)
    for features in all_features.values():
        for name, value in features.items():
            all_values[name].add(str(value))
    rows: list[dict[str, str]] = []
    for name in sorted(all_values):
        touched = false_values.get(name, set())
        denominator = all_values[name]
        rows.append(
            {
                "feature": name,
                "touched_values": str(len(touched)),
                "total_values": str(len(denominator)),
                "coverage_fraction": f"{len(touched) / max(1, len(denominator)):.6f}",
                "missing_values": ";".join(sorted(denominator - touched)),
            }
        )
    return tuple(rows)


def greedy_probe_cover(records: Sequence[WitnessRecord]) -> tuple[dict[str, str], ...]:
    """Greedily order probes by the number of previously uncovered witnesses."""
    by_probe: dict[str, set[tuple[str, str, str, str]]] = defaultdict(set)
    for record in records:
        by_probe[record.probe_id].add(record.key())
    universe = set().union(*by_probe.values()) if by_probe else set()
    covered: set[tuple[str, str, str, str]] = set()
    rows: list[dict[str, str]] = []
    rank = 0
    while covered != universe:
        best_probe = max(sorted(by_probe), key=lambda probe: len(by_probe[probe] - covered))
        gain = len(by_probe[best_probe] - covered)
        if gain == 0:
            break
        rank += 1
        covered |= by_probe[best_probe]
        rows.append(
            {
                "rank": str(rank),
                "probe_id": best_probe,
                "new_witnesses": str(gain),
                "cumulative_witnesses": str(len(covered)),
                "total_witnesses": str(len(universe)),
                "coverage_fraction": f"{len(covered) / max(1, len(universe)):.6f}",
            }
        )
    return tuple(rows)
