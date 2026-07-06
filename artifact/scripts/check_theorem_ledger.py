#!/usr/bin/env python3
"""Machine-check the formal-obligation ledger for OptSem-C.

This script does not use a proof assistant.  It checks the finite obligations
that the paper claims are discharged by the
packaged artifact: state algebra properties, projection witnesses, lattice
frontiers, repair certificates, coverage, and public provenance.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
G = E / "grounded"
OUT = E / "theorem_ledger.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def metric(path: Path, key: str, value_field: str = "value") -> str | None:
    for r in read_csv(path):
        if r.get("metric") == key or r.get("check") == key or r.get("property") == key:
            return r.get(value_field) or r.get("passed") or r.get("value")
    return None


def all_true(path: Path, field: str = "passed") -> bool:
    rows = read_csv(path)
    return bool(rows) and all(r.get(field) == "true" for r in rows)


def count_jsonl(path: Path) -> int:
    with path.open(encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def main() -> None:
    rows: list[dict[str, str]] = []
    def add(theorem: str, obligation: str, support: str, ok: bool, details: str = "") -> None:
        rows.append({
            "theorem_or_claim": theorem,
            "finite_obligation": obligation,
            "support": support,
            "passed": str(bool(ok)).lower(),
            "details": details,
        })

    try:
        rules = count_jsonl(ROOT / "grounded" / "verified_rules.jsonl")
        probes = count_jsonl(ROOT / "benchmark" / "generated_probes.jsonl")
        maps = count_jsonl(E / "grounded_contract_maps.jsonl")
        add("F1 finite evaluation", "finite rules/probes/maps exist and state-join properties hold", "grounded/*.jsonl; benchmark/*.jsonl; state_join_properties.csv", rules == 287 and probes == 4216 and maps > 0 and all_true(E / "state_join_properties.csv"), f"rules={rules};probes={probes};maps={maps}")
    except Exception as exc:
        add("F1 finite evaluation", "finite rules/probes/maps exist and state-join properties hold", "state_join_properties.csv", False, type(exc).__name__)

    try:
        cond = {r["method"]: r for r in read_csv(G / "conditional_trap_rate.csv")}
        strict = {r["projection"]: r for r in read_csv(G / "baseline_portfolio.csv")}["strict"]
        ok = int(cond["keyword"]["false_equivalences"]) == 254 and int(cond["operator_only"]["false_equivalences"]) == 238 and int(strict["false_equivalences"]) == 0
        add("F2 projection loss", "lossy projections have grounded false-equivalence witnesses; exact projection has none", "conditional_trap_rate.csv; baseline_portfolio.csv", ok, f"keyword={cond['keyword']['false_equivalences']};operator={cond['operator_only']['false_equivalences']};strict={strict['false_equivalences']}")
    except Exception as exc:
        add("F2 projection loss", "lossy projections have grounded false-equivalence witnesses; exact projection has none", "conditional_trap_rate.csv", False, type(exc).__name__)

    try:
        sem = {r["check"]: r for r in read_csv(E / "semantics_audit.csv")}
        ok = sem.get("merge_conflict_records", {}).get("value") == "0" and sem.get("conflict_states_in_maps", {}).get("value") == "0"
        add("F3 conflict-aware merge", "accepted grounded maps contain no silent conflicts", "semantics_audit.csv; grounded_conflicts.jsonl", ok, f"merge={sem.get('merge_conflict_records', {}).get('value')};states={sem.get('conflict_states_in_maps', {}).get('value')}")
    except Exception as exc:
        add("F3 conflict-aware merge", "accepted grounded maps contain no silent conflicts", "semantics_audit.csv", False, type(exc).__name__)

    add("F4 projection-lattice monotonicity", "lattice frontier enumeration and monotonicity checks pass", "projection_lattice_check.csv", all_true(E / "projection_lattice_check.csv"), "")
    add("F5 projection proof obligations", "every counted witness is exact-unequal, projection-equal, and repair-separated", "projection_proof_obligations.csv", all_true(E / "projection_proof_obligations.csv"), "")
    add("F6 minimum repair certificates", "direct enumeration, lower-bound checks, and hitting-set certificates agree", "repair_certificate_minimality.csv; repair_hitting_set_check.csv", all_true(E / "repair_certificate_minimality.csv") and all_true(E / "repair_hitting_set_check.csv"), "")

    try:
        rb = read_csv(G / "repair_basis_stability.csv")
        ok = any(r["scope"] == "all_projections" and r["basis"] == "layer+placement" and r["unresolved"] == "0" for r in rb)
        frontier = {r["check"]: r for r in read_csv(E / "semantic_frontier_check.csv")}
        ok = ok and all(r["passed"] == "true" for r in frontier.values())
        add("F7 semantic repair basis", "layer+placement repairs all projections in the core field universe", "repair_basis_stability.csv; semantic_frontier_check.csv", ok, "")
    except Exception as exc:
        add("F7 semantic repair basis", "layer+placement repairs all projections in the core field universe", "repair_basis_stability.csv", False, type(exc).__name__)

    try:
        probe_issues = metric(E / "probe_validity.csv", "issues")
        xw = read_csv(G / "external_benchmark_crosswalk.csv")
        coverage = read_csv(E / "coverage_interactions.csv")
        ok = probe_issues == "0" and all(float(r["coverage"]) == 1.0 for r in coverage) and all(int(r["covered_requirements"]) == int(r["total_requirements"]) for r in xw)
        add("F8 benchmark coverage", "valid probes cover all target interactions and external motif requirements", "probe_validity.csv; coverage_interactions.csv; external_benchmark_crosswalk.csv", ok, f"probe_issues={probe_issues};motifs={len(xw)}")
    except Exception as exc:
        add("F8 benchmark coverage", "valid probes cover all target interactions and external motif requirements", "probe_validity.csv", False, type(exc).__name__)

    try:
        pp = {r["metric"]: r["value"] for r in read_csv(E / "public_provenance_summary.csv")}
        ok = pp.get("verified_segments") == pp.get("segments_with_public_locator") and pp.get("public_provenance_issues") == "0"
        add("F9 public provenance", "every grounded rule has public locator and clean provenance", "public_provenance_summary.csv", ok, str(pp))
    except Exception as exc:
        add("F9 public provenance", "every grounded rule has public locator and clean provenance", "public_provenance_summary.csv", False, type(exc).__name__)

    try:
        bp = {r["projection"]: r for r in read_csv(G / "baseline_portfolio.csv")}
        ok = int(bp["placement_only"]["false_equivalences"]) > 10000 and int(bp["operator_kind_surface"]["false_equivalences"]) == 0
        add("C1 projection-surface stress suite", "coarse one-field surfaces fail while the high-information surface control is safe", "baseline_portfolio.csv; baseline_portfolio_check.csv", ok and all_true(E / "baseline_portfolio_check.csv"), f"placement_only={bp['placement_only']['false_equivalences']};surface={bp['operator_kind_surface']['false_equivalences']}")
    except Exception as exc:
        add("C1 projection-surface stress suite", "coarse one-field surfaces fail while the high-information surface control is safe", "baseline_portfolio.csv", False, type(exc).__name__)

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["theorem_or_claim", "finite_obligation", "support", "passed", "details"])
        writer.writeheader(); writer.writerows(rows)
    passed = sum(r["passed"] == "true" for r in rows)
    print(f"Formal-obligation ledger: {passed}/{len(rows)} checks passed")
    if passed != len(rows):
        for r in rows:
            if r["passed"] != "true":
                print("FAIL", r["theorem_or_claim"], r["details"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
