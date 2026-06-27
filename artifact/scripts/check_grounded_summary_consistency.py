#!/usr/bin/env python3
"""Check that grounded summary CSVs match current verified rules/sources/segments."""
from __future__ import annotations
import csv, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = ROOT / 'grounded'
E = ROOT / 'evaluation'
OUT = E / 'grounded_summary_consistency.csv'


def read_jsonl(path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                yield json.loads(line)


def read_counter(path):
    with path.open(newline='', encoding='utf-8') as f:
        return {r['key']: int(r['count']) for r in csv.DictReader(f)}


def read_summary(path):
    with path.open(newline='', encoding='utf-8') as f:
        return {r['metric']: r['value'] for r in csv.DictReader(f)}


def add(rows, check, passed, details=''):
    rows.append({'check': check, 'passed': str(bool(passed)).lower(), 'details': details})


def main():
    rules=list(read_jsonl(G/'verified_rules.jsonl'))
    segments=list(read_jsonl(G/'verified_segments.jsonl'))
    with (G/'verified_sources.csv').open(newline='', encoding='utf-8') as f:
        sources=list(csv.DictReader(f))
    rows=[]
    engine=Counter(r['engine'] for r in rules)
    state=Counter(r['state'] for r in rules)
    source=Counter(r['evidence']['source_id'] for r in rules)
    add(rows, 'engine_rule_counts_current', read_counter(G/'engine_rule_counts.csv') == dict(engine), f'expected={dict(engine)}')
    add(rows, 'state_rule_counts_current', read_counter(G/'state_rule_counts.csv') == dict(state), f'expected={dict(state)}')
    add(rows, 'source_rule_counts_current', read_counter(G/'source_rule_counts.csv') == dict(source), f'sources={len(source)}')
    summ=read_summary(G/'verified_core_summary.csv')
    add(rows, 'summary_rules_current', summ.get('verified_rules') == str(len(rules)), f"summary={summ.get('verified_rules')} actual={len(rules)}")
    add(rows, 'summary_segments_current', summ.get('verified_segments') == str(len(segments)), f"summary={summ.get('verified_segments')} actual={len(segments)}")
    add(rows, 'summary_sources_current', summ.get('verified_sources') == str(len(sources)), f"summary={summ.get('verified_sources')} actual={len(sources)}")
    add(rows, 'summary_status_current', summ.get('grounding_status') == 'grounded_mainline_current', summ.get('grounding_status',''))
    # source hashes must cover exactly verified sources.
    hash_ids=set(read_counter(G/'grounded_source_hashes.csv')) if False else None
    with (G/'grounded_source_hashes.csv').open(newline='', encoding='utf-8') as f:
        hash_rows=list(csv.DictReader(f))
    source_ids={s['source_id'] for s in sources}
    hash_source_ids={r['source_id'] for r in hash_rows}
    add(rows, 'source_hashes_cover_current_sources', source_ids == hash_source_ids, f'missing={sorted(source_ids-hash_source_ids)} extra={sorted(hash_source_ids-source_ids)}')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=['check','passed','details'])
        w.writeheader(); w.writerows(rows)
    passed=sum(r['passed']=='true' for r in rows)
    print(f'Grounded summary consistency: {passed}/{len(rows)} passed')
    for r in rows:
        if r['passed']!='true':
            print('FAIL', r['check'], r['details'])
    if passed != len(rows): sys.exit(1)

if __name__=='__main__':
    main()
