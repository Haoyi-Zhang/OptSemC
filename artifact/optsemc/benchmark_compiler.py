"""Feature-level compiler for external benchmark motifs.

OptSemBench-C does not copy third-party SQL workloads.  The relevant question is
whether the generated probe domain covers the optimizer surfaces used by known
benchmarks.  This compiler turns workload motifs into feature requirements,
finds matching probes, and computes a greedy minimal cover certificate.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .io import read_jsonl, read_yaml


@dataclass(frozen=True)
class MotifRequirement:
    suite_id: str
    suite_name: str
    motif_id: str
    requirements: tuple[tuple[str, str], ...]

    @property
    def requirement_key(self) -> str:
        return ";".join(f"{k}={v}" for k, v in self.requirements)

    def matches(self, feature_vector: Mapping[str, str]) -> bool:
        return all(str(feature_vector.get(key)) == value for key, value in self.requirements)


@dataclass(frozen=True)
class ProbeFeature:
    probe_id: str
    feature_vector: Mapping[str, str]
    sql_skeleton: str


@dataclass(frozen=True)
class MotifCoverage:
    suite_id: str
    suite_name: str
    motif_id: str
    requirements: str
    matching_probes: tuple[str, ...]

    @property
    def covered(self) -> bool:
        return bool(self.matching_probes)

    def as_row(self) -> dict[str, str]:
        return {
            "suite_id": self.suite_id,
            "suite_name": self.suite_name,
            "motif_id": self.motif_id,
            "requirements": self.requirements,
            "matching_probes": str(len(self.matching_probes)),
            "representative_probe": self.matching_probes[0] if self.matching_probes else "",
            "covered": str(self.covered).lower(),
        }


def _one_or_many(value: Any) -> tuple[str, ...]:
    if isinstance(value, list):
        return tuple(str(v) for v in value)
    return (str(value),)


def load_suite_requirements(path: Path) -> tuple[MotifRequirement, ...]:
    data = read_yaml(path)
    suites = data.get("suites", []) if isinstance(data, Mapping) else []
    motifs: list[MotifRequirement] = []
    for suite in suites:
        suite_id = str(suite.get("suite_id", ""))
        suite_name = str(suite.get("name", suite_id))
        for motif in suite.get("motifs", []):
            req_map = motif.get("requirements", {})
            expanded: list[list[tuple[str, str]]] = [[]]
            for key in sorted(req_map):
                values = _one_or_many(req_map[key])
                expanded = [prefix + [(str(key), value)] for prefix in expanded for value in values]
            # benchmark_suites.yaml uses single values; keep expansion for future
            # ranges and for reader-added motifs.
            for i, reqs in enumerate(expanded, 1):
                motif_id = str(motif.get("motif_id", ""))
                if len(expanded) > 1:
                    motif_id = f"{motif_id}#{i}"
                motifs.append(MotifRequirement(suite_id, suite_name, motif_id, tuple(reqs)))
    return tuple(motifs)


def load_probe_features(path: Path) -> tuple[ProbeFeature, ...]:
    probes = []
    for row in read_jsonl(path):
        fv = row.get("feature_vector", {})
        if isinstance(fv, Mapping):
            probes.append(ProbeFeature(str(row.get("probe_id", "")), {str(k): str(v) for k, v in fv.items()}, str(row.get("sql_skeleton", ""))))
    return tuple(probes)


def compute_motif_coverage(motifs: Sequence[MotifRequirement], probes: Sequence[ProbeFeature]) -> tuple[MotifCoverage, ...]:
    rows: list[MotifCoverage] = []
    for motif in motifs:
        matches = tuple(probe.probe_id for probe in probes if motif.matches(probe.feature_vector))
        rows.append(MotifCoverage(motif.suite_id, motif.suite_name, motif.motif_id, motif.requirement_key, matches))
    return tuple(rows)


def suite_summary(coverage: Sequence[MotifCoverage]) -> list[dict[str, str]]:
    by_suite: dict[str, list[MotifCoverage]] = {}
    names: dict[str, str] = {}
    for row in coverage:
        by_suite.setdefault(row.suite_id, []).append(row)
        names[row.suite_id] = row.suite_name
    out = []
    for suite_id in sorted(by_suite):
        rows = by_suite[suite_id]
        covered = sum(1 for row in rows if row.covered)
        matching = sum(len(row.matching_probes) for row in rows)
        out.append({
            "suite_id": suite_id,
            "suite_name": names[suite_id],
            "motifs": str(len(rows)),
            "covered_motifs": str(covered),
            "coverage_rate": f"{covered / len(rows) if rows else 0.0:.6f}",
            "matching_probes": str(matching),
        })
    return out


def greedy_probe_cover(coverage: Sequence[MotifCoverage]) -> list[dict[str, str]]:
    motif_to_probes = {row.motif_id: set(row.matching_probes) for row in coverage if row.matching_probes}
    uncovered = set(motif_to_probes)
    chosen: list[dict[str, str]] = []
    rank = 1
    while uncovered:
        probe_scores: dict[str, set[str]] = {}
        for motif in uncovered:
            for probe in motif_to_probes[motif]:
                probe_scores.setdefault(probe, set()).add(motif)
        if not probe_scores:
            break
        best_probe, best_motifs = max(probe_scores.items(), key=lambda item: (len(item[1]), item[0]))
        chosen.append({"rank": str(rank), "probe_id": best_probe, "new_motifs_covered": str(len(best_motifs)), "motifs": ";".join(sorted(best_motifs))})
        uncovered -= best_motifs
        rank += 1
    return chosen


def redundancy_rows(coverage: Sequence[MotifCoverage]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in coverage:
        match_count = len(row.matching_probes)
        rows.append({
            "suite_id": row.suite_id,
            "motif_id": row.motif_id,
            "matching_probes": str(match_count),
            "redundancy_level": "high" if match_count >= 100 else "medium" if match_count >= 10 else "low" if match_count >= 1 else "none",
            "covered": str(row.covered).lower(),
        })
    return rows
