#!/usr/bin/env python3
"""Compute the exhaustive field-resolution lattice for public contract comparison."""
from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Sequence

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


def compress_signatures(maps: dict[tuple[str, str], object]) -> tuple[list[object], dict[tuple[str, str], int], dict[int, int]]:
    """Compress duplicate exact signatures before evaluating the finite lattice."""
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
    return signatures, key_to_sig_id, sig_occurrences


def build_probe_signature_rows(
    probes: Sequence[str],
    engines: Sequence[str],
    key_to_sig_id: dict[tuple[str, str], int],
    signatures: Sequence[object],
) -> dict[str, tuple[int, ...]]:
    empty_sig_id = next((sid for sid, sig in enumerate(signatures) if sig == frozenset()), None)
    fallback = empty_sig_id if empty_sig_id is not None else -1
    return {probe: tuple(key_to_sig_id.get((engine, probe), fallback) for engine in engines) for probe in probes}


def exact_pair_counts(
    probes: Sequence[str],
    probe_sid_rows: dict[str, tuple[int, ...]],
    engine_pairs: Sequence[tuple[int, int]],
) -> tuple[int, int]:
    comparisons = 0
    true_equivalences = 0
    for probe in probes:
        sids = probe_sid_rows[probe]
        for i, j in engine_pairs:
            comparisons += 1
            if sids[i] == sids[j]:
                true_equivalences += 1
    return comparisons, true_equivalences


def project_signature_ids(
    signatures: Sequence[object],
    sig_occurrences: dict[int, int],
    fields: Sequence[str],
) -> tuple[dict[int, int], dict[int, int], int]:
    projected_signature_to_id: dict[object, int] = {}
    sid_to_pid: dict[int, int] = {}
    projected_occurrences: dict[int, int] = {}
    for sid, sig in enumerate(signatures):
        psig = project_signature_fields(sig, fields)
        if psig not in projected_signature_to_id:
            projected_signature_to_id[psig] = len(projected_signature_to_id)
        pid = projected_signature_to_id[psig]
        sid_to_pid[sid] = pid
        projected_occurrences[pid] = projected_occurrences.get(pid, 0) + sig_occurrences.get(sid, 0)
    return sid_to_pid, projected_occurrences, len(projected_signature_to_id)


def count_projected_pairs(
    subset_key: str,
    sid_to_pid: dict[int, int],
    probes: Sequence[str],
    engines: Sequence[str],
    probe_sid_rows: dict[str, tuple[int, ...]],
    engine_pairs: Sequence[tuple[int, int]],
    witness_to_subsets: dict[tuple[str, str, str], set[str]],
) -> tuple[int, int]:
    projected_equivalences = 0
    false_equivalences = 0
    sampled_witnesses = 0
    for probe in probes:
        sids = probe_sid_rows[probe]
        pids = [sid_to_pid.get(sid, -2) for sid in sids]
        for i, j in engine_pairs:
            if pids[i] != pids[j]:
                continue
            projected_equivalences += 1
            if sids[i] == sids[j]:
                continue
            false_equivalences += 1
            if sampled_witnesses < 32:
                witness_to_subsets.setdefault((probe, engines[i], engines[j]), set()).add(subset_key)
                sampled_witnesses += 1
    return projected_equivalences, false_equivalences


