#!/usr/bin/env python3
"""Statistical robustness for grounded false-equivalence measurements.

The main trap metric is conditional: among equivalences declared by a lossy
projection, how many are false under full contracts? This script adds two
robustness views used in the paper:

1. Wilson binomial intervals over projected equivalence decisions.
2. Cluster bootstrap intervals that resample query probes rather than raw
   engine-pair comparisons, reducing dependence on repeated engine pairs.
3. Leave-one-engine-out sensitivity.
4. Strict-projection negative control.
"""
from __future__ import annotations
import argparse, csv, itertools, json, math, random
from collections import defaultdict
from pathlib import Path

METHODS = ["keyword", "yesno", "operator_only"]
NEGATIVE_METHOD = "strict"


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def split_action(ak: str):
    parts = ak.split("|")
    if len(parts) == 6:
        op, kind, layer, placement, decision_time, observability = parts
        variant = ""
    else:
        parts = (parts + [""] * 7)[:7]
        op, kind, variant, layer, placement, decision_time, observability = parts
    return op, kind, variant, layer, placement, decision_time, observability


def project_atom(atom, method: str):
    ak, st = atom
    if method == "strict":
        return atom
    op, kind, variant, layer, placement, decision_time, observability = split_action(ak)
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
        if kind == "estimate":
            return ("estimate", "yes")
        return (kind or op, "yes")
    if method == "yesno":
        return (op, kind, "yes")
    if method == "operator_only":
        return (op, "yes")
    raise ValueError(method)


def project_sig(sig, method: str):
    return frozenset(project_atom(atom, method) for atom in sig)


def load_maps(path: Path):
    maps = {}
    engines, probes = set(), set()
    for row in read_jsonl(path):
        e = row["engine"]
        p = row["probe_id"]
        sig = frozenset((k, v) for k, v in row.get("actions", {}).items() if v != "UNSPEC")
        maps[(e, p)] = sig
        engines.add(e)
        probes.add(p)
    return maps, sorted(engines), sorted(probes)


def counts_for(maps, engines, probes, method):
    pairs = list(itertools.combinations(engines, 2))
    projected_equiv = true_equiv = false_equiv = projected_diff = false_diff = 0
    # per-probe counts for cluster bootstrap
    by_probe = {}
    proj_cache = {}
    for p in probes:
        pe = te = fe = pd = fd = 0
        for e1, e2 in pairs:
            s1 = maps.get((e1, p), frozenset())
            s2 = maps.get((e2, p), frozenset())
            full_eq = s1 == s2
            k1, k2 = (method, e1, p), (method, e2, p)
            if k1 not in proj_cache:
                proj_cache[k1] = project_sig(s1, method)
            if k2 not in proj_cache:
                proj_cache[k2] = project_sig(s2, method)
            proj_eq = proj_cache[k1] == proj_cache[k2]
            if proj_eq:
                pe += 1
                if full_eq:
                    te += 1
                else:
                    fe += 1
            else:
                pd += 1
                if full_eq:
                    fd += 1
        by_probe[p] = (pe, te, fe, pd, fd)
        projected_equiv += pe
        true_equiv += te
        false_equiv += fe
        projected_diff += pd
        false_diff += fd
    return {
        "comparisons": len(pairs) * len(probes),
        "projected_equivalences": projected_equiv,
        "true_equivalences": true_equiv,
        "false_equivalences": false_equiv,
        "projected_differences": projected_diff,
        "false_differences": false_diff,
        "conditional_false_equivalence_rate": false_equiv / projected_equiv if projected_equiv else 0.0,
        "unconditional_false_equivalence_rate": false_equiv / (len(pairs) * len(probes)) if pairs and probes else 0.0,
        "projected_equivalence_rate": projected_equiv / (len(pairs) * len(probes)) if pairs and probes else 0.0,
        "by_probe": by_probe,
    }


def wilson_interval(k, n, z=1.96):
    if n <= 0:
        return 0.0, 0.0
    phat = k / n
    denom = 1 + z*z/n
    center = (phat + z*z/(2*n)) / denom
    half = (z * math.sqrt((phat*(1-phat) + z*z/(4*n))/n)) / denom
    return max(0.0, center-half), min(1.0, center+half)


