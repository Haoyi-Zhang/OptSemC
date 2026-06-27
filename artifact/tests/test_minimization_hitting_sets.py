#!/usr/bin/env python3
from optsemc.minimization import exact_set_cover, greedy_set_cover, exact_hitting_set, delta_minimize, minimal_by_inclusion, maximal_by_inclusion

def test_set_cover_case_2_1():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_1():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_2():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_2():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_3():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_3():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_4():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_4():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_5():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_5():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_6():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_6():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_7():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_7():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_8():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_8():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_9():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_9():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_10():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_10():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_11():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_11():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_12():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_12():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_13():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_13():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_14():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_14():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_15():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_15():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_16():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_16():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_17():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_17():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_18():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_18():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_19():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_19():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_20():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_20():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_21():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_21():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_22():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_22():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_23():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_23():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_24():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_24():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_25():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_25():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_26():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_26():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_27():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_27():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_28():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_28():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_29():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_29():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_30():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_30():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_31():
    universe = frozenset(range(5))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_31():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_32():
    universe = frozenset(range(6))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_32():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_33():
    universe = frozenset(range(7))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_33():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_34():
    universe = frozenset(range(8))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_34():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

def test_set_cover_case_2_35():
    universe = frozenset(range(4))
    sets = {"all": universe, "first": frozenset([0, 1]), "last": frozenset(list(universe)[-2:])}
    sol = exact_set_cover(universe, sets)
    assert sol.optimal
    assert sol.uncovered == 0
    assert sol.cardinality == 1

def test_hitting_set_case_2_35():
    families = [{"a", "b"}, {"b", "c"}, {"b", "d"}]
    hits = exact_hitting_set(families, ("a", "b", "c", "d"))
    assert ("b",) in hits
    assert len(hits[0]) == 1

