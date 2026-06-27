#!/usr/bin/env python3
"""Balanced false-portability rates for grounded contract maps.

Micro conditional rates can be dominated by engine pairs or probes that produce
many projected equivalences. This script reports macro-averaged rates over
engine pairs and over probes, using the same projection semantics as the main
conditional-trap analysis.
"""
from __future__ import annotations
import csv, json, itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAPS = ROOT / 'artifact/evaluation/grounded_contract_maps.jsonl'
OUT = ROOT / 'artifact/evaluation/grounded/balanced_false_portability.csv'
METHODS = ['keyword','yesno','operator_only']

def read_jsonl(path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def split_action(ak: str):
    parts = ak.split('|')
    while len(parts) < 7:
        parts.append('')
    return parts[:7]

def project_atom(atom, method):
    ak, st = atom
    op, kind, variant, layer, placement, decision_time, obs = split_action(ak)
    if method == 'keyword':
        if kind in {'delegate','pushdown','prune'}: return ('pushdown','yes')
        if kind == 'observe': return ('explain','yes')
        if kind == 'reorder': return ('join_order','yes')
        if kind == 'adapt': return ('adaptivity','yes')
        if kind in {'materialize','inline'}: return ('materialization','yes')
        if kind == 'estimate': return ('estimate','yes')
        return (kind or op, 'yes')
    if method == 'yesno':
        return (op, kind, 'yes')
    if method == 'operator_only':
        return (op, 'yes')
    raise ValueError(method)

def project_sig(sig, method):
    return frozenset(project_atom(a, method) for a in sig)

def safe_rate(false_eq, proj_eq):
    return false_eq / proj_eq if proj_eq else None

def main():
    maps = {}; engines=set(); probes=set()
    for r in read_jsonl(MAPS):
        e = r['engine']; p = r['probe_id']
        sig = frozenset((k,v) for k,v in r.get('actions', {}).items() if v != 'UNSPEC')
        maps[(e,p)] = sig; engines.add(e); probes.add(p)
    engines = sorted(engines); probes = sorted(probes)
    pairs = list(itertools.combinations(engines, 2))
    rows=[]
    proj_cache={}
    for method in METHODS:
        micro_proj = micro_false = 0
        pair_rates=[]; pair_nonzero=0; pair_false_positive=0
        probe_rates=[]; probe_nonzero=0; probe_false_positive=0
        # per-pair aggregates
        for e1,e2 in pairs:
            peq=feq=0
            for p in probes:
                s1 = maps.get((e1,p), frozenset()); s2 = maps.get((e2,p), frozenset())
                key1=(method,e1,p); key2=(method,e2,p)
                if key1 not in proj_cache: proj_cache[key1] = project_sig(s1, method)
                if key2 not in proj_cache: proj_cache[key2] = project_sig(s2, method)
                if proj_cache[key1] == proj_cache[key2]:
                    peq += 1
                    if s1 != s2: feq += 1
            micro_proj += peq; micro_false += feq
            if peq:
                pair_nonzero += 1
                pair_rates.append(feq/peq)
                if feq: pair_false_positive += 1
        # per-probe aggregates
        for p in probes:
            peq=feq=0
            for e1,e2 in pairs:
                s1 = maps.get((e1,p), frozenset()); s2 = maps.get((e2,p), frozenset())
                key1=(method,e1,p); key2=(method,e2,p)
                if key1 not in proj_cache: proj_cache[key1] = project_sig(s1, method)
                if key2 not in proj_cache: proj_cache[key2] = project_sig(s2, method)
                if proj_cache[key1] == proj_cache[key2]:
                    peq += 1
                    if s1 != s2: feq += 1
            if peq:
                probe_nonzero += 1
                probe_rates.append(feq/peq)
                if feq: probe_false_positive += 1
        def avg(xs): return sum(xs)/len(xs) if xs else 0.0
        rows.append({
            'projection': method,
            'declared_equivalences': micro_proj,
            'false_equivalences': micro_false,
            'micro_conditional_rate': f'{(micro_false/micro_proj if micro_proj else 0):.6f}',
            'engine_pair_macro_rate': f'{avg(pair_rates):.6f}',
            'engine_pairs_with_declared_equivalence': pair_nonzero,
            'engine_pairs_with_false_equivalence': pair_false_positive,
            'probe_macro_rate': f'{avg(probe_rates):.6f}',
            'probes_with_declared_equivalence': probe_nonzero,
            'probes_with_false_equivalence': probe_false_positive,
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f'Wrote {OUT}')

if __name__ == '__main__':
    main()
