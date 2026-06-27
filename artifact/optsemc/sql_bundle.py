"""SQL bundle construction for OptSemBench-C probes."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from .sql_render import normalize_sql, query_shape, sql_hash, shape_consistent_with_features


def sql_filename(probe_id: str) -> str:
    return f"{probe_id}.sql"


def probe_comment(probe: Mapping[str, object]) -> str:
    vector = probe.get("feature_vector", {})
    if isinstance(vector, Mapping):
        features = ", ".join(f"{k}={v}" for k, v in sorted(vector.items()))
    else:
        features = ""
    return f"-- OptSemBench-C probe {probe.get('probe_id','')}\n-- features: {features}\n"


def sql_payload(probe: Mapping[str, object]) -> str:
    sql = str(probe.get("sql_skeleton", "")).strip().rstrip(";") + ";"
    return probe_comment(probe) + sql + "\n"


def bundle_manifest_rows(probes: Sequence[Mapping[str, object]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for probe in probes:
        probe_id = str(probe.get("probe_id", ""))
        vector = probe.get("feature_vector", {}) if isinstance(probe.get("feature_vector", {}), Mapping) else {}
        sql = str(probe.get("sql_skeleton", ""))
        shape = query_shape(sql)
        ok, issues = shape_consistent_with_features(sql, vector)  # type: ignore[arg-type]
        rows.append({
            "probe_id": probe_id,
            "sql_file": sql_filename(probe_id),
            "sql_sha256": sql_hash(sql),
            "normalized_token_count": str(shape.token_count),
            "join_count": str(shape.join_count),
            "has_filter": str(shape.has_filter).lower(),
            "has_group": str(shape.has_group).lower(),
            "has_order": str(shape.has_order).lower(),
            "has_limit": str(shape.has_limit).lower(),
            "has_cte": str(shape.has_cte).lower(),
            "shape_valid": str(ok).lower(),
            "shape_issues": "|".join(issues),
        })
    return rows


def export_sql_bundle(probes: Sequence[Mapping[str, object]], out_dir: Path, representative_ids: Iterable[str] = ()) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    rep_dir = out_dir / "representative"
    rep_dir.mkdir(parents=True, exist_ok=True)
    representative = set(representative_ids)
    all_payload_parts: list[str] = []
    for probe in probes:
        payload = sql_payload(probe)
        all_payload_parts.append(payload)
        all_payload_parts.append("\n-- ----------------------------------------------------------------------\n\n")
        pid = str(probe.get("probe_id", ""))
        if pid in representative:
            (rep_dir / sql_filename(pid)).write_text(payload, encoding="utf-8")
    bundle_text = "".join(all_payload_parts)
    bundle_path = out_dir / "full_probe_bundle.sql"
    bundle_path.write_text(bundle_text, encoding="utf-8")
    return {
        "bundle_path": str(bundle_path),
        "bundle_sha256": hashlib.sha256(bundle_text.encode("utf-8")).hexdigest(),
        "representative_files": str(len(list(rep_dir.glob("*.sql")))),
        "bundle_queries": str(len(probes)),
    }
