#!/usr/bin/env python3
"""Verify finite proof obligations behind projection-loss and repair claims."""
from __future__ import annotations
import csv, itertools, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / 'evaluation' / 'grounded_contract_maps.jsonl'
G = ROOT / 'evaluation' / 'grounded'
OUT = ROOT / 'evaluation' / 'projection_proof_obligations.csv'
FIELDS = ['operator','kind','variant','layer','placement','decision_time','observability','state']
SEMANTIC_FIELDS = ['operator','kind','layer','placement','decision_time','observability','state']
CORE_FIELDS = ['operator','layer','placement','decision_time','observability']
METHODS = ['keyword','yesno','operator_only']

def read_jsonl(path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip(): yield json.loads(line)

def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def split_action(action_key, state):
    parts = action_key.split('|')
    if len(parts) == 6:
        operator, kind, layer, placement, decision_time, observability = parts; variant=''
    else:
        parts = (parts + ['']*7)[:7]
        operator, kind, variant, layer, placement, decision_time, observability = parts
    return (operator, kind, variant, layer, placement, decision_time, observability, state)

def baseline_atom(a, method):
    d = dict(zip(FIELDS, a)); kind=d['kind']; op=d['operator']
    if method == 'keyword':
        if kind in {'delegate','pushdown','prune'}: return ('pushdown','yes')
        if kind == 'observe': return ('explain','yes')
        if kind == 'reorder': return ('join_order','yes')
        if kind == 'adapt': return ('adaptivity','yes')
        if kind in {'materialize','inline'}: return ('materialization','yes')
        if kind == 'choose': return ('choose','yes')
        if kind == 'fallback': return ('fallback','yes')
        return (kind,'yes')
    if method == 'yesno': return (op, kind, 'yes')
    if method == 'operator_only': return (op, 'yes')
    raise ValueError(method)

def project_sig(sig, method, fields=()):
    idx=[FIELDS.index(f) for f in fields]
    return frozenset(baseline_atom(a, method)+tuple(a[i] for i in idx) for a in sig)

def load_maps():
    maps={}; engines=set(); probes=set()
    for row in read_jsonl(MAPS):
        key=(row['engine'], row['probe_id'])
        sig=frozenset(split_action(k,v) for k,v in row.get('actions',{}).items() if v!='UNSPEC')
        maps[key]=sig; engines.add(row['engine']); probes.add(row['probe_id'])
    return maps, sorted(engines), sorted(probes)

def parse_sets(s):
    return [tuple(x for x in chunk.split('+') if x) for chunk in s.split(';') if chunk.strip()]

def add(rows, check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':details})

def main():
    maps, engines, probes = load_maps()
    proj_cache={}
    def proj(key, method, fields=()):
        fields=tuple(fields)
        ck=(key,method,fields)
        v=proj_cache.get(ck)
        if v is None:
            v=project_sig(maps.get(key, frozenset()), method, fields)
            proj_cache[ck]=v
        return v
    witnesses={}
    for method in METHODS:
        ws=[]
        for p in probes:
            keys=[(e,p) for e in engines]
            for k1,k2 in itertools.combinations(keys,2):
                if maps.get(k1,frozenset()) != maps.get(k2,frozenset()) and proj(k1,method) == proj(k2,method):
                    ws.append((method,p,k1,k2))
        witnesses[method]=ws
    def repairs_all(ws, fields):
        return all(proj(k1,method,fields) != proj(k2,method,fields) for method,_p,k1,k2 in ws)
    out=[]; summary={r['method']:r for r in read_csv(G/'repair_certificate_summary.csv')}
    for method in METHODS:
        ws=witnesses[method]; rep=summary[method]
        reported=int(rep['false_equivalences']); min_size=int(rep['minimal_universal_repair_size']); sets=parse_sets(rep['repair_sets'])
        add(out, f'{method}_witness_count_matches_table', len(ws)==reported, f'computed={len(ws)};reported={reported}')
        add(out, f'{method}_all_witnesses_full_unequal', all(maps[k1]!=maps[k2] for _m,_p,k1,k2 in ws), f'witnesses={len(ws)}')
        add(out, f'{method}_all_witnesses_projection_equal', all(proj(k1,method)==proj(k2,method) for _m,_p,k1,k2 in ws), f'witnesses={len(ws)}')
        bad=['+'.join(s) for s in sets if not repairs_all(ws,s)]
        add(out, f'{method}_reported_repairs_are_sufficient', not bad, ';'.join(bad))
        # All current mainline repairs have cardinality one; the general loop is
        # retained for future snapshots, but now operates over cached signatures.
        smaller=False
        for k in range(min_size):
            for sub in itertools.combinations(FIELDS,k):
                if repairs_all(ws, sub): smaller=True; break
            if smaller: break
        add(out, f'{method}_no_smaller_universal_repair', not smaller, f'min_size={min_size}')
    all_ws=[w for m in METHODS for w in witnesses[m]]
    basis=['layer','placement']
    add(out, 'layer_placement_basis_repairs_all_projections', repairs_all(all_ws,basis), f'witnesses={len(all_ws)}')
    add(out, 'layer_placement_basis_excludes_variant', 'variant' not in basis, '+'.join(basis))
    singles=[f for f in SEMANTIC_FIELDS if repairs_all(all_ws,[f])]
    add(out, 'no_single_semantic_field_repairs_all_projections', not singles, ';'.join(singles))
    core2=['+'.join(s) for s in itertools.combinations(CORE_FIELDS,2) if repairs_all(all_ws,s)]
    add(out, 'core_two_field_basis_exists', bool(core2), ';'.join(core2))
    add(out, 'core_two_field_basis_contains_layer_placement', 'layer+placement' in core2, ';'.join(core2))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(out)
    passed=sum(r['passed']=='true' for r in out)
    print(f'Projection proof obligations: {passed}/{len(out)} passed')
    for r in out:
        if r['passed']!='true': print('FAIL', r['check'], r['details'])
    if passed != len(out): raise SystemExit(1)
if __name__ == '__main__': main()
