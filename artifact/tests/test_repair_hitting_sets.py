#!/usr/bin/env python3
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with (ROOT / path).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def test_repair_hitting_sets_match_direct_enumeration():
    rr = rows('evaluation/repair_hitting_set_check.csv')
    assert rr
    assert all(r['passed'] == 'true' for r in rr)


def test_singleton_separability_is_grounded_for_all_witnesses():
    rr = rows('evaluation/grounded/repair_hitting_sets.csv')
    assert rr
    assert all(int(r['no_singleton_separator_witnesses']) == 0 for r in rr)


def test_layer_placement_is_core_semantic_basis():
    rr = rows('evaluation/grounded/repair_hitting_sets.csv')
    core = [r for r in rr if r['scope'] == 'all_projections' and r['field_universe'] == 'core_semantic_state_free']
    assert len(core) == 1
    assert int(core[0]['minimum_hitting_set_size']) == 2
    assert 'layer+placement' in core[0]['example_minimum_hitting_sets']
