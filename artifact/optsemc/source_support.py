"""Evidence-source support diagnostics for contract-level false-equivalence witnesses."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from .corpus import load_contract_maps
from .io import read_jsonl
from .projections import false_equivalence_witnesses


@dataclass(frozen=True)
class WitnessSourceRecord:
    """Source-support summary for one false-equivalence witness."""

    projection: str
    probe_id: str
    engine_left: str
    engine_right: str
    sources: tuple[str, ...]
    rule_count: int

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "probe_id": self.probe_id,
            "engine_left": self.engine_left,
            "engine_right": self.engine_right,
            "source_count": str(len(self.sources)),
            "sources": ";".join(self.sources),
            "supporting_rules": str(self.rule_count),
        }


def rule_source_index(artifact_root: Path) -> dict[str, str]:
    """Return a rule-id to public source-id index."""
    index: dict[str, str] = {}
    for row in read_jsonl(artifact_root / "grounded" / "verified_rules.jsonl"):
        rule_id = str(row.get("rule_id", ""))
        source_id = str(row.get("evidence", {}).get("source_id", ""))
        if rule_id and source_id:
            index[rule_id] = source_id
    return index


def contract_support_index(artifact_root: Path) -> dict[tuple[str, str], dict[str, tuple[str, ...]]]:
    """Return support lists for each engine-probe contract-map record."""
    support: dict[tuple[str, str], dict[str, tuple[str, ...]]] = {}
    for row in read_jsonl(artifact_root / "evaluation" / "grounded_contract_support.jsonl"):
        key = (str(row["engine"]), str(row["probe_id"]))
        action_support = row.get("supporting_rules", {}) or {}
        support[key] = {str(action): tuple(str(r) for r in rules) for action, rules in action_support.items()}
    return support


def _support_sources(
    key: tuple[str, str],
    support: Mapping[tuple[str, str], Mapping[str, Sequence[str]]],
    rule_sources: Mapping[str, str],
) -> tuple[set[str], int]:
    sources: set[str] = set()
    rules_seen: set[str] = set()
    for rules in support.get(key, {}).values():
        for rule_id in rules:
            if rule_id in rule_sources:
                sources.add(rule_sources[rule_id])
                rules_seen.add(rule_id)
    return sources, len(rules_seen)


def witness_source_records(artifact_root: Path, projections: Sequence[str]) -> list[WitnessSourceRecord]:
    """Compute public evidence-source support for every false witness."""
    maps = load_contract_maps(artifact_root)
    rule_sources = rule_source_index(artifact_root)
    support = contract_support_index(artifact_root)
    records: list[WitnessSourceRecord] = []
    for projection in projections:
        for method, probe_id, left_key, right_key in false_equivalence_witnesses(
            maps.maps, maps.engines, maps.probes, projection
        ):
            left_sources, left_rules = _support_sources(left_key, support, rule_sources)
            right_sources, right_rules = _support_sources(right_key, support, rule_sources)
            records.append(
                WitnessSourceRecord(
                    projection=method,
                    probe_id=probe_id,
                    engine_left=left_key[0],
                    engine_right=right_key[0],
                    sources=tuple(sorted(left_sources | right_sources)),
                    rule_count=left_rules + right_rules,
                )
            )
    return records


def _median(values: list[int]) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    mid = len(values) // 2
    if len(values) % 2:
        return float(values[mid])
    return (values[mid - 1] + values[mid]) / 2.0


def witness_source_summary(records: Sequence[WitnessSourceRecord]) -> list[dict[str, str]]:
    """Aggregate witness-source support by projection."""
    projections = sorted({record.projection for record in records})
    rows: list[dict[str, str]] = []
    for projection in projections:
        group = [record for record in records if record.projection == projection]
        source_counts = [len(record.sources) for record in group]
        distinct_sources = sorted({source for record in group for source in record.sources})
        cross_source = sum(1 for count in source_counts if count >= 2)
        rows.append(
            {
                "projection": projection,
                "false_witnesses": str(len(group)),
                "distinct_sources": str(len(distinct_sources)),
                "min_sources_per_witness": str(min(source_counts) if source_counts else 0),
                "median_sources_per_witness": f"{_median(source_counts):.1f}",
                "max_sources_per_witness": str(max(source_counts) if source_counts else 0),
                "cross_source_witnesses": str(cross_source),
                "cross_source_share": f"{(cross_source / len(group)) if group else 0.0:.6f}",
            }
        )
    return rows
