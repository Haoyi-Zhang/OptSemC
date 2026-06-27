"""Load grounded OptSem-C maps, rules, probes, and source manifests."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from functools import lru_cache
from typing import Any, Mapping

from .io import read_csv, read_jsonl
from .semantics import ContractSignature, evidence_signature
from .domain import ContractRule, EvidenceSegment, SourceRecord, Probe, ContractMapRecord


@dataclass(frozen=True)
class ContractMaps:
    maps: dict[tuple[str, str], ContractSignature]
    engines: tuple[str, ...]
    probes: tuple[str, ...]


@dataclass(frozen=True)
class GroundedCorpus:
    rules: tuple[ContractRule, ...]
    segments: tuple[EvidenceSegment, ...]
    sources: tuple[SourceRecord, ...]
    probes: tuple[Probe, ...]
    contract_maps: ContractMaps


def artifact_path(path: Path, relative: str) -> Path:
    """Resolve a path relative to the artifact directory or pass through files."""
    if path.is_file():
        return path
    return path / relative


@lru_cache(maxsize=8)
def load_contract_maps(path: Path) -> ContractMaps:
    file_path = artifact_path(path, "evaluation/grounded_contract_maps.jsonl")
    maps: dict[tuple[str, str], ContractSignature] = {}
    engines: set[str] = set()
    probes: set[str] = set()
    for row in read_jsonl(file_path):
        rec = ContractMapRecord.from_json(row)
        maps[rec.key] = evidence_signature(rec.actions)
        engines.add(rec.engine)
        probes.add(rec.probe_id)
    return ContractMaps(maps, tuple(sorted(engines)), tuple(sorted(probes)))


def load_engines_probes(path: Path) -> tuple[tuple[str, ...], tuple[str, ...]]:
    cm = load_contract_maps(path)
    return cm.engines, cm.probes


def load_rules(path: Path) -> list[dict[str, Any]]:
    return list(read_jsonl(artifact_path(path, "grounded/verified_rules.jsonl")))


def load_rule_objects(path: Path) -> tuple[ContractRule, ...]:
    return tuple(ContractRule.from_json(row) for row in load_rules(path))


def load_segments(path: Path) -> list[dict[str, Any]]:
    return list(read_jsonl(artifact_path(path, "grounded/verified_segments.jsonl")))


def load_segment_objects(path: Path) -> tuple[EvidenceSegment, ...]:
    return tuple(EvidenceSegment.from_json(row) for row in load_segments(path))


@lru_cache(maxsize=8)
def load_probes(path: Path) -> tuple[dict[str, Any], ...]:
    return tuple(read_jsonl(artifact_path(path, "benchmark/generated_probes.jsonl")))


def load_probe_objects(path: Path) -> tuple[Probe, ...]:
    return tuple(Probe.from_json(row) for row in load_probes(path))


def load_sources(path: Path) -> list[dict[str, str]]:
    return read_csv(artifact_path(path, "grounded/verified_sources.csv"))


def load_source_objects(path: Path) -> tuple[SourceRecord, ...]:
    return tuple(SourceRecord.from_mapping(row) for row in load_sources(path))


def load_grounded_corpus(path: Path) -> GroundedCorpus:
    return GroundedCorpus(
        rules=load_rule_objects(path),
        segments=load_segment_objects(path),
        sources=load_source_objects(path),
        probes=load_probe_objects(path),
        contract_maps=load_contract_maps(path),
    )


def contract_map_rows(path: Path) -> tuple[ContractMapRecord, ...]:
    return tuple(ContractMapRecord.from_json(row) for row in read_jsonl(artifact_path(path, "evaluation/grounded_contract_maps.jsonl")))


def engine_rule_counts(rules: tuple[ContractRule, ...]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for rule in rules:
        counts[rule.engine] = counts.get(rule.engine, 0) + 1
    return dict(sorted(counts.items()))


def action_domain(rules: tuple[ContractRule, ...]) -> dict[str, tuple[str, ...]]:
    fields = {name: set() for name in ("operator", "kind", "variant", "layer", "placement", "decision_time", "observability")}
    fields["state"] = set()
    for rule in rules:
        for name in rule.action.field_names():
            fields[name].add(getattr(rule.action, name))
        fields["state"].add(rule.state)
    return {name: tuple(sorted(values)) for name, values in fields.items()}
