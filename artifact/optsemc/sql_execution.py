"""Executable validation for OptSemBench-C SQL probe skeletons.

The executor intentionally uses a small deterministic SQLite catalog.  It is not
used to measure engine performance; it verifies that every generated probe is a
real executable SQL shape with a parseable logical plan, stable catalog objects,
and non-contradictory feature-to-query rendering.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

ALL_TABLES = ("customer", "orders", "fact", "dim1", "dim2", "a", "b", "c", "d", "aux")
ALL_SCHEMAS = ("main", "remote_pg", "hive")
CATALOG_COLUMNS = (
    "custkey INTEGER",
    "name TEXT",
    "nationkey INTEGER",
    "acctbal REAL",
    "flag INTEGER",
    "region TEXT",
    "comment TEXT",
    "orderkey INTEGER",
    "k INTEGER",
    "k1 INTEGER",
    "k2 INTEGER",
    "attr TEXT",
    "measure REAL",
    "key INTEGER",
)


@dataclass(frozen=True)
class ProbeExecution:
    probe_id: str
    plan_ok: bool
    exec_ok: bool
    row_count: int
    plan_steps: int
    plan_hash: str
    error: str = ""

    def as_row(self) -> dict[str, str]:
        return {
            "probe_id": self.probe_id,
            "plan_ok": str(self.plan_ok).lower(),
            "exec_ok": str(self.exec_ok).lower(),
            "row_count": str(self.row_count),
            "plan_steps": str(self.plan_steps),
            "plan_hash": self.plan_hash,
            "error": self.error,
        }


class SyntheticOptimizerCatalog:
    """A deterministic cross-schema catalog for executing probe SQL.

    Remote and hive schemas are SQLite attachments.  This preserves the
    schema-qualified table references used by source-boundary probes while
    keeping the execution local and reproducible.
    """

    def __init__(self, rows_per_table: int = 5) -> None:
        self.rows_per_table = rows_per_table
        self.connection = sqlite3.connect(":memory:")
        self.connection.create_function("expensive_udf", 1, lambda value: 1)
        self.connection.execute("ATTACH DATABASE ':memory:' AS remote_pg")
        self.connection.execute("ATTACH DATABASE ':memory:' AS hive")
        self._create_catalog()

    def _create_catalog(self) -> None:
        cols = ", ".join(CATALOG_COLUMNS)
        for schema in ALL_SCHEMAS:
            for table in ALL_TABLES:
                self.connection.execute(f"CREATE TABLE {schema}.{table} ({cols})")
                self._populate(schema, table)
        self.connection.commit()

    def _populate(self, schema: str, table: str) -> None:
        sql = (
            f"INSERT INTO {schema}.{table} "
            "(custkey,name,nationkey,acctbal,flag,region,comment,orderkey,k,k1,k2,attr,measure,key) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        )
        for i in range(1, self.rows_per_table + 1):
            row = (
                i,
                f"name{i}",
                i % 5,
                float(10 * i),
                i % 2,
                "EU" if i % 2 else "US",
                f"comment {i}",
                1000 + i,
                i,
                i,
                i,
                f"attr{i}",
                float(i) * 1.5,
                i,
            )
            self.connection.execute(sql, row)

    def execute(self, probe_id: str, sql: str) -> ProbeExecution:
        try:
            plan_rows = self.connection.execute("EXPLAIN QUERY PLAN " + sql).fetchall()
            plan_text = json.dumps(plan_rows, sort_keys=True, default=str)
            plan_hash = hashlib.sha256(plan_text.encode("utf-8")).hexdigest()
            result_rows = self.connection.execute(sql).fetchall()
            return ProbeExecution(probe_id, True, True, len(result_rows), len(plan_rows), plan_hash)
        except Exception as exc:  # pragma: no cover - exercised by checker on failure paths
            return ProbeExecution(probe_id, False, False, 0, 0, "", f"{type(exc).__name__}: {exc}")

    def close(self) -> None:
        self.connection.close()


def execute_probe_suite(probes: Sequence[Mapping[str, object]], rows_per_table: int = 5) -> list[ProbeExecution]:
    catalog = SyntheticOptimizerCatalog(rows_per_table=rows_per_table)
    try:
        return [catalog.execute(str(p.get("probe_id", "")), str(p.get("sql_skeleton", ""))) for p in probes]
    finally:
        catalog.close()


def execution_summary(records: Sequence[ProbeExecution]) -> list[dict[str, str]]:
    total = len(records)
    plan_ok = sum(r.plan_ok for r in records)
    exec_ok = sum(r.exec_ok for r in records)
    total_rows = sum(r.row_count for r in records)
    distinct_plan_hashes = len({r.plan_hash for r in records if r.plan_hash})
    max_plan_steps = max((r.plan_steps for r in records), default=0)
    return [
        {"metric": "executed_sql_probes", "value": str(total)},
        {"metric": "plan_successes", "value": str(plan_ok)},
        {"metric": "execution_successes", "value": str(exec_ok)},
        {"metric": "execution_failures", "value": str(total - exec_ok)},
        {"metric": "total_result_rows", "value": str(total_rows)},
        {"metric": "distinct_plan_hashes", "value": str(distinct_plan_hashes)},
        {"metric": "max_plan_steps", "value": str(max_plan_steps)},
    ]


def select_first_matching_probe(probes: Sequence[Mapping[str, object]], requirements: Mapping[str, str]) -> Mapping[str, object] | None:
    for probe in probes:
        vector = probe.get("feature_vector", {})
        if isinstance(vector, Mapping) and all(str(vector.get(k)) == str(v) for k, v in requirements.items()):
            return probe
    return None
