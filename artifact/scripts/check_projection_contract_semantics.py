#!/usr/bin/env python3
"""Audit implemented projections against evidence-atom semantics."""
from __future__ import annotations
import csv, itertools, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evaluation'
G = E / 'grounded'
MAPS = E / 'grounded_contract_maps.jsonl'
OUT = E / 'projection_contract_semantics.csv'
CHECK = E / 'projection_contract_semantics_check.csv'
HEADLINE = ['keyword','yesno','operator_only']
METHODS = HEADLINE + ['strict','no_placement','no_decision_time','no_observability','no_modality']
EMPTY = frozenset()

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as f: return list(csv.DictReader(f))

def write_csv(path: Path, rows, fields=None):
    fields = fields or list(rows[0].keys())
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

def atom(action_key: str, state: str):
    parts=action_key.split('|')
    if len(parts)==6:
        op,kind,layer,placement,decision_time,observability=parts; variant=''
    else:
        parts=(parts+['']*7)[:7]; op,kind,variant,layer,placement,decision_time,observability=parts
    return (op,kind,variant,layer,placement,decision_time,observability,state)

def keyword(kind: str):
    if kind in {'delegate','pushdown','prune'}: return 'pushdown'
    if kind == 'observe': return 'explain'
    if kind == 'reorder': return 'join_order'
    if kind == 'adapt': return 'adaptivity'
    if kind in {'materialize','inline'}: return 'materialization'
    if kind == 'choose': return 'choose'
    if kind == 'fallback': return 'fallback'
    return kind

def project_atom(a, method: str):
    op,kind,variant,layer,placement,decision_time,observability,state = a
    if method == 'strict': return a
    if method == 'keyword': return (keyword(kind),'yes')
    if method == 'yesno': return (op,kind,'yes')
    if method == 'operator_only': return (op,'yes')
    if method == 'no_placement': return (op,kind,variant,layer,'_',decision_time,observability,state)
    if method == 'no_decision_time': return (op,kind,variant,layer,placement,'_',observability,state)
    if method == 'no_observability': return (op,kind,variant,layer,placement,decision_time,'_',state)
    if method == 'no_modality': return (op,kind,variant,layer,placement,decision_time,observability,'evidenced')
    raise ValueError(method)

def project_sig(sig, method: str):
    return frozenset(project_atom(a, method) for a in sig)

def load_maps():
    maps, engines, probes = {}, set(), set()
    with MAPS.open(encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            r=json.loads(line)
            sig=frozenset(atom(k,v) for k,v in r.get('actions',{}).items() if v!='UNSPEC')
            maps[(r['engine'],r['probe_id'])]=sig; engines.add(r['engine']); probes.add(r['probe_id'])
    return maps, sorted(engines), sorted(probes)

def main():
    print('projection semantics: loading', flush=True)
    maps, engines, probes = load_maps(); pairs=list(itertools.combinations(engines,2))
    print(f'projection semantics: {len(maps)} maps, {len(probes)} probes', flush=True)
    rows=[]
    for method in METHODS:
        print(f'projection semantics: {method}', flush=True)
        projected={k:project_sig(v,method) for k,v in maps.items()}
        equiv=true_eq=false_eq=diff=false_diff=0; lossy_groups=total_groups=0
        for p in probes:
            groups={}
            for e in engines:
                key=(e,p); ps=projected.get(key, EMPTY)
                groups.setdefault(ps,set()).add(maps.get(key, EMPTY))
            total_groups += len(groups); lossy_groups += sum(1 for fs in groups.values() if len(fs)>1)
            for e1,e2 in pairs:
                s1=maps.get((e1,p),EMPTY); s2=maps.get((e2,p),EMPTY)
                peq=projected.get((e1,p),EMPTY)==projected.get((e2,p),EMPTY); feq=s1==s2
                if peq:
                    equiv+=1; true_eq+=int(feq); false_eq+=int(not feq)
                else:
                    diff+=1; false_diff+=int(feq)
        rows.append({'method':method,'projected_equivalences':equiv,'true_equivalences':true_eq,'false_equivalences':false_eq,'projected_differences':diff,'false_differences':false_diff,'lossy_projected_groups':lossy_groups,'projected_groups':total_groups,'atom_projection':'true','state_collapsing':str(method in {'keyword','yesno','operator_only','no_modality'}).lower()})
    write_csv(OUT, rows)
    by={r['method']:r for r in rows}; cond={r.get('method') or r.get('projection'):r for r in read_csv(G/'conditional_trap_rate.csv')}
    checks=[]
    def add(check, ok, details=''): checks.append({'check':check,'passed':str(bool(ok)).lower(),'details':details})
    for m in HEADLINE:
        add(f'{m}_headline_counts_match', int(by[m]['projected_equivalences'])==int(cond[m]['projected_equivalences']) and int(by[m]['false_equivalences'])==int(cond[m]['false_equivalences']), f"recomputed={by[m]['projected_equivalences']}/{by[m]['false_equivalences']};reported={cond[m]['projected_equivalences']}/{cond[m]['false_equivalences']}")
    add('strict_projection_zero_false_equivalence', int(by['strict']['false_equivalences'])==0 and int(by['strict']['false_differences'])==0, str(by['strict']))
    add('headline_projections_are_lossy', all(int(by[m]['false_equivalences'])>0 for m in HEADLINE), '')
    add('state_collapsing_declared_for_coarse_projections', all(by[m]['state_collapsing']=='true' for m in HEADLINE), '')
    add('projection_outputs_present', OUT.exists() and len(rows)==len(METHODS), str(OUT.relative_to(ROOT)))
    write_csv(CHECK, checks, ['check','passed','details'])
    passed=sum(r['passed']=='true' for r in checks)
    print(f'Projection-contract semantics check: {passed}/{len(checks)} passed')
    for r in checks:
        if r['passed']!='true': print('FAIL', r['check'], r['details'])
    if passed != len(checks): sys.exit(1)
if __name__ == '__main__': main()
