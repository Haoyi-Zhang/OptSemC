#!/usr/bin/env python3
"""Compute projection-repair certificates for grounded OptSem-C contracts.

For each lossy projection, the script finds the smallest set of semantic
fields that, when restored to the projection, eliminates all observed false
equivalences in the grounded corpus. It also reports field participation and
pair-level repair diagnostics. This is intentionally corpus-dependent: the
corpus witnesses the failure, and the certificate states what repairs the
observed failure.
"""
from __future__ import annotations
import csv, itertools, json
from pathlib import Path
from collections import Counter, defaultdict

FIELDS = ["operator", "kind", "variant", "layer", "placement", "decision_time", "observability", "state"]
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
    return {
        "operator": op,
        "kind": kind,
        "variant": variant,
        "layer": layer,
        "placement": placement,
        "decision_time": decision_time,
        "observability": observability,
        "state": state,
    }


def atom(action_key: str, state: str):
    d = split_action(action_key, state)
    return tuple(d[f] for f in FIELDS)


def baseline_atom(a, method):
    d = dict(zip(FIELDS, a))
    op, kind, state = d["operator"], d["kind"], d["state"]
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
    extra_fields = tuple(extra_fields)
    idx = [FIELDS.index(f) for f in extra_fields]
    out = []
    for a in sig:
        base = baseline_atom(a, method)
        out.append(base + tuple(a[i] for i in idx))
    return frozenset(out)


def load_maps(path: Path):
    maps = {}
    engines, probes = set(), set()
    for row in read_jsonl(path):
        e, p = row["engine"], row["probe_id"]
        sig = frozenset(atom(k, v) for k, v in row.get("actions", {}).items() if v != "UNSPEC")
        maps[(e, p)] = sig
        engines.add(e); probes.add(p)
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
                rows.append((p, e1, e2, s1, s2))
    return rows


def fields_that_repair(s1, s2, method):
    return [f for f in FIELDS if project(s1, method, [f]) != project(s2, method, [f])]


def minimal_universal_repairs(rows, method):
    if not rows:
        return [()]
    for k in range(1, len(FIELDS)+1):
        good = []
        for sub in itertools.combinations(FIELDS, k):
            ok = True
            for _p, _e1, _e2, s1, s2 in rows:
                if project(s1, method, sub) == project(s2, method, sub):
                    ok = False; break
            if ok:
                good.append(sub)
        if good:
            return good
    return []


def main():
    root = Path(__file__).resolve().parents[1]
    maps_path = root/"evaluation"/"grounded_contract_maps.jsonl"
    outdir = root/"evaluation"/"grounded"
    maps, engines, probes = load_maps(maps_path)

    cert_rows = []
    field_rows = []
    hotspot_rows = []
    example_rows = []
    for method in METHODS:
        rows = false_equivalences(maps, engines, probes, method)
        reps = minimal_universal_repairs(rows, method)
        field_counter = Counter()
        pair_counter = Counter()
        pair_best_counter = Counter()
        for p, e1, e2, s1, s2 in rows:
            repair_fields = fields_that_repair(s1, s2, method)
            for f in repair_fields:
                field_counter[f] += 1
            pair = f"{e1}--{e2}"
            pair_counter[pair] += 1
            if repair_fields:
                pair_best_counter[(pair, repair_fields[0])] += 1
            if len(example_rows) < 100:
                example_rows.append({
                    "method": method,
                    "probe_id": p,
                    "engine_i": e1,
                    "engine_j": e2,
                    "repair_fields": ";".join(repair_fields),
                    "sig_i_size": len(s1),
                    "sig_j_size": len(s2),
                })
        total = len(rows)
        cert_rows.append({
            "method": method,
            "false_equivalences": total,
            "minimal_universal_repair_size": len(reps[0]) if reps else 0,
            "repair_sets": ";".join("+".join(r) for r in reps[:10]),
            "num_minimal_repair_sets": len(reps),
        })
        for f, n in field_counter.most_common():
            field_rows.append({
                "method": method,
                "field": f,
                "false_equivalences_repaired_by_field": n,
                "fraction": f"{(n/total if total else 0):.6f}",
            })
        for pair, n in pair_counter.most_common(30):
            best_field, best_n = "", 0
            for (pp, ff), cnt in pair_best_counter.items():
                if pp == pair and cnt > best_n:
                    best_field, best_n = ff, cnt
            hotspot_rows.append({
                "method": method,
                "engine_pair": pair,
                "false_equivalences": n,
                "dominant_repair_field": best_field,
                "dominant_repair_count": best_n,
            })

    def write(name, rows, fields):
        with (outdir/name).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader(); w.writerows(rows)
    write("repair_certificate_summary.csv", cert_rows,
          ["method","false_equivalences","minimal_universal_repair_size","repair_sets","num_minimal_repair_sets"])
    write("repair_field_coverage.csv", field_rows,
          ["method","field","false_equivalences_repaired_by_field","fraction"])
    write("repair_hotspots.csv", hotspot_rows,
          ["method","engine_pair","false_equivalences","dominant_repair_field","dominant_repair_count"])
    write("repair_certificate_examples.csv", example_rows,
          ["method","probe_id","engine_i","engine_j","repair_fields","sig_i_size","sig_j_size"])
    print(f"Wrote repair certificates for {sum(int(r['false_equivalences']) for r in cert_rows)} false equivalences")

if __name__ == "__main__":
    main()
