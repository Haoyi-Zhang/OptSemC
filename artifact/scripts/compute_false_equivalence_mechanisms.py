#!/usr/bin/env python3
"""Classify false optimizer-portability witnesses by semantic mechanism.

The projection-loss metric says that a lossy projection declared two contracts
portable when their full contracts differ.  This script explains *why* each
false equivalence occurs by mapping differing action fields to query-processing
mechanisms: operator family, placement, layer, decision time, observability,
modality, and action variant.
"""
from __future__ import annotations
import argparse, csv, json, itertools, collections
from pathlib import Path

METHODS = ["keyword", "yesno", "operator_only"]
FIELDS = ["operator", "kind", "variant", "layer", "placement", "decision_time", "observability", "state"]
MECHANISM = {
    "operator": "operator-family collision",
    "kind": "action-kind collision",
    "variant": "action-variant collision",
    "layer": "optimizer-layer collision",
    "placement": "execution-placement collision",
    "decision_time": "decision-time collision",
    "observability": "plan-evidence collision",
    "state": "modality collision",
}

def split_action(ak: str):
    p = ak.split('|')
    while len(p) < 7: p.append('')
    return p[:7]

def atom_tuple(atom):
    ak, st = atom
    return tuple(split_action(ak)+[st])

def read_jsonl(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.strip(): yield json.loads(line)

def load_maps(path):
    maps={}; engines=set(); probes=set()
    for r in read_jsonl(path):
        sig=frozenset((k,v) for k,v in r.get('actions',{}).items() if v!='UNSPEC')
        maps[(r['engine'], r['probe_id'])]=sig
        engines.add(r['engine']); probes.add(r['probe_id'])
    return maps, sorted(engines), sorted(probes)

def project_atom(atom, method):
    ak, st = atom
    op, kind, variant, layer, placement, time, obs = split_action(ak)
    if method == 'keyword':
        if kind in {'delegate','pushdown','prune'}: return ('pushdown','yes')
        if kind == 'observe': return ('explain','yes')
        if kind == 'reorder': return ('join_order','yes')
        if kind == 'adapt': return ('adaptivity','yes')
        if kind in {'materialize','inline'}: return ('materialization','yes')
        return (kind,'yes')
    if method == 'yesno': return (op,kind,'yes')
    if method == 'operator_only': return (op,'yes')
    raise ValueError(method)

def project_sig(sig, method):
    return frozenset(project_atom(a, method) for a in sig)

def diff_fields(sig1, sig2):
    # Pair atoms by maximum field overlap and collect field differences.
    atoms1=[atom_tuple(a) for a in sig1]; atoms2=[atom_tuple(a) for a in sig2]
    fields=set()
    if not atoms1 or not atoms2:
        return fields
    for a in atoms1:
        best=max(atoms2, key=lambda b: sum(x==y for x,y in zip(a,b)))
        for name,x,y in zip(FIELDS,a,best):
            if x != y: fields.add(name)
    return fields

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--maps', default='evaluation/grounded_contract_maps.jsonl')
    ap.add_argument('--outdir', default='evaluation/grounded')
    args=ap.parse_args()
    out=Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    maps, engines, probes = load_maps(Path(args.maps))
    pairs=list(itertools.combinations(engines,2))
    per_method=collections.Counter(); per_method_mech=collections.Counter(); global_mech=collections.Counter()
    examples=[]
    for method in METHODS:
        for probe in probes:
            for e1,e2 in pairs:
                s1=maps.get((e1,probe), frozenset()); s2=maps.get((e2,probe), frozenset())
                if s1 == s2: continue
                if project_sig(s1, method) != project_sig(s2, method): continue
                per_method[method]+=1
                fields=diff_fields(s1,s2)
                mechs=sorted(MECHANISM[f] for f in fields if f in MECHANISM)
                if not mechs: mechs=['unclassified contract difference']
                for m in mechs:
                    per_method_mech[(method,m)] += 1; global_mech[m] += 1
                if len(examples) < 80:
                    examples.append({'method':method,'probe_id':probe,'engine_i':e1,'engine_j':e2,'mechanisms':';'.join(mechs),'field_count':len(fields),'full_i_actions':len(s1),'full_j_actions':len(s2)})
    rows=[]
    for (method,mech),n in sorted(per_method_mech.items(), key=lambda x:(x[0][0],-x[1],x[0][1])):
        denom=per_method[method]
        rows.append({'method':method,'mechanism':mech,'false_equivalences_with_mechanism':n,'false_equivalences_for_method':denom,'fraction_of_false_equivalences':f'{n/denom:.6f}' if denom else '0'})
    with open(out/'mechanism_taxonomy.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=['method','mechanism','false_equivalences_with_mechanism','false_equivalences_for_method','fraction_of_false_equivalences']); w.writeheader(); w.writerows(rows)
    total=sum(per_method.values())
    grows=[]
    for mech,n in sorted(global_mech.items(), key=lambda x:-x[1]):
        grows.append({'mechanism':mech,'false_equivalences_with_mechanism':n,'all_false_equivalences':total,'fraction_of_all_false_equivalences':f'{n/total:.6f}' if total else '0'})
    with open(out/'mechanism_taxonomy_global.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=['mechanism','false_equivalences_with_mechanism','all_false_equivalences','fraction_of_all_false_equivalences']); w.writeheader(); w.writerows(grows)
    with open(out/'mechanism_examples.jsonl','w',encoding='utf-8') as f:
        for r in examples: f.write(json.dumps(r)+'\n')
    print(f'Wrote mechanism taxonomy for {total} false equivalence witnesses')
if __name__ == '__main__': main()
