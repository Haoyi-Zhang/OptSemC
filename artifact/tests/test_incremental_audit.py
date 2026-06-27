from optsemc.incremental import incremental_audit, probe_delta
from optsemc.semantics import ActionAtom


def atom(operator="Join", kind="reorder", variant="join_order", layer="logical_rewrite", placement="local_engine", state="MAY"):
    return ActionAtom(operator, kind, variant, layer, placement, "compile_time", "estimated_physical_plan", state)


def test_probe_delta_counts_false_equivalence_for_operator_only():
    maps = {
        ("A", "P1"): frozenset({atom(layer="logical_rewrite")}),
        ("B", "P1"): frozenset({atom(layer="physical_planning")}),
    }
    delta = probe_delta(maps, ("A", "B"), "P1", "operator_only")
    assert delta.comparisons == 1
    assert delta.projected_equivalences == 1
    assert delta.false_equivalences == 1


def test_incremental_audit_matches_full_prefix_counts():
    maps = {
        ("A", "P1"): frozenset({atom(layer="logical_rewrite")}),
        ("B", "P1"): frozenset({atom(layer="physical_planning")}),
        ("A", "P2"): frozenset({atom(operator="Filter", kind="pushdown", variant="predicate")}),
        ("B", "P2"): frozenset({atom(operator="Filter", kind="pushdown", variant="predicate")}),
    }
    rows, deltas = incremental_audit(maps, ("A", "B"), ("P1", "P2"), ("strict", "operator_only"), (1, 2))
    assert len(rows) == 4
    assert len(deltas) == 4
    assert all(row.drift == 0 for row in rows)
    _operator = [row for row in rows if row.projection == "operator_only" and row.probes == 2][0]
    assert _operator.full_false_equivalences == 1
