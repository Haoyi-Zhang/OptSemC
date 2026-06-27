#!/usr/bin/env python3
"""Compute OptSem-C metrics. avoids loading large applicable-rule relations into memory."""
from __future__ import annotations
import argparse, json, csv, itertools
from pathlib import Path
from collections import defaultdict
from typing import Dict, Any


def read_jsonl(path: Path):
    rows=[]
    if path.exists():
        with path.open() as f:
            for line in f:
                if line.strip(): rows.append(json.loads(line))
    return rows


def stream_jsonl(path: Path):
    if not path.exists(): return
    with path.open() as f:
        for line in f:
            if line.strip(): yield json.loads(line)


def action_key_from_rule(r):
    a=r['action']
    return '|'.join(a.get(k,'') for k in ['operator','kind','variant','layer','placement','decision_time','observability'])

def action_dim(action_key: str) -> str:
    parts=action_key.split('|')
    if len(parts)==7: op, kind, var, layer, placement, time, obs = parts
    else: op, kind, layer, placement, time, obs = parts; var=''
    if layer == 'plan_observability' or kind == 'observe': return 'observability'
    if kind in {'delegate','pushdown'}: return 'pushdown'
    if kind == 'adapt': return 'adaptivity'
    if kind == 'reorder': return 'join_search'
    if kind == 'choose' and op in {'Join','Exchange'}: return 'distribution'
    if kind in {'materialize','inline'}: return 'materialization'
    if kind in {'estimate','fallback'} or op == 'Statistics': return 'statistics'
    return layer


def load_maps(path):
    maps={}
    for r in stream_jsonl(path) or []:
        maps[(r['engine'], r['probe_id'])] = r
    return maps


def full_sig(m):
    return frozenset((ak, st) for ak, st in m.get('actions',{}).items() if st != 'UNSPEC')


def split_action(ak):
    parts=ak.split('|')
    if len(parts)==7: return parts
    op,kind,layer,placement,time,obs=parts; return [op,kind,'',layer,placement,time,obs]

def project_atom(atom, method):
    ak, st = atom
    op,kind,var,layer,placement,time,obs = split_action(ak)
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
    if method == 'no_placement':
        return ('|'.join([op,kind,var,layer,'_',time,obs]), st)
    if method == 'no_modality':
        return (ak, 'evidenced')
    if method == 'no_decision_time':
        return ('|'.join([op,kind,var,layer,placement,'_',obs]), st)
    if method == 'no_observability':
        return ('|'.join([op,kind,var,layer,placement,time,'_']), st)
    raise ValueError(method)

def project_sig(sig, method):
    return frozenset(project_atom(a, method) for a in sig)

def beta_keyword(sig): return project_sig(sig, 'keyword')
def beta_yesno(sig): return project_sig(sig, 'yesno')
def beta_operator_only(sig): return project_sig(sig, 'operator_only')
def beta_no_placement(sig): return project_sig(sig, 'no_placement')
def beta_no_modality(sig): return project_sig(sig, 'no_modality')
def beta_no_decision_time(sig): return project_sig(sig, 'no_decision_time')
def beta_no_observability(sig): return project_sig(sig, 'no_observability')

PROJECTIONS={'keyword': beta_keyword,'yesno': beta_yesno,'operator_only': beta_operator_only,'no_placement': beta_no_placement,'no_modality': beta_no_modality,'no_decision_time': beta_no_decision_time,'no_observability': beta_no_observability}


