"""Benchmark-feature helpers and coverage summaries."""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable, Mapping, Sequence


def feature_counter(probes: Iterable[Mapping[str, object]], feature: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for probe in probes:
        vector = probe.get("feature_vector", {})
        if isinstance(vector, Mapping):
            counter[str(vector.get(feature, ""))] += 1
    return counter


def coverage_for_requirements(probes: Sequence[Mapping[str, object]], requirements: Mapping[str, Sequence[str]]) -> tuple[int, int, list[str]]:
    """Return how many named feature-value requirements are covered by probes."""
    present = defaultdict(set)
    for probe in probes:
        vector = probe.get("feature_vector", {})
        if isinstance(vector, Mapping):
            for feature, value in vector.items():
                present[str(feature)].add(str(value))
    required = [(feature, value) for feature, values in requirements.items() for value in values]
    missing = [f"{feature}={value}" for feature, value in required if value not in present.get(feature, set())]
    return len(required) - len(missing), len(required), missing
