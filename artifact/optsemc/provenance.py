"""Public provenance graph and hash checks for grounded evidence."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Mapping, Sequence

from .domain import ContractRule, EvidenceSegment, SourceRecord, duplicate_keys


@dataclass(frozen=True)
class ProvenanceIssue:
    kind: str
    object_id: str
    details: str

    def as_row(self) -> dict[str, str]:
        return {"kind": self.kind, "object_id": self.object_id, "details": self.details}


def audit_provenance(
    rules: Sequence[ContractRule],
    segments: Sequence[EvidenceSegment],
    sources: Sequence[SourceRecord],
) -> tuple[ProvenanceIssue, ...]:
    issues: list[ProvenanceIssue] = []
    segment_by_id = {segment.segment_id: segment for segment in segments}
    source_by_id = {source.source_id: source for source in sources}
    for dup in duplicate_keys(rule.rule_id for rule in rules):
        issues.append(ProvenanceIssue("duplicate_rule_id", dup, "rule_id appears more than once"))
    for dup in duplicate_keys(segment.segment_id for segment in segments):
        issues.append(ProvenanceIssue("duplicate_segment_id", dup, "segment_id appears more than once"))
    for dup in duplicate_keys(source.source_id for source in sources):
        issues.append(ProvenanceIssue("duplicate_source_id", dup, "source_id appears more than once"))
    for rule in rules:
        ok, rule_issues = rule.validates()
        for item in rule_issues:
            issues.append(ProvenanceIssue("invalid_rule", rule.rule_id, item))
        segment = segment_by_id.get(rule.evidence.segment_id)
        if not segment:
            issues.append(ProvenanceIssue("missing_segment", rule.rule_id, rule.evidence.segment_id))
            continue
        if segment.source_id != rule.evidence.source_id:
            issues.append(ProvenanceIssue("segment_source_mismatch", rule.rule_id, f"{segment.source_id}!={rule.evidence.source_id}"))
        if segment.line_range != rule.evidence.line_range:
            issues.append(ProvenanceIssue("line_range_mismatch", rule.rule_id, f"{segment.line_range.as_text()}!={rule.evidence.line_range.as_text()}"))
        if segment.source_id not in source_by_id:
            issues.append(ProvenanceIssue("missing_source", rule.rule_id, segment.source_id))
    for segment in segments:
        ok, segment_issues = segment.validates()
        for item in segment_issues:
            issues.append(ProvenanceIssue("invalid_segment", segment.segment_id, item))
        if segment.source_id not in source_by_id:
            issues.append(ProvenanceIssue("segment_missing_source", segment.segment_id, segment.source_id))
    for source in sources:
        if not source.has_public_url():
            issues.append(ProvenanceIssue("non_public_source", source.source_id, source.source_url))
    return tuple(issues)


def provenance_edges(rules: Sequence[ContractRule], segments: Sequence[EvidenceSegment]) -> list[dict[str, str]]:
    segment_source = {segment.segment_id: segment.source_id for segment in segments}
    rows: list[dict[str, str]] = []
    for rule in rules:
        rows.append({"from_type": "rule", "from_id": rule.rule_id, "to_type": "segment", "to_id": rule.evidence.segment_id, "edge": "grounded_by"})
        source_id = segment_source.get(rule.evidence.segment_id, rule.evidence.source_id)
        rows.append({"from_type": "segment", "from_id": rule.evidence.segment_id, "to_type": "source", "to_id": source_id, "edge": "extracted_from"})
    return rows


def source_coverage(rules: Sequence[ContractRule]) -> list[dict[str, str]]:
    counts: dict[tuple[str, str], int] = defaultdict(int)
    engines: dict[str, set[str]] = defaultdict(set)
    for rule in rules:
        key = (rule.evidence.source_id, rule.evidence.source_class)
        counts[key] += 1
        engines[rule.evidence.source_id].add(rule.engine)
    rows = []
    for (source_id, source_class), count in sorted(counts.items()):
        rows.append({
            "source_id": source_id,
            "source_class": source_class,
            "rules": str(count),
            "engines": str(len(engines[source_id])),
            "engine_list": ";".join(sorted(engines[source_id])),
        })
    return rows


def evidence_depth_by_engine(rules: Sequence[ContractRule]) -> list[dict[str, str]]:
    by_engine: dict[str, dict[str, set[str] | int]] = defaultdict(lambda: {"rules": 0, "sources": set(), "segments": set(), "operators": set(), "layers": set()})
    for rule in rules:
        bucket = by_engine[rule.engine]
        bucket["rules"] = int(bucket["rules"]) + 1
        bucket["sources"].add(rule.evidence.source_id)  # type: ignore[union-attr]
        bucket["segments"].add(rule.evidence.segment_id)  # type: ignore[union-attr]
        bucket["operators"].add(rule.action.operator)  # type: ignore[union-attr]
        bucket["layers"].add(rule.action.layer)  # type: ignore[union-attr]
    rows = []
    for engine, bucket in sorted(by_engine.items()):
        rows.append({
            "engine": engine,
            "rules": str(bucket["rules"]),
            "sources": str(len(bucket["sources"])),
            "segments": str(len(bucket["segments"])),
            "operators": str(len(bucket["operators"])),
            "layers": str(len(bucket["layers"])),
        })
    return rows

