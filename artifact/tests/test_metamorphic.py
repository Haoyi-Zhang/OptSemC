from optsemc.semantics import evidence_signature
from optsemc.metamorphic import (
    check_determinism, check_projection_idempotence, check_refinement_monotonicity,
    check_extra_field_monotonicity, check_negative_control_strictness,
)


def _toy_maps():
    return {
        ('A', 'P1'): evidence_signature({'Join|choose|hash|physical|local|compile|plan': 'MAY'}),
        ('B', 'P1'): evidence_signature({'Join|choose|hash|logical|remote|compile|plan': 'MAY'}),
        ('A', 'P2'): evidence_signature({'Filter|pushdown|pred|logical|remote|compile|plan': 'MAY'}),
        ('B', 'P2'): evidence_signature({'Filter|pushdown|pred|logical|remote|compile|plan': 'MAY'}),
    }


def test_metamorphic_determinism_passes_on_toy_maps():
    rows = check_determinism(_toy_maps(), ('keyword', 'strict'))
    assert all(row.passed for row in rows)


def test_metamorphic_idempotence_passes_on_toy_maps():
    rows = check_projection_idempotence(_toy_maps(), ('keyword', 'strict'))
    assert all(row.passed for row in rows)


def test_metamorphic_refinement_passes_on_toy_maps():
    rows = check_refinement_monotonicity(_toy_maps(), ('A', 'B'), ('P1', 'P2'))
    assert all(row.passed for row in rows)


def test_extra_field_monotonicity_passes_on_toy_maps():
    rows = check_extra_field_monotonicity(_toy_maps(), ('A', 'B'), ('P1', 'P2'), 'keyword', ('layer', 'placement'))
    assert all(row.passed for row in rows)


def test_negative_control_strictness_passes_on_toy_maps():
    rows = check_negative_control_strictness(_toy_maps(), ('A', 'B'), ('P1', 'P2'))
    assert rows[0].passed


def test_extra_field_monotonicity_reduces_or_preserves_equivalence_count():
    rows = check_extra_field_monotonicity(_toy_maps(), ('A', 'B'), ('P1', 'P2'), 'keyword', ('layer', 'placement'))
    counts = [int(row.details.split('=')[1]) for row in rows]
    assert counts == sorted(counts, reverse=True)
