#!/usr/bin/env python3
import csv, json, yaml
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
G=ROOT/'grounded'
EVAL=ROOT/'evaluation'; EVAL.mkdir(exist_ok=True)
features=yaml.safe_load(open(ROOT/'benchmark/feature_domain.yaml'))
actions=yaml.safe_load(open(ROOT/'schema/action_domain.yaml'))
feature_values={k:set(v) for k,v in features.items()}
valid={
  'operator':set(actions['operators']),
  'kind':set(actions['action_kinds']),
  'layer':set(actions['layers']),
  'placement':set(actions['placements']),
  'decision_time':set(actions['decision_times']),
  'observability':set(actions['observability_levels']),
  'state':set(actions['states'].keys()),
}
sources={}
for row in csv.DictReader(open(G/'verified_sources.csv')):
    sources[row['source_id']]=row
segments={}
for line in open(G/'verified_segments.jsonl'):
    if line.strip():
        s=json.loads(line); segments[s['segment_id']]=s
rules=[]
for line in open(G/'verified_rules.jsonl'):
    if line.strip(): rules.append(json.loads(line))
issues=[]
seen=set()
source_rule_counts=Counter(); engine_counts=Counter(); state_counts=Counter(); kind_counts=Counter(); fielddiv={}
for r in rules:
    rid=r.get('rule_id','')
    if rid in seen: issues.append((rid,'duplicate_rule_id','duplicate rule id'))
    seen.add(rid)
    if r.get('state') not in valid['state']:
        issues.append((rid,'invalid_state',str(r.get('state'))))
    ev=r.get('evidence',{})
    sid=ev.get('source_id'); segid=ev.get('segment_id')
    if sid not in sources: issues.append((rid,'missing_source',sid or ''))
    if segid not in segments: issues.append((rid,'missing_segment',segid or ''))
    else:
        seg=segments[segid]
        for key in ['line_range','grounding_status','source_url','public_locator','source_title','source_retrieved_at']:
            if not seg.get(key): issues.append((rid,'segment_missing_'+key,segid))
        if not (seg.get('segment_sha256') or seg.get('segment_hash')):
            issues.append((rid,'segment_missing_hash',segid))
        if seg.get('source_id') != sid:
            issues.append((rid,'segment_source_mismatch',f"{sid}!={seg.get('source_id')}"))
        if seg.get('grounding_status') != 'verified_against_web_lines':
            issues.append((rid,'segment_not_verified',seg.get('grounding_status','')))
    for k,v in (r.get('guard') or {}).items():
        if k not in feature_values:
            issues.append((rid,'invalid_guard_key',k)); continue
        vals=v if isinstance(v,list) else [v]
        bad=[x for x in vals if x not in feature_values[k]]
        if bad: issues.append((rid,'invalid_guard_value',f'{k}={bad}'))
    a=r.get('action',{})
    for fld in ['operator','kind','layer','placement','decision_time','observability']:
        if a.get(fld) not in valid[fld]: issues.append((rid,'invalid_action_'+fld,str(a.get(fld))))
    source_rule_counts[sid]+=1; engine_counts[r.get('engine','')]+=1; state_counts[r.get('state','')]+=1; kind_counts[a.get('kind','')]+=1

with open(EVAL/'grounded_rule_audit.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['rule_id','issue_type','detail']); w.writerows(issues)
with open(EVAL/'grounded_rule_audit_summary.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['metric','value'])
    w.writerow(['verified_rules',len(rules)]); w.writerow(['verified_segments',len(segments)]); w.writerow(['verified_sources',len(sources)])
    w.writerow(['audit_issues',len(issues)]); w.writerow(['engines',len(engine_counts)]); w.writerow(['states',len(state_counts)]); w.writerow(['action_kinds',len(kind_counts)])
with open(EVAL/'grounded_engine_rule_counts.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['engine','rules'])
    for k,v in sorted(engine_counts.items()): w.writerow([k,v])
with open(EVAL/'grounded_state_counts.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['state','rules'])
    for k,v in sorted(state_counts.items()): w.writerow([k,v])
with open(EVAL/'grounded_source_rule_counts.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['source_id','rules'])
    for k,v in sorted(source_rule_counts.items()): w.writerow([k,v])
print(f'Grounded audit: {len(rules)} rules, {len(issues)} issues, {len(sources)} sources, {len(segments)} segments')
if issues:
    for row in issues[:20]: print(row)
    raise SystemExit(1)
