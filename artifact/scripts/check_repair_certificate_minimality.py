#!/usr/bin/env python3
"""Verify that reported repair certificates are exact for grounded contracts.

This check recomputes false-equivalence witnesses from grounded contract maps,
enumerates all candidate repair field subsets, and verifies that the reported
minimal repair certificates are not merely heuristic explanations. It also
checks the semantic-basis certificate that excludes action-variant labels.
"""
from __future__ import annotations
import csv, itertools, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = ROOT / 'evaluation' / 'grounded'
MAPS = ROOT / 'evaluation' / 'grounded_contract_maps.jsonl'
OUT = ROOT / 'evaluation' / 'repair_certificate_verification.csv'

FIELDS = ['operator','kind','variant','layer','placement','decision_time','observability','state']
SEM_FIELDS = ['operator','kind','layer','placement','decision_time','observability','state']
METHODS = ['keyword','yesno','operator_only']


def read_jsonl(path: Path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def split_action(action_key: str, state: str):
    parts = action_key.split('|')
    if len(parts) == 6:
        op, kind, layer, placement, decision_time, observability = parts
        variant = ''
    else:
        parts = (parts + [''] * 7)[:7]
        op, kind, variant, layer, placement, decision_time, observability = parts
    return {
        'operator': op, 'kind': kind, 'variant': variant, 'layer': layer,
        'placement': placement, 'decision_time': decision_time,
        'observability': observability, 'state': state,
    }

def atom(action_key: str, state: str):
    d = split_action(action_key, state)
    return tuple(d[f] for f in FIELDS)

def baseline_atom(a, method):
    d = dict(zip(FIELDS, a))
    op, kind = d['operator'], d['kind']
    if method == 'keyword':
        if kind in {'delegate','pushdown','prune'}:
            return ('pushdown','yes')
        if kind == 'observe':
            return ('explain','yes')
        if kind == 'reorder':
            return ('join_order','yes')
        if kind == 'adapt':
            return ('adaptivity','yes')
        if kind in {'materialize','inline'}:
            return ('materialization','yes')
        if kind == 'choose':
            return ('choose','yes')
        if kind == 'fallback':
            return ('fallback','yes')
        return (kind,'yes')
    if method == 'yesno':
        return (op, kind, 'yes')
    if method == 'operator_only':
        return (op, 'yes')
    raise ValueError(method)

def project(sig, method, extra_fields=()):
    extra_fields = tuple(extra_fields)
    idx = [FIELDS.index(f) for f in extra_fields]
    out = []
    for a in sig:
        base = baseline_atom(a, method)
        out.append(base + tuple(a[i] for i in idx))
    return frozenset(out)

def load_maps():
    maps = {}
    engines, probes = set(), set()
    for row in read_jsonl(MAPS):
        e, p = row['engine'], row['probe_id']
        sig = frozenset(atom(k, v) for k, v in row.get('actions', {}).items() if v != 'UNSPEC')
        maps[(e,p)] = sig
        engines.add(e); probes.add(p)
    return maps, sorted(engines), sorted(probes)

def false_equivalences(maps, engines, probes, method):
    rows = []
    for p in probes:
        for e1, e2 in itertools.combinations(engines, 2):
            s1 = maps.get((e1,p), frozenset())
            s2 = maps.get((e2,p), frozenset())
            if s1 == s2:
                continue
            if project(s1, method) == project(s2, method):
                rows.append((p, e1, e2, s1, s2))
    return rows

def repairs_all(rows, method, fields):
    return all(project(s1, method, fields) != project(s2, method, fields) for _p,_e1,_e2,s1,s2 in rows)

def minimal_sets(rows, method, fields):
    if not rows:
        return [()]
    for k in range(1, len(fields)+1):
        good = []
        for sub in itertools.combinations(fields, k):
            if repairs_all(rows, method, sub):
                good.append(sub)
        if good:
            return good
    return []

def parse_sets(s):
    if not s:
        return set()
    return {tuple(part.split('+')) for part in s.split(';') if part}

def main():
    maps, engines, probes = load_maps()
    cert = {r['method']: r for r in read_csv(G/'repair_certificate_summary.csv')}
    cond = {r['method']: r for r in read_csv(G/'conditional_trap_rate.csv')}
    sem = {r['scope']: r for r in read_csv(G/'semantic_repair_basis.csv')}
    out = []
    errors = []
    per_method_false = {}
    for method in METHODS:
        rows = false_equivalences(maps, engines, probes, method)
        per_method_false[method] = rows
        full_sets = minimal_sets(rows, method, FIELDS)
        reported = cert.get(method, {})
        reported_count = int(reported.get('false_equivalences', -1))
        cond_count = int(cond.get(method, {}).get('false_equivalences', -2))
        reported_min = int(reported.get('minimal_universal_repair_size', -1))
        reported_sets = parse_sets(reported.get('repair_sets',''))
        full_ok = (reported_count == len(rows) == cond_count and reported_min == len(full_sets[0]) and reported_sets.issubset(set(full_sets)))
        if not full_ok:
            errors.append(f'{method}: reported full repair certificate does not match recomputation')
        out.append({
            'scope': method,
            'field_universe': 'all_fields',
            'false_equivalences': len(rows),
            'reported_min_size': reported_min,
            'verified_min_size': len(full_sets[0]) if full_sets else 0,
            'verified_num_minimal_sets': len(full_sets),
            'reported_sets_are_minimal': str(reported_sets.issubset(set(full_sets))).lower(),
            'count_consistent': str(reported_count == len(rows) == cond_count).lower(),
            'passed': str(full_ok).lower(),
        })
        sem_sets = minimal_sets(rows, method, SEM_FIELDS)
        sem_reported = sem.get(method, {})
        sem_min = int(sem_reported.get('minimal_semantic_repair_size', -1))
        sem_reported_sets = parse_sets(sem_reported.get('minimal_semantic_repair_sets',''))
        sem_ok = (sem_min == len(sem_sets[0]) and sem_reported_sets.issubset(set(sem_sets)))
        if not sem_ok:
            errors.append(f'{method}: reported semantic repair basis does not match recomputation')
        out.append({
            'scope': method,
            'field_universe': 'semantic_fields_no_variant',
            'false_equivalences': len(rows),
            'reported_min_size': sem_min,
            'verified_min_size': len(sem_sets[0]) if sem_sets else 0,
            'verified_num_minimal_sets': len(sem_sets),
            'reported_sets_are_minimal': str(sem_reported_sets.issubset(set(sem_sets))).lower(),
            'count_consistent': 'true',
            'passed': str(sem_ok).lower(),
        })
    all_rows = [x for rows in per_method_false.values() for x in rows]
    sem_sets = minimal_sets(all_rows, 'keyword', SEM_FIELDS)  # cannot use one method for all rows? Need per-row method.
    # Recompute all-projections semantic basis with method attached.
    all_tagged = [(m, r) for m, rows in per_method_false.items() for r in rows]
    def repairs_all_tagged(fields):
        return all(project(s1, m, fields) != project(s2, m, fields) for m, (_p,_e1,_e2,s1,s2) in all_tagged)
    all_good = []
    for k in range(1, len(SEM_FIELDS)+1):
        for sub in itertools.combinations(SEM_FIELDS, k):
            if repairs_all_tagged(sub):
                all_good.append(sub)
        if all_good:
            break
    all_rep = sem.get('all_projections', {})
    all_rep_min = int(all_rep.get('minimal_semantic_repair_size', -1))
    all_rep_sets = parse_sets(all_rep.get('minimal_semantic_repair_sets',''))
    all_ok = (all_rep_min == len(all_good[0]) and all_rep_sets.issubset(set(all_good)))
    if not all_ok:
        errors.append('all_projections semantic repair basis does not match recomputation')
    out.append({
        'scope': 'all_projections',
        'field_universe': 'semantic_fields_no_variant',
        'false_equivalences': len(all_tagged),
        'reported_min_size': all_rep_min,
        'verified_min_size': len(all_good[0]) if all_good else 0,
        'verified_num_minimal_sets': len(all_good),
        'reported_sets_are_minimal': str(all_rep_sets.issubset(set(all_good))).lower(),
        'count_consistent': 'true',
        'passed': str(all_ok).lower(),
    })
    with OUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['scope','field_universe','false_equivalences','reported_min_size','verified_min_size','verified_num_minimal_sets','reported_sets_are_minimal','count_consistent','passed'])
        w.writeheader(); w.writerows(out)
    if errors:
        print('Repair certificate minimality check FAILED')
        for e in errors:
            print(e)
        sys.exit(1)
    print(f'Repair certificate minimality check passed: {len(out)} certificate families verified')

if __name__ == '__main__':
    main()
