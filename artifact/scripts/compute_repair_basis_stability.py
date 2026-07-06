#!/usr/bin/env python3
"""Evaluate stable semantic repair bases across probes and engine pairs.

The universal repair certificate says a field set repairs all observed false
comparison validity. This script checks a stricter reader-facing property: a fixed,
interpretable semantic basis resolves false equivalences under both probe-level
and engine-pair-level partitions. The basis deliberately excludes action
variants and uses query-processing fields only.
"""
from __future__ import annotations
import csv, hashlib, itertools, json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / 'evaluation' / 'grounded_contract_maps.jsonl'
OUTDIR = ROOT / 'evaluation' / 'grounded'
FIELDS = ['operator','kind','variant','layer','placement','decision_time','observability','state']
METHODS = ['keyword','yesno','operator_only']
# A small semantic basis that avoids fine-grained action-variant labels.
# It captures where in the optimizer pipeline the behavior belongs and where
# execution is placed.
BASIS_NAME = 'layer+placement'
BASIS = ('layer','placement')


def read_jsonl(path: Path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def split_action(key: str, state: str):
    parts = key.split('|')
    if len(parts) == 6:
        op, kind, layer, placement, time, obs = parts
        variant = ''
    else:
        parts = (parts + [''] * 7)[:7]
        op, kind, variant, layer, placement, time, obs = parts
    d = {'operator': op, 'kind': kind, 'variant': variant, 'layer': layer,
         'placement': placement, 'decision_time': time, 'observability': obs,
         'state': state}
    return tuple(d[f] for f in FIELDS)


def baseline_atom(a, method):
    d = dict(zip(FIELDS, a)); op = d['operator']; kind = d['kind']
    if method == 'keyword':
        if kind in {'delegate','pushdown','prune'}:
            return ('pushdown','yes')
        if kind == 'observe': return ('explain','yes')
        if kind == 'reorder': return ('join_order','yes')
        if kind == 'adapt': return ('adaptivity','yes')
        if kind in {'materialize','inline'}: return ('materialization','yes')
        if kind == 'choose': return ('choose','yes')
        if kind == 'fallback': return ('fallback','yes')
        return (kind,'yes')
    if method == 'yesno':
        return (op, kind, 'yes')
    if method == 'operator_only':
        return (op, 'yes')
    raise ValueError(method)


def project(sig, method, extra_fields=()):
    idx = [FIELDS.index(f) for f in extra_fields]
    return frozenset(baseline_atom(a, method) + tuple(a[i] for i in idx) for a in sig)


def load_maps():
    maps = {}; engines = set(); probes = set()
    for row in read_jsonl(MAPS):
        e, p = row['engine'], row['probe_id']
        sig = frozenset(split_action(k, v) for k, v in row.get('actions', {}).items() if v != 'UNSPEC')
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
                rows.append({'method': method, 'probe_id': p, 'engine_i': e1, 'engine_j': e2,
                             'engine_pair': '--'.join([e1, e2]), 'sig_i': s1, 'sig_j': s2})
    return rows


def resolves(row, fields=BASIS):
    return project(row['sig_i'], row['method'], fields) != project(row['sig_j'], row['method'], fields)


def fold_id(probe_id: str, folds: int = 10):
    # Probe IDs are P0001-like; keep deterministic grouping.
    try:
        n = int(''.join(ch for ch in probe_id if ch.isdigit()))
    except ValueError:
        n = int(hashlib.sha256(probe_id.encode('utf-8')).hexdigest()[:12], 16)
    return n % folds


def main():
    maps, engines, probes = load_maps()
    OUTDIR.mkdir(parents=True, exist_ok=True)
    summary = []
    by_pair_rows = []
    by_fold_rows = []
    all_rows = []
    for method in METHODS:
        rows = false_equivalences(maps, engines, probes, method)
        all_rows.extend(rows)
        total = len(rows)
        resolved = sum(1 for r in rows if resolves(r))
        summary.append({'scope': method, 'basis': BASIS_NAME, 'false_equivalences': total,
                        'resolved': resolved, 'unresolved': total - resolved,
                        'resolution_rate': f'{(resolved/total if total else 1.0):.6f}'})
        for pair in sorted(set(r['engine_pair'] for r in rows)):
            prs = [r for r in rows if r['engine_pair'] == pair]
            res = sum(1 for r in prs if resolves(r))
            by_pair_rows.append({'method': method, 'engine_pair': pair, 'basis': BASIS_NAME,
                                 'false_equivalences': len(prs), 'resolved': res,
                                 'unresolved': len(prs)-res,
                                 'resolution_rate': f'{(res/len(prs) if prs else 1.0):.6f}'})
        for f in range(10):
            frs = [r for r in rows if fold_id(r['probe_id']) == f]
            res = sum(1 for r in frs if resolves(r))
            by_fold_rows.append({'method': method, 'fold': f, 'basis': BASIS_NAME,
                                 'false_equivalences': len(frs), 'resolved': res,
                                 'unresolved': len(frs)-res,
                                 'resolution_rate': f'{(res/len(frs) if frs else 1.0):.6f}'})
    total = len(all_rows); resolved = sum(1 for r in all_rows if resolves(r))
    summary.append({'scope': 'all_projections', 'basis': BASIS_NAME,
                    'false_equivalences': total, 'resolved': resolved, 'unresolved': total-resolved,
                    'resolution_rate': f'{(resolved/total if total else 1.0):.6f}'})

    def write(name, rows, fields):
        with (OUTDIR / name).open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    write('repair_basis_stability.csv', summary,
          ['scope','basis','false_equivalences','resolved','unresolved','resolution_rate'])
    write('repair_basis_enginepair.csv', by_pair_rows,
          ['method','engine_pair','basis','false_equivalences','resolved','unresolved','resolution_rate'])
    write('repair_basis_probe_folds.csv', by_fold_rows,
          ['method','fold','basis','false_equivalences','resolved','unresolved','resolution_rate'])
    print(f'Wrote repair-basis stability with {resolved}/{total} total resolved by {BASIS_NAME}')

if __name__ == '__main__':
    main()
