#!/usr/bin/env python3
"""Derive the semantic-repair frontier used in the paper.

The frontier is a compact view of the full projection-lattice enumeration.  It
reports how many field subsets are safe/unsafe, the size of minimum safe repairs,
and the largest unsafe subsets.  The output turns repair minimality from a table
claim into a auditable finite certificate.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = ROOT / "evaluation" / "grounded"
OUT = G / "semantic_frontier.csv"
CHECK = ROOT / "evaluation" / "semantic_frontier_check.csv"
PAPER_TABLE = ROOT.parent / "Paper" / "latex" / "tables" / "tab_semantic_frontier.tex"
ROW_END = r" \\" 


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    if not rows:
        return
    if fields is None:
        fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def esc(value: object) -> str:
    s = str(value)
    return (s.replace("\\", r"\textbackslash{}")
             .replace("&", r"\&")
             .replace("%", r"\%")
             .replace("$", r"\$")
             .replace("#", r"\#")
             .replace("_", r"\_")
             .replace("{", r"\{")
             .replace("}", r"\}"))


def choose_example(examples: str) -> str:
    parts = [p for p in examples.split(";") if p]
    for target in ["layer+placement", "placement", "layer"]:
        if target in parts:
            return target
    return parts[0] if parts else ""


def main() -> None:
    source = read_csv(G / "projection_lattice_summary.csv")
    keep = []
    for r in source:
        if r["scope"] in {"keyword", "yesno", "operator_only", "all_projections"} and r["field_universe"] in {"core_semantic_state_free", "semantic_no_variant"}:
            keep.append({
                "scope": r["scope"],
                "field_universe": r["field_universe"],
                "false_equivalences": r["baseline_false_equivalences"],
                "total_field_subsets": r["total_subsets"],
                "safe_subsets": r["safe_subsets"],
                "unsafe_subsets": r["unsafe_subsets"],
                "minimum_safe_size": r["minimum_safe_size"],
                "minimum_safe_sets": r["example_minimum_safe_sets"],
                "representative_minimum_safe_set": choose_example(r["example_minimum_safe_sets"]),
                "maximum_unsafe_size": r["maximum_unsafe_size"],
                "representative_maximum_unsafe_set": choose_example(r["example_maximum_unsafe_sets"]),
            })
    fields = ["scope", "field_universe", "false_equivalences", "total_field_subsets", "safe_subsets", "unsafe_subsets", "minimum_safe_size", "minimum_safe_sets", "representative_minimum_safe_set", "maximum_unsafe_size", "representative_maximum_unsafe_set"]
    write_csv(OUT, keep, fields)

    core = [r for r in keep if r["field_universe"] == "core_semantic_state_free"]
    labels = {"keyword": "Keyword", "yesno": "Yes/No", "operator_only": "Operator-only", "all_projections": "All"}
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Semantic repair frontier over the core field universe. Safe subsets repair all projection-induced collisions for the projection scope; unsafe subsets leave at least one grounded counter-witness.}",
        r"\label{tab:semantic-frontier}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\begin{tabular}{@{}lrrrrl@{}}",
        r"\toprule",
        "Scope & False & Safe & Unsafe & Min. & Example" + ROW_END,
        r"\midrule",
    ]
    order = {"keyword": 0, "yesno": 1, "operator_only": 2, "all_projections": 3}
    for r in sorted(core, key=lambda x: order[x["scope"]]):
        lines.append(f"{labels[r['scope']]} & {int(r['false_equivalences']):,} & {int(r['safe_subsets']):,} & {int(r['unsafe_subsets']):,} & {r['minimum_safe_size']} & {esc(r['representative_minimum_safe_set'])}" + ROW_END)
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    PAPER_TABLE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    checks = []
    def add(check: str, ok: bool, details: str = "") -> None:
        checks.append({"check": check, "passed": str(bool(ok)).lower(), "details": details})
    add("frontier_rows_cover_scopes_and_universes", len(keep) == 8, f"rows={len(keep)}")
    by_key = {(r["scope"], r["field_universe"]): r for r in keep}
    add("core_all_projection_minimum_is_two", by_key[("all_projections", "core_semantic_state_free")]["minimum_safe_size"] == "2")
    add("layer_placement_is_core_all_projection_basis", "layer+placement" in by_key[("all_projections", "core_semantic_state_free")]["minimum_safe_sets"])
    add("keyword_placement_singleton_is_safe", "placement" in by_key[("keyword", "core_semantic_state_free")]["minimum_safe_sets"])
    add("operator_layer_singleton_is_safe", "layer" in by_key[("operator_only", "core_semantic_state_free")]["minimum_safe_sets"])
    add("unsafe_counterfrontier_nonempty", all(int(r["unsafe_subsets"]) > 0 for r in core))
    write_csv(CHECK, checks, ["check", "passed", "details"])
    passed = sum(r["passed"] == "true" for r in checks)
    print(f"Semantic frontier: {passed}/{len(checks)} checks passed")
    if passed != len(checks):
        for r in checks:
            if r["passed"] != "true":
                print("FAIL", r["check"], r["details"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
