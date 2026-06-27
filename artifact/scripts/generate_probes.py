#!/usr/bin/env python3
"""Generate OptSemBench-C covering query probes.

Supports global t-wise coverage plus selected higher-order feature tuples.
The output is deterministic and intentionally small enough for paper artifacts.
"""
from __future__ import annotations
import argparse, itertools, json, re
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, FrozenSet
try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

Assignment = Dict[str, str]
Interaction = Tuple[Tuple[str, str], ...]

def load_yaml(path: Path) -> Any:
    if not path or not path.exists(): return None
    return yaml.safe_load(path.read_text())

def parse_atom(expr: str):
    expr=expr.strip()
    m=re.match(r"^(\w+)\s+in\s+\[([^\]]+)\]$", expr)
    if m:
        var=m.group(1); vals=[v.strip() for v in m.group(2).split(',')]
        return lambda a, partial=False: None if var not in a else a[var] in vals
    m=re.match(r"^(\w+)\s*==\s*(\w+)$", expr)
    if m:
        var,val=m.group(1),m.group(2)
        return lambda a, partial=False: None if var not in a else a[var]==val
    m=re.match(r"^(\w+)\s*!=\s*(\w+)$", expr)
    if m:
        var,val=m.group(1),m.group(2)
        return lambda a, partial=False: None if var not in a else a[var]!=val
    raise ValueError(f"Unsupported constraint atom: {expr}")

def parse_rule(rule: str):
    if '->' in rule:
        left_s,right_s=[x.strip() for x in rule.split('->',1)]
        left=parse_atom(left_s); right=parse_atom(right_s)
        def check(a:Assignment, partial:bool=False):
            l=left(a,partial); r=right(a,partial)
            if l is False: return True
            if l is True and r is False: return False
            if l is True and r is True: return True
            if not partial: return (not bool(l)) or bool(r)
            return None
        return check
    return parse_atom(rule)

def load_constraints(path: Path):
    data=load_yaml(path) or {}
    return [(c['name'], parse_rule(c['rule'])) for c in data.get('constraints',[])]

def valid_assignment(a:Assignment, constraints)->bool:
    return all(fn(a, partial=False) is not False for _,fn in constraints)

def partial_ok(a:Assignment,constraints)->bool:
    return all(fn(a, partial=True) is not False for _,fn in constraints)

def complete_assignment(partial:Assignment, domain:Dict[str,List[str]], constraints)->Optional[Assignment]:
    features=list(domain.keys())
    order=sorted(features, key=lambda f:(f not in partial, len(domain[f]), f))
    assigned=dict(partial)
    if not partial_ok(assigned,constraints): return None
    preferred=['none','local','not_applicable','low','none_control']
    def backtrack(i:int)->Optional[Assignment]:
        if i==len(order):
            return dict(assigned) if valid_assignment(assigned,constraints) else None
        f=order[i]
        if f in assigned: return backtrack(i+1)
        vals=list(domain[f])
        vals.sort(key=lambda x: preferred.index(x) if x in preferred else len(preferred))
        for v in vals:
            assigned[f]=v
            if partial_ok(assigned,constraints):
                out=backtrack(i+1)
                if out is not None: return out
            assigned.pop(f,None)
        return None
    return backtrack(0)

def interactions_for_features(features:List[str], domain:Dict[str,List[str]], constraints)->List[Interaction]:
    # A target interaction is counted only if it has at least one valid full
    # assignment. Partial consistency is not sufficient: e.g.,
    # aggregation=group_by_after_join with join_type=none has no valid
    # completion once join-shape constraints are enforced. Filtering here makes
    # the benchmark denominator exactly the set of renderable valid
    # interactions rather than a superset that later fails generation.
    out=[]; seen=set(); completion_cache={}
    for vals in itertools.product(*(domain[f] for f in features)):
        partial=dict(zip(features, vals))
        if not partial_ok(partial,constraints):
            continue
        inter=tuple(sorted(partial.items()))
        if inter in seen:
            continue
        comp=completion_cache.get(inter)
        if comp is None:
            comp=complete_assignment(partial, domain, constraints)
            completion_cache[inter]=comp
        if comp is not None:
            seen.add(inter); out.append(inter)
    return out

