#!/usr/bin/env python3
"""Check real-engine validation certificates for generated SQL probes."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
CHECK = E / "real_engine_validation_check.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def count_lines(path: Path) -> int:
    with path.open(encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


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


def main() -> None:
    expected = {"full": count_lines(ROOT / "benchmark" / "generated_probes.jsonl"), "motif": unique_motif_probe_count()}
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
