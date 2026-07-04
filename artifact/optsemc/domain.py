"""Typed domain objects for the OptSem-C repository.

The repository stores most packaged data as CSV, JSONL, and YAML so that the
artifact is easy to inspect without a database server.  This module gives those
records a typed interface for checkers, certificates, and command-line tools.
The goal is deliberately modest: provide deterministic, auditable parsing for
public optimizer-contract evidence rather than a mutable ORM or hidden database.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

LINE_RANGE_RE = re.compile(r"^L(?P<start>[0-9]+)-L(?P<end>[0-9]+)$")
VALID_STATES = frozenset({"MUST", "MAY", "MUST_NOT", "UNSPEC"})
VALID_CONFIDENCE = frozenset({"high", "medium", "low"})
PUBLIC_SCHEMES = ("https://", "http://")


def canonical_json(value: Any) -> str:
    """Return a deterministic JSON representation used in hashes and reports."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_blank(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


@dataclass(frozen=True, order=True)
class LineRange:
    """Closed line range in a public evidence source."""

    start: int
    end: int

    @classmethod
    def parse(cls, text: str) -> "LineRange":
        match = LINE_RANGE_RE.match(text.strip())
        if not match:
            raise ValueError(f"invalid line range {text!r}; expected L<start>-L<end>")
        start = int(match.group("start"))
        end = int(match.group("end"))
        if start <= 0 or end < start:
            raise ValueError(f"invalid line range bounds: {text!r}")
        return cls(start, end)

    def overlaps(self, other: "LineRange") -> bool:
        return not (self.end < other.start or other.end < self.start)

    def contains(self, line: int) -> bool:
        return self.start <= line <= self.end

    @property
    def width(self) -> int:
        return self.end - self.start + 1

    def as_text(self) -> str:
        return f"L{self.start}-L{self.end}"


@dataclass(frozen=True)
class ActionRecord:
    """Optimizer action fields admitted into public contract rules."""

    operator: str
    kind: str
    variant: str
    layer: str
    placement: str
    decision_time: str
    observability: str

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "ActionRecord":
        missing = [name for name in cls.field_names() if not normalize_blank(mapping.get(name))]
        if missing:
            raise ValueError(f"action is missing required fields: {missing}")
        return cls(*(normalize_blank(mapping.get(name)) for name in cls.field_names()))

    @staticmethod
    def field_names() -> tuple[str, ...]:
        return ("operator", "kind", "variant", "layer", "placement", "decision_time", "observability")

    def key(self) -> str:
        return "|".join(getattr(self, name) for name in self.field_names())

    def as_dict(self) -> dict[str, str]:
        return {name: getattr(self, name) for name in self.field_names()}


@dataclass(frozen=True)
class EvidenceRef:
    """Reference from a rule to an admitted public evidence segment."""

    source_id: str
    segment_id: str
    line_range: LineRange
    source_class: str

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "EvidenceRef":
        return cls(
            source_id=normalize_blank(mapping.get("source_id")),
            segment_id=normalize_blank(mapping.get("segment_id")),
            line_range=LineRange.parse(normalize_blank(mapping.get("line_range"))),
            source_class=normalize_blank(mapping.get("source_class")),
        )

    def as_dict(self) -> dict[str, str]:
        return {
            "source_id": self.source_id,
            "segment_id": self.segment_id,
            "line_range": self.line_range.as_text(),
            "source_class": self.source_class,
        }


