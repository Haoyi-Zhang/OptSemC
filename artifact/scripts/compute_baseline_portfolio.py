#!/usr/bin/env python3
"""Compute a reader-facing projection-surface portfolio for optimizer-contract comparison.

The portfolio deliberately includes (i) exact negative controls, (ii) common
coarse comparison styles, (iii) single-field ablations, and (iv) adversarial
one-field or strengthened matrix projections.  All rows are computed by the
same projection semantics used by the proof-obligation and repair checks.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from optsemc.baselines import BASELINES
from optsemc.corpus import ContractMaps, load_contract_maps
from optsemc.io import read_csv, write_csv
from optsemc.projections import project_signature

MAPS = ROOT / "evaluation" / "grounded_contract_maps.jsonl"
COND = ROOT / "evaluation" / "grounded" / "conditional_trap_rate.csv"
REPAIR = ROOT / "evaluation" / "grounded" / "repair_certificate_summary.csv"
OUT = ROOT / "evaluation" / "grounded" / "baseline_portfolio.csv"
CHECK = ROOT / "evaluation" / "baseline_portfolio_check.csv"
EMPTY = frozenset()


def recompute_projection(bundle: ContractMaps, method: str) -> dict[str, object]:
    maps, engines, probes = bundle.maps, bundle.engines, bundle.probes
    pairs = list(itertools.combinations(engines, 2))
    # Cache at signature granularity: the corpus has many repeated contract maps.
    sig_cache: dict[object, frozenset[tuple[str, ...]]] = {}
    projected: dict[tuple[str, str], frozenset[tuple[str, ...]]] = {}
    for key, sig in maps.items():
        if sig not in sig_cache:
            sig_cache[sig] = project_signature(sig, method)
        projected[key] = sig_cache[sig]
    comparisons = len(probes) * len(pairs)
    projected_equivalences = true_equivalences = false_equivalences = 0
    projected_differences = false_differences = 0
    for probe in probes:
        for left, right in pairs:
            left_key, right_key = (left, probe), (right, probe)
            left_sig, right_sig = maps.get(left_key, EMPTY), maps.get(right_key, EMPTY)
            projection_equal = projected.get(left_key, EMPTY) == projected.get(right_key, EMPTY)
            exact_equal = left_sig == right_sig
            if projection_equal:
                projected_equivalences += 1
                true_equivalences += int(exact_equal)
                false_equivalences += int(not exact_equal)
            else:
                projected_differences += 1
                false_differences += int(exact_equal)
    return {
        "comparisons": comparisons,
        "projected_equivalences": projected_equivalences,
        "true_equivalences": true_equivalences,
        "false_equivalences": false_equivalences,
        "projected_differences": projected_differences,
        "false_differences": false_differences,
        "conditional_false_equivalence_rate": f"{false_equivalences / projected_equivalences:.6f}" if projected_equivalences else "0.000000",
        "projected_equivalence_rate": f"{projected_equivalences / comparisons:.6f}" if comparisons else "0.000000",
    }


def main() -> None:
    bundle = load_contract_maps(MAPS)
    reported = {r["method"]: r for r in read_csv(COND)}
    repair = {r["method"]: r for r in read_csv(REPAIR)}
    rows = []
    for baseline in BASELINES:
        metrics = recompute_projection(bundle, baseline.projection)
        rep = repair.get(baseline.projection, {})
        rows.append({
            "baseline_id": baseline.baseline_id,
            "projection": baseline.projection,
            "comparison_object": baseline.comparison_object,
            "erased_semantics": baseline.erased_semantics,
            "comparisons": metrics["comparisons"],
            "projected_equivalences": metrics["projected_equivalences"],
            "true_equivalences": metrics["true_equivalences"],
            "false_equivalences": metrics["false_equivalences"],
            "conditional_false_equivalence_rate": metrics["conditional_false_equivalence_rate"],
            "projected_equivalence_rate": metrics["projected_equivalence_rate"],
            "false_differences": metrics["false_differences"],
            "minimum_repair_size": rep.get("minimal_universal_repair_size", "0" if metrics["false_equivalences"] == 0 else "NA"),
            "minimum_repairs": rep.get("repair_sets", "none" if metrics["false_equivalences"] == 0 else "NA"),
            "expected_failure_mode": baseline.expected_failure_mode,
        })
    write_csv(OUT, rows)

    by_projection = {r["projection"]: r for r in rows}
    checks = []
    def add(check: str, ok: bool, details: str = "") -> None:
        checks.append({"check": check, "passed": str(bool(ok)).lower(), "details": details})
    for method in ["keyword", "yesno", "operator_only"]:
        add(
            f"{method}_matches_conditional_trap_rate",
            int(by_projection[method]["projected_equivalences"]) == int(reported[method]["projected_equivalences"])
            and int(by_projection[method]["false_equivalences"]) == int(reported[method]["false_equivalences"]),
            f"surface={by_projection[method]['projected_equivalences']}/{by_projection[method]['false_equivalences']};reported={reported[method]['projected_equivalences']}/{reported[method]['false_equivalences']}",
        )
    add("strict_surface_is_negative_control", int(by_projection["strict"]["false_equivalences"]) == 0 and int(by_projection["strict"]["false_differences"]) == 0)
    add("headline_surfaces_cover_three_granularities", all(method in by_projection for method in ["keyword", "yesno", "operator_only"]))
    add("keyword_and_operator_surfaces_are_lossy", int(by_projection["keyword"]["false_equivalences"]) > 0 and int(by_projection["operator_only"]["false_equivalences"]) > 0)
    add("diagnostic_ablations_noninflating", all(int(by_projection[m]["false_differences"]) == 0 for m in ["no_placement", "no_decision_time", "no_observability", "no_modality"]))
    add("adversarial_projection_suite_present", len(rows) >= 15 and all(m in by_projection for m in ["kind_only", "layer_only", "placement_only", "observability_only", "operator_kind_surface"]))
    add("strengthened_projection_surface_safe", int(by_projection["operator_kind_surface"]["false_equivalences"]) == 0)
    add("coarse_one_field_surfaces_fail", all(int(by_projection[m]["false_equivalences"]) > 0 for m in ["kind_only", "layer_only", "placement_only", "observability_only"]))
    write_csv(CHECK, checks, ["check", "passed", "details"])
    passed = sum(r["passed"] == "true" for r in checks)
    print(f"Projection-surface portfolio: {passed}/{len(checks)} checks passed")
    if passed != len(checks):
        for r in checks:
            if r["passed"] != "true":
                print("FAIL", r["check"], r["details"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
