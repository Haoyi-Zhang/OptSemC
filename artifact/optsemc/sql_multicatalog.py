"""Multi-catalog execution validation for generated SQL probes.

The base executor validates parseability, planability, and execution on one
small deterministic catalog.  Multi-catalog validation repeats the same probe
set over several deterministic catalog densities.  This is still not a latency
benchmark; it is a robustness check that generated SQL does not accidentally
rely on a single population size or empty-result artifact.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .sql_execution import ProbeExecution, execute_probe_suite


@dataclass(frozen=True)
class CatalogExecutionSummary:
    rows_per_table: int
    probes: int
    plan_successes: int
    execution_successes: int
    execution_failures: int
    total_result_rows: int
    distinct_plan_hashes: int
    max_plan_steps: int

    def as_row(self) -> dict[str, str]:
        return {
            "rows_per_table": str(self.rows_per_table),
            "probes": str(self.probes),
            "plan_successes": str(self.plan_successes),
            "execution_successes": str(self.execution_successes),
            "execution_failures": str(self.execution_failures),
            "total_result_rows": str(self.total_result_rows),
            "distinct_plan_hashes": str(self.distinct_plan_hashes),
            "max_plan_steps": str(self.max_plan_steps),
        }


def summarize_catalog(rows_per_table: int, records: Sequence[ProbeExecution]) -> CatalogExecutionSummary:
    return CatalogExecutionSummary(
        rows_per_table=rows_per_table,
        probes=len(records),
        plan_successes=sum(r.plan_ok for r in records),
        execution_successes=sum(r.exec_ok for r in records),
        execution_failures=sum(not r.exec_ok for r in records),
        total_result_rows=sum(r.row_count for r in records),
        distinct_plan_hashes=len({r.plan_hash for r in records if r.plan_hash}),
        max_plan_steps=max((r.plan_steps for r in records), default=0),
    )


def execute_probe_suite_multicatalog(
    probes: Sequence[Mapping[str, object]],
    catalog_sizes: Sequence[int] = (1, 5, 17),
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    detail_rows: list[dict[str, str]] = []
    summary_rows: list[dict[str, str]] = []
    for rows_per_table in catalog_sizes:
        records = execute_probe_suite(probes, rows_per_table=rows_per_table)
        summary_rows.append(summarize_catalog(rows_per_table, records).as_row())
        for rec in records:
            row = rec.as_row()
            row["rows_per_table"] = str(rows_per_table)
            detail_rows.append(row)
    return detail_rows, summary_rows


def multicatalog_totals(summary_rows: Sequence[Mapping[str, str]]) -> dict[str, str]:
    catalogs = len(summary_rows)
    probes_per_catalog = int(summary_rows[0]["probes"]) if summary_rows else 0
    total_probe_runs = sum(int(r["probes"]) for r in summary_rows)
    total_successes = sum(int(r["execution_successes"]) for r in summary_rows)
    total_failures = sum(int(r["execution_failures"]) for r in summary_rows)
    total_rows = sum(int(r["total_result_rows"]) for r in summary_rows)
    return {
        "catalogs": str(catalogs),
        "probes_per_catalog": str(probes_per_catalog),
        "total_probe_catalog_runs": str(total_probe_runs),
        "total_execution_successes": str(total_successes),
        "total_execution_failures": str(total_failures),
        "total_result_rows": str(total_rows),
    }
