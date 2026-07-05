#!/usr/bin/env python3
"""Engine-pair holdout stress for repair certificates.

This complements probe-fold stability. For each coarse projection, it learns a
minimal semantic repair from false-equivalence witnesses excluding one engine
pair, and tests the repair on the held-out engine pair. This detects whether a
repair field only explains a single pair of engines. A failure is reported as a
boundary, not used as a transfer claim.
"""
from __future__ import annotations
import csv, itertools, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / 'evaluation' / 'grounded_contract_maps.jsonl'
OUTDIR = ROOT / 'evaluation' / 'grounded'
METHODS = ['keyword','yesno','operator_only']
FIELDS = ['operator','kind','layer','placement','decision_time','observability','state']
ALL_FIELDS = ['operator','kind','variant','layer','placement','decision_time','observability','state']

def read_jsonl(path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def split_action(action_key: str, state: str):
    parts = action_key.split('|')
    if len(parts) == 6:
        op, kind, layer, placement, time, obs = parts
        variant = ''
    else:
        parts = (parts + ['']*7)[:7]
        op, kind, variant, layer, placement, time, obs = parts
    return {'operator': op, 'kind': kind, 'variant': variant, 'layer': layer, 'placement': placement, 'decision_time': time, 'observability': obs, 'state': state}

def atom(action_key, state):
    d = split_action(action_key, state)
    return tuple(d[f] for f in ALL_FIELDS)

def baseline_atom(a, method):
    d = dict(zip(ALL_FIELDS, a))
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
    idx = [ALL_FIELDS.index(f) for f in extra_fields]
    return frozenset(baseline_atom(a, method) + tuple(a[i] for i in idx) for a in sig)

def load_maps():
    maps={}; engines=set(); probes=set()
    for r in read_jsonl(MAPS):
        e,p = r['engine'], r['probe_id']
        sig=frozenset(atom(k,v) for k,v in r.get('actions',{}).items() if v!='UNSPEC')
        maps[(e,p)] = sig
        engines.add(e); probes.add(p)
    return maps, sorted(engines), sorted(probes)

def false_equivalences(maps, engines, probes, method):
    rows=[]
    for p in probes:
        for e1,e2 in itertools.combinations(engines,2):
            s1=maps.get((e1,p), frozenset())
            s2=maps.get((e2,p), frozenset())
            if s1 == s2:
                continue
            if project(s1, method) == project(s2, method):
                pair = '--'.join([e1,e2])
                rows.append({'probe_id':p,'engine_i':e1,'engine_j':e2,'engine_pair':pair,'sig_i':s1,'sig_j':s2})
    return rows

def repair_resolves(row, method, fields):
    return project(row['sig_i'], method, fields) != project(row['sig_j'], method, fields)

def minimal_repairs(rows, method):
    if not rows:
        return [tuple()]
    for k in range(1, len(FIELDS)+1):
        good=[]
        for sub in itertools.combinations(FIELDS, k):
            if all(repair_resolves(r, method, sub) for r in rows):
                good.append(sub)
        if good:
            return good
    return []

def main():
    maps, engines, probes = load_maps()
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows_out=[]; summary=[]
    for method in METHODS:
        rows = false_equivalences(maps, engines, probes, method)
        pairs = sorted(set(r['engine_pair'] for r in rows))
        total_held=0; total_resolved=0; repairs=set(); unresolved=0; nonempty=0
        for pair in pairs:
            train=[r for r in rows if r['engine_pair'] != pair]
            test=[r for r in rows if r['engine_pair'] == pair]
            if not test:
                continue
            nonempty += 1
            reps = minimal_repairs(train, method)
            chosen = sorted(reps, key=lambda x:(len(x), '+'.join(x)))[0] if reps else tuple()
            resolved = sum(1 for r in test if repair_resolves(r, method, chosen))
            total_held += len(test); total_resolved += resolved; unresolved += len(test)-resolved
            repairs.add('+'.join(chosen) if chosen else 'none')
            rows_out.append({'method':method,'heldout_engine_pair':pair,'train_false_equivalences':len(train),'heldout_false_equivalences':len(test),'learned_repair_size':len(chosen),'learned_repair':'+'.join(chosen) if chosen else 'none','num_train_minimal_repairs':len(reps),'heldout_resolved':resolved,'heldout_unresolved':len(test)-resolved,'heldout_resolution_rate':f'{(resolved/len(test) if test else 1.0):.6f}'})
        summary.append({'method':method,'heldout_engine_pairs':nonempty,'heldout_false_equivalences':total_held,'heldout_resolved':total_resolved,'heldout_unresolved':unresolved,'heldout_resolution_rate':f'{(total_resolved/total_held if total_held else 1.0):.6f}','distinct_learned_repairs':';'.join(sorted(repairs))})
    with (OUTDIR/'repair_enginepair_generalization.csv').open('w', newline='', encoding='utf-8') as f:
        fields=['method','heldout_engine_pair','train_false_equivalences','heldout_false_equivalences','learned_repair_size','learned_repair','num_train_minimal_repairs','heldout_resolved','heldout_unresolved','heldout_resolution_rate']
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows_out)
    with (OUTDIR/'repair_enginepair_generalization_summary.csv').open('w', newline='', encoding='utf-8') as f:
        fields=['method','heldout_engine_pairs','heldout_false_equivalences','heldout_resolved','heldout_unresolved','heldout_resolution_rate','distinct_learned_repairs']
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(summary)
    print('Wrote engine-pair repair stress')

if __name__ == '__main__':
    main()
