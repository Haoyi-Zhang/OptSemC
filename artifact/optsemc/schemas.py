"""Lightweight schema validators for packaged OptSem-C files."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class SchemaIssue:
    object_type: str
    object_id: str
    field: str
    detail: str

    def as_row(self) -> dict[str, str]:
        return {"object_type": self.object_type, "object_id": self.object_id, "field": self.field, "detail": self.detail}


def require_fields(object_type: str, object_id: str, record: Mapping[str, Any], fields: Sequence[str]) -> list[SchemaIssue]:
    issues = []
    for field in fields:
        value = record.get(field)
        if field not in record or value is None or value == "":
            issues.append(SchemaIssue(object_type, object_id, field, "missing required field"))
    return issues


def require_nested(object_type: str, object_id: str, record: Mapping[str, Any], parent: str, fields: Sequence[str]) -> list[SchemaIssue]:
    value = record.get(parent)
    if not isinstance(value, Mapping):
        return [SchemaIssue(object_type, object_id, parent, "missing nested mapping")]
    return require_fields(object_type, object_id, value, fields)


def validate_rule_record(record: Mapping[str, Any]) -> list[SchemaIssue]:
    rid = str(record.get("rule_id", ""))
    issues = require_fields("rule", rid, record, ("rule_id", "engine", "state", "action", "guard", "evidence", "version"))
    issues.extend(require_nested("rule", rid, record, "action", ("operator", "kind", "variant", "layer", "placement", "decision_time", "observability")))
    issues.extend(require_nested("rule", rid, record, "evidence", ("source_id", "segment_id", "line_range", "source_class")))
    issues.extend(require_nested("rule", rid, record, "version", ("type", "retrieved_at")))
    return issues


def validate_probe_record(record: Mapping[str, Any]) -> list[SchemaIssue]:
    pid = str(record.get("probe_id", ""))
    issues = require_fields("probe", pid, record, ("probe_id", "feature_vector", "sql_skeleton", "covered_interactions"))
    fv = record.get("feature_vector")
    if not isinstance(fv, Mapping) or len(fv) < 8:
        issues.append(SchemaIssue("probe", pid, "feature_vector", "expected feature mapping with optimizer fields"))
    return issues


def validate_contract_map_record(record: Mapping[str, Any]) -> list[SchemaIssue]:
    cid = f"{record.get('engine','')}::{record.get('probe_id','')}"
    issues = require_fields("contract_map", cid, record, ("engine", "probe_id", "actions"))
    if not isinstance(record.get("actions"), Mapping):
        issues.append(SchemaIssue("contract_map", cid, "actions", "expected action-state mapping"))
    return issues

