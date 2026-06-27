#!/usr/bin/env python3
"""Fast leave-one-source-out robustness for grounded OptSem-C projections."""
from __future__ import annotations
import csv, json, itertools
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METHODS = ["keyword", "yesno", "operator_only"]
CONFLICT = "CONFLICT"
JOIN = {
    ("UNSPEC", "UNSPEC"): "UNSPEC", ("UNSPEC", "MAY"): "MAY", ("UNSPEC", "MUST"): "MUST", ("UNSPEC", "MUST_NOT"): "MUST_NOT",
    ("MAY", "UNSPEC"): "MAY", ("MAY", "MAY"): "MAY", ("MAY", "MUST"): "MUST", ("MAY", "MUST_NOT"): CONFLICT,
    ("MUST", "UNSPEC"): "MUST", ("MUST", "MAY"): "MUST", ("MUST", "MUST"): "MUST", ("MUST", "MUST_NOT"): CONFLICT,
    ("MUST_NOT", "UNSPEC"): "MUST_NOT", ("MUST_NOT", "MAY"): CONFLICT, ("MUST_NOT", "MUST"): CONFLICT, ("MUST_NOT", "MUST_NOT"): "MUST_NOT",
}

def read_jsonl(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def join_state(a,b):
    if a == CONFLICT or b == CONFLICT:
        return CONFLICT
    return JOIN[(a,b)]

def merge_states(states):
    s = 'UNSPEC'
    for st in states:
        s = join_state(s, st)
        if s == CONFLICT:
            break
    return s

def split_action(action_key, state):
    parts = action_key.split('|')
    if len(parts) == 6:
        op, kind, layer, placement, decision_time, observability = parts
        variant = ''
    else:
        parts = (parts + ['']*7)[:7]
        op, kind, variant, layer, placement, decision_time, observability = parts
    return (op, kind, variant, layer, placement, decision_time, observability, state)

def base_atom(atom_tuple, method):
    op, kind, variant, layer, placement, decision_time, observability, state = atom_tuple
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

def main():
    rule_src = {}
    source_counts = defaultdict(int)
    for r in read_jsonl(ROOT/'grounded/verified_rules.jsonl'):
        sid = r['evidence']['source_id']
        rule_src[r['rule_id']] = sid
        source_counts[sid] += 1
    sources = sorted(source_counts)
    # key -> action -> source -> list states
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    engines=set(); probes=set()
    for r in read_jsonl(ROOT/'evaluation/grounded_applicable_rules.jsonl'):
        sid = rule_src.get(r['rule_id'])
        if sid is None: continue
        key=(r['engine'], r['probe_id'])
        data[key][r['action_key']][sid].append(r['state'])
        engines.add(r['engine']); probes.add(r['probe_id'])
    engines=sorted(engines); probes=sorted(probes)
    key_index={k:i for i,k in enumerate(sorted(data))}
    # atom interning
    atom_to_id={}; id_to_atom=[]
    def atom_id(action_key, state):
        t=split_action(action_key,state)
        if t not in atom_to_id:
            atom_to_id[t]=len(id_to_atom); id_to_atom.append(t)
        return atom_to_id[t]
    full_sigs=[frozenset() for _ in range(len(key_index))]
    changes={sid:{} for sid in sources}
    for key, actions in data.items():
        idx=key_index[key]
        full_atoms=set()
        per_source_delta=defaultdict(lambda: [set(), set()])  # sid -> [remove, add]
        for ak, bysrc in actions.items():
            source_states={sid: merge_states(states) for sid, states in bysrc.items()}
            full_state=merge_states(source_states.values())
            full_atom=None
            if full_state != 'UNSPEC':
                full_atom=atom_id(ak, full_state); full_atoms.add(full_atom)
            for sid in source_states:
                other=[st for ss, st in source_states.items() if ss != sid]
                without=merge_states(other) if other else 'UNSPEC'
                if without != full_state:
                    if full_atom is not None: per_source_delta[sid][0].add(full_atom)
                    if without != 'UNSPEC': per_source_delta[sid][1].add(atom_id(ak, without))
        full_sigs[idx]=frozenset(full_atoms)
        for sid,(rem,add) in per_source_delta.items():
            changes[sid][idx]=(frozenset(rem), frozenset(add))
    # projection cache by signature object value
    proj_cache={}
    def project_sig(sig, method):
        k=(method,sig)
        if k in proj_cache: return proj_cache[k]
        out=frozenset(base_atom(id_to_atom[i], method) for i in sig)
        proj_cache[k]=out
        return out
    # precompute key lookup per engine/probe
    empty=frozenset()
    key_idx={(e,p): key_index.get((e,p), -1) for e in engines for p in probes}
    pairs=list(itertools.combinations(engines,2))
    def get_sig_for_source(src, idx):
        if idx < 0: return empty
        base=full_sigs[idx]
        if src is None: return base
        delta=changes.get(src,{}).get(idx)
        if not delta: return base
        rem,add=delta
        return frozenset((base - rem) | add)
    rows=[]
    for src in [None]+sources:
        # materialize projected ids per key/method lazily via dicts per method/source
        proj_by_method={m:{} for m in METHODS}
        for method in METHODS:
            projected=true_eq=false_eq=0
            cache=proj_by_method[method]
            for p in probes:
                for e1,e2 in pairs:
                    idx1=key_idx[(e1,p)]; idx2=key_idx[(e2,p)]
                    s1=get_sig_for_source(src, idx1); s2=get_sig_for_source(src, idx2)
                    if idx1 not in cache: cache[idx1]=project_sig(s1, method)
                    # NOTE: idx == -1 means empty; cache key -1 is ok because empty signature invariant.
                    if idx2 not in cache: cache[idx2]=project_sig(s2, method)
                    if cache[idx1] == cache[idx2]:
                        projected += 1
                        if s1 == s2: true_eq += 1
                        else: false_eq += 1
            rows.append({
                'removed_source': src or '<none>',
                'removed_rules': 0 if src is None else source_counts[src],
                'method': method,
                'comparisons': len(probes)*len(pairs),
                'projected_equivalences': projected,
                'true_equivalences': true_eq,
                'false_equivalences': false_eq,
                'conditional_false_equivalence_rate': f'{(false_eq/projected if projected else 0):.6f}',
                'unconditional_false_equivalence_rate': f'{(false_eq/(len(probes)*len(pairs))):.6f}',
            })
    outdir=ROOT/'evaluation/grounded'
    fields=['removed_source','removed_rules','method','comparisons','projected_equivalences','true_equivalences','false_equivalences','conditional_false_equivalence_rate','unconditional_false_equivalence_rate']
    with open(outdir/'source_robustness.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    summary=[]
    for method in METHODS:
        full=next(r for r in rows if r['removed_source']=='<none>' and r['method']==method)
        sub=[r for r in rows if r['removed_source']!='<none>' and r['method']==method]
        false_vals=[int(r['false_equivalences']) for r in sub]
        rate_vals=[float(r['conditional_false_equivalence_rate']) for r in sub]
        summary.append({
            'method':method,
            'full_false_equivalences':full['false_equivalences'],
            'full_conditional_rate':full['conditional_false_equivalence_rate'],
            'leave_one_source_runs':len(sub),
            'min_false_equivalences':min(false_vals) if false_vals else 0,
            'max_false_equivalences':max(false_vals) if false_vals else 0,
            'min_conditional_rate':f'{(min(rate_vals) if rate_vals else 0):.6f}',
            'max_conditional_rate':f'{(max(rate_vals) if rate_vals else 0):.6f}',
            'runs_with_nonzero_false_equivalences':sum(1 for v in false_vals if v>0),
        })
    with open(outdir/'source_robustness_summary.csv','w',newline='',encoding='utf-8') as f:
        fields=list(summary[0].keys()); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(summary)
    print(f'Wrote fast source robustness for {len(sources)} sources and {len(probes)} probes')
if __name__ == '__main__': main()
