#!/usr/bin/env python3
"""Check the reusable optsemc library against frozen artifact metrics."""
from __future__ import annotations

import compileall
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from optsemc.corpus import load_contract_maps
from optsemc.io import read_csv, write_csv
from optsemc.projections import ADVERSARIAL_METHODS, false_equivalence_witnesses, project_signature
from optsemc.semantics import evidence_signature, parse_action_key

OUT = ROOT / "evaluation" / "core_library_contract.csv"


def main() -> None:
    rows = []
    def add(check: str, ok: bool, details: str = "") -> None:
        rows.append({"check": check, "passed": str(bool(ok)).lower(), "details": details})

    add("library_compileall", compileall.compile_dir(str(ROOT / "optsemc"), quiet=1), "artifact/optsemc")
    legacy = parse_action_key("Join|choose|physical_planning|local_engine|compile_time|estimated_physical_plan", "MAY")
    current = parse_action_key("Join|choose|hash|physical_planning|local_engine|compile_time|estimated_physical_plan", "MAY")
    add("legacy_six_field_action_keys_supported", legacy.variant == "" and legacy.layer == "physical_planning")
    add("current_seven_field_action_keys_supported", current.variant == "hash" and current.state == "MAY")
    sig = evidence_signature({"Join|choose|hash|physical_planning|local_engine|compile_time|estimated_physical_plan": "MAY", "Scan|scan||physical_planning|local_engine|compile_time|estimated_physical_plan": "UNSPEC"})
    add("evidence_signature_excludes_unspec", len(sig) == 1)
    add("strict_projection_is_identity_on_atoms", project_signature(sig, "strict") == frozenset(a.as_tuple() for a in sig))

    bundle = load_contract_maps(ROOT / "evaluation" / "grounded_contract_maps.jsonl")
    reported = {r["method"]: int(r["false_equivalences"]) for r in read_csv(ROOT / "evaluation" / "grounded" / "conditional_trap_rate.csv")}
    for method in ("keyword", "yesno", "operator_only"):
        computed = len(false_equivalence_witnesses(bundle.maps, bundle.engines, bundle.probes, method))
        add(f"{method}_witness_count_via_library", computed == reported[method], f"computed={computed};reported={reported[method]}")

    portfolio = {r["projection"]: r for r in read_csv(ROOT / "evaluation" / "grounded" / "baseline_portfolio.csv")}
    add("adversarial_projection_methods_registered", all(method in portfolio for method in ADVERSARIAL_METHODS), ",".join(ADVERSARIAL_METHODS))
    add("coarse_one_field_baseline_counts_via_library", int(portfolio["placement_only"]["false_equivalences"]) == 10702 and int(portfolio["observability_only"]["false_equivalences"]) == 6652)
    add("strengthened_surface_projection_is_safe", int(portfolio["operator_kind_surface"]["false_equivalences"]) == 0)

    write_csv(OUT, rows, ["check", "passed", "details"])
    passed = sum(r["passed"] == "true" for r in rows)
    print(f"Core library contract: {passed}/{len(rows)} checks passed")
    if passed != len(rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
