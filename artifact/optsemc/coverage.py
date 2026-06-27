"""Benchmark and feature-coverage utilities."""
from __future__ import annotations

import ast
import itertools
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from .domain import Probe


def interaction_key(items: Sequence[tuple[str, str]]) -> str:
    return repr(tuple(sorted(items)))


def combinations_from_vector(vector: Mapping[str, str], strength: int) -> tuple[str, ...]:
    pairs = sorted(vector.items())
    return tuple(interaction_key(combo) for combo in itertools.combinations(pairs, strength))


def parse_interaction(text: str) -> tuple[tuple[str, str], ...]:
    value = ast.literal_eval(text)
    return tuple((str(k), str(v)) for k, v in value)


@dataclass(frozen=True)
class CoverageSummary:
    strength: int
    covered: int
    required: int
    probes: int

    @property
    def rate(self) -> float:
        return self.covered / self.required if self.required else 1.0

    def as_row(self) -> dict[str, str]:
        return {
            "strength": str(self.strength),
            "covered": str(self.covered),
            "required": str(self.required),
            "coverage_rate": f"{self.rate:.6f}",
            "probes": str(self.probes),
        }


def observed_interactions(probes: Sequence[Probe], strength: int) -> set[str]:
    seen: set[str] = set()
    for probe in probes:
        seen.update(combinations_from_vector(probe.feature_vector, strength))
    return seen


def declared_interactions(probes: Sequence[Probe]) -> set[str]:
    seen: set[str] = set()
    for probe in probes:
        seen.update(probe.covered_interactions)
    return seen


def required_interactions_from_domain(feature_domain: Mapping[str, Sequence[str]], strength: int) -> set[str]:
    fields = sorted(feature_domain)
    interactions: set[str] = set()
    for names in itertools.combinations(fields, strength):
        for values in itertools.product(*(feature_domain[name] for name in names)):
            interactions.add(interaction_key(tuple(zip(names, map(str, values)))))
    return interactions


def coverage_summary(probes: Sequence[Probe], feature_domain: Mapping[str, Sequence[str]], strength: int) -> CoverageSummary:
    observed = observed_interactions(probes, strength)
    required = required_interactions_from_domain(feature_domain, strength)
    return CoverageSummary(strength, len(observed & required), len(required), len(probes))


def feature_value_counts(probes: Sequence[Probe]) -> list[dict[str, str]]:
    counts: dict[tuple[str, str], int] = defaultdict(int)
    for probe in probes:
        for feature, value in probe.feature_vector.items():
            counts[(feature, value)] += 1
    rows = []
    for (feature, value), count in sorted(counts.items()):
        rows.append({"feature": feature, "value": value, "probe_count": str(count)})
    return rows


def motif_covered(probes: Sequence[Probe], requirements: Mapping[str, str]) -> tuple[bool, int]:
    count = 0
    for probe in probes:
        if all(probe.feature_vector.get(feature) == value for feature, value in requirements.items()):
            count += 1
    return count > 0, count


def benchmark_suite_crosswalk(probes: Sequence[Probe], suites: Sequence[Mapping[str, object]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for suite in suites:
        suite_id = str(suite.get("suite_id") or suite.get("name") or "unknown")
        suite_name = str(suite.get("name") or suite_id)
        motifs = list(suite.get("motifs") or [])
        covered = 0
        total_probe_hits = 0
        for motif in motifs:
            req = {str(k): str(v) for k, v in dict(motif.get("requirements") or {}).items()}
            ok, hits = motif_covered(probes, req)
            covered += int(ok)
            total_probe_hits += hits
        rows.append({
            "suite_id": suite_id,
            "suite_name": suite_name,
            "motifs": str(len(motifs)),
            "covered_motifs": str(covered),
            "coverage_rate": f"{covered / len(motifs) if motifs else 1.0:.6f}",
            "matching_probes": str(total_probe_hits),
        })
    return rows


def greedy_probe_cover(probes: Sequence[Probe], universe: Iterable[str], max_steps: int | None = None) -> list[dict[str, str]]:
    remaining = set(universe)
    chosen: list[dict[str, str]] = []
    available = list(probes)
    step = 0
    while remaining and available and (max_steps is None or step < max_steps):
        best = max(available, key=lambda p: len(set(p.covered_interactions) & remaining))
        gain = set(best.covered_interactions) & remaining
        if not gain:
            break
        step += 1
        remaining -= gain
        chosen.append({
            "step": str(step),
            "probe_id": best.probe_id,
            "new_interactions": str(len(gain)),
            "remaining_interactions": str(len(remaining)),
            "sql_skeleton_hash": str(abs(hash(best.sql_skeleton))),
        })
        available = [probe for probe in available if probe.probe_id != best.probe_id]
    return chosen

