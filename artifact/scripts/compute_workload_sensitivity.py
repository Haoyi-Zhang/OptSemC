#!/usr/bin/env python3
"""Compute workload-feature sensitivity over generated probes.

Uses a dominant-signature toggle metric: for each engine, feature, and
assignment of all other features, it compares the dominant contract signature
for each alternative value of the toggled feature. This preserves controlled
feature toggling while avoiding quadratic explosion from duplicate generated
probes and rule-forced completions.
"""
from __future__ import annotations
import argparse, json, csv
from pathlib import Path
from collections import defaultdict, Counter

def read_jsonl(p: Path):
    rows=[]
    if p.exists():
        with p.open() as f:
            for line in f:
                if line.strip(): rows.append(json.loads(line))
    return rows

def sig_tuple(m):
    return frozenset((ak,st) for ak,st in m.get('actions',{}).items() if st!='UNSPEC')

def dist(a,b):
    if a==b: return 0.0
    if not a and not b: return 0.0
    return 1.0-len(a&b)/len(a|b)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--probes', type=Path, default=Path('benchmark/generated_probes.jsonl'))
    ap.add_argument('--maps', type=Path, default=Path('evaluation/contract_maps.jsonl'))
    ap.add_argument('--out', type=Path, default=Path('evaluation/workload_sensitivity.csv'))
    args=ap.parse_args()
    probes=read_jsonl(args.probes)
    maps={(m['engine'],m['probe_id']):m for m in read_jsonl(args.maps)}
    engines=sorted(set(e for e,_ in maps))
    if not probes: return
    features=list(probes[0]['feature_vector'].keys())
    sig_cache={(e,p['probe_id']): sig_tuple(maps.get((e,p['probe_id']), {'actions':{}})) for e in engines for p in probes}
    rows=[]
    for e in engines:
        for feat in features:
            # key_without_feat -> value -> Counter(signature)
            groups=defaultdict(lambda: defaultdict(Counter))
            for p in probes:
                fv=p['feature_vector']
                key=tuple((k,v) for k,v in sorted(fv.items()) if k!=feat)
                groups[key][fv[feat]][sig_cache[(e,p['probe_id'])]] += 1
            total_pairs=0; weighted_sum=0.0; maxd=0.0; nonzero=0; groups_used=0
            for by_val in groups.values():
                if len(by_val)<2: continue
                reps=[]
                for val,counter in by_val.items():
                    sig,count=counter.most_common(1)[0]
                    reps.append((val,sig,count))
                for i in range(len(reps)):
                    for j in range(i+1,len(reps)):
                        _,s1,n1=reps[i]; _,s2,n2=reps[j]
                        w=max(1, min(n1,n2))
                        d=dist(s1,s2)
                        total_pairs += w
                        weighted_sum += d*w
                        if d>0: nonzero += w
                        if d>maxd: maxd=d
                groups_used += 1
            if total_pairs:
                rows.append({'engine':e,'feature':feat,'groups':groups_used,'pairs':total_pairs,'mean_distance':round(weighted_sum/total_pairs,6),'max_distance':round(maxd,6),'nonzero_fraction':round(nonzero/total_pairs,6),'metric':'dominant_controlled_toggle'})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('w', newline='') as f:
        fields=['engine','feature','groups','pairs','mean_distance','max_distance','nonzero_fraction','metric']
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f'Wrote {args.out}')
if __name__=='__main__': main()
