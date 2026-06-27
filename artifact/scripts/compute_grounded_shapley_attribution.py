#!/usr/bin/env python3
"""Exact Shapley attribution for projection-induced false equivalences.

The implementation groups repeated signature pairs and memoizes projections so
that the check remains lightweight for the paper artifact. For a false
-equivalent pair, utility(S)=1 iff adding field subset S to the lossy projection
separates the two full contracts.
"""
from __future__ import annotations
import csv, itertools, json, math
from collections import Counter, defaultdict
from pathlib import Path

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
    return (op, kind, variant, layer, placement, decision_time, observability, state)


def baseline_atom(a, method):
    op, kind, variant, layer, placement, decision_time, observability, state = a
    if method == "keyword":
        if kind in {"delegate", "pushdown", "prune"}: return ("pushdown", "yes")
        if kind == "observe": return ("explain", "yes")
        if kind == "reorder": return ("join_order", "yes")
        if kind == "adapt": return ("adaptivity", "yes")
        if kind in {"materialize", "inline"}: return ("materialization", "yes")
        if kind == "choose": return ("choose", "yes")
        if kind == "fallback": return ("fallback", "yes")
        return (kind, "yes")
    if method == "yesno": return (op, kind, "yes")
    if method == "operator_only": return (op, "yes")
    raise ValueError(method)


def load_maps(path: Path):
    maps = {}
    engines, probes = set(), set()
    for row in read_jsonl(path):
        e, p = row["engine"], row["probe_id"]
        sig = frozenset(split_action(k, v) for k, v in row.get("actions", {}).items() if v != "UNSPEC")
        maps[(e, p)] = sig
        engines.add(e); probes.add(p)
    return maps, sorted(engines), sorted(probes)


def main():
    root = Path(__file__).resolve().parents[1]
    maps, engines, probes = load_maps(root / "evaluation" / "grounded_contract_maps.jsonl")
    outdir = root / "evaluation" / "grounded"
    field_index = {f:i for i, f in enumerate(FIELDS)}
    factorial = [math.factorial(i) for i in range(len(FIELDS)+1)]
    n = len(FIELDS)
    weights = {k: factorial[k] * factorial[n-k-1] / factorial[n] for k in range(n)}
    subset_masks = list(range(1 << n))
    mask_fields = {m: tuple(FIELDS[i] for i in range(n) if m & (1 << i)) for m in subset_masks}
    proj_cache = {}

    def project(sig, method, mask=0):
        key = (method, mask, sig)
        if key in proj_cache:
            return proj_cache[key]
        idx = [i for i in range(n) if mask & (1 << i)]
        out = frozenset(baseline_atom(a, method) + tuple(a[i] for i in idx) for a in sig)
        proj_cache[key] = out
        return out

    summary_rows = []
    example_rows = []
    for method in METHODS:
        pair_counts = Counter()
        for p in probes:
            for e1, e2 in itertools.combinations(engines, 2):
                s1 = maps.get((e1, p), frozenset())
                s2 = maps.get((e2, p), frozenset())
                if s1 == s2:
                    continue
                if project(s1, method, 0) == project(s2, method, 0):
                    pair_counts[(s1, s2)] += 1
                    if len(example_rows) < 20:
                        example_rows.append({"method": method, "probe_id": p, "engine_i": e1, "engine_j": e2, "top_fields": ""})
        accum = defaultdict(float)
        total = sum(pair_counts.values())
        for (s1, s2), count in pair_counts.items():
            # Utility cache over subsets for this pair.
            util = {}
            def v(mask):
                if mask not in util:
                    util[mask] = int(project(s1, method, mask) != project(s2, method, mask))
                return util[mask]
            phi = dict.fromkeys(FIELDS, 0.0)
            for fi, f in enumerate(FIELDS):
                bit = 1 << fi
                val = 0.0
                for mask in subset_masks:
                    if mask & bit:
                        continue
                    k = mask.bit_count()
                    val += weights[k] * (v(mask | bit) - v(mask))
                phi[f] = val
                accum[f] += count * val
        for f in FIELDS:
            summary_rows.append({
                "method": method,
                "field": f,
                "false_equivalences": total,
                "shapley_total": f"{accum[f]:.9f}",
                "shapley_mean": f"{(accum[f]/total if total else 0.0):.9f}",
                "share": f"{(accum[f]/total if total else 0.0):.9f}",
            })
    with (outdir / "semantic_field_shapley.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["method","field","false_equivalences","shapley_total","shapley_mean","share"])
        w.writeheader(); w.writerows(summary_rows)
    with (outdir / "semantic_field_shapley_examples.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["method","probe_id","engine_i","engine_j","top_fields"])
        w.writeheader(); w.writerows(example_rows)
    print(f"Wrote Shapley attribution for {len(summary_rows)} method-field rows")

if __name__ == "__main__":
    main()
