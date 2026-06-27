"""Metric computations for public optimizer-contract comparison."""
from __future__ import annotations

import itertools
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from .projections import project_signature
from .semantics import ContractSignature


@dataclass(frozen=True)
class EquivalenceMetrics:
    projection: str
    comparisons: int
    projected_equivalences: int
    true_equivalences: int
    false_equivalences: int
    false_differences: int

    @property
    def projected_equivalence_rate(self) -> float:
        return self.projected_equivalences / self.comparisons if self.comparisons else 0.0

    @property
    def conditional_false_equivalence_rate(self) -> float:
        return self.false_equivalences / self.projected_equivalences if self.projected_equivalences else 0.0

    @property
    def exact_equivalence_rate(self) -> float:
        return self.true_equivalences / self.comparisons if self.comparisons else 0.0

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "comparisons": str(self.comparisons),
            "projected_equivalences": str(self.projected_equivalences),
            "true_equivalences": str(self.true_equivalences),
            "false_equivalences": str(self.false_equivalences),
            "false_differences": str(self.false_differences),
            "projected_equivalence_rate": f"{self.projected_equivalence_rate:.6f}",
            "conditional_false_equivalence_rate": f"{self.conditional_false_equivalence_rate:.6f}",
            "exact_equivalence_rate": f"{self.exact_equivalence_rate:.6f}",
        }


def equivalence_metrics(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projection: str,
    extra_fields: Sequence[str] = (),
) -> EquivalenceMetrics:
    comparisons = projected_equivalences = true_equivalences = false_equivalences = false_differences = 0
    pairs = list(itertools.combinations(engines, 2))
    empty: ContractSignature = frozenset()
    projected_cache = {key: project_signature(sig, projection, extra_fields) for key, sig in maps.items()}
    for probe in probes:
        for left, right in pairs:
            left_key = (left, probe)
            right_key = (right, probe)
            left_sig = maps.get(left_key, empty)
            right_sig = maps.get(right_key, empty)
            exact_equal = left_sig == right_sig
            projected_equal = projected_cache.get(left_key, frozenset()) == projected_cache.get(right_key, frozenset())
            comparisons += 1
            if projected_equal:
                projected_equivalences += 1
            if exact_equal:
                true_equivalences += 1
            if projected_equal and not exact_equal:
                false_equivalences += 1
            if exact_equal and not projected_equal:
                false_differences += 1
    return EquivalenceMetrics(projection, comparisons, projected_equivalences, true_equivalences, false_equivalences, false_differences)


def engine_pair_matrix(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projection: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    empty: ContractSignature = frozenset()
    projected_cache = {key: project_signature(sig, projection) for key, sig in maps.items()}
    for left, right in itertools.combinations(sorted(engines), 2):
        comparisons = true_eq = projected_eq = false_eq = false_diff = 0
        for probe in probes:
            lk, rk = (left, probe), (right, probe)
            ls, rs = maps.get(lk, empty), maps.get(rk, empty)
            exact = ls == rs
            proj = projected_cache.get(lk, frozenset()) == projected_cache.get(rk, frozenset())
            comparisons += 1
            true_eq += int(exact)
            projected_eq += int(proj)
            false_eq += int(proj and not exact)
            false_diff += int(exact and not proj)
        rows.append({
            "projection": projection,
            "engine_left": left,
            "engine_right": right,
            "comparisons": str(comparisons),
            "true_equivalences": str(true_eq),
            "projected_equivalences": str(projected_eq),
            "false_equivalences": str(false_eq),
            "false_differences": str(false_diff),
            "conditional_false_equivalence_rate": f"{(false_eq / projected_eq) if projected_eq else 0.0:.6f}",
        })
    return rows


def wilson_interval(successes: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    if trials == 0:
        return (0.0, 0.0)
    p = successes / trials
    denom = 1 + z * z / trials
    centre = (p + z * z / (2 * trials)) / denom
    spread = z * math.sqrt((p * (1 - p) + z * z / (4 * trials)) / trials) / denom
    return max(0.0, centre - spread), min(1.0, centre + spread)


def aggregate_by(rows: Iterable[Mapping[str, str]], key_fields: Sequence[str], value_field: str) -> list[dict[str, str]]:
    buckets: dict[tuple[str, ...], int] = defaultdict(int)
    counts: dict[tuple[str, ...], int] = defaultdict(int)
    for row in rows:
        key = tuple(row.get(field, "") for field in key_fields)
        buckets[key] += int(float(row.get(value_field, 0) or 0))
        counts[key] += 1
    out = []
    for key in sorted(buckets):
        rec = {field: value for field, value in zip(key_fields, key)}
        rec[f"sum_{value_field}"] = str(buckets[key])
        rec["rows"] = str(counts[key])
        out.append(rec)
    return out


def rank_counter(items: Iterable[str]) -> list[dict[str, str]]:
    counter = Counter(items)
    total = sum(counter.values())
    rows = []
    for rank, (item, count) in enumerate(counter.most_common(), 1):
        rows.append({"rank": str(rank), "item": item, "count": str(count), "share": f"{count / total if total else 0.0:.6f}"})
    return rows

