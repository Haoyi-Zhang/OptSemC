#!/usr/bin/env python3
"""Compute minimal safe and maximal unsafe antichains for the OptSem-C projection lattice."""
from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from optsemc.lattice import FieldSubset, ProjectionCounts, field_projection_frontier

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
EVAL = PACKAGE_ROOT / "artifact" / "evaluation"
IN = EVAL / "projection_resolution_lattice.csv"
OUT = EVAL / "projection_frontier_antichains.csv"
SUMMARY = EVAL / "projection_frontier_antichain_summary.csv"


def parse_fields(value: str) -> tuple[str, ...]:
    value = value.strip()
    if not value or value == "none":
        return tuple()
    return tuple(value.split("+"))


def format_fields(fields: Iterable[str]) -> str:
    fs = tuple(fields)
    return "+".join(fs) if fs else "none"


def read_counts() -> list[ProjectionCounts]:
    with IN.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"empty lattice input: {IN}")
    counts: list[ProjectionCounts] = []
    for row in rows:
        fields = FieldSubset(parse_fields(row["fields"]))
        counts.append(
            ProjectionCounts(
                fields=fields,
                comparisons=int(row["comparisons"]),
                projected_equivalences=int(row["projected_equivalences"]),
                true_equivalences=int(row["true_equivalences"]),
                false_equivalences=int(row["false_equivalences"]),
                projected_classes=int(row["projected_classes"]),
                exact_classes=int(row["exact_classes"]),
                entropy_retained=float(row["entropy_retained"]),
            )
        )
    return counts


def emit_frontier(counts: list[ProjectionCounts], *, include_variant: bool) -> tuple[list[dict[str, str]], dict[str, str]]:
    frontier = field_projection_frontier(counts, include_variant=include_variant)
    universe = "all_fields" if include_variant else "semantic_no_variant"
    out_rows: list[dict[str, str]] = []
    for kind, rows in (("minimal_safe", frontier.minimal_safe_counts), ("maximal_unsafe", frontier.maximal_unsafe_counts)):
        for row in rows:
            out_rows.append(
                {
                    "universe": universe,
                    "frontier": kind,
                    "fields": row.fields.key,
                    "subset_size": str(row.fields.size),
                    "projected_classes": str(row.projected_classes),
                    "entropy_retained": f"{row.entropy_retained:.6f}",
                    "projected_equivalences": str(row.projected_equivalences),
                    "false_equivalences": str(row.false_equivalences),
                }
            )
    min_safe_sizes = sorted({row.fields.size for row in frontier.minimal_safe_counts})
    max_unsafe_sizes = sorted({row.fields.size for row in frontier.maximal_unsafe_counts})
    summary = {
        "universe": universe,
        "subsets": str(len(frontier.counts)),
        "safe_subsets": str(len(frontier.safe_counts)),
        "unsafe_subsets": str(len(frontier.unsafe_counts)),
        "minimal_safe_count": str(len(frontier.minimal_safe_counts)),
        "minimum_safe_size": str(min_safe_sizes[0] if min_safe_sizes else -1),
        "minimum_safe_fields": ";".join(row.fields.key for row in frontier.minimal_safe_counts if row.fields.size == (min_safe_sizes[0] if min_safe_sizes else -1)),
        "maximal_unsafe_count": str(len(frontier.maximal_unsafe_counts)),
        "maximal_unsafe_sizes": ";".join(str(x) for x in max_unsafe_sizes),
        "monotone_safe": str(frontier.monotone_safe()).lower(),
        "monotone_unsafe": str(frontier.monotone_unsafe()).lower(),
        "every_safe_covered": str(frontier.every_safe_covered()).lower(),
        "every_unsafe_covered": str(frontier.every_unsafe_covered()).lower(),
    }
    return out_rows, summary


def main() -> None:
    counts = read_counts()
    all_rows: list[dict[str, str]] = []
    summaries: list[dict[str, str]] = []
    for include_variant in (True, False):
        rows, summary = emit_frontier(counts, include_variant=include_variant)
        all_rows.extend(rows)
        summaries.append(summary)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["universe", "frontier", "fields", "subset_size", "projected_classes", "entropy_retained", "projected_equivalences", "false_equivalences"])
        writer.writeheader()
        writer.writerows(all_rows)
    with SUMMARY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["universe", "subsets", "safe_subsets", "unsafe_subsets", "minimal_safe_count", "minimum_safe_size", "minimum_safe_fields", "maximal_unsafe_count", "maximal_unsafe_sizes", "monotone_safe", "monotone_unsafe", "every_safe_covered", "every_unsafe_covered"])
        writer.writeheader()
        writer.writerows(summaries)
    print(f"Projection frontier antichains: {len(all_rows)} frontier rows over {len(summaries)} universes")


if __name__ == "__main__":
    main()
