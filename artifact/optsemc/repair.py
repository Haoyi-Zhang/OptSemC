"""Finite repair search over OptSem-C semantic fields."""
from __future__ import annotations

import itertools
from typing import Iterable, Mapping, Sequence

from .semantics import ContractSignature, FIELDS
from .projections import project_signature

ALL_FIELDS = ("operator", "kind", "variant", "layer", "placement", "decision_time", "observability", "state")
SEMANTIC_NO_VARIANT = ("operator", "kind", "layer", "placement", "decision_time", "observability", "state")
CORE_SEMANTIC_STATE_FREE = ("operator", "layer", "placement", "decision_time", "observability")

Witness = tuple[str, str, tuple[str, str], tuple[str, str]]


def repairs_all(
    witnesses: Sequence[Witness],
    maps: Mapping[tuple[str, str], ContractSignature],
    fields: Sequence[str],
) -> bool:
    """Return true iff adding fields separates every witness."""
    return all(project_signature(maps[left], method, fields) != project_signature(maps[right], method, fields) for method, _probe, left, right in witnesses)


def separator_fields(
    method: str,
    left: ContractSignature,
    right: ContractSignature,
    universe: Sequence[str],
) -> frozenset[str]:
    """Fields whose singleton restoration separates one witness."""
    return frozenset(field for field in universe if project_signature(left, method, (field,)) != project_signature(right, method, (field,)))


def minimum_repairs(
    witnesses: Sequence[Witness],
    maps: Mapping[tuple[str, str], ContractSignature],
    universe: Sequence[str],
) -> list[tuple[str, ...]]:
    """Enumerate all minimum-cardinality universal repairs."""
    if not witnesses:
        return [tuple()]
    for size in range(1, len(universe) + 1):
        good = [subset for subset in itertools.combinations(universe, size) if repairs_all(witnesses, maps, subset)]
        if good:
            return good
    return []


def minimum_hitting_sets(separator_sets: Sequence[frozenset[str]], universe: Sequence[str]) -> list[tuple[str, ...]]:
    """Enumerate minimum hitting sets for singleton separator families."""
    if not separator_sets:
        return [tuple()]
    for size in range(1, len(universe) + 1):
        good = []
        for subset in itertools.combinations(universe, size):
            sub = set(subset)
            if all(sub & separators for separators in separator_sets):
                good.append(subset)
        if good:
            return good
    return []


def distinguishing_fields(left: ContractSignature, right: ContractSignature) -> frozenset[str]:
    """Return semantic fields whose singleton restoration distinguishes signatures.

    The function is method-agnostic in the sense that it asks whether projecting
    each full signature to a single field produces different field-value sets.
    It is useful as a finite certificate explaining which fields carry the
    difference between two exact optimizer-contract signatures.
    """
    out: set[str] = set()
    for field in ALL_FIELDS:
        left_values = frozenset(atom.field(field) for atom in left)
        right_values = frozenset(atom.field(field) for atom in right)
        if left_values != right_values:
            out.add(field)
    return frozenset(out)
