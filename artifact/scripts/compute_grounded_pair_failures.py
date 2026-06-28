#!/usr/bin/env python3
"""Engine-pair decomposition of grounded false equivalence."""
from __future__ import annotations
import argparse, csv, itertools, json
from collections import defaultdict
from pathlib import Path

METHODS = ["keyword", "yesno", "operator_only"]


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def split_action(ak):
    parts = ak.split("|")
    while len(parts) < 7:
        parts.append("")
    return parts[:7]


def project_atom(atom, method):
    ak, st = atom
    op, kind, variant, layer, placement, decision_time, observability = split_action(ak)
    if method == "keyword":
        if kind in {"delegate", "pushdown", "prune"}: label = "pushdown"
        elif kind == "observe": label = "explain"
        elif kind == "reorder": label = "join_order"
        elif kind == "adapt": label = "adaptivity"
        elif kind in {"materialize", "inline"}: label = "materialization"
        elif kind == "estimate": label = "estimate"
        else: label = kind or op
        return (label, "yes")
    if method == "yesno":
        return (op, kind, "yes")
    if method == "operator_only":
        return (op, "yes")
    raise ValueError(method)


def project_sig(sig, method):
    return frozenset(project_atom(a, method) for a in sig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maps", type=Path, default=Path("artifact/evaluation/grounded_contract_maps.jsonl"))
    ap.add_argument("--out", type=Path, default=Path("artifact/evaluation/grounded/pair_false_equivalence.csv"))
    args = ap.parse_args()
    maps = {}; engines = set(); probes = set()
    for r in read_jsonl(args.maps):
        e = r["engine"]; p = r["probe_id"]
        sig = frozenset((k,v) for k,v in r.get("actions", {}).items() if v != "UNSPEC")
        maps[(e,p)] = sig; engines.add(e); probes.add(p)
    engines = sorted(engines); probes = sorted(probes)
    rows = []
    for method in METHODS:
        for e1,e2 in itertools.combinations(engines,2):
            projected_equiv = false_equiv = true_equiv = 0
            for p in probes:
                s1 = maps.get((e1,p), frozenset()); s2 = maps.get((e2,p), frozenset())
                if project_sig(s1, method) == project_sig(s2, method):
                    projected_equiv += 1
                    if s1 == s2: true_equiv += 1
                    else: false_equiv += 1
            rows.append({
                "method": method,
                "engine_pair": f"{e1}--{e2}",
                "projected_equivalences": projected_equiv,
                "true_equivalences": true_equiv,
                "false_equivalences": false_equiv,
                "conditional_false_equivalence_rate": f"{false_equiv/projected_equiv:.6f}" if projected_equiv else "0.000000",
            })
    rows.sort(key=lambda r: (r["method"], -int(r["false_equivalences"]), r["engine_pair"]))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
