#!/usr/bin/env python3
import csv, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def count_jsonl(path):
    with (ROOT/path).open(encoding='utf-8') as f:
        return sum(1 for line in f if line.strip())

def test_grounded_corpus_size():
    assert count_jsonl('grounded/verified_rules.jsonl') >= 287
    assert count_jsonl('grounded/verified_segments.jsonl') >= 287

def test_no_grounded_conflicts():
    assert count_jsonl('evaluation/grounded_conflicts.jsonl') == 0

def test_repair_certificate_exists():
    rows=list(csv.DictReader((ROOT/'evaluation/grounded/repair_certificate_summary.csv').open()))
    methods={r['method'] for r in rows}
    assert {'keyword','yesno','operator_only'} <= methods
    for r in rows:
        assert int(r['false_equivalences']) >= 0
        if r['method'] in {'keyword','operator_only'}:
            assert int(r['minimal_universal_repair_size']) >= 1

def test_conditional_trap_nonzero():
    rows=list(csv.DictReader((ROOT/'evaluation/grounded/conditional_trap_rate.csv').open()))
    d={r['method']: float(r['conditional_false_equivalence_rate']) for r in rows}
    assert d['keyword'] > 0
    assert d['operator_only'] > 0

def test_semantic_repair_basis_exists_and_is_interpretable():
    rows=list(csv.DictReader((ROOT/'evaluation/grounded/semantic_repair_basis.csv').open()))
    by={r['scope']:r for r in rows}
    assert by['keyword']['minimal_semantic_repair_size'] == '1'
    assert 'placement' in by['keyword']['minimal_semantic_repair_sets']
    assert by['operator_only']['minimal_semantic_repair_size'] == '1'
    assert 'layer' in by['operator_only']['minimal_semantic_repair_sets']
    assert int(by['all_projections']['minimal_semantic_repair_size']) <= 2
