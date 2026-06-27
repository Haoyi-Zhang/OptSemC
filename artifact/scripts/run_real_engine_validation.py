#!/usr/bin/env python3
"""Validate generated OptSemBench-C probes on real SQL engines.

The deterministic SQLite catalog checks that generated SQL is executable.  This
script is a separate evidence path: it runs selected probes on real engines,
captures EXPLAIN output, executes the query, and records whether visible plan
surfaces match the probe feature vector.  It is intended for cloud execution.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from optsemc.corpus import load_probes
from optsemc.io import write_csv

ALL_TABLES = ("customer", "orders", "fact", "dim1", "dim2", "a", "b", "c", "d", "aux")
ALL_SCHEMAS = ("main", "remote_pg", "hive")
CATALOG_COLUMNS = (
    ("custkey", "INTEGER"),
    ("name", "TEXT"),
    ("nationkey", "INTEGER"),
    ("acctbal", "DOUBLE PRECISION"),
    ("flag", "INTEGER"),
    ("region", "TEXT"),
    ("comment", "TEXT"),
    ("orderkey", "INTEGER"),
    ("k", "INTEGER"),
    ("k1", "INTEGER"),
    ("k2", "INTEGER"),
    ("attr", "TEXT"),
    ("measure", "DOUBLE PRECISION"),
    ("key", "INTEGER"),
)
VISIBLE_TAGS = ("aggregate", "cte", "filter", "join", "sort_or_limit")


@dataclass(frozen=True)
class ValidationRow:
    engine: str
    subset: str
    probe_id: str
    plan_ok: bool
    exec_ok: bool
    result_rows: int
    plan_hash: str
    visible_expected_tags: str
    visible_observed_tags: str
    visible_matched_tags: str
    visible_match_rate: str
    error: str

    def as_row(self) -> dict[str, str]:
        return {
            "engine": self.engine,
            "subset": self.subset,
            "probe_id": self.probe_id,
            "plan_ok": str(self.plan_ok).lower(),
            "exec_ok": str(self.exec_ok).lower(),
            "result_rows": str(self.result_rows),
            "plan_hash": self.plan_hash,
            "visible_expected_tags": self.visible_expected_tags,
            "visible_observed_tags": self.visible_observed_tags,
            "visible_matched_tags": self.visible_matched_tags,
            "visible_match_rate": self.visible_match_rate,
            "error": self.error,
        }


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_probe_subset(subset: str, limit: int | None = None) -> tuple[Mapping[str, Any], ...]:
    probes = tuple(load_probes(ROOT))
    by_id = {str(p["probe_id"]): p for p in probes}
    if subset == "full":
        selected = list(probes)
    elif subset == "motif":
        ids = []
        for row in read_csv_rows(ROOT / "evaluation" / "workload_representative_probes.csv"):
            probe_id = row["probe_id"]
            if probe_id not in ids:
                ids.append(probe_id)
        selected = [by_id[probe_id] for probe_id in ids if probe_id in by_id]
    elif subset == "cover":
        ids = [row["probe_id"] for row in read_csv_rows(ROOT / "evaluation" / "benchmark_minimal_probe_cover.csv")]
        selected = [by_id[probe_id] for probe_id in ids if probe_id in by_id]
    else:
        raise ValueError(f"unknown subset: {subset}")
    if limit is not None:
        selected = selected[:limit]
    return tuple(selected)


def strip_sql(sql: str) -> str:
    return sql.strip().rstrip(";").strip()


def sql_for_engine(sql: str, engine: str) -> str:
    cleaned = strip_sql(sql)
    if engine == "duckdb":
        return cleaned
    if engine == "postgres":
        return cleaned
    return cleaned


def plan_hash(plan_text: str) -> str:
    return hashlib.sha256(plan_text.encode("utf-8")).hexdigest()


def expected_visible_tags(vector: Mapping[str, Any]) -> set[str]:
    tags: set[str] = set()
    aggregation = str(vector.get("aggregation", "none"))
    predicate = str(vector.get("predicate_class", "none"))
    join_type = str(vector.get("join_type", "none"))
    order_limit = str(vector.get("order_limit", "none"))
    reuse = str(vector.get("reuse_structure", "none"))
    if aggregation not in {"none", "not_applicable"}:
        tags.add("aggregate")
    if predicate not in {"none", "not_applicable"}:
        tags.add("filter")
    if join_type not in {"none", "not_applicable"}:
        tags.add("join")
    if order_limit not in {"none", "not_applicable"}:
        tags.add("sort_or_limit")
    if reuse not in {"none", "not_applicable"}:
        tags.add("cte")
    return tags


def observed_visible_tags(plan_text: str) -> set[str]:
    text = plan_text.lower()
    tags: set[str] = set()
    if re.search(r"\b(join|nested loop|hash join|merge join)\b", text):
        tags.add("join")
    if re.search(r"\b(aggregate|hashagg|group by|group_aggregate|distinct)\b", text):
        tags.add("aggregate")
    if re.search(r"\b(filter|where|selection)\b", text):
        tags.add("filter")
    if re.search(r"\b(sort|limit|topn|top-n|order_by|order by)\b", text):
        tags.add("sort_or_limit")
    if re.search(r"\b(cte|materialize|materialized)\b", text):
        tags.add("cte")
    return tags


def tag_columns(vector: Mapping[str, Any], plan_text_value: str) -> tuple[str, str, str, str]:
    expected = expected_visible_tags(vector)
    observed = observed_visible_tags(plan_text_value)
    matched = expected & observed
    rate = len(matched) / len(expected) if expected else 1.0
    return (
        ";".join(sorted(expected)),
        ";".join(sorted(observed)),
        ";".join(sorted(matched)),
        f"{rate:.6f}",
    )


def row_error(engine: str, subset: str, probe: Mapping[str, Any], exc: Exception) -> ValidationRow:
    expected = ";".join(sorted(expected_visible_tags(probe.get("feature_vector", {}))))
    return ValidationRow(
        engine=engine,
        subset=subset,
        probe_id=str(probe.get("probe_id", "")),
        plan_ok=False,
        exec_ok=False,
        result_rows=0,
        plan_hash="",
        visible_expected_tags=expected,
        visible_observed_tags="",
        visible_matched_tags="",
        visible_match_rate="0.000000" if expected else "1.000000",
        error=f"{type(exc).__name__}: {exc}",
    )


class DuckDBRunner:
    engine = "duckdb"

    def __init__(self, rows_per_table: int) -> None:
        import duckdb  # type: ignore

        self.connection = duckdb.connect(database=":memory:")
        self.rows_per_table = rows_per_table
        self._create_catalog()

    def _create_catalog(self) -> None:
        for schema in ALL_SCHEMAS:
            if schema != "main":
                self.connection.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
            for table in ALL_TABLES:
                prefix = "" if schema == "main" else f"{schema}."
                columns = ", ".join(f"{name} {dtype.replace('DOUBLE PRECISION', 'DOUBLE')}" for name, dtype in CATALOG_COLUMNS)
                self.connection.execute(f"CREATE TABLE {prefix}{table} ({columns})")
                placeholders = ", ".join(["?"] * len(CATALOG_COLUMNS))
                sql = f"INSERT INTO {prefix}{table} VALUES ({placeholders})"
                for row in catalog_rows(self.rows_per_table):
                    self.connection.execute(sql, row)

    def validate(self, subset: str, probe: Mapping[str, Any]) -> ValidationRow:
        sql = sql_for_engine(str(probe.get("sql_skeleton", "")), self.engine)
        plan_rows = self.connection.execute("EXPLAIN " + sql).fetchall()
        plan_text_value = "\n".join(" ".join(map(str, row)) for row in plan_rows)
        result_rows = self.connection.execute(f"SELECT COUNT(*) FROM ({sql}) AS optsemc_probe").fetchone()[0]
        expected, observed, matched, rate = tag_columns(probe.get("feature_vector", {}), plan_text_value)
        return ValidationRow(self.engine, subset, str(probe["probe_id"]), True, True, int(result_rows), plan_hash(plan_text_value), expected, observed, matched, rate, "")

    def close(self) -> None:
        self.connection.close()


class PostgresRunner:
    engine = "postgres"

    def __init__(self, rows_per_table: int, dsn: str | None = None) -> None:
        try:
            import psycopg  # type: ignore
        except ImportError as exc:  # pragma: no cover - cloud dependency gate
            raise RuntimeError("Install psycopg[binary] or psycopg-binary to run PostgreSQL validation") from exc

        self.psycopg = psycopg
        self.connection = psycopg.connect(dsn or os.environ.get("OPTSEMC_POSTGRES_DSN", "dbname=optsemc user=optsemc host=127.0.0.1 port=5432"))
        self.connection.autocommit = True
        self.rows_per_table = rows_per_table
        self._create_catalog()

    def _create_catalog(self) -> None:
        with self.connection.cursor() as cur:
            for schema in ALL_SCHEMAS:
                if schema != "main":
                    cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
            for schema in ALL_SCHEMAS:
                for table in ALL_TABLES:
                    qualified = table if schema == "main" else f"{schema}.{table}"
                    cur.execute(f"DROP TABLE IF EXISTS {qualified}")
                    columns = ", ".join(f"{name} {dtype}" for name, dtype in CATALOG_COLUMNS)
                    cur.execute(f"CREATE TABLE {qualified} ({columns})")
                    placeholders = ", ".join(["%s"] * len(CATALOG_COLUMNS))
                    cur.executemany(f"INSERT INTO {qualified} VALUES ({placeholders})", catalog_rows(self.rows_per_table))
            cur.execute("ANALYZE")

    def validate(self, subset: str, probe: Mapping[str, Any]) -> ValidationRow:
        sql = sql_for_engine(str(probe.get("sql_skeleton", "")), self.engine)
        with self.connection.cursor() as cur:
            cur.execute("EXPLAIN (FORMAT TEXT) " + sql)
            plan_text_value = "\n".join(row[0] for row in cur.fetchall())
            cur.execute(f"SELECT COUNT(*) FROM ({sql}) AS optsemc_probe")
            result_rows = cur.fetchone()[0]
        expected, observed, matched, rate = tag_columns(probe.get("feature_vector", {}), plan_text_value)
        return ValidationRow(self.engine, subset, str(probe["probe_id"]), True, True, int(result_rows), plan_hash(plan_text_value), expected, observed, matched, rate, "")

    def close(self) -> None:
        self.connection.close()


def catalog_rows(rows_per_table: int) -> list[tuple[Any, ...]]:
    rows = []
    for i in range(1, rows_per_table + 1):
        rows.append((
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
        ))
    return rows


def make_runner(engine: str, rows_per_table: int, postgres_dsn: str | None):
    if engine == "duckdb":
        return DuckDBRunner(rows_per_table)
    if engine == "postgres":
        return PostgresRunner(rows_per_table, postgres_dsn)
    raise ValueError(f"unsupported engine: {engine}")


def summarize(rows: Sequence[ValidationRow]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[ValidationRow]] = {}
    for row in rows:
        grouped.setdefault((row.engine, row.subset), []).append(row)
    out = []
    for (engine, subset), group in sorted(grouped.items()):
        visible_expected = sum(1 for row in group if row.visible_expected_tags)
        avg_match = sum(float(row.visible_match_rate) for row in group) / len(group) if group else 0.0
        out.append({
            "engine": engine,
            "subset": subset,
            "probes": str(len(group)),
            "plan_successes": str(sum(row.plan_ok for row in group)),
            "execution_successes": str(sum(row.exec_ok for row in group)),
            "execution_failures": str(sum(not row.exec_ok for row in group)),
            "visible_expected_probe_rows": str(visible_expected),
            "mean_visible_match_rate": f"{avg_match:.6f}",
            "distinct_plan_hashes": str(len({row.plan_hash for row in group if row.plan_hash})),
        })
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engines", default="duckdb,postgres", help="comma-separated engines: duckdb,postgres")
    parser.add_argument("--subset", choices=["full", "motif", "cover"], default="motif")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--rows-per-table", type=int, default=17)
    parser.add_argument("--postgres-dsn", default=None)
    parser.add_argument("--out", default="evaluation/real_engine_probe_validation.csv")
    parser.add_argument("--summary-out", default="evaluation/real_engine_probe_validation_summary.csv")
    args = parser.parse_args()

    probes = load_probe_subset(args.subset, args.limit)
    all_rows: list[ValidationRow] = []
    for engine in [item.strip() for item in args.engines.split(",") if item.strip()]:
        runner = make_runner(engine, args.rows_per_table, args.postgres_dsn)
        try:
            for probe in probes:
                try:
                    all_rows.append(runner.validate(args.subset, probe))
                except Exception as exc:  # pragma: no cover - exercised on cloud dialect failures
                    all_rows.append(row_error(engine, args.subset, probe, exc))
        finally:
            runner.close()

    out = ROOT / args.out
    summary_out = ROOT / args.summary_out
    write_csv(out, [row.as_row() for row in all_rows], list(ValidationRow.__dataclass_fields__))
    write_csv(summary_out, summarize(all_rows))
    failures = sum(not row.exec_ok for row in all_rows)
    print(f"Real-engine validation: rows={len(all_rows)} failures={failures}; summary={summary_out}")


if __name__ == "__main__":
    main()
