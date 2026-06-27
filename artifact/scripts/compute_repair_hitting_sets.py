#!/usr/bin/env python3
"""Compute exact repair lower bounds as finite hitting-set certificates.

The repair-certificate checker enumerates all field subsets directly.  This
script exposes the dual view used in the paper audit: for every false
projection witness, list the semantic fields that separate that witness and
compute the minimum field sets that hit every witness.  The output is a compact
reader-facing certificate that the repair fields are not chosen heuristically.
"""
from __future__ import annotations
import csv
import itertools
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / 'evaluation' / 'grounded_contract_maps.jsonl'
OUT = ROOT / 'evaluation' / 'grounded' / 'repair_hitting_sets.csv'
CHECK = ROOT / 'evaluation' / 'repair_hitting_set_check.csv'

FIELDS = ['operator','kind','variant','layer','placement','decision_time','observability','state']
SEM_FIELDS = ['operator','kind','layer','placement','decision_time','observability','state']
CORE_SEM_FIELDS = ['operator','layer','placement','decision_time','observability']
METHODS = ['keyword','yesno','operator_only']


def read_jsonl(path: Path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def split_action(action_key: str, state: str):
    parts = action_key.split('|')
    if len(parts) == 6:
        op, kind, layer, placement, decision_time, observability = parts
        variant = ''
    else:
        parts = (parts + [''] * 7)[:7]
        op, kind, variant, layer, placement, decision_time, observability = parts
    return {
        'operator': op,
        'kind': kind,
        'variant': variant,
        'layer': layer,
        'placement': placement,
        'decision_time': decision_time,
        'observability': observability,
        'state': state,
    }


def atom(action_key: str, state: str):
    d = split_action(action_key, state)
    return tuple(d[f] for f in FIELDS)


def baseline_atom(a, method: str):
    d = dict(zip(FIELDS, a))
    op, kind = d['operator'], d['kind']
    if method == 'keyword':
        if kind in {'delegate', 'pushdown', 'prune'}:
            return ('pushdown', 'yes')
        if kind == 'observe':
            return ('explain', 'yes')
        if kind == 'reorder':
            return ('join_order', 'yes')
        if kind == 'adapt':
            return ('adaptivity', 'yes')
        if kind in {'materialize', 'inline'}:
            return ('materialization', 'yes')
        if kind == 'choose':
            return ('choose', 'yes')
        if kind == 'fallback':
            return ('fallback', 'yes')
        return (kind, 'yes')
    if method == 'yesno':
        return (op, kind, 'yes')
    if method == 'operator_only':
        return (op, 'yes')
    raise ValueError(method)


def project(sig, method: str, extra_fields=()):
    extra_fields = tuple(extra_fields)
    idx = [FIELDS.index(f) for f in extra_fields]
    return frozenset(baseline_atom(a, method) + tuple(a[i] for i in idx) for a in sig)


def load_maps():
    maps, engines, probes = {}, set(), set()
    for row in read_jsonl(MAPS):
        e, p = row['engine'], row['probe_id']
        sig = frozenset(atom(k, v) for k, v in row.get('actions', {}).items() if v != 'UNSPEC')
        maps[(e, p)] = sig
        engines.add(e)
        probes.add(p)
    return maps, sorted(engines), sorted(probes)


def false_equivalences(maps, engines, probes, method: str):
    rows = []
    for p in probes:
        for e1, e2 in itertools.combinations(engines, 2):
            s1 = maps.get((e1, p), frozenset())
            s2 = maps.get((e2, p), frozenset())
            if s1 != s2 and project(s1, method) == project(s2, method):
                rows.append((method, p, e1, e2, s1, s2))
    return rows


def direct_repairs_all(rows, fields):
    return all(project(s1, method, fields) != project(s2, method, fields) for method, _p, _e1, _e2, s1, s2 in rows)


def singleton_separator_sets(rows, universe):
    out = []
    for method, _p, _e1, _e2, s1, s2 in rows:
        out.append(frozenset(f for f in universe if project(s1, method, [f]) != project(s2, method, [f])))
    return out


def minimum_hitting_sets(separator_sets, universe):
    if not separator_sets:
        return [()]
    for k in range(1, len(universe) + 1):
        good = []
        for sub in itertools.combinations(universe, k):
            s = set(sub)
            if all(s & sep for sep in separator_sets):
                good.append(sub)
        if good:
            return good
    return []


def minimum_direct_sets(rows, universe):
    if not rows:
        return [()]
    for k in range(1, len(universe) + 1):
        good = []
        for sub in itertools.combinations(universe, k):
            if direct_repairs_all(rows, sub):
                good.append(sub)
        if good:
            return good
    return []


def fmt_sets(sets, limit=12):
    return ';'.join('+'.join(s) for s in sets[:limit])


def row_for(scope, rows, universe_name, universe):
    seps = singleton_separator_sets(rows, universe)
    sizes = [len(s) for s in seps]
    min_hit = minimum_hitting_sets(seps, universe)
    min_direct = minimum_direct_sets(rows, universe)
    no_single = sum(1 for s in seps if not s)
    # For this grounded corpus the hitting-set view should be exactly equivalent
    # to direct projection repair.  If future data contain a witness that needs a
    # two-field interaction, this flag will fail and force the paper text to be
    # updated.
    hit_set = {tuple(s) for s in min_hit}
    direct_set = {tuple(s) for s in min_direct}
    equivalent = hit_set == direct_set
    return {
        'scope': scope,
        'field_universe': universe_name,
        'false_equivalences': len(rows),
        'no_singleton_separator_witnesses': no_single,
        'min_singleton_separator_fields': min(sizes) if sizes else 0,
        'max_singleton_separator_fields': max(sizes) if sizes else 0,
        'mean_singleton_separator_fields': f'{mean(sizes):.3f}' if sizes else '0.000',
        'minimum_hitting_set_size': len(min_hit[0]) if min_hit else -1,
        'num_minimum_hitting_sets': len(min_hit),
        'example_minimum_hitting_sets': fmt_sets(min_hit),
        'minimum_direct_repair_size': len(min_direct[0]) if min_direct else -1,
        'num_minimum_direct_repair_sets': len(min_direct),
        'hitting_equals_direct_repair': str(equivalent).lower(),
        'passed': str(no_single == 0 and equivalent).lower(),
    }


def main():
    maps, engines, probes = load_maps()
    per_method = {m: false_equivalences(maps, engines, probes, m) for m in METHODS}
    rows = []
    for method in METHODS:
        method_rows = per_method[method]
        rows.append(row_for(method, method_rows, 'all_fields', FIELDS))
        rows.append(row_for(method, method_rows, 'semantic_no_variant', SEM_FIELDS))
        rows.append(row_for(method, method_rows, 'core_semantic_state_free', CORE_SEM_FIELDS))
    all_rows = [r for method_rows in per_method.values() for r in method_rows]
    rows.append(row_for('all_projections', all_rows, 'semantic_no_variant', SEM_FIELDS))
    rows.append(row_for('all_projections', all_rows, 'core_semantic_state_free', CORE_SEM_FIELDS))

    fields = ['scope','field_universe','false_equivalences','no_singleton_separator_witnesses',
              'min_singleton_separator_fields','max_singleton_separator_fields','mean_singleton_separator_fields',
              'minimum_hitting_set_size','num_minimum_hitting_sets','example_minimum_hitting_sets',
              'minimum_direct_repair_size','num_minimum_direct_repair_sets','hitting_equals_direct_repair','passed']
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    check_rows = [
        {
            'check': 'repair_hitting_sets_match_direct_enumeration',
            'passed': str(all(r['passed'] == 'true' for r in rows)).lower(),
            'details': f'{sum(r["passed"] == "true" for r in rows)}/{len(rows)} rows passed',
        },
        {
            'check': 'all_grounded_witnesses_singleton_separable',
            'passed': str(all(int(r['no_singleton_separator_witnesses']) == 0 for r in rows)).lower(),
            'details': ';'.join(f"{r['scope']}:{r['field_universe']}={r['no_singleton_separator_witnesses']}" for r in rows),
        },
        {
            'check': 'layer_placement_is_core_two_field_basis',
            'passed': str(any(r['scope'] == 'all_projections' and r['field_universe'] == 'core_semantic_state_free' and 'layer+placement' in r['example_minimum_hitting_sets'] for r in rows)).lower(),
            'details': next((r['example_minimum_hitting_sets'] for r in rows if r['scope'] == 'all_projections' and r['field_universe'] == 'core_semantic_state_free'), ''),
        },
    ]
    CHECK.parent.mkdir(parents=True, exist_ok=True)
    with CHECK.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['check','passed','details'])
        w.writeheader()
        w.writerows(check_rows)

    ok = all(r['passed'] == 'true' for r in check_rows)
    print(f'Repair hitting-set certificates: {sum(r["passed"] == "true" for r in check_rows)}/{len(check_rows)} checks passed')
    if not ok:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
