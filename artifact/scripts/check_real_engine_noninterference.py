#!/usr/bin/env python3
"""Verify real-engine validation is a support check, not an input to C3/C8 computations."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT.parent
E = ROOT / "evaluation"
OUT = E / "real_engine_noninterference_check.csv"

REAL_TOKENS = ("real_engine", "duckdb", "postgres", "psycopg")
CORE_COMPUTE_FILES = [
    "scripts/compute_grounded_conditional_traps.py",
    "scripts/compute_baseline_portfolio.py",
    "scripts/compute_grounded_repair_certificates.py",
    "scripts/compute_repair_basis_stability.py",
    "scripts/compute_projection_resolution_lattice.py",
    "scripts/compute_projection_frontier_antichains.py",
    "scripts/compute_semantic_frontier.py",
    "scripts/compute_repair_hitting_sets.py",
    "optsemc/projections.py",
    "optsemc/repair.py",
    "optsemc/repair_stability.py",
    "optsemc/lattice.py",
]
CORE_TABLES = {
    "core_results",
    "false_equivalence_robustness",
    "projection_resolution_lattice",
    "semantic_frontier",
    "anti_overfit_audit",
    "resource_profile",
    "scalability_family",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains_real_engine_reference(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    return any(token in text for token in REAL_TOKENS)


def main() -> int:
    checks: list[dict[str, str]] = []

    def add(check: str, passed: bool, details: str = "") -> None:
        checks.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})

    real_outputs = [
        E / "real_engine_probe_validation_full.csv",
        E / "real_engine_probe_validation_full_summary.csv",
        E / "real_engine_probe_validation_motif.csv",
        E / "real_engine_probe_validation_motif_summary.csv",
        E / "real_engine_validation_check.csv",
        E / "real_engine_validation_environment.csv",
    ]
    add("real_engine_outputs_present", all(path.exists() for path in real_outputs), ";".join(path.name for path in real_outputs if not path.exists()))

    leaking_compute = [rel for rel in CORE_COMPUTE_FILES if contains_real_engine_reference(ROOT / rel)]
    add("core_collision_repair_code_independent", not leaking_compute, ";".join(leaking_compute))

    manifest = E / "paper_table_manifest.csv"
    table_leaks: list[str] = []
    if manifest.exists():
        for row in read_csv(manifest):
            if row.get("paper_table") in CORE_TABLES and any(token in row.get("source_files", "").lower() for token in REAL_TOKENS):
                table_leaks.append(row["paper_table"])
    add("core_paper_tables_do_not_source_real_engine", not table_leaks, ";".join(table_leaks))

    source_check = E / "paper_table_source_check.csv"
    artifact_only = not (PKG / "Paper").exists()
    if source_check.exists():
        source_details = source_check.relative_to(PKG).as_posix()
    elif artifact_only:
        source_details = "artifact-only package excludes paper-table gate"
    else:
        source_details = "missing"
    add("paper_table_source_gate_available", source_check.exists() or artifact_only, source_details)

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
        writer.writeheader()
        writer.writerows(checks)
    passed = sum(row["passed"] == "true" for row in checks)
    print(f"Real-engine noninterference check: {passed}/{len(checks)} passed")
    for row in checks:
        if row["passed"] != "true":
            print("FAIL", row["check"], row["details"])
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
