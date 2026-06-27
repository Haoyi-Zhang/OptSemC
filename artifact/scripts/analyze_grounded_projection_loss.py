#!/usr/bin/env python3
"""Projection-loss diagnostics for grounded contract maps.

This version keeps only compact stable strings for compression accounting so the
analysis remains bounded after benchmark regeneration.
"""
from __future__ import annotations
import argparse, collections, csv, hashlib, itertools, json, statistics
from pathlib import Path

METHODS = ["keyword", "yesno", "operator_only", "no_placement", "no_decision_time", "no_observability", "no_modality"]
FIELD_NAMES = ["operator", "kind", "variant", "layer", "placement", "decision_time", "observability", "state"]


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def split_action(ak: str):
    p = ak.split("|")
    while len(p) < 7:
        p.append("")
    return p[:7]


def atom_tuple(atom):
    ak, st = atom
    return tuple(split_action(ak) + [st])


def project_atom(atom, method):
    ak, st = atom
    op, kind, variant, layer, placement, time, obs = split_action(ak)
    if method == "strict":
        return (op, kind, variant, layer, placement, time, obs, st)
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
    if method == "no_placement":
        return (op, kind, variant, layer, "_", time, obs, st)
    if method == "no_decision_time":
        return (op, kind, variant, layer, placement, "_", obs, st)
    if method == "no_observability":
        return (op, kind, variant, layer, placement, time, "_", st)
    if method == "no_modality":
        return (op, kind, variant, layer, placement, time, obs, "evidenced")
    raise ValueError(method)


def project_sig(sig, method):
    return frozenset(project_atom(a, method) for a in sig)


def stable_sig_id(sig):
    # Compact deterministic identity for a full signature.
    payload = json.dumps(sorted([list(x) for x in sig]), separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def diff_fields(sig1, sig2):
    fields = collections.Counter()
    atoms1 = [atom_tuple(a) for a in sig1]
    atoms2 = [atom_tuple(a) for a in sig2]
    if not atoms1 or not atoms2:
        return fields
    for a in atoms1:
        best = None; best_score = -1
        for b in atoms2:
            score = sum(1 for x, y in zip(a, b) if x == y)
            if score > best_score:
                best = b; best_score = score
        for name, x, y in zip(FIELD_NAMES, a, best):
            if x != y:
                fields[name] += 1
    return fields


def load_maps(path):
    maps = {}; engines = set(); probes = set()
    for r in read_jsonl(path):
        e = r['engine']; p = r['probe_id']
        sig = frozenset((k, v) for k, v in r.get('actions', {}).items() if v != 'UNSPEC')
        maps[(e, p)] = sig
        engines.add(e); probes.add(p)
    return maps, sorted(engines), sorted(probes)


def write_csv(path: Path, rows):
    if not rows:
        rows = [{'empty': 'true'}]
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--maps', default='artifact/evaluation/grounded_contract_maps.jsonl')
    ap.add_argument('--outdir', default='artifact/evaluation/grounded')
    args = ap.parse_args()
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    maps, engines, probes = load_maps(args.maps)
    pairs = list(itertools.combinations(engines, 2))
    total = len(pairs) * len(probes)
    rows = []; compression = []; field_counts = {m: collections.Counter() for m in METHODS}; example_rows = []
    # Per-method projected-signature cache avoids repeated projection work.
    full_id_cache = {k: stable_sig_id(v) for k, v in maps.items()}
    for m in METHODS:
        projected = {k: project_sig(v, m) for k, v in maps.items()}
        projected_equiv = false_equiv = true_equiv = projected_diff = false_diff = 0
        group_to_full_ids = collections.defaultdict(set)
        for p in probes:
            for e in engines:
                k = (e, p)
                ps = projected.get(k, frozenset())
                group_to_full_ids[(p, ps)].add(full_id_cache.get(k, 'EMPTY'))
            for e1, e2 in pairs:
                s1 = maps.get((e1, p), frozenset()); s2 = maps.get((e2, p), frozenset())
                full_eq = (s1 == s2)
                ps1 = projected.get((e1, p), frozenset()); ps2 = projected.get((e2, p), frozenset())
                if ps1 == ps2:
                    projected_equiv += 1
                    if full_eq:
                        true_equiv += 1
                    else:
                        false_equiv += 1
                        d = diff_fields(s1, s2)
                        field_counts[m].update(d)
                        if len(example_rows) < 200:
                            example_rows.append({
                                'method': m, 'probe_id': p, 'engine_i': e1, 'engine_j': e2,
                                'projected_signature_size': len(ps1), 'full_i_size': len(s1), 'full_j_size': len(s2),
                                'differing_fields': ';'.join(k for k, _ in d.most_common(6))
                            })
                else:
                    projected_diff += 1
                    if full_eq: false_diff += 1
        sizes = [len(v) for v in group_to_full_ids.values() if len(v) > 0]
        lossy = [x for x in sizes if x > 1]
        rows.append({
            'method': m, 'comparisons': total, 'projected_equivalences': projected_equiv,
            'true_equivalences': true_equiv, 'false_equivalences': false_equiv,
            'projected_differences': projected_diff, 'false_differences': false_diff,
            'unconditional_false_equivalence_rate': f'{false_equiv/total:.6f}',
            'conditional_false_equivalence_rate': f'{false_equiv/projected_equiv:.6f}' if projected_equiv else '0',
            'projected_equivalence_rate': f'{projected_equiv/total:.6f}',
        })
        compression.append({
            'method': m, 'projected_groups': len(sizes), 'lossy_groups': len(lossy),
            'lossy_group_rate': f'{len(lossy)/len(sizes):.6f}' if sizes else '0',
            'mean_full_signatures_per_projected_group': f'{statistics.mean(sizes):.6f}' if sizes else '0',
            'max_full_signatures_per_projected_group': max(sizes) if sizes else 0,
        })
    write_csv(outdir / 'projection_false_equivalence_analysis.csv', rows)
    write_csv(outdir / 'projection_compression.csv', compression)
    fc_rows = []
    for m, cnt in field_counts.items():
        total_counts = sum(cnt.values())
        for field, n in cnt.most_common():
            fc_rows.append({'method': m, 'field': field, 'count': n,
                            'fraction': f'{n/total_counts:.6f}' if total_counts else '0'})
    write_csv(outdir / 'projection_distinguishing_fields.csv', fc_rows or [{'method': 'none', 'field': 'none', 'count': 0, 'fraction': '0'}])
    write_csv(outdir / 'projection_false_equivalence_examples.csv', example_rows or [{'method': 'none', 'probe_id': '', 'engine_i': '', 'engine_j': '', 'projected_signature_size': 0, 'full_i_size': 0, 'full_j_size': 0, 'differing_fields': ''}])
    print('Wrote projection-loss diagnostics to', outdir)

if __name__ == '__main__':
    main()
