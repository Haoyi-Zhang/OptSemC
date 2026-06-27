"""Executable finite proof obligations for the OptSem-C semantics."""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Callable, Iterable, Mapping, Sequence

from .semantics import STATE_JOIN, join_state, ActionAtom, ContractSignature
from .projections import project_signature
from .lattice import powerset

STATES = tuple(STATE_JOIN.keys())


@dataclass(frozen=True)
class ObligationResult:
    theorem: str
    obligation: str
    passed: bool
    details: str = ""

    def as_row(self) -> dict[str, str]:
        return {"theorem": self.theorem, "obligation": self.obligation, "passed": str(self.passed).lower(), "details": self.details}


def state_join_obligations() -> list[ObligationResult]:
    rows: list[ObligationResult] = []
    comm_bad = [(a, b) for a, b in itertools.product(STATES, repeat=2) if join_state(a, b) != join_state(b, a)]
    rows.append(ObligationResult("state_join_semilattice", "commutative", not comm_bad, str(comm_bad[:3])))
    idem_bad = [a for a in STATES if join_state(a, a) != a]
    rows.append(ObligationResult("state_join_semilattice", "idempotent", not idem_bad, str(idem_bad[:3])))
    ident_bad = [a for a in STATES if join_state(a, "UNSPEC") != a or join_state("UNSPEC", a) != a]
    rows.append(ObligationResult("state_join_semilattice", "unspec_identity", not ident_bad, str(ident_bad[:3])))
    assoc_bad = []
    for a, b, c in itertools.product(STATES, repeat=3):
        left = join_state(join_state(a, b), c)
        right = join_state(a, join_state(b, c))
        if left != right:
            assoc_bad.append((a, b, c, left, right))
    rows.append(ObligationResult("state_join_semilattice", "associative", not assoc_bad, str(assoc_bad[:3])))
    conflict_bad = [a for a in STATES if join_state("CONFLICT", a) != "CONFLICT" or join_state(a, "CONFLICT") != "CONFLICT"]
    rows.append(ObligationResult("state_join_semilattice", "conflict_absorbing", not conflict_bad, str(conflict_bad[:3])))
    return rows


def projection_determinism_obligations(signatures: Sequence[ContractSignature], methods: Sequence[str]) -> list[ObligationResult]:
    rows: list[ObligationResult] = []
    for method in methods:
        bad = 0
        for sig in signatures:
            if project_signature(sig, method) != project_signature(sig, method):
                bad += 1
        rows.append(ObligationResult("projection_determinism", method, bad == 0, f"bad={bad}"))
    return rows


def strict_projection_identity_obligation(signatures: Sequence[ContractSignature]) -> ObligationResult:
    bad = sum(1 for sig in signatures if len(project_signature(sig, "strict")) != len(sig))
    return ObligationResult("strict_projection_identity", "cardinality_preserved", bad == 0, f"bad={bad}")


def lattice_monotonicity_obligations(fields: Sequence[str]) -> list[ObligationResult]:
    subsets = powerset(fields)
    bad = []
    for left in subsets:
        for right in subsets:
            if set(left).issubset(right) and len(left) > len(right):
                bad.append((left, right))
    return [ObligationResult("field_lattice", "subset_order_well_formed", not bad, f"bad={bad[:3]}"), ObligationResult("field_lattice", "finite_cardinality", len(subsets) == 2 ** len(fields), f"subsets={len(subsets)}")]


def all_formal_obligations(signatures: Sequence[ContractSignature], methods: Sequence[str], fields: Sequence[str]) -> list[ObligationResult]:
    rows = []
    rows.extend(state_join_obligations())
    rows.extend(projection_determinism_obligations(signatures, methods))
    rows.append(strict_projection_identity_obligation(signatures))
    rows.extend(lattice_monotonicity_obligations(fields))
    return rows