@dataclass(frozen=True)
class ContractRule:
    """A grounded public optimizer-contract rule."""

    rule_id: str
    engine: str
    state: str
    action: ActionRecord
    guard: Mapping[str, str]
    evidence: EvidenceRef
    confidence: str = "high"
    version_type: str = "web_verified_snapshot"
    retrieved_at: str = ""
    notes: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_json(cls, record: Mapping[str, Any]) -> "ContractRule":
        version = record.get("version") or {}
        state = normalize_blank(record.get("state"))
        if state not in VALID_STATES:
            raise ValueError(f"invalid rule state {state!r} in {record.get('rule_id')}")
        confidence = normalize_blank(record.get("confidence") or "high")
        if confidence and confidence not in VALID_CONFIDENCE:
            raise ValueError(f"invalid confidence {confidence!r} in {record.get('rule_id')}")
        guard_map = {str(k): normalize_blank(v) for k, v in dict(record.get("guard") or {}).items()}
        return cls(
            rule_id=normalize_blank(record.get("rule_id")),
            engine=normalize_blank(record.get("engine")),
            state=state,
            action=ActionRecord.from_mapping(record.get("action") or {}),
            guard=guard_map,
            evidence=EvidenceRef.from_mapping(record.get("evidence") or {}),
            confidence=confidence or "high",
            version_type=normalize_blank(version.get("type")),
            retrieved_at=normalize_blank(version.get("retrieved_at")),
            notes=tuple(str(x) for x in record.get("notes") or ()),
        )

    @property
    def action_key(self) -> str:
        return self.action.key()

    @property
    def guard_key(self) -> str:
        return canonical_json(dict(sorted(self.guard.items())))

    @property
    def stable_id_payload(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "engine": self.engine,
            "state": self.state,
            "action": self.action.as_dict(),
            "guard": dict(sorted(self.guard.items())),
            "evidence": self.evidence.as_dict(),
        }

    @property
    def payload_hash(self) -> str:
        return sha256_text(canonical_json(self.stable_id_payload))

    def validates(self) -> tuple[bool, tuple[str, ...]]:
        issues: list[str] = []
        if not self.rule_id:
            issues.append("missing rule_id")
        if not self.engine:
            issues.append("missing engine")
        if self.state not in VALID_STATES:
            issues.append(f"bad state {self.state}")
        if self.evidence.line_range.width <= 0:
            issues.append("empty evidence line range")
        for field_name, value in self.action.as_dict().items():
            if not value:
                issues.append(f"blank action.{field_name}")
        return not issues, tuple(issues)


@dataclass(frozen=True)
class EvidenceSegment:
    """Text segment that grounds one or more public contract rules."""

    segment_id: str
    source_id: str
    source_url: str
    public_locator: str
    line_range: LineRange
    segment_text: str
    segment_sha256: str
    source_title: str = ""
    source_class: str = ""
    retrieved_at: str = ""

    @classmethod
    def from_json(cls, record: Mapping[str, Any]) -> "EvidenceSegment":
        return cls(
            segment_id=normalize_blank(record.get("segment_id")),
            source_id=normalize_blank(record.get("source_id")),
            source_url=normalize_blank(record.get("source_url")),
            public_locator=normalize_blank(record.get("public_locator")),
            line_range=LineRange.parse(normalize_blank(record.get("line_range"))),
            segment_text=normalize_blank(record.get("segment_text") or record.get("claim_paraphrase")),
            segment_sha256=normalize_blank(record.get("segment_sha256") or record.get("segment_hash")),
            source_title=normalize_blank(record.get("source_title")),
            source_class=normalize_blank(record.get("source_class")),
            retrieved_at=normalize_blank(record.get("retrieved_at") or record.get("source_retrieved_at")),
        )

    @property
    def computed_sha256(self) -> str:
        return sha256_text(self.segment_text)

    def has_public_url(self) -> bool:
        return self.source_url.startswith(PUBLIC_SCHEMES) and self.public_locator.startswith(PUBLIC_SCHEMES)

    def validates(self) -> tuple[bool, tuple[str, ...]]:
        issues: list[str] = []
        if not self.segment_id:
            issues.append("missing segment_id")
        if not self.source_id:
            issues.append("missing source_id")
        if not self.has_public_url():
            issues.append("non-public source_url or public_locator")
        # Older grounded packages store a stable segment hash over public locator
        # metadata rather than over raw segment text.  The deep audit therefore
        # requires a well-formed stored hash and defers exact convention checks to
        # the public-provenance gate that created the package snapshot.
        if not re.match(r"^[0-9a-f]{64}$", self.segment_sha256):
            issues.append("missing or malformed segment hash")
        if self.line_range.width <= 0:
            issues.append("invalid line range")
        return not issues, tuple(issues)