def cluster_bootstrap(by_probe, n_boot=1000, seed=20260621):
    rng = random.Random(seed)
    probes = list(by_probe.keys())
    vals = []
    if not probes:
        return 0.0, 0.0, 0.0
    for _ in range(n_boot):
        pe = fe = 0
        for p in (rng.choice(probes) for _ in range(len(probes))):
            c = by_probe[p]
            pe += c[0]
            fe += c[2]
        vals.append(fe / pe if pe else 0.0)
    vals.sort()
    mean = sum(vals) / len(vals)
    lo = vals[int(0.025 * (len(vals)-1))]
    hi = vals[int(0.975 * (len(vals)-1))]
    return mean, lo, hi


def write_csv(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maps", type=Path, default=Path("artifact/evaluation/grounded_contract_maps.jsonl"))
    ap.add_argument("--out-dir", type=Path, default=Path("artifact/evaluation/grounded"))
    ap.add_argument("--boot", type=int, default=1000)
    args = ap.parse_args()
    maps, engines, probes = load_maps(args.maps)

    ci_rows = []
    for method in METHODS:
        c = counts_for(maps, engines, probes, method)
        lo, hi = wilson_interval(c["false_equivalences"], c["projected_equivalences"])
        bmean, blo, bhi = cluster_bootstrap(c["by_probe"], args.boot)
        ci_rows.append({
            "method": method,
            "projected_equivalences": c["projected_equivalences"],
            "false_equivalences": c["false_equivalences"],
            "conditional_rate": f"{c['conditional_false_equivalence_rate']:.6f}",
            "wilson_low": f"{lo:.6f}",
            "wilson_high": f"{hi:.6f}",
            "bootstrap_mean": f"{bmean:.6f}",
            "bootstrap_low": f"{blo:.6f}",
            "bootstrap_high": f"{bhi:.6f}",
            "bootstrap_clusters": len(probes),
            "bootstrap_replicates": args.boot,
        })
    write_csv(args.out_dir / "conditional_trap_confidence.csv", ci_rows,
              ["method", "projected_equivalences", "false_equivalences", "conditional_rate", "wilson_low", "wilson_high", "bootstrap_mean", "bootstrap_low", "bootstrap_high", "bootstrap_clusters", "bootstrap_replicates"])

    loo_rows = []
    for method in METHODS:
        for omitted in engines:
            keep = [e for e in engines if e != omitted]
            c = counts_for(maps, keep, probes, method)
            loo_rows.append({
                "method": method,
                "omitted_engine": omitted,
                "engines_remaining": len(keep),
                "comparisons": c["comparisons"],
                "projected_equivalences": c["projected_equivalences"],
                "false_equivalences": c["false_equivalences"],
                "conditional_rate": f"{c['conditional_false_equivalence_rate']:.6f}",
                "unconditional_rate": f"{c['unconditional_false_equivalence_rate']:.6f}",
            })
    write_csv(args.out_dir / "leave_one_engine_out.csv", loo_rows,
              ["method", "omitted_engine", "engines_remaining", "comparisons", "projected_equivalences", "false_equivalences", "conditional_rate", "unconditional_rate"])

    summary = []
    for method in METHODS:
        vals = [float(r["conditional_rate"]) for r in loo_rows if r["method"] == method]
        fes = [int(r["false_equivalences"]) for r in loo_rows if r["method"] == method]
        summary.append({
            "method": method,
            "leave_one_engine_runs": len(vals),
            "min_conditional_rate": f"{min(vals):.6f}" if vals else "0.000000",
            "max_conditional_rate": f"{max(vals):.6f}" if vals else "0.000000",
            "min_false_equivalences": min(fes) if fes else 0,
            "max_false_equivalences": max(fes) if fes else 0,
            "all_runs_have_false_equivalences": "true" if all(x > 0 for x in fes) else "false",
        })
    write_csv(args.out_dir / "leave_one_engine_summary.csv", summary,
              ["method", "leave_one_engine_runs", "min_conditional_rate", "max_conditional_rate", "min_false_equivalences", "max_false_equivalences", "all_runs_have_false_equivalences"])

    neg = counts_for(maps, engines, probes, NEGATIVE_METHOD)
    neg_rows = [{
        "projection": NEGATIVE_METHOD,
        "comparisons": neg["comparisons"],
        "projected_equivalences": neg["projected_equivalences"],
        "false_equivalences": neg["false_equivalences"],
        "expected_false_equivalences": 0,
        "passed": "true" if neg["false_equivalences"] == 0 else "false",
    }]
    write_csv(args.out_dir / "negative_control.csv", neg_rows,
              ["projection", "comparisons", "projected_equivalences", "false_equivalences", "expected_false_equivalences", "passed"])
    print("Wrote statistical robustness, leave-one-engine, and negative-control outputs")

if __name__ == "__main__":
    main()
