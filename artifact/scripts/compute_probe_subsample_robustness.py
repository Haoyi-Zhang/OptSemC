#!/usr/bin/env python3
"""Probe-subsample robustness for grounded false-equivalence measurements.

The main false-equivalence results are reported on all generated probes. This
analysis checks whether the conditional false-equivalence rate remains visible
when the probe set is randomly subsampled. It aggregates by probe first so that
samples respect the benchmark unit rather than treating engine pairs as fully
independent observations.
"""
from __future__ import annotations
import argparse, csv, itertools, json, random
from pathlib import Path

METHODS = ['keyword','yesno','operator_only']
FRACTIONS = [0.10, 0.25, 0.50, 0.75, 1.00]


def read_jsonl(path: Path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def split_action(ak: str):
    parts = ak.split('|')
    if len(parts)==6:
        op,kind,layer,placement,time,obs=parts; variant=''
    elif len(parts)==7:
        op,kind,variant,layer,placement,time,obs=parts
    else:
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
        if kind in {'materialize','inline'}: return ('materialization','yes')
        if kind == 'choose': return ('choose','yes')
        if kind == 'fallback': return ('fallback','yes')
        return (kind,'yes')
    if method == 'yesno':
        return (op,kind,'yes')
    if method == 'operator_only':
        return (op,'yes')
    raise ValueError(method)


def project_sig(sig, method):
    return frozenset(project_atom(a, method) for a in sig)


def load_maps(path: Path):
    maps={}; engines=set(); probes=set()
    for r in read_jsonl(path):
        e=r['engine']; p=r['probe_id']
        sig=frozenset((k,v) for k,v in r.get('actions',{}).items() if v!='UNSPEC')
        maps[(e,p)] = sig
        engines.add(e); probes.add(p)
    return maps, sorted(engines), sorted(probes)


def per_probe_counts(maps, engines, probes):
    pairs=list(itertools.combinations(engines,2))
    out={m:{} for m in METHODS}
    proj_cache={}
    for p in probes:
        for m in METHODS:
            projected=0; false=0; true=0
            for e1,e2 in pairs:
                s1=maps.get((e1,p), frozenset())
                s2=maps.get((e2,p), frozenset())
                full_eq=(s1==s2)
                k1=(m,e1,p); k2=(m,e2,p)
                if k1 not in proj_cache: proj_cache[k1]=project_sig(s1,m)
                if k2 not in proj_cache: proj_cache[k2]=project_sig(s2,m)
                if proj_cache[k1] == proj_cache[k2]:
                    projected += 1
                    if full_eq: true += 1
                    else: false += 1
            out[m][p]={'projected_equivalences':projected,'true_equivalences':true,'false_equivalences':false}
    return out


def summarize(vals):
    vals=sorted(vals)
    if not vals: return (0,0,0,0)
    mean=sum(vals)/len(vals)
    median=vals[len(vals)//2] if len(vals)%2 else (vals[len(vals)//2-1]+vals[len(vals)//2])/2
    return (min(vals), mean, median, max(vals))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--maps', type=Path, default=Path('evaluation/grounded_contract_maps.jsonl'))
    ap.add_argument('--out-summary', type=Path, default=Path('evaluation/grounded/probe_subsample_robustness.csv'))
    ap.add_argument('--out-trials', type=Path, default=Path('evaluation/grounded/probe_subsample_trials.csv'))
    ap.add_argument('--trials', type=int, default=30)
    ap.add_argument('--seed', type=int, default=20260622)
    args=ap.parse_args()
    maps, engines, probes = load_maps(args.maps)
    counts = per_probe_counts(maps, engines, probes)
    rng=random.Random(args.seed)
    trial_rows=[]
    for frac in FRACTIONS:
        n=max(1, int(round(len(probes)*frac)))
        n=min(n, len(probes))
        reps = 1 if frac == 1.0 else args.trials
        for trial in range(reps):
            sample = probes if frac == 1.0 else rng.sample(probes, n)
            for m in METHODS:
                proj=sum(counts[m][p]['projected_equivalences'] for p in sample)
                false=sum(counts[m][p]['false_equivalences'] for p in sample)
                true=sum(counts[m][p]['true_equivalences'] for p in sample)
                trial_rows.append({
                    'method':m,
                    'fraction':frac,
                    'trial':trial,
                    'probes':n,
                    'projected_equivalences':proj,
                    'true_equivalences':true,
                    'false_equivalences':false,
                    'conditional_false_equivalence_rate': round(false/proj, 6) if proj else 0.0,
                    'nonzero_false_equivalence': int(false>0),
                })
    summary=[]
    for m in METHODS:
        for frac in FRACTIONS:
            rows=[r for r in trial_rows if r['method']==m and r['fraction']==frac]
            rates=[float(r['conditional_false_equivalence_rate']) for r in rows]
            falses=[int(r['false_equivalences']) for r in rows]
            nonzero=sum(int(r['nonzero_false_equivalence']) for r in rows)
            rmin,rmean,rmed,rmax=summarize(rates)
            fmin,fmean,fmed,fmax=summarize(falses)
            summary.append({
                'method':m,
                'fraction':frac,
                'trials':len(rows),
                'probes_per_trial': rows[0]['probes'] if rows else 0,
                'nonzero_trials':nonzero,
                'rate_min':round(rmin,6),
                'rate_mean':round(rmean,6),
                'rate_median':round(rmed,6),
                'rate_max':round(rmax,6),
                'false_min':round(fmin,3),
                'false_mean':round(fmean,3),
                'false_median':round(fmed,3),
                'false_max':round(fmax,3),
            })
    args.out_summary.parent.mkdir(parents=True, exist_ok=True)
    with args.out_trials.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=list(trial_rows[0].keys())); w.writeheader(); w.writerows(trial_rows)
    with args.out_summary.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=list(summary[0].keys())); w.writeheader(); w.writerows(summary)
    print(f'Wrote {args.out_summary} and {args.out_trials}')

if __name__ == '__main__':
    main()
