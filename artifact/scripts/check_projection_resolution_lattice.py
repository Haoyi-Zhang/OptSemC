#!/usr/bin/env python3
"""Validate the exhaustive projection-resolution lattice and its counterexample cover."""
from __future__ import annotations

import csv
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from optsemc.corpus import load_contract_maps
from optsemc.lattice import FIELD_UNIVERSE, project_signature_fields

E = ROOT / "evaluation"
OUT = E / "projection_resolution_check.csv"
rows: list[dict[str, str]] = []


def add(check: str, passed: bool, details: object = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": str(details)})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_key(key: str) -> set[str]:
    if key == "none" or not key:
        return set()
    return set(key.split("+"))


def main() -> None:
    try:
        lattice = read_csv(E / "projection_resolution_lattice.csv")
        by_key = {r["fields"]: r for r in lattice}
        add("all_256_field_subsets_present", len(lattice) == 2 ** len(FIELD_UNIVERSE), len(lattice))
        add("full_field_signature_safe", by_key.get("operator+kind+variant+layer+placement+decision_time+observability+state", {}).get("safe") == "true", "")
        add("empty_projection_is_unsafe", int(by_key["none"]["false_equivalences"]) > 0 and by_key["none"]["safe"] == "false", by_key["none"]["false_equivalences"])
        true_eq = {r["true_equivalences"] for r in lattice}
        comps = {r["comparisons"] for r in lattice}
        add("common_denominator_across_lattice", len(true_eq) == 1 and len(comps) == 1, f"true={true_eq};comparisons={comps}")
        # Upward closure of safe sets and downward closure of unsafe sets.
        closure_ok = True
        bad = []
        keys = list(by_key)
        sets = {k: parse_key(k) for k in keys}
        for small, large in combinations(keys, 2):
            a, b = sets[small], sets[large]
            if not a <= b:
                a, b = b, a
                small, large = large, small
            if a <= b:
                if by_key[small]["safe"] == "true" and by_key[large]["safe"] != "true":
                    closure_ok = False
                    bad.append(f"safe {small} not upward to {large}")
                    break
                if by_key[large]["safe"] == "false" and by_key[small]["safe"] != "false":
                    closure_ok = False
                    bad.append(f"unsafe {large} not downward to {small}")
                    break
        add("field_lattice_closure", closure_ok, ";".join(bad[:2]))
        min_safe = min(int(r["subset_size"]) for r in lattice if r["safe"] == "true")
        add("minimum_safe_field_count_at_most_five", min_safe <= 5, min_safe)
        sem = {r["metric"]: r["value"] for r in read_csv(E / "projection_resolution_semantic_summary.csv")}
        add("semantic_no_variant_lattice_present", sem.get("semantic_no_variant_subsets") == "128", sem)
        add("semantic_no_variant_minimum_safe_is_two_fields", sem.get("semantic_no_variant_minimum_safe_field_count") == "2", sem.get("semantic_no_variant_minimum_safe_field_sets"))
    except Exception as exc:
        add("lattice_files_parse", False, type(exc).__name__)

    try:
        cover = read_csv(E / "projection_resolution_counterexample_cover.csv")
        summary = {r["metric"]: r["value"] for r in read_csv(E / "projection_resolution_counterexample_summary.csv")}
        covered = set()
        for row in cover:
            covered.update(k for k in row["covered_subset_keys"].split(";") if k)
        unsafe = {r["fields"] for r in lattice if r["safe"] == "false"}
        add("counterexample_cover_covers_all_unsafe_subsets", covered == unsafe, f"covered={len(covered)};unsafe={len(unsafe)}")
        add("counterexample_cover_is_compact", len(cover) <= max(1, len(unsafe) // 2), f"cover={len(cover)};unsafe={len(unsafe)}")
        # Verify every assigned subset is truly falsified by that witness.
        cm = load_contract_maps(ROOT)
        verified = True
        failures = []
        empty_exact = frozenset()
        for row in cover:
            probe = row["probe_id"]
            left = row["left_engine"]
            right = row["right_engine"]
            left_exact = cm.maps.get((left, probe), empty_exact)
            right_exact = cm.maps.get((right, probe), empty_exact)
            for subset_key in [k for k in row["covered_subset_keys"].split(";") if k]:
                fields = tuple(parse_key(subset_key))
                if left_exact == right_exact or project_signature_fields(left_exact, fields) != project_signature_fields(right_exact, fields):
                    verified = False
                    failures.append(f"{probe}:{left}:{right}:{subset_key}")
                    break
            if not verified:
                break
        add("counterexample_cover_witnesses_verify", verified, ";".join(failures[:2]))
        add("minimum_safe_summary_matches_lattice", summary.get("minimum_safe_field_count") == str(min_safe), summary.get("minimum_safe_field_count"))
    except Exception as exc:
        add("counterexample_cover_parse", False, type(exc).__name__)

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
        writer.writeheader()
        writer.writerows(rows)
    passed = sum(r["passed"] == "true" for r in rows)
    print(f"Projection-resolution lattice check: {passed}/{len(rows)} passed")
    for row in rows:
        if row["passed"] != "true":
            print("FAIL", row["check"], row["details"])
    if passed != len(rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
