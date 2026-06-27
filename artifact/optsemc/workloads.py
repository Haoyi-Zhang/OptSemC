"""Workload-family abstractions for external optimizer benchmark motifs."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Sequence

from .domain import Probe
from .io import read_yaml
from .coverage import motif_covered


@dataclass(frozen=True)
class WorkloadMotif:
    motif_id: str
    requirements: Mapping[str, str]
    description: str = ""

    @classmethod
    def from_mapping(cls, record: Mapping[str, object]) -> "WorkloadMotif":
        return cls(str(record.get("motif_id") or record.get("id") or "unknown"), {str(k): str(v) for k, v in dict(record.get("requirements") or {}).items()}, str(record.get("description") or ""))

    def matches(self, probe: Probe) -> bool:
        return all(probe.feature_vector.get(k) == v for k, v in self.requirements.items())

    def matching_probe_ids(self, probes: Sequence[Probe]) -> tuple[str, ...]:
        return tuple(probe.probe_id for probe in probes if self.matches(probe))


@dataclass(frozen=True)
class WorkloadSuite:
    suite_id: str
    name: str
    motifs: tuple[WorkloadMotif, ...] = field(default_factory=tuple)

    @classmethod
    def from_mapping(cls, record: Mapping[str, object]) -> "WorkloadSuite":
        return cls(str(record.get("suite_id") or record.get("id") or record.get("name") or "unknown"), str(record.get("name") or record.get("suite_id") or "unknown"), tuple(WorkloadMotif.from_mapping(m) for m in record.get("motifs") or ()))

    def coverage(self, probes: Sequence[Probe]) -> dict[str, str]:
        covered = 0
        hits = 0
        for motif in self.motifs:
            ids = motif.matching_probe_ids(probes)
            covered += int(bool(ids))
            hits += len(ids)
        return {"suite_id": self.suite_id, "suite_name": self.name, "motifs": str(len(self.motifs)), "covered_motifs": str(covered), "coverage_rate": f"{covered/len(self.motifs) if self.motifs else 1.0:.6f}", "matching_probes": str(hits)}

    def gaps(self, probes: Sequence[Probe]) -> tuple[WorkloadMotif, ...]:
        return tuple(motif for motif in self.motifs if not motif.matching_probe_ids(probes))


def load_workload_suites(path: Path) -> tuple[WorkloadSuite, ...]:
    data = read_yaml(path) or {}
    return tuple(WorkloadSuite.from_mapping(row) for row in data.get("suites") or ())


def suite_coverage_matrix(suites: Sequence[WorkloadSuite], probes: Sequence[Probe]) -> list[dict[str, str]]:
    rows = []
    for suite in suites:
        for motif in suite.motifs:
            ids = motif.matching_probe_ids(probes)
            rows.append({"suite_id": suite.suite_id, "suite_name": suite.name, "motif_id": motif.motif_id, "requirements": ";".join(f"{k}={v}" for k, v in sorted(motif.requirements.items())), "covered": str(bool(ids)).lower(), "matching_probes": str(len(ids)), "example_probe": ids[0] if ids else ""})
    return rows


def suite_depth_summary(suites: Sequence[WorkloadSuite], probes: Sequence[Probe]) -> list[dict[str, str]]:
    rows = []
    for suite in suites:
        hit_counts = [len(motif.matching_probe_ids(probes)) for motif in suite.motifs]
        rows.append({"suite_id": suite.suite_id, "motifs": str(len(hit_counts)), "min_hits": str(min(hit_counts) if hit_counts else 0), "median_hits": str(sorted(hit_counts)[len(hit_counts)//2] if hit_counts else 0), "max_hits": str(max(hit_counts) if hit_counts else 0), "total_hits": str(sum(hit_counts))})
    return rows


def representative_probe_set(suites: Sequence[WorkloadSuite], probes: Sequence[Probe]) -> list[dict[str, str]]:
    rows = []
    for suite in suites:
        for motif in suite.motifs:
            ids = motif.matching_probe_ids(probes)
            if ids:
                rows.append({"suite_id": suite.suite_id, "motif_id": motif.motif_id, "probe_id": ids[0], "alternatives": str(max(0, len(ids)-1))})
    return rows

