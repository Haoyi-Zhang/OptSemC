"""Executable data contracts for the OptSem-C repository.

The repository ships many generated CSV, JSONL, and YAML files.  A normal
"file exists" audit is not enough for a reader: a stale or shape-compatible
file can still silently invalidate a claim.  This module provides small,
dependency-light data contracts with line-aware diagnostics, typed column
checks, cross-file cardinality checks, and public-contract-specific validators.
"""
from __future__ import annotations

import csv
import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from .io import read_csv, read_jsonl, read_yaml

Validator = Callable[[str], bool]
JSONObject = Mapping[str, Any]

BOOL_STRINGS = {"true", "false", "yes", "no", "PASS", "FAIL"}
STATE_VALUES = {"MUST", "MAY", "MUST_NOT", "UNSPEC"}
ACTION_FIELDS = ("operator", "kind", "variant", "layer", "placement", "decision_time", "observability")
RULE_ID_RE = re.compile(r"^[A-Z0-9_\-]+$")
PROBE_ID_RE = re.compile(r"^P\d{4}$")
SEGMENT_HASH_RE = re.compile(r"^[0-9a-f]{64}$")
URL_RE = re.compile(r"^https?://")


def nonempty(value: str) -> bool:
    return value is not None and str(value).strip() != ""


def integer(value: str) -> bool:
    try:
        int(str(value))
        return True
    except Exception:
        return False


def nonnegative_integer(value: str) -> bool:
    try:
        return int(str(value)) >= 0
    except Exception:
        return False


def finite_float(value: str) -> bool:
    try:
        return math.isfinite(float(str(value)))
    except Exception:
        return False


def rate(value: str) -> bool:
    try:
        f = float(str(value))
    except Exception:
        return False
    return 0.0 <= f <= 1.0


def boolish(value: str) -> bool:
    return str(value) in BOOL_STRINGS


def enum(values: Iterable[str]) -> Validator:
    allowed = {str(v) for v in values}
    return lambda value: str(value) in allowed


def regex(pattern: re.Pattern[str]) -> Validator:
    return lambda value: bool(pattern.match(str(value)))


@dataclass(frozen=True)
class ValidationIssue:
    contract: str
    path: str
    row: str
    field: str
    severity: str
    message: str

    def as_row(self) -> dict[str, str]:
        return {
            "contract": self.contract,
            "path": self.path,
            "row": self.row,
            "field": self.field,
            "severity": self.severity,
            "message": self.message,
        }


@dataclass(frozen=True)
class ContractResult:
    contract: str
    path: str
    rows: int
    issues: tuple[ValidationIssue, ...]

    @property
    def passed(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)

    def as_row(self) -> dict[str, str]:
        return {
            "contract": self.contract,
            "path": self.path,
            "rows": str(self.rows),
            "errors": str(sum(1 for issue in self.issues if issue.severity == "error")),
            "warnings": str(sum(1 for issue in self.issues if issue.severity == "warning")),
            "passed": str(self.passed).lower(),
        }


@dataclass(frozen=True)
class ColumnSpec:
    name: str
    required: bool = True
    validator: Validator | None = None
    description: str = ""

    def validate(self, contract: str, path: Path, row_no: int, row: Mapping[str, str]) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if self.required and self.name not in row:
            issues.append(ValidationIssue(contract, path.as_posix(), str(row_no), self.name, "error", "missing required column"))
            return issues
        value = row.get(self.name, "")
        if self.required and not nonempty(value):
            issues.append(ValidationIssue(contract, path.as_posix(), str(row_no), self.name, "error", "empty required value"))
            return issues
        if self.validator is not None and nonempty(value) and not self.validator(str(value)):
            issues.append(ValidationIssue(contract, path.as_posix(), str(row_no), self.name, "error", f"value failed validator: {value!r}"))
        return issues


