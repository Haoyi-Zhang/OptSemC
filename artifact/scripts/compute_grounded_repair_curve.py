#!/usr/bin/env python3
"""Greedy semantic-repair curve for grounded public optimizer contracts.

Given a lossy baseline projection, this analysis asks which contract fields
must be restored to eliminate false equivalences.  It is deliberately
projection-agnostic: the baseline can be keyword, yes/no, or operator-only;
the algorithm greedily adds the remaining action fields that most reduce
false equivalence under the full contract semantics.
"""
from __future__ import annotations
import argparse, csv, itertools, json
from pathlib import Path
from typing import FrozenSet, Iterable, Tuple

FIELDS = ["operator", "kind", "variant", "layer", "placement", "decision_time", "observability", "state"]
METHOD_BASE = {
    "keyword": [],
    "yesno": ["operator", "kind"],
    "operator_only": ["operator"],
}
METHOD_CANDIDATES = {
    "keyword": FIELDS,
    "yesno": [f for f in FIELDS if f not in {"operator", "kind"}],
    "operator_only": [f for f in FIELDS if f != "operator"],
}


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def split_action(action_key: str) -> dict:
    parts = action_key.split("|")
    while len(parts) < 7:
        parts.append("")
    op, kind, variant, layer, placement, decision_time, observability = parts[:7]
    return {
        "operator": op,
        "kind": kind,
        "variant": variant,
        "layer": layer,
        "placement": placement,
        "decision_time": decision_time,
        "observability": observability,
    }


def coarse_keyword(fields: dict) -> str:
    kind = fields["kind"]
    if kind in {"delegate", "pushdown", "prune"}:
        return "pushdown"
    if kind == "observe":
        return "explain"
    if kind == "reorder":
        return "join_order"
    if kind == "adapt":
        return "adaptivity"
    if kind in {"materialize", "inline"}:
        return "materialization"
    if kind == "estimate":
        return "estimate"
    return kind or fields["operator"]


def project_atom(atom: Tuple[str, str], method: str, extra_fields: Tuple[str, ...]) -> Tuple[str, ...]:
    action_key, state = atom
    f = split_action(action_key)
    f["state"] = state
    if method == "keyword":
        base = ["keyword", coarse_keyword(f)]
    elif method == "yesno":
        base = ["yesno", f["operator"], f["kind"]]
    elif method == "operator_only":
        base = ["operator", f["operator"]]
    else:
        raise ValueError(method)
    return tuple(base + [f[x] for x in extra_fields])


def project_signature(sig: FrozenSet[Tuple[str, str]], method: str, extra_fields: Tuple[str, ...]) -> FrozenSet[Tuple[str, ...]]:
    return frozenset(project_atom(a, method, extra_fields) for a in sig)


def load_maps(path: Path):
    maps = {}
    engines = set(); probes = set()
    for row in read_jsonl(path):
        e = row["engine"]; p = row["probe_id"]
        sig = frozenset((k, v) for k, v in row.get("actions", {}).items() if v != "UNSPEC")
        maps[(e, p)] = sig
        engines.add(e); probes.add(p)
    return maps, sorted(engines), sorted(probes)


def count_false_equiv(full_sigs, engines, probes, method: str, extra_fields: Tuple[str, ...]):
    pairs = list(itertools.combinations(engines, 2))
    projected_equiv = true_equiv = false_equiv = 0
    cache = {}
    for p in probes:
        for e in engines:
            sig = full_sigs.get((e, p), frozenset())
            cache[(e, p)] = project_signature(sig, method, extra_fields)
        for e1, e2 in pairs:
            s1 = full_sigs.get((e1, p), frozenset())
            s2 = full_sigs.get((e2, p), frozenset())
            if cache[(e1, p)] == cache[(e2, p)]:
                projected_equiv += 1
                if s1 == s2:
                    true_equiv += 1
                else:
                    false_equiv += 1
    total = len(pairs) * len(probes)
    return {
        "comparisons": total,
        "projected_equivalences": projected_equiv,
        "true_equivalences": true_equiv,
        "false_equivalences": false_equiv,
        "conditional_false_equivalence_rate": false_equiv / projected_equiv if projected_equiv else 0.0,
    }


def greedy_curve(full_sigs, engines, probes, method: str):
    used = []
    remaining = list(METHOD_CANDIDATES[method])
    rows = []
    base = count_false_equiv(full_sigs, engines, probes, method, tuple(used))
    initial_false = base["false_equivalences"] or 1
    rows.append({
        "method": method,
        "step": 0,
        "added_field": "baseline",
        "fields_used": "+".join(used) if used else "baseline",
        **base,
        "false_equivalence_repaired": 0.0,
    })
    step = 0
    while remaining:
        best = None
        for field in remaining:
            trial_fields = tuple(used + [field])
            res = count_false_equiv(full_sigs, engines, probes, method, trial_fields)
            key = (res["false_equivalences"], res["projected_equivalences"], field)
            if best is None or key < best[0]:
                best = (key, field, res)
        _, field, res = best
        used.append(field); remaining.remove(field); step += 1
        rows.append({
            "method": method,
            "step": step,
            "added_field": field,
            "fields_used": "+".join(used),
            **res,
            "false_equivalence_repaired": 1 - (res["false_equivalences"] / initial_false),
        })
        if res["false_equivalences"] == 0:
            break
    return rows


def write_csv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        fields = list(rows[0].keys())
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maps", type=Path, default=Path("artifact/evaluation/grounded_contract_maps.jsonl"))
    ap.add_argument("--out", type=Path, default=Path("artifact/evaluation/grounded/semantic_repair_curve.csv"))
    args = ap.parse_args()
    full_sigs, engines, probes = load_maps(args.maps)
    rows = []
    for method in ["keyword", "yesno", "operator_only"]:
        rows.extend(greedy_curve(full_sigs, engines, probes, method))
    # Round floats for stable paper output.
    for r in rows:
        r["conditional_false_equivalence_rate"] = f"{r['conditional_false_equivalence_rate']:.6f}"
        r["false_equivalence_repaired"] = f"{r['false_equivalence_repaired']:.6f}"
    write_csv(args.out, rows)
    print(f"Wrote {args.out} with {len(rows)} repair-curve rows")


if __name__ == "__main__":
    main()