def write_csv(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rules', type=Path, default=Path('extraction/accepted_rules.jsonl'))
    ap.add_argument('--probes', type=Path, default=Path('benchmark/generated_probes.jsonl'))
    ap.add_argument('--applicable', type=Path, default=Path('evaluation/applicable_rules.jsonl'))
    ap.add_argument('--maps', type=Path, default=Path('evaluation/contract_maps.jsonl'))
    ap.add_argument('--outdir', type=Path, default=Path('evaluation'))
    args=ap.parse_args()
    rules=read_jsonl(args.rules); probes=read_jsonl(args.probes); maps=load_maps(args.maps)
    engines=sorted(set(r['engine'] for r in rules)); probe_ids=[p['probe_id'] for p in probes]

    rules_by_engine=defaultdict(set); triggered=defaultdict(set)
    for r in rules: rules_by_engine[r['engine']].add(r['rule_id'])
    for a in stream_jsonl(args.applicable) or []: triggered[a['engine']].add(a['rule_id'])
    rows=[]
    for e in engines:
        denom=len(rules_by_engine[e]); num=len(triggered[e])
        rows.append({'engine':e,'rules_total':denom,'rules_triggered':num,'contract_coverage': round(num/denom,4) if denom else 0})
    write_csv(args.outdir/'contract_coverage.csv', rows, ['engine','rules_total','rules_triggered','contract_coverage'])

    full_sigs={(e,pid): full_sig(maps.get((e,pid), {'actions':{}})) for e in engines for pid in probe_ids}

    sep_rows=[]
    for pid in probe_ids:
        sigs={full_sigs[(e,pid)] for e in engines}
        sep_rows.append({'probe_id':pid,'distinct_signatures':len(sigs),'engines':len(engines),'separability':round(len(sigs)/len(engines),4)})
    write_csv(args.outdir/'separability.csv', sep_rows, ['probe_id','distinct_signatures','engines','separability'])

    pairs=list(itertools.combinations(engines,2))
    trap_rows=[]
    for name, proj in PROJECTIONS.items():
        false_eq=false_diff=0; total=0; proj_cache={}
        def getp(sig):
            if sig not in proj_cache: proj_cache[sig]=proj(sig)
            return proj_cache[sig]
        for pid in probe_ids:
            for e1,e2 in pairs:
                s1=full_sigs[(e1,pid)]; s2=full_sigs[(e2,pid)]
                p1=getp(s1); p2=getp(s2)
                if p1 == p2 and s1 != s2: false_eq += 1
                if p1 != p2 and s1 == s2: false_diff += 1
                total += 1
        trap_rows.append({'method':name,'comparisons':total,'false_equivalence':false_eq,'false_difference':false_diff,'trap_rate':round((false_eq+false_diff)/total,4) if total else 0})
    write_csv(args.outdir/'trap_rate.csv', trap_rows, ['method','comparisons','false_equivalence','false_difference','trap_rate'])

    action_keys=sorted(set(action_key_from_rule(r) for r in rules))
    dims=sorted(set(action_dim(a) for a in action_keys))
    unspec_rows=[]
    for e in engines:
        for dim in dims:
            dim_actions=[a for a in action_keys if action_dim(a)==dim]
            total=len(dim_actions)*len(probe_ids); unspec=0
            for pid in probe_ids:
                acts=maps.get((e,pid), {'actions':{}}).get('actions',{})
                for a in dim_actions:
                    if acts.get(a,'UNSPEC') == 'UNSPEC': unspec += 1
            unspec_rows.append({'engine':e,'dimension':dim,'cells':total,'unspec_cells':unspec,'unspec_exposure':round(unspec/total,4) if total else 0})
    write_csv(args.outdir/'unspec_exposure.csv', unspec_rows, ['engine','dimension','cells','unspec_cells','unspec_exposure'])

    rows=[]
    for e in engines:
        rows.append({'engine':e,'accepted_rules':len(rules_by_engine[e]),'triggered_rules':len(triggered[e]),'dimensions':len(set(action_dim(action_key_from_rule(r)) for r in rules if r['engine']==e))})
    write_csv(args.outdir/'contract_extraction.csv', rows, ['engine','accepted_rules','triggered_rules','dimensions'])
    print(f"Computed metrics for {len(engines)} engines and {len(probe_ids)} probes")

if __name__ == '__main__': main()