@dataclass(frozen=True)
class CSVContract:
    name: str
    relative_path: str
    columns: tuple[ColumnSpec, ...]
    min_rows: int = 1
    unique_key: tuple[str, ...] = ()

    def validate(self, root: Path) -> ContractResult:
        path = root / self.relative_path
        issues: list[ValidationIssue] = []
        rows: list[dict[str, str]] = []
        if not path.exists():
            return ContractResult(self.name, self.relative_path, 0, (ValidationIssue(self.name, self.relative_path, "0", "path", "error", "file missing"),))
        try:
            rows = read_csv(path)
        except Exception as exc:
            return ContractResult(self.name, self.relative_path, 0, (ValidationIssue(self.name, self.relative_path, "0", "file", "error", f"cannot read CSV: {type(exc).__name__}: {exc}"),))
        if len(rows) < self.min_rows:
            issues.append(ValidationIssue(self.name, self.relative_path, "0", "rows", "error", f"expected at least {self.min_rows} rows, found {len(rows)}"))
        header = set(rows[0].keys()) if rows else set()
        for spec in self.columns:
            if spec.required and spec.name not in header:
                issues.append(ValidationIssue(self.name, self.relative_path, "0", spec.name, "error", "required column absent from header"))
        seen: dict[tuple[str, ...], int] = {}
        for row_no, row in enumerate(rows, 2):
            for spec in self.columns:
                issues.extend(spec.validate(self.name, path.relative_to(root), row_no, row))
            if self.unique_key:
                key = tuple(row.get(k, "") for k in self.unique_key)
                if key in seen:
                    issues.append(ValidationIssue(self.name, self.relative_path, str(row_no), "+".join(self.unique_key), "error", f"duplicate key first seen at CSV row {seen[key]}: {key}"))
                else:
                    seen[key] = row_no
        return ContractResult(self.name, self.relative_path, len(rows), tuple(issues))


@dataclass(frozen=True)
class JSONFieldSpec:
    path: tuple[str, ...]
    required: bool = True
    validator: Callable[[Any], bool] | None = None
    description: str = ""

    @property
    def dotted(self) -> str:
        return ".".join(self.path)

    def extract(self, obj: JSONObject) -> tuple[bool, Any]:
        current: Any = obj
        for part in self.path:
            if not isinstance(current, Mapping) or part not in current:
                return False, None
            current = current[part]
        return True, current

    def validate(self, contract: str, rel: str, row_no: int, obj: JSONObject) -> list[ValidationIssue]:
        present, value = self.extract(obj)
        if self.required and not present:
            return [ValidationIssue(contract, rel, str(row_no), self.dotted, "error", "missing required field")]
        if self.required and present and value in (None, "", [], {}):
            return [ValidationIssue(contract, rel, str(row_no), self.dotted, "error", "empty required field")]
        if present and self.validator is not None and not self.validator(value):
            return [ValidationIssue(contract, rel, str(row_no), self.dotted, "error", f"field failed validator: {value!r}")]
        return []


@dataclass(frozen=True)
class JSONLContract:
    name: str
    relative_path: str
    fields: tuple[JSONFieldSpec, ...]
    min_rows: int = 1
    unique_path: tuple[str, ...] | None = None

    def validate(self, root: Path) -> ContractResult:
        path = root / self.relative_path
        rel = self.relative_path
        issues: list[ValidationIssue] = []
        if not path.exists():
            return ContractResult(self.name, rel, 0, (ValidationIssue(self.name, rel, "0", "path", "error", "file missing"),))
        try:
            rows = list(read_jsonl(path))
        except Exception as exc:
            return ContractResult(self.name, rel, 0, (ValidationIssue(self.name, rel, "0", "file", "error", f"cannot read JSONL: {type(exc).__name__}: {exc}"),))
        if len(rows) < self.min_rows:
            issues.append(ValidationIssue(self.name, rel, "0", "rows", "error", f"expected at least {self.min_rows} rows, found {len(rows)}"))
        seen: dict[str, int] = {}
        key_spec = JSONFieldSpec(self.unique_path) if self.unique_path else None
        for row_no, obj in enumerate(rows, 1):
            for spec in self.fields:
                issues.extend(spec.validate(self.name, rel, row_no, obj))
            if key_spec is not None:
                present, value = key_spec.extract(obj)
                key = str(value) if present else ""
                if key in seen:
                    issues.append(ValidationIssue(self.name, rel, str(row_no), key_spec.dotted, "error", f"duplicate key first seen at JSONL line {seen[key]}: {key}"))
                else:
                    seen[key] = row_no
        return ContractResult(self.name, rel, len(rows), tuple(issues))


def _is_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_state(value: Any) -> bool:
    return isinstance(value, str) and value in STATE_VALUES


def _is_url(value: Any) -> bool:
    return isinstance(value, str) and bool(URL_RE.match(value))