def all_valid_interactions(domain:Dict[str,List[str]], constraints, t:int)->List[Interaction]:
    features=list(domain.keys())
    all_int=[]; seen=set()
    for fs in itertools.combinations(features,t):
        for inter in interactions_for_features(list(fs),domain,constraints):
            if inter not in seen:
                seen.add(inter); all_int.append(inter)
    return all_int

def load_selected(path: Optional[Path])->List[List[str]]:
    if not path or not path.exists(): return []
    data=load_yaml(path) or {}
    rows=[]
    for item in data.get('selected_interactions',[]):
        feats=item.get('features') if isinstance(item,dict) else item
        if feats: rows.append(list(feats))
    return rows

def covered_by_assignment(a:Assignment, interaction_specs:List[List[str]])->FrozenSet[Interaction]:
    out=[]
    for fs in interaction_specs:
        if all(f in a for f in fs):
            out.append(tuple(sorted((f,a[f]) for f in fs)))
    return frozenset(out)

def render_sql(a:Assignment, idx:int)->str:
    js,jt=a['join_shape'],a['join_type']; pred=a['predicate_class']; agg=a['aggregation']; order=a['order_limit']; src=a['source_boundary']; reuse=a['reuse_structure']; control=a.get('control_surface','none_control')
    hint=''
    if control=='broadcast_hint': hint='/*+ BROADCAST(d1) */ '
    def rel(name):
        if src=='same_connector': return f"remote_pg.{name}"
        if src=='cross_connector': return f"remote_pg.{name}" if name in ['customer','dim1','dim2','a','b'] else f"hive.{name}"
        return name
    where=[]
    pred_alias = 'd1' if js in ['none', 'binary'] else ('f' if js in ['star', 'snowflake'] else 'a')
    if pred in ['simple','conjunctive']: where.append(f'{pred_alias}.flag = 1')
    elif pred=='disjunctive': where.append(f"({pred_alias}.flag = 1 OR {pred_alias}.region = 'EU')")
    elif pred in ['function','udf']: where.append(f'expensive_udf({pred_alias}.comment) = TRUE')
    elif pred=='correlated':
        if js == 'none':
            where.append('d1.custkey IN (SELECT x.custkey FROM aux x WHERE x.custkey = d1.custkey)')
        elif js == 'binary':
            where.append('f.custkey IN (SELECT x.custkey FROM aux x WHERE x.custkey = f.custkey)')
        elif js in ['star','snowflake']:
            where.append('f.k1 IN (SELECT x.k1 FROM aux x WHERE x.k1 = f.k1)')
        else:
            where.append('a.k IN (SELECT x.k FROM aux x WHERE x.k = a.k)')
    if reuse=='reused_cte' or control in ['materialized_hint','not_materialized_hint']:
        mat=' AS '
        if control=='materialized_hint': mat=' AS MATERIALIZED '
        if control=='not_materialized_hint': mat=' AS NOT MATERIALIZED '
        cte_source = 'remote_pg.orders' if src == 'cross_connector' else rel('orders')
        base=f"WITH cte{mat}(SELECT custkey, COUNT(*) AS n FROM {cte_source} GROUP BY custkey)\n"
        if src == 'cross_connector':
            body = f"SELECT c1.custkey FROM cte c1 JOIN {rel('fact')} f ON c1.custkey = f.custkey WHERE c1.n > 1"
        else:
            body = "SELECT c1.custkey FROM cte c1 JOIN cte c2 ON c1.custkey = c2.custkey WHERE c1.n > 1"
        if order=='topn': body += " ORDER BY 1 LIMIT 10"
        elif order=='order_by': body += " ORDER BY 1"
        elif order=='limit': body += " LIMIT 10"
        elif order=='window_order': body = "SELECT *, ROW_NUMBER() OVER (ORDER BY 1) AS rn FROM (" + body + ") s"
        return base + body + ";"
    if js=='none':
        select=f"SELECT {hint}custkey, name"; from_clause=f"FROM {rel('customer')} d1"
    elif js=='binary':
        select=f"SELECT {hint}d1.custkey, f.orderkey"; from_clause=f"FROM {rel('customer')} d1 JOIN {rel('orders')} f ON d1.custkey = f.custkey"
    elif js in ['star','snowflake']:
        select=f"SELECT {hint}f.key, d1.attr, d2.attr, SUM(f.measure)"; from_clause=f"FROM {rel('fact')} f JOIN {rel('dim1')} d1 ON f.k1=d1.k JOIN {rel('dim2')} d2 ON f.k2=d2.k"
    elif js=='chain':
        select=f"SELECT {hint}a.k, COUNT(*)"; from_clause=f"FROM {rel('a')} a JOIN {rel('b')} b ON a.k=b.k JOIN {rel('c')} c ON b.k=c.k JOIN {rel('d')} d ON c.k=d.k"
    else:
        select=f"SELECT {hint}a.k, COUNT(*)"; from_clause=f"FROM {rel('a')} a JOIN {rel('b')} b ON a.k=b.k JOIN {rel('c')} c ON a.k=c.k JOIN {rel('d')} d ON b.k=d.k"
    if agg in ['group_by','group_by_after_join']:
        select = select if ('SUM' in select or 'COUNT' in select) else 'SELECT d1.nationkey, COUNT(*)'
        group=' GROUP BY 1' if 'SUM' not in select else ' GROUP BY f.key, d1.attr, d2.attr'
    elif agg=='distinct':
        select=select.replace('SELECT','SELECT DISTINCT',1); group=''
    elif agg=='expression_aggregate':
        if js in ['none', 'binary']:
            select='SELECT d1.nationkey, SUM(d1.acctbal * 1.08)'; group=' GROUP BY d1.nationkey'
        elif js in ['star', 'snowflake']:
            select='SELECT f.key, SUM(f.measure * 1.08)'; group=' GROUP BY f.key'
        else:
            select='SELECT a.k, SUM(a.acctbal * 1.08)'; group=' GROUP BY a.k'
    else: group=''
    q=f"{select}\n{from_clause}"
    if where: q+='\nWHERE '+' AND '.join(where)
    q+=group
    if order=='topn': q+='\nORDER BY 1 LIMIT 10'
    elif order=='order_by': q+='\nORDER BY 1'
    elif order=='limit': q+='\nLIMIT 10'
    elif order=='window_order': q='SELECT *, ROW_NUMBER() OVER (ORDER BY 1) AS rn FROM ('+q+') s'
    if control=='join_distribution_broadcast': q+='\n-- contract probe: join_distribution_type=BROADCAST'
    if control=='no_reorder_setting': q+='\n-- contract probe: join_reordering_strategy=NONE'
    return q+';'

