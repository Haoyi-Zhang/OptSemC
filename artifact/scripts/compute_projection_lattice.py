#!/usr/bin/env python3
"""Exhaustive projection-lattice audit for grounded optimizer contracts."""
from __future__ import annotations
import csv, itertools, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / 'evaluation' / 'grounded_contract_maps.jsonl'
POINTS = ROOT / 'evaluation' / 'grounded' / 'projection_lattice_points.csv'
SUMMARY = ROOT / 'evaluation' / 'grounded' / 'projection_lattice_summary.csv'
FIELDS = ['operator','kind','variant','layer','placement','decision_time','observability','state']
METHODS = ['keyword','yesno','operator_only']
UNIVERSES = {
    'semantic_no_variant': ['operator','kind','layer','placement','decision_time','observability','state'],
    'core_semantic_state_free': ['operator','layer','placement','decision_time','observability'],
}

def read_jsonl(path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip(): yield json.loads(line)

def split_action(action_key, state):
    parts = action_key.split('|')
    if len(parts) == 6:
        op, kind, layer, placement, decision_time, observability = parts; variant = ''
    else:
        parts = (parts + [''] * 7)[:7]
        op, kind, variant, layer, placement, decision_time, observability = parts
    return (op, kind, variant, layer, placement, decision_time, observability, state)

def baseline_atom(atom, method):
    d = dict(zip(FIELDS, atom)); op, kind = d['operator'], d['kind']
    if method == 'keyword':
        if kind in {'delegate','pushdown','prune'}: return ('pushdown','yes')
        if kind == 'observe': return ('explain','yes')
        if kind == 'reorder': return ('join_order','yes')
        if kind == 'adapt': return ('adaptivity','yes')
        if kind in {'materialize','inline'}: return ('materialization','yes')
        if kind == 'choose': return ('choose','yes')
        if kind == 'fallback': return ('fallback','yes')
        return (kind,'yes')
    if method == 'yesno': return (op, kind, 'yes')
    if method == 'operator_only': return (op, 'yes')
    raise ValueError(method)

def project(sig, method, extra_fields=()):
    idx = tuple(FIELDS.index(f) for f in extra_fields)
    return frozenset(baseline_atom(a, method) + tuple(a[i] for i in idx) for a in sig)

def load_maps():
    maps, engines, probes = {}, set(), set()
    for row in read_jsonl(MAPS):
        sig = frozenset(split_action(a, s) for a, s in row.get('actions', {}).items() if s != 'UNSPEC')
        maps[(row['engine'], row['probe_id'])] = sig
        engines.add(row['engine']); probes.add(row['probe_id'])
    return maps, sorted(engines), sorted(probes)

def false_equivalences(maps, engines, probes, method):
    rows = []
    for p in probes:
        for e1, e2 in itertools.combinations(engines, 2):
            s1 = maps.get((e1,p), frozenset()); s2 = maps.get((e2,p), frozenset())
            if s1 != s2 and project(s1, method) == project(s2, method):
                rows.append((method, p, e1, e2, s1, s2))
    return rows

def powerset(items):
    items = tuple(items)
    for k in range(len(items) + 1): yield from itertools.combinations(items, k)

def false_remaining(rows, fields):
    return sum(1 for method, _p, _e1, _e2, s1, s2 in rows if project(s1, method, fields) == project(s2, method, fields))

def fmt(fields): return '+'.join(fields) if fields else 'EMPTY'

def minimal_safe_sets(safe, universe):
    safe = set(safe); out = []
    for sub in powerset(universe):
        if sub not in safe: continue
        if not any(set(other).issubset(sub) and set(other) != set(sub) for other in safe): out.append(sub)
    return out

def summarize(scope, universe_name, universe, rows):
    pts = []
    for sub in powerset(universe):
        rem = false_remaining(rows, sub)
        pts.append({'scope':scope,'field_universe':universe_name,'fields':fmt(sub),'field_count':len(sub),'false_remaining':rem,'safe':str(rem==0).lower()})
    safe = [tuple(r['fields'].split('+')) if r['fields']!='EMPTY' else tuple() for r in pts if r['safe']=='true']
    mins = minimal_safe_sets(safe, universe)
    unsafe = [r for r in pts if r['safe']=='false']
    max_unsafe_size = max((int(r['field_count']) for r in unsafe), default=-1)
    max_unsafe = [r['fields'] for r in unsafe if int(r['field_count']) == max_unsafe_size]
    summ = {'scope':scope,'field_universe':universe_name,'baseline_false_equivalences':len(rows),'total_subsets':len(pts),
            'safe_subsets':sum(r['safe']=='true' for r in pts),'unsafe_subsets':sum(r['safe']=='false' for r in pts),
            'minimum_safe_size':len(mins[0]) if mins else -1,'num_minimum_safe_sets':len(mins),
            'example_minimum_safe_sets':';'.join(fmt(s) for s in mins[:12]),
            'maximum_unsafe_size':max_unsafe_size,'example_maximum_unsafe_sets':';'.join(max_unsafe[:12])}
    return pts, summ

def main():
    maps, engines, probes = load_maps()
    per = {m:false_equivalences(maps, engines, probes, m) for m in METHODS}
    all_rows = [r for rs in per.values() for r in rs]
    all_points, summaries = [], []
    for scope, rows in list(per.items()) + [('all_projections', all_rows)]:
        for uname, universe in UNIVERSES.items():
            pts, summ = summarize(scope, uname, universe, rows)
            all_points.extend(pts); summaries.append(summ)
    POINTS.parent.mkdir(parents=True, exist_ok=True)
    with POINTS.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=['scope','field_universe','fields','field_count','false_remaining','safe']); w.writeheader(); w.writerows(all_points)
    with SUMMARY.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=['scope','field_universe','baseline_false_equivalences','total_subsets','safe_subsets','unsafe_subsets','minimum_safe_size','num_minimum_safe_sets','example_minimum_safe_sets','maximum_unsafe_size','example_maximum_unsafe_sets']); w.writeheader(); w.writerows(summaries)
    print(f'Projection lattice: {len(summaries)} summaries, {len(all_points)} lattice points')
if __name__ == '__main__': main()
