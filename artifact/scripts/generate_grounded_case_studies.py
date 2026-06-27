#!/usr/bin/env python3
"""Generate grounded case-study tables from verified contract rules."""
import json, csv, pathlib, collections
from pathlib import Path

ROOT=Path('.')
RULES=ROOT/'artifact/grounded/verified_rules.jsonl'
OUT=ROOT/'artifact/evaluation/grounded/case_studies'
OUT.mkdir(parents=True, exist_ok=True)

rules=[json.loads(l) for l in RULES.open(encoding='utf-8') if l.strip()]

def akey(r):
    a=r['action']
    return '|'.join([a.get('operator',''),a.get('kind',''),a.get('variant',''),a.get('layer',''),a.get('placement',''),a.get('decision_time',''),a.get('observability','')])

def compact_guard(g):
    if not g: return '{}'
    return '; '.join(f'{k}={v}' for k,v in sorted(g.items()))

def row(r, theme):
    a=r['action']
    ev=r.get('evidence',{})
    return {
        'theme':theme,
        'engine':r['engine'],
        'state':r['state'],
        'operator':a.get('operator',''),
        'kind':a.get('kind',''),
        'variant':a.get('variant',''),
        'placement':a.get('placement',''),
        'decision_time':a.get('decision_time',''),
        'observability':a.get('observability',''),
        'guard':compact_guard(r.get('guard',{})),
        'rule_id':r['rule_id'],
        'source_id':ev.get('source_id',''),
        'line_range':ev.get('line_range',''),
    }

def pick(pred, theme, limit=12):
    picked=[r for r in rules if pred(r)]
    # diversify by engine, then variant
    seen=set(); out=[]
    for r in picked:
        key=(r['engine'], r['action'].get('variant',''), r['state'])
        if key not in seen:
            out.append(row(r, theme)); seen.add(key)
        if len(out)>=limit: break
    return out

cases=[]
# Case 1: pushdown/source delegation family
cases += pick(lambda r: r['action'].get('kind') in {'pushdown','delegate','prune'} or r['action'].get('placement')=='connector_source', 'C1_pushdown_is_not_binary', 16)
# Case 2: plan evidence levels and operator disappearance/observability
cases += pick(lambda r: r['action'].get('kind') in {'observe','profile','estimate'} and r['action'].get('layer') in {'plan_observability','statistics_contract'}, 'C2_observability_is_non_isomorphic', 16)
# Case 3: runtime/adaptive decision time
cases += pick(lambda r: r['action'].get('decision_time')=='runtime' or r['action'].get('kind') in {'adapt','convert','coalesce'}, 'C3_decision_time_matters', 16)
# Case 4: materialization/reuse semantics
cases += pick(lambda r: r['action'].get('operator')=='Materialize' or r['action'].get('kind') in {'materialize','inline','reuse'}, 'C4_materialization_and_reuse', 16)

with (OUT/'case_study_rules.csv').open('w',newline='',encoding='utf-8') as f:
    fields=list(cases[0].keys())
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(cases)

# Summaries per case
summary=[]
for theme, rows in collections.defaultdict(list, {k:[r for r in cases if r['theme']==k] for k in sorted(set(r['theme'] for r in cases))}).items():
    summary.append({
        'theme':theme,
        'rules':len(rows),
        'engines':len(set(r['engine'] for r in rows)),
        'states':','.join(sorted(set(r['state'] for r in rows))),
        'placements':','.join(sorted(set(r['placement'] for r in rows))),
        'decision_times':','.join(sorted(set(r['decision_time'] for r in rows))),
        'observability_modes':','.join(sorted(set(r['observability'] for r in rows))),
    })
with (OUT/'case_study_summary.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=list(summary[0].keys())); w.writeheader(); w.writerows(summary)

print('Wrote case-study tables with', len(cases), 'rules')