@dataclass(frozen=True)
class SourceRecord:
    """Public source manifest record."""

    source_id: str
    source_title: str
    source_url: str
    retrieved_at: str
    source_class: str = ""
    source_sha256: str = ""

    @classmethod
    def from_mapping(cls, record: Mapping[str, Any]) -> "SourceRecord":
        return cls(
            source_id=normalize_blank(record.get("source_id")),
            source_title=normalize_blank(record.get("source_title") or record.get("title")),
            source_url=normalize_blank(record.get("source_url") or record.get("url")),
            retrieved_at=normalize_blank(record.get("retrieved_at")),
            source_class=normalize_blank(record.get("source_class")),
            source_sha256=normalize_blank(record.get("source_sha256") or record.get("sha256")),
        )

    def has_public_url(self) -> bool:
        return self.source_url.startswith(PUBLIC_SCHEMES)


@dataclass(frozen=True)
class Probe:
    """Generated query probe over the OptSemBench-C feature domain."""

    probe_id: str
    feature_vector: Mapping[str, str]
    sql_skeleton: str
    covered_interactions: tuple[str, ...] = field(default_factory=tuple)
    forced_by_rule_guard: bool = False

    @classmethod
    def from_json(cls, record: Mapping[str, Any]) -> "Probe":
        return cls(
            probe_id=normalize_blank(record.get("probe_id")),
            feature_vector={str(k): normalize_blank(v) for k, v in dict(record.get("feature_vector") or {}).items()},
            sql_skeleton=normalize_blank(record.get("sql_skeleton")),
            covered_interactions=tuple(str(x) for x in record.get("covered_interactions") or ()),
            forced_by_rule_guard=bool(record.get("forced_by_rule_guard", False)),
        )

    def feature_key(self, fields: Sequence[str] | None = None) -> tuple[tuple[str, str], ...]:
        keys = list(fields) if fields is not None else sorted(self.feature_vector)
        return tuple((k, self.feature_vector.get(k, "")) for k in keys)

    def validates(self, feature_domain: Mapping[str, Sequence[str]] | None = None) -> tuple[bool, tuple[str, ...]]:
        issues: list[str] = []
        if not self.probe_id:
            issues.append("missing probe_id")
        if not self.feature_vector:
            issues.append("missing feature_vector")
        if not self.sql_skeleton:
            issues.append("missing sql_skeleton")
        if feature_domain:
            for name, values in feature_domain.items():
                if name not in self.feature_vector:
                    issues.append(f"missing feature {name}")
                elif self.feature_vector[name] not in set(map(str, values)):
                    issues.append(f"out-of-domain feature {name}={self.feature_vector[name]}")
        return not issues, tuple(issues)


@dataclass(frozen=True)
class ContractMapRecord:
    """Engine/probe contract-map row before conversion to full signatures."""

    engine: str
    probe_id: str
    actions: Mapping[str, str]

    @classmethod
    def from_json(cls, record: Mapping[str, Any]) -> "ContractMapRecord":
        return cls(
            engine=normalize_blank(record.get("engine")),
            probe_id=normalize_blank(record.get("probe_id")),
            actions={str(k): normalize_blank(v) for k, v in dict(record.get("actions") or {}).items()},
        )

    @property
    def key(self) -> tuple[str, str]:
        return (self.engine, self.probe_id)

    def validates(self) -> tuple[bool, tuple[str, ...]]:
        issues: list[str] = []
        if not self.engine:
            issues.append("missing engine")
        if not self.probe_id:
            issues.append("missing probe_id")
        for action_key, state in self.actions.items():
            if state not in VALID_STATES:
                issues.append(f"invalid state {state!r} for {action_key}")
            if len(action_key.split("|")) not in {6, 7}:
                issues.append(f"invalid action key arity for {action_key}")
        return not issues, tuple(issues)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL at {path}:{line_no}: {exc}") from exc
    return records


def typed_records(path: Path, factory: Any) -> list[Any]:
    return [factory.from_json(record) for record in load_jsonl(path)]


def duplicate_keys(values: Iterable[Any]) -> tuple[Any, ...]:
    seen: set[Any] = set()
    dup: list[Any] = []
    for value in values:
        if value in seen and value not in dup:
            dup.append(value)
        seen.add(value)
    return tuple(dup)
