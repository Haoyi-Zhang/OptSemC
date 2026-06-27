#!/usr/bin/env python3
"""Compute semantic repair bases for grounded OptSem-C comparisons.

The repair-certificate analysis in earlier snapshots allowed the action
variant field. This script reports a stricter, reader-facing diagnostic:
minimal repairs using only interpretable semantic fields, excluding the
fine-grained variant label. It also computes repair bases that work across
all lossy projections at once.
"""
from __future__ import annotations
import csv, itertools, json
from pathlib import Path
from collections import Counter, defaultdict

FIELDS = ["operator", "kind", "variant", "layer", "placement", "decision_time", "observability", "state"]
SEMANTIC_FIELDS = [f for f in FIELDS if f != "variant"]
METHODS = ["keyword", "yesno", "operator_only"]


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def split_action(action_key: str, state: str):
    parts = action_key.split("|")
    if len(parts) == 6:
        op, kind, layer, placement, decision_time, observability = parts
        variant = ""
    else:
        parts = (parts + [""] * 7)[:7]
        op, kind, variant, layer, placement, decision_time, observability = parts
    d = {
        "operator": op,
        "kind": kind,
        "variant": variant,
        "layer": layer,
        "placement": placement,
        "decision_time": decision_time,
        "observability": observability,
        "state": state,
    }
    return tuple(d[f] for f in FIELDS)


def baseline_atom(a, method):
    d = dict(zip(FIELDS, a))
    op, kind = d["operator"], d["kind"]
    if method == "keyword":
        if kind in {"delegate", "pushdown", "prune"}:
            return ("pushdown", "yes")
        if kind == "observe":
            return ("explain", "yes")
        if kind == "reorder":
            return ("join_order", "yes")
        if kind == "adapt":
            return ("adaptivity", "yes")
        if kind in {"materialize", "inline"}:
            return ("materialization", "yes")
        if kind == "choose":
            return ("choose", "yes")
        if kind == "fallback":
            return ("fallback", "yes")
        return (kind, "yes")
    if method == "yesno":
        return (op, kind, "yes")
    if method == "operator_only":
        return (op, "yes")
    raise ValueError(method)


def project(sig, method, extra_fields=()):
    idx = [FIELDS.index(f) for f in extra_fields]
    return frozenset(baseline_atom(a, method) + tuple(a[i] for i in idx) for a in sig)


def load_maps(path: Path):
    maps = {}
    engines, probes = set(), set()
    for row in read_jsonl(path):
        sig = frozenset(split_action(k, v) for k, v in row.get("actions", {}).items() if v != "UNSPEC")
        key = (row["engine"], row["probe_id"])
        maps[key] = sig
        engines.add(row["engine"])
        probes.add(row["probe_id"])
    return maps, sorted(engines), sorted(probes)


def false_equivalences(maps, engines, probes, method):
    rows = []
    for p in probes:
        for e1, e2 in itertools.combinations(engines, 2):
            s1 = maps.get((e1, p), frozenset())
            s2 = maps.get((e2, p), frozenset())
            if s1 == s2:
                continue
            if project(s1, method) == project(s2, method):
                rows.append((method, p, e1, e2, s1, s2))
    return rows


def minimal_repairs(rows, fields):
    if not rows:
        return [()]
    # Every row stores its method because projections differ.
    for k in range(1, len(fields) + 1):
        good = []
        for sub in itertools.combinations(fields, k):
            ok = True
            for method, _p, _e1, _e2, s1, s2 in rows:
                if project(s1, method, sub) == project(s2, method, sub):
                    ok = False
                    break
            if ok:
                good.append(sub)
        if good:
            return good
    return []


def row_repair_fields(row, fields):
    method, _p, _e1, _e2, s1, s2 = row
    return [f for f in fields if project(s1, method, [f]) != project(s2, method, [f])]


def main():
    root = Path(__file__).resolve().parents[1]
    maps, engines, probes = load_maps(root / "evaluation" / "grounded_contract_maps.jsonl")
    outdir = root / "evaluation" / "grounded"
    outdir.mkdir(parents=True, exist_ok=True)

    by_method = {m: false_equivalences(maps, engines, probes, m) for m in METHODS}
    all_rows = [r for rows in by_method.values() for r in rows]

    summary = []
    coverage = []
    examples = []
    for method, rows in by_method.items():
        reps = minimal_repairs(rows, SEMANTIC_FIELDS)
        summary.append({
            "scope": method,
            "false_equivalences": len(rows),
            "semantic_fields_allowed": ";".join(SEMANTIC_FIELDS),
            "minimal_semantic_repair_size": len(reps[0]) if reps else 0,
            "minimal_semantic_repair_sets": ";".join("+".join(r) for r in reps),
            "num_minimal_semantic_repair_sets": len(reps),
        })
        counter = Counter()
        for row in rows:
            fs = row_repair_fields(row, SEMANTIC_FIELDS)
            for f in fs:
                counter[f] += 1
            if len(examples) < 150:
                method2, p, e1, e2, s1, s2 = row
                examples.append({
                    "scope": method2,
                    "probe_id": p,
                    "engine_i": e1,
                    "engine_j": e2,
                    "semantic_repair_fields": ";".join(fs),
                    "sig_i_size": len(s1),
                    "sig_j_size": len(s2),
                })
        for f, n in counter.most_common():
            coverage.append({
                "scope": method,
                "field": f,
                "false_equivalences_repaired_by_field": n,
                "fraction": f"{(n/len(rows) if rows else 0):.6f}",
            })

    global_reps = minimal_repairs(all_rows, SEMANTIC_FIELDS)
    summary.append({
        "scope": "all_projections",
        "false_equivalences": len(all_rows),
        "semantic_fields_allowed": ";".join(SEMANTIC_FIELDS),
        "minimal_semantic_repair_size": len(global_reps[0]) if global_reps else 0,
        "minimal_semantic_repair_sets": ";".join("+".join(r) for r in global_reps),
        "num_minimal_semantic_repair_sets": len(global_reps),
    })

    def write(name, rows, fields):
        with (outdir / name).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    write("semantic_repair_basis.csv", summary,
          ["scope", "false_equivalences", "semantic_fields_allowed", "minimal_semantic_repair_size", "minimal_semantic_repair_sets", "num_minimal_semantic_repair_sets"])
    write("semantic_repair_field_coverage.csv", coverage,
          ["scope", "field", "false_equivalences_repaired_by_field", "fraction"])
    write("semantic_repair_examples.csv", examples,
          ["scope", "probe_id", "engine_i", "engine_j", "semantic_repair_fields", "sig_i_size", "sig_j_size"])
    print(f"Wrote semantic repair basis for {len(all_rows)} false equivalences across {len(METHODS)} projections")

if __name__ == "__main__":
    main()
