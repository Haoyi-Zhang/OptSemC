#!/usr/bin/env python3
"""Compute the exhaustive field-resolution lattice for public contract comparison."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from optsemc.corpus import load_contract_maps
from optsemc.lattice import (
    ProjectionCounts,
    enumerate_field_subsets,
    entropy_of_signatures,
    project_signature_fields,
    summarize_by_size,
)

E = ROOT / "evaluation"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    cm = load_contract_maps(ROOT)
    maps = cm.maps
    engines = cm.engines
    probes = cm.probes

    # Compress repeated contract signatures.  The grounded maps contain many
    # duplicate exact signatures across probes; evaluating the lattice at the
    # signature-class level makes the exhaustive 2^8 search fast and exact.
    signature_to_id: dict[object, int] = {}
    signatures: list[object] = []
    key_to_sig_id: dict[tuple[str, str], int] = {}
    sig_occurrences: dict[int, int] = {}
    for key, sig in maps.items():
        if sig not in signature_to_id:
            signature_to_id[sig] = len(signatures)
            signatures.append(sig)
        sid = signature_to_id[sig]
        key_to_sig_id[key] = sid
        sig_occurrences[sid] = sig_occurrences.get(sid, 0) + 1

    exact_entropy = entropy_of_signatures(key_to_sig_id.values())
    exact_classes = len(signatures)
    empty_sig_id = signature_to_id.get(frozenset())
    probe_sid_rows: dict[str, tuple[int, ...]] = {}
    for probe in probes:
        probe_sid_rows[probe] = tuple(key_to_sig_id.get((engine, probe), empty_sig_id if empty_sig_id is not None else -1) for engine in engines)

    comparisons = 0
    true_equivalences = 0
    engine_pair_indices = [(i, j) for i in range(len(engines)) for j in range(i + 1, len(engines))]
    for probe in probes:
        sids = probe_sid_rows[probe]
        for i, j in engine_pair_indices:
            comparisons += 1
            if sids[i] == sids[j]:
                true_equivalences += 1

    counts = []
    unsafe_subset_keys: list[str] = []
    witness_to_subsets: dict[tuple[str, str, str], set[str]] = {}
    for subset in enumerate_field_subsets():
        projected_signature_to_id: dict[object, int] = {}
        sid_to_pid: dict[int, int] = {}
        projected_occurrences: dict[int, int] = {}
        for sid, sig in enumerate(signatures):
            psig = project_signature_fields(sig, subset.fields)
            if psig not in projected_signature_to_id:
                projected_signature_to_id[psig] = len(projected_signature_to_id)
            pid = projected_signature_to_id[psig]
            sid_to_pid[sid] = pid
            projected_occurrences[pid] = projected_occurrences.get(pid, 0) + sig_occurrences.get(sid, 0)
        projected_equivalences = 0
        false_equivalences = 0
        sampled_witnesses = 0
        for probe in probes:
            sids = probe_sid_rows[probe]
            pids = [sid_to_pid.get(sid, -2) for sid in sids]
            for i, j in engine_pair_indices:
                if pids[i] == pids[j]:
                    projected_equivalences += 1
                    if sids[i] != sids[j]:
                        false_equivalences += 1
                        if sampled_witnesses < 32:
                            witness_to_subsets.setdefault((probe, engines[i], engines[j]), set()).add(subset.key)
                            sampled_witnesses += 1
        h_projected = entropy_of_signatures(
            pid for pid, count in projected_occurrences.items() for _ in range(count)
        )
        retained = 1.0 if exact_entropy == 0 else h_projected / exact_entropy
        counts.append(
            ProjectionCounts(
                fields=subset,
                comparisons=comparisons,
                projected_equivalences=projected_equivalences,
                true_equivalences=true_equivalences,
                false_equivalences=false_equivalences,
                projected_classes=len(projected_signature_to_id),
                exact_classes=exact_classes,
                entropy_retained=retained,
            )
        )
        if false_equivalences:
            unsafe_subset_keys.append(subset.key)

    rows: list[dict[str, object]] = []
    for c in counts:
        rows.append(
            {
                "fields": c.fields.key,
                "subset_size": c.fields.size,
                "projected_classes": c.projected_classes,
                "exact_classes": c.exact_classes,
                "entropy_retained": f"{c.entropy_retained:.6f}",
                "comparisons": c.comparisons,
                "projected_equivalences": c.projected_equivalences,
                "true_equivalences": c.true_equivalences,
                "false_equivalences": c.false_equivalences,
                "conditional_false_equivalence_rate": f"{c.conditional_false_rate:.6f}",
                "kernel_inflation": f"{c.kernel_inflation:.6f}",
                "safe": str(c.safe).lower(),
            }
        )
    write_csv(
        E / "projection_resolution_lattice.csv",
        rows,
        [
            "fields",
            "subset_size",
            "projected_classes",
            "exact_classes",
            "entropy_retained",
            "comparisons",
            "projected_equivalences",
            "true_equivalences",
            "false_equivalences",
            "conditional_false_equivalence_rate",
            "kernel_inflation",
            "safe",
        ],
    )
    summary = summarize_by_size(counts)
    write_csv(
        E / "projection_resolution_summary.csv",
        summary,
        [
            "subset_size",
            "subsets",
            "safe_subsets",
            "unsafe_subsets",
            "min_false_equivalences",
            "median_false_equivalences",
            "max_false_equivalences",
            "best_fields",
            "best_entropy_retained",
            "worst_fields",
        ],
    )

    by_key = {c.fields.key: c for c in counts}
    semantic_counts = [c for c in counts if "variant" not in c.fields.fields]
    min_safe_size = min(c.fields.size for c in counts if c.safe)
    min_safe_keys = [c.fields.key for c in counts if c.safe and c.fields.size == min_safe_size]
    min_semantic_safe_size = min(c.fields.size for c in semantic_counts if c.safe)
    min_semantic_safe_keys = [c.fields.key for c in semantic_counts if c.safe and c.fields.size == min_semantic_safe_size]

    semantic_summary_rows = [
        {"metric": "all_field_subsets", "value": len(counts)},
        {"metric": "all_safe_subsets", "value": sum(c.safe for c in counts)},
        {"metric": "all_unsafe_subsets", "value": sum(not c.safe for c in counts)},
        {"metric": "all_minimum_safe_field_count", "value": min_safe_size},
        {"metric": "all_minimum_safe_field_sets", "value": ";".join(sorted(min_safe_keys))},
        {"metric": "semantic_no_variant_subsets", "value": len(semantic_counts)},
        {"metric": "semantic_no_variant_safe_subsets", "value": sum(c.safe for c in semantic_counts)},
        {"metric": "semantic_no_variant_unsafe_subsets", "value": sum(not c.safe for c in semantic_counts)},
        {"metric": "semantic_no_variant_minimum_safe_field_count", "value": min_semantic_safe_size},
        {"metric": "semantic_no_variant_minimum_safe_field_sets", "value": ";".join(sorted(min_semantic_safe_keys))},
    ]
    write_csv(E / "projection_resolution_semantic_summary.csv", semantic_summary_rows, ["metric", "value"])

    candidate_keys = [
        "none",
        "operator",
        "kind",
        "layer",
        "placement",
        "operator+layer",
        "kind+placement",
        "operator+kind+layer+placement+observability",
        "operator+kind+layer+placement+decision_time+observability+state",
    ]
    seen: set[str] = set()
    paper_rows: list[dict[str, object]] = []
    for key in candidate_keys + min_semantic_safe_keys:
        if key in seen or key not in by_key:
            continue
        seen.add(key)
        c = by_key[key]
        paper_rows.append(
            {
                "retained_fields": key.replace("+", "+\\allowbreak "),
                "field_count": c.fields.size,
                "classes": c.projected_classes,
                "entropy_retained": f"{c.entropy_retained:.3f}",
                "declared_equivalences": c.projected_equivalences,
                "false_equivalences": c.false_equivalences,
                "status": "safe" if c.safe else "unsafe",
            }
        )
    write_csv(
        E / "projection_resolution_paper.csv",
        paper_rows,
        [
            "retained_fields",
            "field_count",
            "classes",
            "entropy_retained",
            "declared_equivalences",
            "false_equivalences",
            "status",
        ],
    )

    uncovered = set(unsafe_subset_keys)
    cover_rows: list[dict[str, object]] = []
    rank = 1
    while uncovered:
        best_witness, covered = max(
            ((w, ss & uncovered) for w, ss in witness_to_subsets.items()),
            key=lambda item: (len(item[1]), item[0]),
        )
        if not covered:
            raise SystemExit("internal error: unsafe subset without sampled witness")
        probe, left, right = best_witness
        cover_rows.append(
            {
                "rank": rank,
                "probe_id": probe,
                "left_engine": left,
                "right_engine": right,
                "covered_unsafe_subsets": len(covered),
                "covered_subset_keys": ";".join(sorted(covered)),
            }
        )
        uncovered -= covered
        rank += 1
    write_csv(
        E / "projection_resolution_counterexample_cover.csv",
        cover_rows,
        ["rank", "probe_id", "left_engine", "right_engine", "covered_unsafe_subsets", "covered_subset_keys"],
    )
    write_csv(
        E / "projection_resolution_counterexample_summary.csv",
        [
            {"metric": "field_subsets", "value": len(counts)},
            {"metric": "unsafe_field_subsets", "value": len(unsafe_subset_keys)},
            {"metric": "counterexample_cover_size", "value": len(cover_rows)},
            {"metric": "minimum_safe_field_count", "value": min_safe_size},
            {"metric": "minimum_safe_field_sets", "value": ";".join(sorted(min_safe_keys))},
        ],
        ["metric", "value"],
    )
    print(
        "Projection-resolution lattice: "
        f"{len(counts)} subsets; {sum(c.safe for c in counts)} safe; "
        f"{len(unsafe_subset_keys)} unsafe; cover={len(cover_rows)} witnesses"
    )


if __name__ == "__main__":
    main()
