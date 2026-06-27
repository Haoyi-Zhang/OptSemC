#!/usr/bin/env python3
"""Verify finite-state OptSem-C semantics and corpus consistency.

This script is intentionally small and exhaustive: the state domain has only
four public states plus CONFLICT, so algebraic properties can be checked by
enumeration. It also audits the accepted corpus against the semantic state
space and the current merged maps.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
try:
    import yaml
except Exception as e:
    raise SystemExit('PyYAML is required for verify_semantics.py') from e

BASE_STATES = ['UNSPEC','MAY','MUST','MUST_NOT']
ALL_STATES = BASE_STATES + ['CONFLICT']

EXPECTED_TUPLES = {
    'MUST': {'must':1,'allowed':1,'evidenced':1},
    'MAY': {'must':0,'allowed':1,'evidenced':1},
    'MUST_NOT': {'must':0,'allowed':0,'evidenced':1},
    'UNSPEC': {'must':0,'allowed':1,'evidenced':0},
}

def iter_jsonl(path: Path):
    if not path.exists():
        return
    with path.open(encoding='utf-8') as f:
        for i,line in enumerate(f,1):
            if line.strip():
                try:
                    yield json.loads(line)
                except Exception as e:
                    raise SystemExit(f'Invalid JSON at {path}:{i}: {e}')

def load_join(domain):
    jt = domain.get('state_join', {})
    table = {s: dict(jt.get(s, {})) for s in BASE_STATES}
    # Make CONFLICT absorbing and complete the table symmetrically.
    table['CONFLICT'] = {s:'CONFLICT' for s in ALL_STATES}
    for a in ALL_STATES:
        table.setdefault(a, {})
        for b in ALL_STATES:
            if b == 'CONFLICT' or a == 'CONFLICT':
                table[a][b] = 'CONFLICT'
            elif b not in table[a]:
                table[a][b] = table.get(b, {}).get(a, 'MISSING')
    return table

def join(table, a, b):
    return table.get(a, {}).get(b, 'MISSING')

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path('.'))
    ap.add_argument('--out-properties', type=Path, default=Path('evaluation/state_join_properties.csv'))
    ap.add_argument('--out-audit', type=Path, default=Path('evaluation/semantics_audit.csv'))
    args=ap.parse_args()
    root=args.root
    domain=yaml.safe_load((root/'schema/action_domain.yaml').read_text(encoding='utf-8'))
    table=load_join(domain)
    rows=[]
    def add(prop, passed, counter=''):
        rows.append({'property':prop,'passed':str(bool(passed)).lower(),'counterexample':counter})
    # Totality
    missing=[]
    for a in ALL_STATES:
        for b in ALL_STATES:
            if join(table,a,b) not in ALL_STATES:
                missing.append(f'{a},{b}->{join(table,a,b)}')
    add('totality_over_states_plus_conflict', not missing, ';'.join(missing[:5]))
    # Commutativity
    bad=[]
    for a in ALL_STATES:
        for b in ALL_STATES:
            if join(table,a,b)!=join(table,b,a): bad.append(f'{a},{b}')
    add('commutativity', not bad, ';'.join(bad[:5]))
    # Idempotence
    bad=[a for a in ALL_STATES if join(table,a,a)!=a]
    add('idempotence', not bad, ';'.join(bad))
    # UNSPEC identity
    bad=[a for a in ALL_STATES if join(table,'UNSPEC',a)!=a or join(table,a,'UNSPEC')!=a]
    add('unspec_identity', not bad, ';'.join(bad))
    # Conflict absorbing
    bad=[a for a in ALL_STATES if join(table,'CONFLICT',a)!='CONFLICT' or join(table,a,'CONFLICT')!='CONFLICT']
    add('conflict_absorbing', not bad, ';'.join(bad))
    # Associativity
    bad=[]
    for a in ALL_STATES:
        for b in ALL_STATES:
            for c in ALL_STATES:
                if join(table, join(table,a,b), c) != join(table, a, join(table,b,c)):
                    bad.append(f'{a},{b},{c}')
    add('associativity', not bad, ';'.join(bad[:5]))
    # Expected contradictions
    contradictions=[('MAY','MUST_NOT'),('MUST','MUST_NOT')]
    bad=[f'{a},{b}' for a,b in contradictions if join(table,a,b)!='CONFLICT' or join(table,b,a)!='CONFLICT']
    add('documented_contradictions_conflict', not bad, ';'.join(bad))
    # MUST dominates MAY
    add('must_dominates_may', join(table,'MUST','MAY')=='MUST' and join(table,'MAY','MUST')=='MUST', '')
    # State tuples
    state_defs=domain.get('states', {})
    bad=[]
    for s, exp in EXPECTED_TUPLES.items():
        got=state_defs.get(s, {})
        for k,v in exp.items():
            if int(got.get(k,-1)) != v:
                bad.append(f'{s}.{k}={got.get(k)} expected {v}')
    add('state_tuple_definitions', not bad, ';'.join(bad))

    write_csv(root/args.out_properties, rows, ['property','passed','counterexample'])

    # Corpus-level semantic audit.
    rules=list(iter_jsonl(root/'grounded/verified_rules.jsonl'))
    conflicts=list(iter_jsonl(root/'evaluation/grounded_conflicts.jsonl')) if (root/'evaluation/grounded_conflicts.jsonl').exists() else []
    maps=list(iter_jsonl(root/'evaluation/grounded_contract_maps.jsonl')) if (root/'evaluation/grounded_contract_maps.jsonl').exists() else []
    valid_states=set(BASE_STATES)
    invalid_rule_states=[r.get('rule_id','?') for r in rules if r.get('state') not in valid_states]
    conflict_maps=sum(1 for m in maps for s in m.get('actions',{}).values() if s=='CONFLICT')
    audit=[
        {'check':'accepted_rules','value':len(rules),'passed':'true' if rules else 'false','details':''},
        {'check':'invalid_rule_states','value':len(invalid_rule_states),'passed':str(len(invalid_rule_states)==0).lower(),'details':';'.join(invalid_rule_states[:10])},
        {'check':'merge_conflict_records','value':len(conflicts),'passed':str(len(conflicts)==0).lower(),'details':''},
        {'check':'conflict_states_in_maps','value':conflict_maps,'passed':str(conflict_maps==0).lower(),'details':''},
        {'check':'state_join_properties_passed','value':sum(1 for r in rows if r['passed']=='true'),'passed':str(all(r['passed']=='true' for r in rows)).lower(),'details':f'{sum(1 for r in rows if r["passed"]=="true")}/{len(rows)}'},
    ]
    write_csv(root/args.out_audit, audit, ['check','value','passed','details'])
    print(f'Verified {len(rows)} semantic properties; corpus rules={len(rules)}, conflicts={len(conflicts)}')

if __name__=='__main__': main()
