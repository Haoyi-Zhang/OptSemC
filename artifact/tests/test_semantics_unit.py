#!/usr/bin/env python3
from itertools import product

STATES = ["UNSPEC", "MAY", "MUST", "MUST_NOT"]
CONFLICT = "CONFLICT"
JOIN = {
    ("UNSPEC", "UNSPEC"): "UNSPEC", ("UNSPEC", "MAY"): "MAY", ("UNSPEC", "MUST"): "MUST", ("UNSPEC", "MUST_NOT"): "MUST_NOT",
    ("MAY", "UNSPEC"): "MAY", ("MAY", "MAY"): "MAY", ("MAY", "MUST"): "MUST", ("MAY", "MUST_NOT"): CONFLICT,
    ("MUST", "UNSPEC"): "MUST", ("MUST", "MAY"): "MUST", ("MUST", "MUST"): "MUST", ("MUST", "MUST_NOT"): CONFLICT,
    ("MUST_NOT", "UNSPEC"): "MUST_NOT", ("MUST_NOT", "MAY"): CONFLICT, ("MUST_NOT", "MUST"): CONFLICT, ("MUST_NOT", "MUST_NOT"): "MUST_NOT",
}

def join(a,b):
    if a == CONFLICT or b == CONFLICT:
        return CONFLICT
    return JOIN[(a,b)]

def test_commutative():
    for a,b in product(STATES, repeat=2):
        assert join(a,b) == join(b,a)

def test_idempotent():
    for a in STATES:
        assert join(a,a) == a

def test_unspec_identity():
    for a in STATES:
        assert join("UNSPEC", a) == a

def test_associative():
    for a,b,c in product(STATES, repeat=3):
        assert join(join(a,b), c) == join(a, join(b,c))

def test_contradictions():
    assert join("MAY", "MUST_NOT") == CONFLICT
    assert join("MUST", "MUST_NOT") == CONFLICT
    assert join("MUST", "MAY") == "MUST"
