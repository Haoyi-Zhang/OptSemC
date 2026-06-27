#!/usr/bin/env python3
from optsemc.minimization import exact_set_cover, greedy_set_cover, exact_hitting_set, delta_minimize, minimal_by_inclusion, maximal_by_inclusion

def test_set_cover_case_3_1():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_1():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_2():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_2():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_3():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_3():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_4():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_4():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_5():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_5():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_6():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_6():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_7():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_7():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_8():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_8():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_9():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_9():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_10():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_10():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_11():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_11():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_12():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_12():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_13():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_13():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_14():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_14():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_15():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_15():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_16():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_16():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_17():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_17():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_18():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_18():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_19():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_19():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_20():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_20():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_21():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_21():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_22():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_22():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_23():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_23():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_24():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_24():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_25():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_25():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_26():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_26():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_27():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_27():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_28():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_28():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_29():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_29():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_30():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_30():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_31():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_31():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_32():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_32():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_33():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_33():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_34():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_34():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_3_35():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_3_35():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

