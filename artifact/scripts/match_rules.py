#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any, Dict, List
NON_VALUES={None,'','none','not_applicable','unavailable',False,'false','unknown'}

def read_jsonl(path: Path) -> List[Dict[str,Any]]:
    if not path.exists(): return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def value_matches(rule_val, probe_val):
    if isinstance(rule_val,list): return probe_val in rule_val
    if rule_val=='required': return probe_val not in NON_VALUES
    return probe_val==rule_val

def guard_matches(guard, features):
    for k,v in guard.items():
        pv=features.get(k, None)
        if pv is None or not value_matches(v,pv): return False
    return True

def action_key(a):
    return '|'.join(a.get(k,'') for k in ['operator','kind','variant','layer','placement','decision_time','observability'])

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rules', type=Path, default=Path('extraction/accepted_rules.jsonl'))
    ap.add_argument('--probes', type=Path, default=Path('benchmark/generated_probes.jsonl'))
    ap.add_argument('--out', type=Path, default=Path('evaluation/applicable_rules.jsonl'))
    args=ap.parse_args()
    rules=read_jsonl(args.rules)
    # Precompute compact rule data.
    crules=[]
    for r in rules:
        crules.append((r.get('guard',{}), r['engine'], r['rule_id'], action_key(r['action']), r['state']))
    count=0; probes_count=0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('w') as f:
        for line in args.probes.read_text().splitlines():
            if not line.strip(): continue
            probes_count+=1
            p=json.loads(line); fv=p['feature_vector']; pid=p['probe_id']
            for guard,engine,rid,ak,state in crules:
                if guard_matches(guard,fv):
                    f.write(json.dumps({'probe_id':pid,'engine':engine,'rule_id':rid,'action_key':ak,'state':state}, separators=(',',':'))+'\n')
                    count+=1
    print(f'Matched {count} applicable rules for {probes_count} probes and {len(rules)} rules')
if __name__=='__main__': main()