def _is_line_range(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("L") and "-L" in value


def _is_action_object(value: Any) -> bool:
    return isinstance(value, Mapping) and all(_is_str(value.get(field)) for field in ACTION_FIELDS)


def _is_feature_vector(value: Any) -> bool:
    return isinstance(value, Mapping) and len(value) >= 8 and all(_is_str(k) and _is_str(v) for k, v in value.items())


def _is_actions_map(value: Any) -> bool:
    return isinstance(value, Mapping) and all(isinstance(k, str) and isinstance(v, str) and v in STATE_VALUES for k, v in value.items())


def default_contracts() -> tuple[CSVContract | JSONLContract, ...]:
    """Return repository contracts for the grounded mainline and repository hardening outputs."""
    return (
        JSONLContract(
            "grounded_rules",
            "artifact/grounded/verified_rules.jsonl",
            fields=(
                JSONFieldSpec(("rule_id",), validator=lambda v: isinstance(v, str) and bool(RULE_ID_RE.match(v))),
                JSONFieldSpec(("engine",), validator=_is_str),
                JSONFieldSpec(("state",), validator=_is_state),
                JSONFieldSpec(("action",), validator=_is_action_object),
                JSONFieldSpec(("evidence", "source_id"), validator=_is_str),
                JSONFieldSpec(("evidence", "segment_id"), validator=_is_str),
                JSONFieldSpec(("evidence", "line_range"), validator=_is_line_range),
                JSONFieldSpec(("version", "retrieved_at"), validator=_is_str),
            ),
            min_rows=250,
            unique_path=("rule_id",),
        ),
        JSONLContract(
            "grounded_segments",
            "artifact/grounded/verified_segments.jsonl",
            fields=(
                JSONFieldSpec(("segment_id",), validator=_is_str),
                JSONFieldSpec(("source_id",), validator=_is_str),
                JSONFieldSpec(("line_range",), validator=_is_line_range),
                            ),
            min_rows=250,
            unique_path=("segment_id",),
        ),
        CSVContract(
            "grounded_sources",
            "artifact/grounded/verified_sources.csv",
            columns=(
                ColumnSpec("source_id", validator=nonempty),
                ColumnSpec("url", validator=lambda v: bool(URL_RE.match(v))),
                ColumnSpec("source_class", validator=nonempty),
            ),
            min_rows=20,
            unique_key=("source_id",),
        ),
        JSONLContract(
            "generated_probes",
            "artifact/benchmark/generated_probes.jsonl",
            fields=(
                JSONFieldSpec(("probe_id",), validator=lambda v: isinstance(v, str) and bool(PROBE_ID_RE.match(v))),
                JSONFieldSpec(("feature_vector",), validator=_is_feature_vector),
                JSONFieldSpec(("sql_skeleton",), validator=_is_str),
                JSONFieldSpec(("covered_interactions",), required=False, validator=lambda v: isinstance(v, list)),
            ),
            min_rows=4000,
            unique_path=("probe_id",),
        ),
        JSONLContract(
            "contract_maps",
            "artifact/evaluation/grounded_contract_maps.jsonl",
            fields=(
                JSONFieldSpec(("engine",), validator=_is_str),
                JSONFieldSpec(("probe_id",), validator=lambda v: isinstance(v, str) and bool(PROBE_ID_RE.match(v))),
                JSONFieldSpec(("actions",), validator=_is_actions_map),
            ),
            min_rows=1,
        ),
        CSVContract(
            "baseline_portfolio",
            "artifact/evaluation/grounded/baseline_portfolio.csv",
            columns=(
                ColumnSpec("projection", validator=nonempty),
                ColumnSpec("comparisons", validator=nonnegative_integer),
                ColumnSpec("projected_equivalences", validator=nonnegative_integer),
                ColumnSpec("false_equivalences", validator=nonnegative_integer),
            ),
            min_rows=4,
            unique_key=("projection",),
        ),
        CSVContract(
            "projection_mutation_suite",
            "artifact/evaluation/projection_mutation_suite.csv",
            columns=(
                ColumnSpec("projection", validator=nonempty),
                ColumnSpec("comparisons", validator=nonnegative_integer),
                ColumnSpec("projected_equivalences", validator=nonnegative_integer),
                ColumnSpec("false_equivalences", validator=nonnegative_integer),
                ColumnSpec("false_differences", validator=nonnegative_integer),
            ),
            min_rows=40,
            unique_key=("projection",),
        ),
        CSVContract(
            "external_benchmark_suite",
            "artifact/evaluation/external_benchmark_suite.csv",
            columns=(
                ColumnSpec("suite_id", validator=nonempty),
                ColumnSpec("motifs", validator=nonnegative_integer),
                ColumnSpec("covered_motifs", validator=nonnegative_integer),
                ColumnSpec("coverage_rate", validator=rate),
                ColumnSpec("matching_probes", validator=nonnegative_integer),
            ),
            min_rows=8,
            unique_key=("suite_id",),
        ),
        CSVContract(
            "theorem_ledger",
            "artifact/evaluation/theorem_ledger.csv",
            columns=(ColumnSpec("theorem_or_claim", validator=nonempty), ColumnSpec("finite_obligation", validator=nonempty), ColumnSpec("support", validator=nonempty), ColumnSpec("passed", validator=boolish)),
            min_rows=8,
            unique_key=("theorem_or_claim",),
        ),
        CSVContract(
            "repository_audit",
            "artifact/evaluation/repository_audit.csv",
            columns=(ColumnSpec("check", validator=nonempty), ColumnSpec("passed", validator=boolish), ColumnSpec("score", validator=nonnegative_integer), ColumnSpec("weight", validator=nonnegative_integer)),
            min_rows=10,
            unique_key=("check",),
        ),
    )


def validate_contracts(root: Path, contracts: Sequence[CSVContract | JSONLContract] | None = None) -> tuple[ContractResult, ...]:
    suite = tuple(contracts or default_contracts())
    return tuple(contract.validate(root) for contract in suite)


def result_rows(results: Sequence[ContractResult]) -> list[dict[str, str]]:
    return [result.as_row() for result in results]


def issue_rows(results: Sequence[ContractResult]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for result in results:
        rows.extend(issue.as_row() for issue in result.issues)
    if not rows:
        rows.append({"contract": "all", "path": "", "row": "", "field": "", "severity": "info", "message": "no issues"})
    return rows


def cross_file_invariants(root: Path) -> list[dict[str, str]]:
    """Validate cross-file cardinality and referential-integrity invariants."""
    checks: list[dict[str, str]] = []
    try:
        rules = list(read_jsonl(root / "artifact/grounded/verified_rules.jsonl"))
        segments = list(read_jsonl(root / "artifact/grounded/verified_segments.jsonl"))
        sources = read_csv(root / "artifact/grounded/verified_sources.csv")
        probes = list(read_jsonl(root / "artifact/benchmark/generated_probes.jsonl"))
        maps = list(read_jsonl(root / "artifact/evaluation/grounded_contract_maps.jsonl"))
    except Exception as exc:
        return [{"check": "cross_file_readability", "passed": "false", "details": f"{type(exc).__name__}: {exc}"}]
    rule_segment_ids = {row.get("evidence", {}).get("segment_id") for row in rules}
    segment_ids = {row.get("segment_id") for row in segments}
    rule_source_ids = {row.get("evidence", {}).get("source_id") for row in rules}
    source_ids = {row.get("source_id") for row in sources}
    probe_ids = {row.get("probe_id") for row in probes}
    map_probe_ids = {row.get("probe_id") for row in maps}
    actions_nonempty = sum(1 for row in maps if row.get("actions"))
    checks.append({"check": "rule_segments_resolve", "passed": str(rule_segment_ids <= segment_ids).lower(), "details": f"rule_segments={len(rule_segment_ids)};segments={len(segment_ids)}"})
    checks.append({"check": "rule_sources_resolve", "passed": str(rule_source_ids <= source_ids).lower(), "details": f"rule_sources={len(rule_source_ids)};sources={len(source_ids)}"})
    checks.append({"check": "contract_map_probes_resolve", "passed": str(map_probe_ids <= probe_ids).lower(), "details": f"map_probes={len(map_probe_ids)};probes={len(probe_ids)}"})
    checks.append({"check": "grounded_rule_count", "passed": str(len(rules) == 287).lower(), "details": f"rules={len(rules)}"})
    hash_ok = all((row.get("segment_hash") or row.get("segment_sha256")) for row in segments)
    checks.append({"check": "evidence_span_count", "passed": str(len(segments) == 287).lower(), "details": f"segments={len(segments)}"})
    checks.append({"check": "evidence_segments_hashed", "passed": str(hash_ok).lower(), "details": f"segments={len(segments)}"})
    checks.append({"check": "probe_count", "passed": str(len(probes) == 4216).lower(), "details": f"probes={len(probes)}"})
    checks.append({"check": "nonempty_contract_maps", "passed": str(actions_nonempty > 0).lower(), "details": f"nonempty_maps={actions_nonempty};maps={len(maps)}"})
    return checks
