#!/usr/bin/env python3
"""Check real-engine validation certificates for generated SQL probes."""
from __future__ import annotations

import csv
import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
CHECK = E / "real_engine_validation_check.csv"
ENV = E / "real_engine_validation_environment.csv"
FRESH = E / "real_engine_fresh_run.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def rows_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    passable = [row for row in rows if any(key in row for key in ("passed", "status", "ok"))]
    if not passable:
        return False
    for row in passable:
        if "passed" in row and row["passed"].lower() != "true":
            return False
        if "status" in row and row["status"].upper() != "PASS":
            return False
        if "ok" in row and row["ok"].lower() != "true":
            return False
    return True


def count_lines(path: Path) -> int:
    with path.open(encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def environment_value(key: str) -> str:
    env_path = E / "environment.csv"
    if not env_path.exists():
        return "environment-report-not-built"
    for row in read_csv(env_path):
        if row.get("key") == key:
            return row.get("value", "")
    return "missing"


def available(value: str) -> bool:
    return bool(value) and value != "not-requested" and not value.startswith("unavailable:") and value != "missing"


def unique_motif_probe_count() -> int:
    seen: list[str] = []
    for row in read_csv(E / "workload_representative_probes.csv"):
        probe_id = row["probe_id"]
        if probe_id not in seen:
            seen.append(probe_id)
    return len(seen)


def summary_rows(subset: str) -> list[dict[str, str]]:
    return read_csv(E / f"real_engine_probe_validation_{subset}_summary.csv")


def detail_rows(subset: str) -> list[dict[str, str]]:
    return read_csv(E / f"real_engine_probe_validation_{subset}.csv")


def fresh_marker_rows() -> dict[str, str]:
    if not FRESH.exists():
        return {}
    return {row.get("key", ""): row.get("value", "") for row in read_csv(FRESH)}


def main() -> None:
    expected = {"full": count_lines(ROOT / "benchmark" / "generated_probes.jsonl"), "motif": unique_motif_probe_count()}
    require_fresh = os.environ.get("OPTSEMC_REQUIRE_FRESH_REAL_ENGINE", "0") == "1"
    checks: list[dict[str, str]] = []

    def add(check: str, passed: bool, details: str) -> None:
        checks.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})

    for subset, expected_probes in expected.items():
        summary = summary_rows(subset)
        details = detail_rows(subset)
        engines = {row["engine"] for row in summary}
        add(f"{subset}_has_duckdb_and_postgres", engines == {"duckdb", "postgres"}, f"engines={sorted(engines)}")
        add(f"{subset}_detail_row_count", len(details) == expected_probes * len(engines), f"rows={len(details)};expected={expected_probes * len(engines)}")
        add(f"{subset}_all_detail_success", all(row["plan_ok"] == "true" and row["exec_ok"] == "true" and not row["error"] for row in details), "")
        for row in summary:
            engine = row["engine"]
            probes = int(row["probes"])
            plan_successes = int(row["plan_successes"])
            exec_successes = int(row["execution_successes"])
            failures = int(row["execution_failures"])
            match_rate = float(row["mean_visible_match_rate"])
            distinct_plans = int(row["distinct_plan_hashes"])
            add(f"{subset}_{engine}_all_probes_present", probes == expected_probes, f"probes={probes};expected={expected_probes}")
            add(f"{subset}_{engine}_no_execution_failures", plan_successes == probes and exec_successes == probes and failures == 0, f"plan={plan_successes};exec={exec_successes};fail={failures}")
            add(f"{subset}_{engine}_visible_match_floor", match_rate >= 0.70, f"mean_visible_match_rate={match_rate:.6f}")
            add(f"{subset}_{engine}_plan_diversity_present", distinct_plans > 0, f"distinct_plan_hashes={distinct_plans}")

    evidence_files = [
        ROOT / "benchmark" / "generated_probes.jsonl",
        E / "sql_probe_execution.csv",
        E / "sql_probe_execution_summary.csv",
        E / "sql_probe_execution_check.csv",
        E / "sql_probe_multicatalog_summary.csv",
        E / "sql_probe_multicatalog_totals.csv",
        E / "sql_probe_multicatalog_check.csv",
        E / "real_engine_probe_validation_full.csv",
        E / "real_engine_probe_validation_full_summary.csv",
        E / "real_engine_probe_validation_motif.csv",
        E / "real_engine_probe_validation_motif_summary.csv",
    ]
    marker = fresh_marker_rows()
    evidence_mtime = max(path.stat().st_mtime for path in evidence_files if path.exists())
    fresh_marker_current = (
        FRESH.exists()
        and marker.get("validation_mode") == "fresh-engine-rerun"
        and marker.get("engines") == "duckdb,postgres"
        and FRESH.stat().st_mtime >= evidence_mtime
    )
    validation_mode = "fresh-engine-rerun" if fresh_marker_current else "saved-engine-certificate-replay"
    environment_rows = [
        {"key": "validation_mode", "value": validation_mode},
        {"key": "full_detail_rows", "value": str(len(detail_rows("full")))},
        {"key": "motif_detail_rows", "value": str(len(detail_rows("motif")))},
        {"key": "current_python_duckdb", "value": environment_value("duckdb")},
        {"key": "current_python_psycopg", "value": environment_value("psycopg")},
        {"key": "current_postgres", "value": environment_value("postgres")},
    ]
    environment_rows.extend({"key": f"{path.name}_sha256", "value": sha256_file(path)} for path in evidence_files)
    with ENV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "value"])
        writer.writeheader()
        writer.writerows(environment_rows)
    add("saved_evidence_environment_bound", ENV.exists() and len(environment_rows) >= 11, f"rows={len(environment_rows)}")
    dependency_values = {key: environment_value(key) for key in ("duckdb", "psycopg", "postgres")}
    add("current_dependency_status_recorded", all(dependency_values.values()), str(dependency_values))
    add("fresh_dependency_available_when_required", (not require_fresh) or all(available(value) for value in dependency_values.values()), str(dependency_values))
    if require_fresh:
        add("fresh_run_marker_present", FRESH.exists(), FRESH.relative_to(ROOT).as_posix() if FRESH.exists() else "missing")
        add("fresh_run_marker_matches_scope", marker.get("validation_mode") == "fresh-engine-rerun" and marker.get("engines") == "duckdb,postgres", str(marker))
        add("fresh_marker_after_engine_outputs", fresh_marker_current, f"marker={FRESH.stat().st_mtime if FRESH.exists() else 'missing'};evidence={evidence_mtime}")
    add(
        "current_sql_replay_chain_bound",
        rows_pass(E / "sql_probe_execution_check.csv") and rows_pass(E / "sql_probe_multicatalog_check.csv"),
        "full-sql-plus-three-catalog-replay",
    )
    sql_rows = len(read_csv(E / "sql_probe_execution.csv"))
    multicatalog_totals = {row["metric"]: row["value"] for row in read_csv(E / "sql_probe_multicatalog_totals.csv")}
    add(
        "current_sql_replay_counts_match_corpus",
        sql_rows == 4216
        and multicatalog_totals.get("total_probe_catalog_runs") == "12648"
        and multicatalog_totals.get("total_execution_failures") == "0",
        f"sql_rows={sql_rows};multicatalog={multicatalog_totals}",
    )

    with CHECK.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
        writer.writeheader()
        writer.writerows(checks)
    passed = sum(row["passed"] == "true" for row in checks)
    print(f"Real-engine validation check: {passed}/{len(checks)} passed")
    if passed != len(checks):
        for row in checks:
            if row["passed"] != "true":
                print("FAIL", row["check"], row["details"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
