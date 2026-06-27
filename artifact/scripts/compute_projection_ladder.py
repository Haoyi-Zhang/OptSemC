#!/usr/bin/env python3
"""Compute projection ladders efficiently by grouping signatures per probe."""
from __future__ import annotations
import csv, json, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT/'evaluation/grounded_contract_maps.jsonl'
OUT = ROOT/'evaluation/grounded/projection_ladder.csv'

def read_jsonl(path):
    with path.open() as f:
        for line in f:
            if line.strip(): yield json.loads(line)

def split_action(ak):
    parts=ak.split('|')
    if len(parts)==6:
        op,kind,layer,placement,time,obs=parts; variant=''
    else:
        parts=(parts+['']*7)[:7]
        op,kind,variant,layer,placement,time,obs=parts
    return {'operator':op,'kind':kind,'variant':variant,'layer':layer,'placement':placement,'decision_time':time,'observability':obs}

def keyword_label(kind):
    if kind in {'delegate','pushdown','prune'}: return 'pushdown'
    if kind == 'observe': return 'explain'
    if kind == 'reorder': return 'join_order'
    if kind == 'adapt': return 'adaptivity'
    if kind in {'materialize','inline'}: return 'materialization'
    if kind == 'choose': return 'choose'
    if kind == 'fallback': return 'fallback'
    return kind

def project_atom(atom, base, added):
    ak, st = atom
    fields=split_action(ak)
    if base=='keyword': vals=[('label',keyword_label(fields['kind']))]
    elif base=='yesno': vals=[('operator',fields['operator']),('kind',fields['kind'])]
    elif base=='operator_only': vals=[('operator',fields['operator'])]
    else: raise ValueError(base)
    for f in added:
        vals.append((f, st if f=='state' else fields[f]))
    return tuple(vals)

def project_sig(sig, base, added):
    return frozenset(project_atom(a,base,added) for a in sig)

def nC2(n): return n*(n-1)//2

def load_by_probe():
    raw=collections.defaultdict(dict); engines=set(); probes=set()
    for r in read_jsonl(MAPS):
        sig=frozenset((k,v) for k,v in r.get('actions',{}).items() if v!='UNSPEC')
        raw[r['probe_id']][r['engine']] = sig
        engines.add(r['engine']); probes.add(r['probe_id'])
    # Include empty signatures for engine/probe pairs without applicable public-contract actions,
    # matching the conditional false-equivalence denominator.
    by_probe={}
    engines=sorted(engines)
    for p in sorted(probes):
        by_probe[p]=[(e, raw[p].get(e, frozenset())) for e in engines]
    return by_probe, engines

def evaluate(base, added, by_probe, n_engines):
    total = len(by_probe) * nC2(n_engines)
    projected_equiv = 0
    true_equiv = 0
    for probe, items in by_probe.items():
        groups=collections.defaultdict(list)
        for e, full_sig in items:
            psig=project_sig(full_sig,base,added)
            groups[psig].append(full_sig)
        for fsigs in groups.values():
            n=len(fsigs)
            if n<2: continue
            projected_equiv += nC2(n)
            # true equivalence within each projected group: same full signature
            fc=collections.Counter(fsigs)
            true_equiv += sum(nC2(c) for c in fc.values() if c>1)
    false_equiv=projected_equiv-true_equiv
    return {
        'projection':base,
        'added_fields': '+'.join(added) if added else '<none>',
        'comparisons': total,
        'projected_equivalences': projected_equiv,
        'false_equivalences': false_equiv,
        'conditional_false_equivalence_rate': round(false_equiv/projected_equiv,6) if projected_equiv else 0.0,
    }

def main():
    by_probe, engines = load_by_probe()
    configs=[]
    for base in ['keyword','yesno','operator_only']:
        configs.append((base,[]))
        for f in ['operator','kind','variant','layer','placement','decision_time','observability','state']:
            if base=='operator_only' and f=='operator': continue
            if base=='yesno' and f in {'operator','kind'}: continue
            configs.append((base,[f]))
        configs.append((base,['layer','placement']))
        configs.append((base,['layer','placement','state']))
        configs.append((base,['operator','layer','placement']))
    rows=[evaluate(base,added,by_probe,len(engines)) for base,added in configs]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f'Wrote {OUT} with {len(rows)} rows')
if __name__=='__main__': main()
