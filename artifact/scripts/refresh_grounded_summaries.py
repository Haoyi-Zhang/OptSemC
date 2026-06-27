#!/usr/bin/env python3
"""Regenerate grounded corpus summary files from the current verified rules.

This prevents stale package-summary CSVs from surviving after rule expansion.
The script is intentionally small and dependency-free so it can run inside the
mainline integrity suite.
"""
from __future__ import annotations
import csv, json, hashlib
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = ROOT / 'grounded'
RULES = G / 'verified_rules.jsonl'
SEGMENTS = G / 'verified_segments.jsonl'
SOURCES = G / 'verified_sources.csv'


def read_jsonl(path: Path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def write_counter(path: Path, counts: Counter):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['key', 'count'])
        w.writeheader()
        for key in sorted(counts):
            w.writerow({'key': key, 'count': counts[key]})


def main() -> None:
    rules = list(read_jsonl(RULES))
    segments = list(read_jsonl(SEGMENTS))
    with SOURCES.open(newline='', encoding='utf-8') as f:
        sources = list(csv.DictReader(f))

    engine_counts = Counter(r['engine'] for r in rules)
    state_counts = Counter(r.get('state', '') for r in rules)
    source_counts = Counter(r.get('evidence', {}).get('source_id', '') for r in rules)

    write_counter(G / 'engine_rule_counts.csv', engine_counts)
    write_counter(G / 'state_rule_counts.csv', state_counts)
    write_counter(G / 'source_rule_counts.csv', source_counts)

    operators = {r['action']['operator'] for r in rules}
    kinds = {r['action']['kind'] for r in rules}
    variants = {r['action'].get('variant', '') for r in rules}
    layers = {r['action']['layer'] for r in rules}
    placements = {r['action']['placement'] for r in rules}
    decision_times = {r['action']['decision_time'] for r in rules}
    observability = {r['action']['observability'] for r in rules}
    engines = set(engine_counts)
    states = set(state_counts)

    summary = [
        ('verified_rules', len(rules)),
        ('verified_segments', len(segments)),
        ('verified_sources', len(sources)),
        ('engines_covered', len(engines)),
        ('states_covered', len(states)),
        ('operators_covered', len(operators)),
        ('action_kinds_covered', len(kinds)),
        ('variants_covered', len(variants)),
        ('layers_covered', len(layers)),
        ('placements_covered', len(placements)),
        ('decision_times_covered', len(decision_times)),
        ('observability_modes_covered', len(observability)),
        ('grounding_status', 'grounded_mainline_current'),
    ]
    with (G / 'verified_core_summary.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['metric', 'value'])
        w.writeheader()
        for metric, value in summary:
            w.writerow({'metric': metric, 'value': value})

    # Regenerate grounded source hashes from the current verified segments.
    by_source = defaultdict(list)
    for seg in segments:
        by_source[seg['source_id']].append(seg)
    with (G / 'grounded_source_hashes.csv').open('w', newline='', encoding='utf-8') as f:
        fieldnames = ['source_id', 'segment_count', 'hash_type', 'sha256', 'bytes']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for source_id in sorted(by_source):
            payload = '\n'.join(json.dumps(s, sort_keys=True, ensure_ascii=False) for s in sorted(by_source[source_id], key=lambda x: x['segment_id']))
            b = payload.encode('utf-8')
            w.writerow({
                'source_id': source_id,
                'segment_count': len(by_source[source_id]),
                'hash_type': 'verified_segments_sha256',
                'sha256': hashlib.sha256(b).hexdigest(),
                'bytes': len(b),
            })
    print(f'Refreshed grounded summaries: rules={len(rules)}, sources={len(sources)}, segments={len(segments)}')


if __name__ == '__main__':
    main()
