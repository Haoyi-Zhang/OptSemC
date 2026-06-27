#!/usr/bin/env python3
"""Merge applicable OptSem-C rules into engine-query contract maps.

Compact output: contract_maps.jsonl stores only action states. Supporting
rule lists are written separately to contract_support.jsonl to keep the main
metric input compact and fast to read.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
STATE_JOIN={
 'UNSPEC':{'UNSPEC':'UNSPEC','MAY':'MAY','MUST':'MUST','MUST_NOT':'MUST_NOT'},
 'MAY':{'UNSPEC':'MAY','MAY':'MAY','MUST':'MUST','MUST_NOT':'CONFLICT'},
 'MUST':{'UNSPEC':'MUST','MAY':'MUST','MUST':'MUST','MUST_NOT':'CONFLICT'},
 'MUST_NOT':{'UNSPEC':'MUST_NOT','MAY':'CONFLICT','MUST':'CONFLICT','MUST_NOT':'MUST_NOT'},
 'CONFLICT':{'UNSPEC':'CONFLICT','MAY':'CONFLICT','MUST':'CONFLICT','MUST_NOT':'CONFLICT','CONFLICT':'CONFLICT'}}

def iter_jsonl(path: Path):
    with path.open() as f:
        for i,line in enumerate(f,1):
            if line.strip():
                try: yield json.loads(line)
                except Exception as e: raise SystemExit(f'Invalid JSON at {path}:{i}: {e}')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--applicable',type=Path,default=Path('evaluation/applicable_rules.jsonl'))
    ap.add_argument('--out',type=Path,default=Path('evaluation/contract_maps.jsonl'))
    ap.add_argument('--support',type=Path,default=Path('evaluation/contract_support.jsonl'))
    ap.add_argument('--conflicts',type=Path,default=Path('evaluation/conflicts.jsonl'))
    args=ap.parse_args()
    maps={}; support={}; conflicts=[]; count=0
    for row in iter_jsonl(args.applicable):
        count+=1; k=(row['engine'],row['probe_id'])
        rec=maps.setdefault(k, {'engine':row['engine'],'probe_id':row['probe_id'],'actions':{}})
        sup=support.setdefault(k, {'engine':row['engine'],'probe_id':row['probe_id'],'supporting_rules':{}})
        ak=row.get('action_key')
        if not ak and 'action' in row:
            a=row['action']; ak='|'.join(a.get(k,'') for k in ['operator','kind','variant','layer','placement','decision_time','observability'])
        old=rec['actions'].get(ak,'UNSPEC'); new=STATE_JOIN[old].get(row['state'],'CONFLICT')
        if new=='CONFLICT':
            conflicts.append({'engine':row['engine'],'probe_id':row['probe_id'],'action_key':ak,'old_state':old,'new_rule_state':row['state'],'rule_id':row['rule_id']})
        rec['actions'][ak]=new
        sup['supporting_rules'].setdefault(ak,[]).append(row['rule_id'])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('w') as f:
        for rec in sorted(maps.values(), key=lambda x:(x['engine'],x['probe_id'])):
            f.write(json.dumps(rec,separators=(',',':'),ensure_ascii=False)+'\n')
    with args.support.open('w') as f:
        for rec in sorted(support.values(), key=lambda x:(x['engine'],x['probe_id'])):
            f.write(json.dumps(rec,separators=(',',':'),ensure_ascii=False)+'\n')
    with args.conflicts.open('w') as f:
        for c in conflicts: f.write(json.dumps(c,separators=(',',':'),ensure_ascii=False)+'\n')
    print(f'Wrote {len(maps)} compact contract maps and {len(conflicts)} conflicts from {count} applicable rules')
if __name__=='__main__': main()
