from pathlib import Path

from optsemc.corpus import load_contract_maps, load_probe_objects, load_rule_objects
from optsemc.guards import guard_applies, invalid_guard_dimensions, support_table
from optsemc.repair_stability import evaluate_feature_holdout

ROOT = Path(__file__).resolve().parents[1]


def test_guard_list_literals_are_finite_disjunctions():
    assert guard_applies({'predicate_class': "['simple', 'conjunctive']"}, {'predicate_class': 'simple'})
    assert guard_applies({'predicate_class': "['simple', 'conjunctive']"}, {'predicate_class': 'conjunctive'})
    assert not guard_applies({'predicate_class': "['simple', 'conjunctive']"}, {'predicate_class': 'none'})


def test_every_grounded_guard_has_probe_support():
    rules = load_rule_objects(ROOT)
    probes = load_probe_objects(ROOT)
    supports = support_table(rules, probes)
    assert len(supports) == 287
    assert min(s.support_count for s in supports) > 0
    assert not invalid_guard_dimensions(rules, probes)


def test_feature_holdout_robust_basis_resolves_headline_witnesses():
    cm = load_contract_maps(ROOT)
    probes = load_probe_objects(ROOT)
    rows = evaluate_feature_holdout(cm, probes)
    assert len(rows) >= 15
    assert {row.method for row in rows} == {'keyword', 'yesno', 'operator_only'}
    assert sum(row.heldout_false for row in rows) > 0
    assert sum(row.robust_unresolved for row in rows) == 0
