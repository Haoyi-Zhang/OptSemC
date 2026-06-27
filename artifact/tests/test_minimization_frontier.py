#!/usr/bin/env python3
from optsemc.minimization import exact_set_cover, greedy_set_cover, exact_hitting_set, delta_minimize, minimal_by_inclusion, maximal_by_inclusion

def test_set_cover_case_1_1():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_1():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_2():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_2():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_3():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_3():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_4():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_4():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_5():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_5():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_6():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_6():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_7():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_7():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_8():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_8():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_9():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_9():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_10():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_10():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_11():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_11():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_12():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_12():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_13():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_13():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_14():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_14():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_15():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_15():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_16():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_16():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_17():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_17():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_18():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_18():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_19():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_19():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_20():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_20():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_21():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_21():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_22():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_22():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_23():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_23():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_24():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_24():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_25():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_25():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_26():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_26():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_27():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_27():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_28():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_28():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_29():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_29():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_30():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_30():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_31():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_31():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_32():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_32():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_33():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_33():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_34():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_34():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_1_35():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_1_35():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

