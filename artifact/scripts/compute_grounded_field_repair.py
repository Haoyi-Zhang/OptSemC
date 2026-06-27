#!/usr/bin/env python3
"""Compute minimal semantic fields that repair false equivalences.

For every engine-pair/probe pair that a lossy projection declares equivalent
but full OptSem-C declares different, this script asks: what is the smallest
set of canonical-action fields that separates the two full contract maps?
This is stronger than counting differing fields; it identifies minimal repair
sets and quantifies which fields are necessary in practice.
"""
from __future__ import annotations
import argparse, csv, itertools, json, collections
from pathlib import Path

FIELDS = ["operator", "kind", "variant", "layer", "placement", "decision_time", "observability", "state"]
METHODS = ["keyword", "yesno", "operator_only"]

def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def split_action(ak: str):
    p = ak.split("|")
    if len(p) == 6:
        op, kind, layer, placement, time, obs = p
        variant = ""
    else:
        p = (p + [""] * 7)[:7]
        op, kind, variant, layer, placement, time, obs = p
    return {
        "operator": op, "kind": kind, "variant": variant, "layer": layer,
        "placement": placement, "decision_time": time, "observability": obs,
    }

def atom_fields(atom):
    ak, st = atom
    d = split_action(ak)
    d["state"] = st
    return d

def project(sig, fields):
    fields = tuple(fields)
    return frozenset(tuple(atom_fields(a).get(f, "") for f in fields) for a in sig)

def project_baseline_atom(atom, method):
    d = atom_fields(atom)
    op, kind = d["operator"], d["kind"]
    if method == "keyword":
        if kind in {"delegate", "pushdown", "prune"}: return ("pushdown", "yes")
        if kind == "observe": return ("explain", "yes")
        if kind == "reorder": return ("join_order", "yes")
        if kind == "adapt": return ("adaptivity", "yes")
        if kind in {"materialize", "inline"}: return ("materialization", "yes")
        if kind == "choose": return ("choose", "yes")
        if kind == "fallback": return ("fallback", "yes")
        return (kind, "yes")
    if method == "yesno":
        return (op, kind, "yes")
    if method == "operator_only":
        return (op, "yes")
    raise ValueError(method)

def project_baseline(sig, method):
    return frozenset(project_baseline_atom(a, method) for a in sig)

def load_maps(path):
    maps = {}; engines=set(); probes=set()
    for r in read_jsonl(path):
        e, p = r["engine"], r["probe_id"]
        sig = frozenset((k, v) for k, v in r.get("actions", {}).items() if v != "UNSPEC")
        maps[(e,p)] = sig; engines.add(e); probes.add(p)
    return maps, sorted(engines), sorted(probes)

def minimal_repair_sets(sig1, sig2):
    # Return all minimal subsets of FIELDS whose projection separates sig1/sig2.
    if sig1 == sig2:
        return []
    for k in range(1, len(FIELDS)+1):
        found=[]
        for sub in itertools.combinations(FIELDS, k):
            if project(sig1, sub) != project(sig2, sub):
                found.append(sub)
        if found:
            return found
    return []

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maps", default="artifact/evaluation/grounded_contract_maps.jsonl")
    ap.add_argument("--outdir", default="artifact/evaluation/grounded")
    args = ap.parse_args()
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    maps, engines, probes = load_maps(Path(args.maps))
    pairs = list(itertools.combinations(engines, 2))
    summary=[]; repair_rows=[]; example_rows=[]
    for method in METHODS:
        false_pairs=0; repair_counter=collections.Counter(); size_counter=collections.Counter(); field_counter=collections.Counter()
        for p in probes:
            for e1,e2 in pairs:
                s1 = maps.get((e1,p), frozenset()); s2 = maps.get((e2,p), frozenset())
                if s1 == s2:
                    continue
                if project_baseline(s1, method) != project_baseline(s2, method):
                    continue
                false_pairs += 1
                reps = minimal_repair_sets(s1, s2)
                if not reps:
                    continue
                min_size = len(reps[0]); size_counter[min_size] += 1
                # count all minimal repair alternatives, but for summary use canonical sorted string
                for rep in reps:
                    repair_counter["+".join(rep)] += 1
                    for f in rep:
                        field_counter[f] += 1
                if len(example_rows) < 100:
                    example_rows.append({
                        "method": method, "probe_id": p, "engine_i": e1, "engine_j": e2,
                        "minimal_size": min_size,
                        "repair_sets": ";".join("+".join(r) for r in reps[:10]),
                        "full_i_size": len(s1), "full_j_size": len(s2),
                    })
        total_rep = sum(repair_counter.values())
        for size, n in sorted(size_counter.items()):
            summary.append({"method": method, "view": "minimal_size", "key": str(size), "count": n, "fraction": f"{n/false_pairs:.6f}" if false_pairs else "0", "false_equivalences": false_pairs})
        for rep, n in repair_counter.most_common(20):
            repair_rows.append({"method": method, "repair_set": rep, "count": n, "fraction_of_repair_alternatives": f"{n/total_rep:.6f}" if total_rep else "0", "false_equivalences": false_pairs})
        for f, n in field_counter.most_common():
            summary.append({"method": method, "view": "field_participation", "key": f, "count": n, "fraction": f"{n/total_rep:.6f}" if total_rep else "0", "false_equivalences": false_pairs})
    def write(path, rows, fields=None):
        if not rows: rows=[{}]
        if fields is None: fields=list(rows[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    write(outdir/"field_repair_summary.csv", summary, ["method","view","key","count","fraction","false_equivalences"])
    write(outdir/"field_repair_sets.csv", repair_rows, ["method","repair_set","count","fraction_of_repair_alternatives","false_equivalences"])
    write(outdir/"field_repair_examples.csv", example_rows, ["method","probe_id","engine_i","engine_j","minimal_size","repair_sets","full_i_size","full_j_size"])
    print(f"Wrote minimal field repair analysis for {len(example_rows)} examples to {outdir}")

if __name__ == "__main__":
    main()
