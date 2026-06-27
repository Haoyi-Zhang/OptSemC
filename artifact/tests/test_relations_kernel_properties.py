#!/usr/bin/env python3
from optsemc.relations import Relation, equivalence_relation, equivalence_closure, partition_refines, quotient_statistics

def test_relation_identity_1_1():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_1():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_2():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_2():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_3():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_3():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_4():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_4():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_5():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_5():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_6():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_6():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_7():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_7():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_8():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_8():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_9():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_9():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_10():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_10():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_11():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_11():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_12():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_12():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_13():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_13():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_14():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_14():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_15():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_15():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_16():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_16():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_17():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_17():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_18():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_18():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_19():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_19():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_20():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_20():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_21():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_21():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_22():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_22():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_23():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_23():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_24():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_24():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_25():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_25():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_26():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_26():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_27():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_27():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_28():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_28():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_29():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_29():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_1_30():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_1_30():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