def evaluate_resolution_lattice(
    signatures: Sequence[object],
    sig_occurrences: dict[int, int],
    engines: Sequence[str],
    probes: Sequence[str],
    probe_sid_rows: dict[str, tuple[int, ...]],
) -> tuple[list[ProjectionCounts], list[str], dict[tuple[str, str, str], set[str]]]:
    exact_entropy = entropy_of_signatures(sid for sid, count in sig_occurrences.items() for _ in range(count))
    exact_classes = len(signatures)
    engine_pairs = [(i, j) for i in range(len(engines)) for j in range(i + 1, len(engines))]
    comparisons, true_equivalences = exact_pair_counts(probes, probe_sid_rows, engine_pairs)
    counts: list[ProjectionCounts] = []
    unsafe_subset_keys: list[str] = []
    witness_to_subsets: dict[tuple[str, str, str], set[str]] = {}
    for subset in enumerate_field_subsets():
        sid_to_pid, projected_occurrences, projected_classes = project_signature_ids(signatures, sig_occurrences, subset.fields)
        projected_equivalences, false_equivalences = count_projected_pairs(
            subset.key,
            sid_to_pid,
            probes,
            engines,
            probe_sid_rows,
            engine_pairs,
            witness_to_subsets,
        )
        h_projected = entropy_of_signatures(pid for pid, count in projected_occurrences.items() for _ in range(count))
        retained = 1.0 if exact_entropy == 0 else h_projected / exact_entropy
        counts.append(
            ProjectionCounts(
                fields=subset,
                comparisons=comparisons,
                projected_equivalences=projected_equivalences,
                true_equivalences=true_equivalences,
                false_equivalences=false_equivalences,
                projected_classes=projected_classes,
                exact_classes=exact_classes,
                entropy_retained=retained,
            )
        )
        if false_equivalences:
            unsafe_subset_keys.append(subset.key)
    return counts, unsafe_subset_keys, witness_to_subsets


def write_lattice_outputs(counts: Sequence[ProjectionCounts]) -> None:
    rows = [
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
        for c in counts
    ]
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
    write_csv(
        E / "projection_resolution_summary.csv",
        summarize_by_size(counts),
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


def semantic_resolution_summary(counts: Sequence[ProjectionCounts]) -> tuple[int, list[str], list[str]]:
    semantic_counts = [c for c in counts if "variant" not in c.fields.fields]
    min_safe_size = min(c.fields.size for c in counts if c.safe)
    min_safe_keys = [c.fields.key for c in counts if c.safe and c.fields.size == min_safe_size]
    min_semantic_safe_size = min(c.fields.size for c in semantic_counts if c.safe)
    min_semantic_safe_keys = [c.fields.key for c in semantic_counts if c.safe and c.fields.size == min_semantic_safe_size]
    rows = [
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
    write_csv(E / "projection_resolution_semantic_summary.csv", rows, ["metric", "value"])
    return min_safe_size, min_safe_keys, min_semantic_safe_keys


def write_paper_projection_rows(counts: Sequence[ProjectionCounts], min_semantic_safe_keys: Sequence[str]) -> None:
    by_key = {c.fields.key: c for c in counts}
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
    for key in candidate_keys + list(min_semantic_safe_keys):
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


def write_counterexample_cover(
    counts: Sequence[ProjectionCounts],
    unsafe_subset_keys: Sequence[str],
    witness_to_subsets: dict[tuple[str, str, str], set[str]],
    min_safe_size: int,
    min_safe_keys: Sequence[str],
) -> list[dict[str, object]]:
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
    return cover_rows


def main() -> None:
    cm = load_contract_maps(ROOT)
    signatures, key_to_sig_id, sig_occurrences = compress_signatures(cm.maps)
    probe_sid_rows = build_probe_signature_rows(cm.probes, cm.engines, key_to_sig_id, signatures)
    counts, unsafe_subset_keys, witness_to_subsets = evaluate_resolution_lattice(
        signatures,
        sig_occurrences,
        cm.engines,
        cm.probes,
        probe_sid_rows,
    )
    write_lattice_outputs(counts)
    min_safe_size, min_safe_keys, min_semantic_safe_keys = semantic_resolution_summary(counts)
    write_paper_projection_rows(counts, min_semantic_safe_keys)
    cover_rows = write_counterexample_cover(counts, unsafe_subset_keys, witness_to_subsets, min_safe_size, min_safe_keys)
    print(
        "Projection-resolution lattice: "
        f"{len(counts)} subsets; {sum(c.safe for c in counts)} safe; "
        f"{len(unsafe_subset_keys)} unsafe; cover={len(cover_rows)} witnesses"
    )


if __name__ == "__main__":
    main()
