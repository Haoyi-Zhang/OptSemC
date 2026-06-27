#!/usr/bin/env python3
from optsemc.relations import Relation, equivalence_relation, equivalence_closure, partition_refines, quotient_statistics

def test_relation_identity_4_1():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_1():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_2():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_2():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_3():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_3():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_4():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_4():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_5():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_5():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_6():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_6():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_7():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_7():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_8():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_8():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_9():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_9():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_10():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_10():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_11():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_11():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_12():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_12():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_13():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_13():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_14():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_14():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_15():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_15():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_16():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_16():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_17():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_17():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_18():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_18():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_19():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_19():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_20():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_20():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_21():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_21():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_22():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_22():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_23():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_23():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_24():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_24():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_25():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_25():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_26():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_26():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_27():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_27():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_28():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_28():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_29():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_29():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_4_30():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_4_30():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

