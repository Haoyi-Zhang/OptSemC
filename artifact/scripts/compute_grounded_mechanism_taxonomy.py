#!/usr/bin/env python3
"""Classify false optimizer-portability witnesses into query-processing mechanisms.

This diagnostic complements field-level repair counts. It groups the semantic
fields that repair false equivalences into database-mechanism labels that are
usable in the paper narrative: operator-family confusion, source-placement
confusion, optimizer-layer confusion, decision-time/adaptivity confusion,
observability confusion, and modality confusion.
"""
from __future__ import annotations
import csv, itertools, json
from pathlib import Path
from collections import Counter, defaultdict

FIELDS = ["operator", "kind", "variant", "layer", "placement", "decision_time", "observability", "state"]
METHODS = ["keyword", "yesno", "operator_only"]
MECHANISM_MAP = {
    "operator": "operator-family",
    "kind": "action-kind",
    "variant": "action-variant",
    "layer": "optimizer-layer",
    "placement": "execution-placement",
    "decision_time": "decision-time",
    "observability": "plan-observability",
    "state": "contract-modality",
}


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
    return tuple({
        "operator": op,
        "kind": kind,
        "variant": variant,
        "layer": layer,
        "placement": placement,
        "decision_time": decision_time,
        "observability": observability,
        "state": state,
    }[f] for f in FIELDS)


def load_maps(path: Path):
    maps = {}
    engines, probes = set(), set()
    for row in read_jsonl(path):
        e, p = row["engine"], row["probe_id"]
        sig = frozenset(split_action(k, v) for k, v in row.get("actions", {}).items() if v != "UNSPEC")
        maps[(e, p)] = sig
        engines.add(e); probes.add(p)
    return maps, sorted(engines), sorted(probes)


def baseline_atom(atom, method):
    d = dict(zip(FIELDS, atom))
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


def false_rows(maps, engines, probes, method):
    for p in probes:
        for e1, e2 in itertools.combinations(engines, 2):
            s1 = maps.get((e1, p), frozenset())
            s2 = maps.get((e2, p), frozenset())
            if s1 == s2:
                continue
            if project(s1, method) == project(s2, method):
                yield (method, p, e1, e2, s1, s2)


def repair_fields(s1, s2, method):
    return [f for f in FIELDS if project(s1, method, [f]) != project(s2, method, [f])]


def first_examples(sig, limit=3):
    out=[]
    for a in sorted(sig)[:limit]:
        d=dict(zip(FIELDS,a))
        out.append(f"{d['operator']}:{d['kind']}:{d['variant']}:{d['layer']}:{d['placement']}:{d['decision_time']}:{d['observability']}:{d['state']}")
    return " | ".join(out)


def main():
    root = Path(__file__).resolve().parents[1]
    maps, engines, probes = load_maps(root / "evaluation" / "grounded_contract_maps.jsonl")
    outdir = root / "evaluation" / "grounded"
    outdir.mkdir(parents=True, exist_ok=True)

    mech_counts = Counter()
    mech_by_method = Counter()
    field_counts = Counter()
    examples = []
    total_by_method = Counter()
    for method in METHODS:
        for method, probe, e1, e2, s1, s2 in false_rows(maps, engines, probes, method):
            total_by_method[method] += 1
            fields = repair_fields(s1, s2, method)
            mechanisms = sorted({MECHANISM_MAP[f] for f in fields})
            for f in fields:
                field_counts[(method, f)] += 1
            for m in mechanisms:
                mech_counts[m] += 1
                mech_by_method[(method, m)] += 1
            if len(examples) < 80:
                examples.append({
                    "method": method,
                    "probe_id": probe,
                    "engine_i": e1,
                    "engine_j": e2,
                    "repair_fields": ";".join(fields),
                    "mechanisms": ";".join(mechanisms),
                    "left_examples": first_examples(s1),
                    "right_examples": first_examples(s2),
                })

    rows=[]
    for (method, mech), n in sorted(mech_by_method.items(), key=lambda kv:(kv[0][0], -kv[1], kv[0][1])):
        denom = total_by_method[method]
        rows.append({
            "method": method,
            "mechanism": mech,
            "false_equivalences_with_mechanism": n,
            "fraction_of_false_equivalences": f"{(n/denom if denom else 0):.6f}",
        })
    global_rows=[]
    total_all=sum(total_by_method.values())
    for mech, n in mech_counts.most_common():
        global_rows.append({
            "mechanism": mech,
            "false_equivalences_with_mechanism": n,
            "fraction_of_all_false_equivalences": f"{(n/total_all if total_all else 0):.6f}",
        })

    def write(path, rows, fields):
        with path.open("w", newline="", encoding="utf-8") as f:
            w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    write(outdir/"mechanism_taxonomy.csv", rows,
          ["method", "mechanism", "false_equivalences_with_mechanism", "fraction_of_false_equivalences"])
    write(outdir/"mechanism_taxonomy_global.csv", global_rows,
          ["mechanism", "false_equivalences_with_mechanism", "fraction_of_all_false_equivalences"])
    write(outdir/"mechanism_examples.csv", examples,
          ["method", "probe_id", "engine_i", "engine_j", "repair_fields", "mechanisms", "left_examples", "right_examples"])
    print(f"Wrote mechanism taxonomy for {total_all} false equivalences")

if __name__ == "__main__":
    main()
