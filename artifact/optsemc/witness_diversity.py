"""Diversity diagnostics for false-equivalence witnesses.

A projection can look convincing if all of its false equivalences come from one
query shape or one engine pair.  These helpers summarize false-equivalence
witnesses over probe features and engine pairs so that the artifact can reject
that failure mode explicitly.
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Mapping, Sequence

Witness = tuple[str, str, tuple[str, str], tuple[str, str]]

FEATURE_AXES: tuple[str, ...] = (
    "source_boundary",
    "join_type",
    "join_shape",
    "aggregation",
    "adaptivity_trigger",
    "distribution_trigger",
    "reuse_structure",
    "control_surface",
    "statistics_need",
)


def normalized_entropy(counter: Counter[str]) -> float:
    """Return entropy normalized by the maximum for the observed support."""
    total = sum(counter.values())
    if total <= 0 or len(counter) <= 1:
        return 0.0
    ent = -sum((count / total) * math.log2(count / total) for count in counter.values() if count)
    return ent / math.log2(len(counter))


@dataclass(frozen=True)
class WitnessDiversitySummary:
    """Aggregate diversity of false witnesses for one projection."""

    projection: str
    witnesses: int
    distinct_probes: int
    distinct_engine_pairs: int
    feature_axes_with_multiple_values: int
    max_feature_values: int
    mean_normalized_entropy: float
    max_single_value_share: float

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "witnesses": str(self.witnesses),
            "distinct_probes": str(self.distinct_probes),
            "distinct_engine_pairs": str(self.distinct_engine_pairs),
            "feature_axes_with_multiple_values": str(self.feature_axes_with_multiple_values),
            "max_feature_values": str(self.max_feature_values),
            "mean_normalized_entropy": f"{self.mean_normalized_entropy:.6f}",
            "max_single_value_share": f"{self.max_single_value_share:.6f}",
        }


@dataclass(frozen=True)
class WitnessFeatureRow:
    """One feature-axis diversity row for one projection."""

    projection: str
    feature: str
    values: int
    dominant_value: str
    dominant_count: int
    dominant_share: float
    normalized_entropy: float

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "feature": self.feature,
            "values": str(self.values),
            "dominant_value": self.dominant_value,
            "dominant_count": str(self.dominant_count),
            "dominant_share": f"{self.dominant_share:.6f}",
            "normalized_entropy": f"{self.normalized_entropy:.6f}",
        }


def feature_rows(
    projection: str,
    witnesses: Sequence[Witness],
    probe_features: Mapping[str, Mapping[str, str]],
    feature_axes: Sequence[str] = FEATURE_AXES,
) -> tuple[WitnessFeatureRow, ...]:
    """Summarize feature-axis diversity for a projection's witnesses."""
    rows: list[WitnessFeatureRow] = []
    for feature in feature_axes:
        counter: Counter[str] = Counter(str(probe_features[w[1]].get(feature, "")) for w in witnesses)
        if counter:
            dominant_value, dominant_count = counter.most_common(1)[0]
            total = sum(counter.values())
            rows.append(WitnessFeatureRow(
                projection=projection,
                feature=feature,
                values=len(counter),
                dominant_value=dominant_value,
                dominant_count=dominant_count,
                dominant_share=dominant_count / total,
                normalized_entropy=normalized_entropy(counter),
            ))
        else:
            rows.append(WitnessFeatureRow(projection, feature, 0, "", 0, 0.0, 0.0))
    return tuple(rows)


def summarize_witness_diversity(
    projection: str,
    witnesses: Sequence[Witness],
    probe_features: Mapping[str, Mapping[str, str]],
    feature_axes: Sequence[str] = FEATURE_AXES,
) -> WitnessDiversitySummary:
    """Return aggregate diversity for one projection."""
    if not witnesses:
        return WitnessDiversitySummary(projection, 0, 0, 0, 0, 0, 0.0, 0.0)
    rows = feature_rows(projection, witnesses, probe_features, feature_axes)
    distinct_pairs = {tuple(sorted((w[2][0], w[3][0]))) for w in witnesses}
    return WitnessDiversitySummary(
        projection=projection,
        witnesses=len(witnesses),
        distinct_probes=len({w[1] for w in witnesses}),
        distinct_engine_pairs=len(distinct_pairs),
        feature_axes_with_multiple_values=sum(1 for row in rows if row.values >= 2),
        max_feature_values=max(row.values for row in rows),
        mean_normalized_entropy=sum(row.normalized_entropy for row in rows) / len(rows),
        max_single_value_share=max(row.dominant_share for row in rows),
    )
