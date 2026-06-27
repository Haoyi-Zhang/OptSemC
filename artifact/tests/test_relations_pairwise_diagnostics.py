#!/usr/bin/env python3
from optsemc.relations import Relation, equivalence_relation, equivalence_closure, partition_refines, quotient_statistics

def test_relation_identity_3_1():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_1():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_2():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_2():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_3():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_3():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_4():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_4():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_5():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_5():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_6():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_6():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_7():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_7():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_8():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_8():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_9():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_9():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_10():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_10():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_11():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_11():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_12():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_12():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_13():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_13():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_14():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_14():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_15():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_15():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_16():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_16():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_17():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_17():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_18():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_18():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_19():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_19():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_20():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_20():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_21():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_21():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_22():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_22():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_23():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_23():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_24():
    nodes = tuple(range(9))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_24():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_25():
    nodes = tuple(range(3))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_25():
    nodes = tuple(range(8))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_26():
    nodes = tuple(range(4))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_26():
    nodes = tuple(range(9))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_27():
    nodes = tuple(range(5))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_27():
    nodes = tuple(range(4))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_28():
    nodes = tuple(range(6))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_28():
    nodes = tuple(range(5))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_29():
    nodes = tuple(range(7))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_29():
    nodes = tuple(range(6))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

def test_relation_identity_3_30():
    nodes = tuple(range(8))
    rel = Relation.identity(nodes)
    assert rel.is_reflexive()
    assert rel.is_symmetric()
    assert rel.is_transitive()
    assert rel.is_equivalence()

def test_relation_closure_3_30():
    nodes = tuple(range(7))
    rel = Relation.empty(nodes).with_edge(nodes[0], nodes[1])
    closed = equivalence_closure(rel)
    assert closed.is_equivalence()
    assert closed.contains(nodes[0], nodes[1])
    assert closed.contains(nodes[1], nodes[0])

