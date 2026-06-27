#!/usr/bin/env python3
"""Budgeted benchmark-efficiency analysis for OptSemBench-C."""
from __future__ import annotations
import argparse, csv, json, random, statistics
from collections import defaultdict
from pathlib import Path

def read_jsonl(path: Path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip(): yield json.loads(line)

def pct(vals, q):
    xs=sorted(vals)
    if not xs: return 0.0
    if len(xs)==1: return xs[0]
    pos=q*(len(xs)-1); lo=int(pos); hi=min(lo+1,len(xs)-1); w=pos-lo
    return xs[lo]*(1-w)+xs[hi]*w

def coverage_at_order(order, rules_by_probe, budgets, total_rules):
    out={}; seen=set(); bset=set(budgets)
    for i,p in enumerate(order,1):
        seen.update(rules_by_probe.get(p,set()))
        if i in bset: out[i]=(len(seen), len(seen)/total_rules if total_rules else 0.0)
    return out

def diagnostic_order(probes, rules_by_probe, all_rules):
    # Use bit masks for speed.  Only the prefix until all rules are covered needs
    # greedy search; the remaining probes cannot add new rules and are appended
    # in deterministic probe-id order.
    rule_index = {r:i for i,r in enumerate(sorted(all_rules))}
    masks = {}
    for p in probes:
        mask = 0
        for r in rules_by_probe.get(p,set()):
            mask |= 1 << rule_index[r]
        masks[p] = mask
    full_mask = (1 << len(rule_index)) - 1
    remaining=set(probes); seen=0; order=[]
    while remaining and seen != full_mask:
        def key(p):
            tie = -int(p[1:]) if p.startswith('P') and p[1:].isdigit() else 0
            return (((masks[p] & ~seen).bit_count()), tie)
        best=max(remaining, key=key)
        new_mask = masks[best] & ~seen
        seen |= masks[best]
        remaining.remove(best)
        order.append((best,new_mask.bit_count(),seen.bit_count()))
    for p in sorted(remaining, key=lambda x: int(x[1:]) if x.startswith('P') and x[1:].isdigit() else x):
        order.append((p,0,seen.bit_count()))
    return order

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--trials', type=int, default=100)
    ap.add_argument('--seed', type=int, default=20260621)
    ap.add_argument('--budgets', default='50,100,250,500,1000,2000,3000,4216')
    args=ap.parse_args(); root=args.root
    probes=[r['probe_id'] for r in read_jsonl(root/'benchmark'/'generated_probes.jsonl')]
    budgets=sorted(set(min(int(x), len(probes)) for x in args.budgets.split(',') if x.strip()))
    rules_by_probe=defaultdict(set); all_rules=set()
    for r in read_jsonl(root/'evaluation'/'grounded_applicable_rules.jsonl'):
        rules_by_probe[r['probe_id']].add(r['rule_id']); all_rules.add(r['rule_id'])
    total_rules=len(all_rules)
    gen_cov=coverage_at_order(probes, rules_by_probe, budgets, total_rules)
    diag=diagnostic_order(probes, rules_by_probe, all_rules)
    diag_cov=coverage_at_order([p for p,_n,_c in diag], rules_by_probe, budgets, total_rules)
    rng=random.Random(args.seed); rows=[]
    for budget in budgets:
        gen_rules, gc=gen_cov[budget]; diag_rules, dc=diag_cov[budget]
        vals=[]
        for _ in range(args.trials):
            sample=rng.sample(probes,budget); cov=set()
            for p in sample: cov.update(rules_by_probe.get(p,set()))
            vals.append(len(cov)/total_rules if total_rules else 0.0)
        rows.append({'budget':budget,'generated_prefix_rules':gen_rules,'diagnostic_prefix_rules':diag_rules,'total_rules':total_rules,'generated_rule_coverage':f'{gc:.6f}','diagnostic_rule_coverage':f'{dc:.6f}','random_mean':f'{statistics.mean(vals):.6f}','random_p05':f'{pct(vals,0.05):.6f}','random_p95':f'{pct(vals,0.95):.6f}','random_min':f'{min(vals):.6f}','random_max':f'{max(vals):.6f}','random_trials':args.trials})
    outdir=root/'evaluation'/'grounded'; outdir.mkdir(parents=True, exist_ok=True)
    with (outdir/'benchmark_efficiency.csv').open('w', newline='', encoding='utf-8') as f:
        fields=['budget','generated_prefix_rules','diagnostic_prefix_rules','total_rules','generated_rule_coverage','diagnostic_rule_coverage','random_mean','random_p05','random_p95','random_min','random_max','random_trials']
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    with (outdir/'diagnostic_probe_order.csv').open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=['rank','probe_id','new_rules','cumulative_rules','total_rules','cumulative_rule_coverage']); w.writeheader()
        for i,(p,new,cum) in enumerate(diag,1):
            w.writerow({'rank':i,'probe_id':p,'new_rules':new,'cumulative_rules':cum,'total_rules':total_rules,'cumulative_rule_coverage':f'{cum/total_rules if total_rules else 0.0:.6f}'})
    full_gen=next((r['budget'] for r in rows if float(r['generated_rule_coverage'])>=1.0),'NA')
    full_diag=next((r['budget'] for r in rows if float(r['diagnostic_rule_coverage'])>=1.0),'NA')
    with (outdir/'benchmark_efficiency_summary.csv').open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=['metric','value']); w.writeheader()
        w.writerow({'metric':'budgets','value':len(rows)}); w.writerow({'metric':'total_rules','value':total_rules})
        w.writerow({'metric':'generated_full_rule_coverage_budget','value':full_gen}); w.writerow({'metric':'diagnostic_full_rule_coverage_budget','value':full_diag})
        for label,b in [('budget50',50),('budget100',100)]:
            row=next((r for r in rows if int(r['budget'])==b), None)
            if row:
                w.writerow({'metric':f'generated_{label}_rule_coverage','value':row['generated_rule_coverage']})
                w.writerow({'metric':f'diagnostic_{label}_rule_coverage','value':row['diagnostic_rule_coverage']})
                w.writerow({'metric':f'random_mean_at_{b}','value':row['random_mean']})
                w.writerow({'metric':f'random_p95_at_{b}','value':row['random_p95']})
    print(f"Wrote benchmark efficiency outputs in {outdir}")
if __name__ == '__main__': main()