def expand_rule_guards(rules_path:Optional[Path], domain:Dict[str,List[str]])->List[Assignment]:
    if not rules_path or not rules_path.exists(): return []
    partials=[]
    for line in rules_path.read_text().splitlines():
        if not line.strip(): continue
        r=json.loads(line); guard=r.get('guard',{})
        keys=[]; vals=[]; skip=False
        for k,v in guard.items():
            if k not in domain: skip=True; break
            if isinstance(v,list): vv=[x for x in v if x in domain[k]]
            elif v=='required': vv=[x for x in domain[k] if x not in ['none','not_applicable','unavailable','none_control']]
            else: vv=[v] if v in domain[k] else []
            if not vv: skip=True; break
            keys.append(k); vals.append(vv)
        if skip: continue
        for combo in itertools.product(*vals): partials.append(dict(zip(keys,combo)))
    return partials

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--features', type=Path, default=Path('benchmark/feature_domain.yaml'))
    ap.add_argument('--constraints', type=Path, default=Path('benchmark/validity_constraints.yaml'))
    ap.add_argument('--selected', type=Path, default=Path('benchmark/selected_3wise.yaml'))
    ap.add_argument('--out', type=Path, default=Path('benchmark/generated_probes.jsonl'))
    ap.add_argument('--coverage-out', type=Path, default=Path('evaluation/coverage_interactions.csv'))
    ap.add_argument('--rules', type=Path, default=None)
    ap.add_argument('-t','--strength', type=int, default=2)
    args=ap.parse_args()
    domain=load_yaml(args.features); constraints=load_constraints(args.constraints)
    base_specs=[list(fs) for fs in itertools.combinations(domain.keys(), args.strength)]
    selected_specs=load_selected(args.selected)
    specs=base_specs + selected_specs
    # Build finite universe and coverage denominator.
    universe=set(); coverage_rows=[]; completion_cache={}
    for fs in specs:
        name = (f'{args.strength}wise:' if len(fs)==args.strength else f'{len(fs)}wise:') + ','.join(fs)
        ints=interactions_for_features(fs,domain,constraints)
        coverage_rows.append({'coverage_target':name,'arity':len(fs),'valid_interactions':len(ints)})
        universe.update(ints)
    uncovered=set(universe); probes=[]; idx=0; assignment_seen=set()

    # Candidate generation: the initial implementation completed each uncovered
    # interaction independently, which was correct but unnecessarily large.  We
    # now build a deterministic candidate pool and run greedy set cover over the
    # same renderable interaction universe.  This keeps the denominator exactly
    # the same while reducing the benchmark size and making probe count a
    # meaningful efficiency metric rather than an artifact of interaction order.
    candidates = {}
    candidate_forced = {}
    def add_candidate(comp, forced=False):
        key=tuple(sorted(comp.items()))
        cov=covered_by_assignment(comp, specs) & universe
        if not cov:
            return
        candidates[key]=(comp,cov)
        candidate_forced[key]=candidate_forced.get(key, False) or bool(forced)

    for partial in expand_rule_guards(args.rules, domain):
        key=tuple(sorted(partial.items()))
        comp=completion_cache.get(key)
        if comp is None:
            comp=complete_assignment(partial,domain,constraints); completion_cache[key]=comp
        if comp is not None: add_candidate(comp, forced=True)
    for inter in sorted(list(universe)):
        comp=completion_cache.get(inter)
        if comp is None:
            comp=complete_assignment(dict(inter),domain,constraints); completion_cache[inter]=comp
        if comp is None: raise RuntimeError(f'No renderable assignment for interaction {inter}')
        add_candidate(comp, forced=False)

    # Include rule-forced completions first so that every grounded rule guard is
    # represented directly by at least one probe, then greedily cover the
    # remaining target interactions.  We use a lazy max-heap: gains are
    # recomputed only when a candidate reaches the heap top.
    selected=[]
    def select_key(key):
        nonlocal uncovered
        if key in assignment_seen: return
        comp,cov=candidates[key]
        assignment_seen.add(key); selected.append(key); uncovered -= cov
    for key in sorted(k for k,v in candidate_forced.items() if v):
        select_key(key)

    import heapq
    heap=[]
    for key,(comp,cov) in candidates.items():
        if key in assignment_seen: continue
        gain=len(cov & uncovered)
        if gain>0:
            heapq.heappush(heap, (-gain, key))
    while uncovered:
        if not heap:
            raise RuntimeError(f'Internal error: {len(uncovered)} interactions uncovered')
        neg_gain,key=heapq.heappop(heap)
        if key in assignment_seen: continue
        comp,cov=candidates[key]
        actual=len(cov & uncovered)
        if actual<=0: continue
        if actual != -neg_gain:
            heapq.heappush(heap, (-actual, key)); continue
        select_key(key)

    # Emit probes.  Coverage listed per probe is the marginal coverage after
    # previous probes, which makes redundancy visible in the artifact.
    covered_so_far=set()
    for key in selected:
        comp,cov=candidates[key]
        idx+=1
        marginal=cov-covered_so_far
        covered_so_far |= cov
        probes.append({'probe_id':f'P{idx:04d}','feature_vector':comp,'sql_skeleton':render_sql(comp,idx),'covered_interactions':[str(tuple(i)) for i in sorted(marginal)],'forced_by_rule_guard':bool(candidate_forced.get(key,False))})
    uncovered=universe-covered_so_far
    if uncovered: raise RuntimeError(f'Internal error: {len(uncovered)} interactions uncovered')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('w') as f:
        for p in probes: f.write(json.dumps(p, ensure_ascii=False)+'\n')
    args.coverage_out.parent.mkdir(parents=True, exist_ok=True)
    import csv
    with args.coverage_out.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['coverage_target','arity','valid_interactions','generated_probes','total_unique_interactions','coverage'])
        writer.writeheader()
        for row in coverage_rows:
            out = dict(row)
            out['generated_probes'] = len(probes)
            out['total_unique_interactions'] = len(universe)
            out['coverage'] = 1.0
            writer.writerow(out)
        writer.writerow({'coverage_target':'ALL','arity':'NA','valid_interactions':len(universe),'generated_probes':len(probes),'total_unique_interactions':len(universe),'coverage':1.0})
    print(f"Generated {len(probes)} probes covering {len(universe)} unique interactions ({len(base_specs)} pairwise targets + {len(selected_specs)} selected targets)")
if __name__=='__main__': main()
