"""Held-out repair stability over query-feature families.

The core repair certificate proves that a field set separates all observed false
projection equivalences.  This module adds an overfitting stress test: learn
minimum repairs on probes outside a feature family and evaluate on the held-out
family.  A robust repair basis is useful only if it keeps separating witnesses
when the query-feature denominator changes.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Mapping, Sequence

from .corpus import ContractMaps
from .domain import Probe
from .projections import false_equivalence_witnesses, project_signature
from .semantics import ContractSignature

REPAIR_FIELD_UNIVERSE: tuple[str, ...] = (
    "operator",
    "kind",
    "layer",
    "placement",
    "decision_time",
    "observability",
    "state",
)
ROBUST_SEMANTIC_BASIS: tuple[str, ...] = ("layer", "placement")
DEFAULT_FEATURE_VALUES = frozenset({"none", "local", "not_applicable", "low", "none_control"})


@dataclass(frozen=True)
class RepairEvaluation:
    method: str
    fold: str
    train_false: int
    heldout_false: int
    learned_repair: tuple[str, ...]
    learned_unresolved: int
    robust_repair: tuple[str, ...]
    robust_unresolved: int


def separates_witness(
    maps: Mapping[tuple[str, str], ContractSignature],
    witness: tuple[str, str, tuple[str, str], tuple[str, str]],
    fields: Sequence[str],
) -> bool:
    method, _probe, left_key, right_key = witness
    empty: ContractSignature = frozenset()
    left = maps.get(left_key, empty)
    right = maps.get(right_key, empty)
    return project_signature(left, method, fields) != project_signature(right, method, fields)


def unresolved_count(
    maps: Mapping[tuple[str, str], ContractSignature],
    witnesses: Sequence[tuple[str, str, tuple[str, str], tuple[str, str]]],
    fields: Sequence[str],
) -> int:
    return sum(1 for witness in witnesses if not separates_witness(maps, witness, fields))


def minimum_repair(
    maps: Mapping[tuple[str, str], ContractSignature],
    witnesses: Sequence[tuple[str, str, tuple[str, str], tuple[str, str]]],
    field_universe: Sequence[str] = REPAIR_FIELD_UNIVERSE,
) -> tuple[str, ...]:
    if not witnesses:
        return tuple()
    for size in range(len(field_universe) + 1):
        for combo in combinations(field_universe, size):
            if unresolved_count(maps, witnesses, combo) == 0:
                return tuple(combo)
    return tuple(field_universe)


def feature_family_folds(probes: Sequence[Probe]) -> dict[str, frozenset[str]]:
    """Return overlapping held-out folds for each non-default feature family."""
    folds: dict[str, set[str]] = {}
    for probe in probes:
        for field, value in probe.feature_vector.items():
            if str(value) not in DEFAULT_FEATURE_VALUES:
                folds.setdefault(field, set()).add(probe.probe_id)
    return {field: frozenset(ids) for field, ids in sorted(folds.items()) if ids}


def evaluate_feature_holdout(
    contract_maps: ContractMaps,
    probes: Sequence[Probe],
    methods: Sequence[str] = ("keyword", "yesno", "operator_only"),
    robust_basis: Sequence[str] = ROBUST_SEMANTIC_BASIS,
) -> list[RepairEvaluation]:
    folds = feature_family_folds(probes)
    out: list[RepairEvaluation] = []
    for method in methods:
        witnesses = false_equivalence_witnesses(contract_maps.maps, contract_maps.engines, contract_maps.probes, method)
        for fold, heldout_ids in folds.items():
            train = [w for w in witnesses if w[1] not in heldout_ids]
            heldout = [w for w in witnesses if w[1] in heldout_ids]
            if not train or not heldout:
                continue
            learned = minimum_repair(contract_maps.maps, train)
            out.append(
                RepairEvaluation(
                    method=method,
                    fold=fold,
                    train_false=len(train),
                    heldout_false=len(heldout),
                    learned_repair=learned,
                    learned_unresolved=unresolved_count(contract_maps.maps, heldout, learned),
                    robust_repair=tuple(robust_basis),
                    robust_unresolved=unresolved_count(contract_maps.maps, heldout, robust_basis),
                )
            )
    return out
