#!/usr/bin/env python3
"""Compute conditional false-equivalence rates for grounded contract maps.

The ordinary trap rate divides false equivalences by all engine-pair/probe
comparisons. This script adds the precision-style denominator that strict
readers ask for: among comparisons that a lossy baseline declares equivalent,
how often is that equivalence false under the full contract semantics?
"""
from __future__ import annotations
import argparse, csv, json, itertools
from pathlib import Path

def read_jsonl(path: Path):
    with path.open() as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def load_maps(path: Path):
    maps={}
    engines=set(); probes=set()
    for r in read_jsonl(path):
        e=r['engine']; p=r['probe_id']
        actions=frozenset((k,v) for k,v in r.get('actions',{}).items() if v!='UNSPEC')
        maps[(e,p)] = actions
        engines.add(e); probes.add(p)
    return maps, sorted(engines), sorted(probes)

def split_action(ak: str):
    parts=ak.split('|')
    if len(parts)==6:
        op,kind,layer,placement,time,obs=parts; variant=''
    elif len(parts)==7:
        op,kind,variant,layer,placement,time,obs=parts
    else:
        # tolerate unexpected by padding
        parts=(parts+['']*7)[:7]
        op,kind,variant,layer,placement,time,obs=parts
    return op,kind,variant,layer,placement,time,obs

def project_atom(atom, method):
    ak, st = atom
    op,kind,variant,layer,placement,time,obs = split_action(ak)
    if method == 'strict':
        return atom
    if method == 'keyword':
        if kind in {'delegate','pushdown','prune'}: return ('pushdown','yes')
        if kind == 'observe': return ('explain','yes')
        if kind == 'reorder': return ('join_order','yes')
        if kind == 'adapt': return ('adaptivity','yes')
        if kind == 'materialize' or kind == 'inline': return ('materialization','yes')
        if kind == 'choose': return ('choose','yes')
        if kind == 'fallback': return ('fallback','yes')
        return (kind,'yes')
    if method == 'yesno':
        # operator-kind feature matrix, modality erased
        return (op,kind,'yes')
    if method == 'operator_only':
        return (op,'yes')
    if method == 'no_placement':
        return ('|'.join([op,kind,variant,layer,'_',time,obs]), st)
    if method == 'no_decision_time':
        return ('|'.join([op,kind,variant,layer,placement,'_',obs]), st)
    if method == 'no_observability':
        return ('|'.join([op,kind,variant,layer,placement,time,'_']), st)
    if method == 'no_modality':
        return (ak,'evidenced')
    raise ValueError(method)

def project_sig(sig, method):
    return frozenset(project_atom(a, method) for a in sig)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--maps', type=Path, default=Path('artifact/evaluation/grounded_contract_maps.jsonl'))
    ap.add_argument('--out', type=Path, default=Path('artifact/evaluation/grounded/conditional_trap_rate.csv'))
    ap.add_argument('--examples-out', type=Path, default=Path('artifact/evaluation/grounded/conditional_trap_examples.jsonl'))
    args=ap.parse_args()
    maps, engines, probes = load_maps(args.maps)
    methods=['keyword','yesno','operator_only','no_placement','no_decision_time','no_observability','no_modality']
    pairs=list(itertools.combinations(engines,2))
    total=len(pairs)*len(probes)
    rows=[]; examples=[]
    # cache projections
    proj_cache={}
    for method in methods:
        projected_equiv=0; false_equiv=0; true_equiv=0; projected_diff=0; false_diff=0
        for p in probes:
            for e1,e2 in pairs:
                s1=maps.get((e1,p), frozenset())
                s2=maps.get((e2,p), frozenset())
                full_eq = (s1 == s2)
                k1=(method,e1,p); k2=(method,e2,p)
                if k1 not in proj_cache: proj_cache[k1]=project_sig(s1,method)
                if k2 not in proj_cache: proj_cache[k2]=project_sig(s2,method)
                proj_eq = (proj_cache[k1] == proj_cache[k2])
                if proj_eq:
                    projected_equiv += 1
                    if full_eq: true_equiv += 1
                    else:
                        false_equiv += 1
                        if len(examples)<100:
                            examples.append({'method':method,'probe_id':p,'engine_i':e1,'engine_j':e2,'projected_signature':sorted(map(str,proj_cache[k1]))[:20],'full_i_size':len(s1),'full_j_size':len(s2)})
                else:
                    projected_diff += 1
                    if full_eq: false_diff += 1
        rows.append({
            'method': method,
            'comparisons': total,
            'projected_equivalences': projected_equiv,
            'true_equivalences': true_equiv,
            'false_equivalences': false_equiv,
            'projected_differences': projected_diff,
            'false_differences': false_diff,
            'unconditional_trap_rate': round(false_equiv/total, 6) if total else 0,
            'conditional_false_equivalence_rate': round(false_equiv/projected_equiv, 6) if projected_equiv else 0,
            'projected_equivalence_rate': round(projected_equiv/total, 6) if total else 0,
        })
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('w', newline='') as f:
        fields=list(rows[0].keys())
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    with args.examples_out.open('w') as f:
        for e in examples:
            f.write(json.dumps(e,ensure_ascii=False)+'\n')
    print(f'Wrote {args.out} and {args.examples_out}')
if __name__=='__main__':
    main()
