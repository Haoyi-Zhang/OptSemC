from pathlib import Path
import csv

from optsemc.lattice import enumerate_field_subsets, project_signature_fields
from optsemc.semantics import ActionAtom

ROOT = Path(__file__).resolve().parents[1]


def read_csv(rel):
    with (ROOT / rel).open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def test_field_subset_count_is_exhaustive():
    subsets = enumerate_field_subsets()
    assert len(subsets) == 256
    assert subsets[0].key == 'none'
    assert subsets[-1].key == 'operator+kind+variant+layer+placement+decision_time+observability+state'


def test_empty_field_projection_collapses_supported_atoms():
    sig = frozenset({
        ActionAtom('Filter', 'pushdown', 'predicate', 'logical_rewrite', 'local_engine', 'compile_time', 'logical_plan', 'MAY'),
        ActionAtom('Join', 'delegate', 'join', 'physical_plan', 'connector_source', 'compile_time', 'physical_plan', 'MAY'),
    })
    assert project_signature_fields(sig, ()) == frozenset({('_evidenced_',)})


def test_resolution_lattice_has_semantic_no_variant_frontier():
    rows = {r['metric']: r['value'] for r in read_csv('evaluation/projection_resolution_semantic_summary.csv')}
    assert rows['semantic_no_variant_subsets'] == '128'
    assert rows['semantic_no_variant_minimum_safe_field_count'] == '2'
    assert 'operator+layer' in rows['semantic_no_variant_minimum_safe_field_sets']
    assert 'kind+placement' in rows['semantic_no_variant_minimum_safe_field_sets']


def test_resolution_lattice_counterexample_cover_is_checked():
    rows = {r['check']: r['passed'] for r in read_csv('evaluation/projection_resolution_check.csv')}
    assert rows['counterexample_cover_covers_all_unsafe_subsets'] == 'true'
    assert rows['counterexample_cover_witnesses_verify'] == 'true'
