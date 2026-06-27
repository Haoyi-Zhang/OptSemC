"""Projection baselines and false-equivalence enumeration."""
from __future__ import annotations

import itertools
from functools import lru_cache
from typing import Dict, FrozenSet, Iterable, Mapping, Sequence, Tuple

from .semantics import ActionAtom, ContractSignature, FIELDS

HEADLINE_METHODS = ("keyword", "yesno", "operator_only")
DIAGNOSTIC_METHODS = ("strict", "no_placement", "no_decision_time", "no_observability", "no_modality")
ADVERSARIAL_METHODS = (
    "kind_only",
    "layer_only",
    "placement_only",
    "decision_time_only",
    "observability_only",
    "state_only",
    "operator_kind_layer",
    "operator_kind_placement",
    "operator_kind_surface",
)
METHODS = HEADLINE_METHODS + DIAGNOSTIC_METHODS + ADVERSARIAL_METHODS


def keyword_label(kind: str) -> str:
    if kind in {"delegate", "pushdown", "prune"}:
        return "pushdown"
    if kind == "observe":
        return "explain"
    if kind == "reorder":
        return "join_order"
    if kind == "adapt":
        return "adaptivity"
    if kind in {"materialize", "inline"}:
        return "materialization"
    if kind == "choose":
        return "choose"
    if kind == "fallback":
        return "fallback"
    return kind


def _append_fields(base: tuple[str, ...], atom: ActionAtom, extra_fields: Sequence[str]) -> tuple[str, ...]:
    return base + tuple(atom.field(field) for field in extra_fields)


def project_atom(atom: ActionAtom, method: str, extra_fields: Sequence[str] = ()) -> tuple[str, ...]:
    """Project one full evidence atom into a comparison vocabulary."""
    if method == "strict":
        base = atom.as_tuple()
    elif method == "keyword":
        base = (keyword_label(atom.kind), "yes")
    elif method == "yesno":
        base = (atom.operator, atom.kind, "yes")
    elif method == "operator_only":
        base = (atom.operator, "yes")
    elif method == "no_placement":
        base = (atom.operator, atom.kind, atom.variant, atom.layer, "_", atom.decision_time, atom.observability, atom.state)
    elif method == "no_decision_time":
        base = (atom.operator, atom.kind, atom.variant, atom.layer, atom.placement, "_", atom.observability, atom.state)
    elif method == "no_observability":
        base = (atom.operator, atom.kind, atom.variant, atom.layer, atom.placement, atom.decision_time, "_", atom.state)
    elif method == "no_modality":
        base = (atom.operator, atom.kind, atom.variant, atom.layer, atom.placement, atom.decision_time, atom.observability, "evidenced")
    elif method == "kind_only":
        base = (atom.kind, "yes")
    elif method == "layer_only":
        base = (atom.layer, "yes")
    elif method == "placement_only":
        base = (atom.placement, "yes")
    elif method == "decision_time_only":
        base = (atom.decision_time, "yes")
    elif method == "observability_only":
        base = (atom.observability, "yes")
    elif method == "state_only":
        base = (atom.state, "yes")
    elif method == "operator_kind_layer":
        base = (atom.operator, atom.kind, atom.layer, "yes")
    elif method == "operator_kind_placement":
        base = (atom.operator, atom.kind, atom.placement, "yes")
    elif method == "operator_kind_surface":
        base = (atom.operator, atom.kind, atom.layer, atom.placement, atom.observability, "yes")
    else:
        raise ValueError(f"unknown projection method: {method}")
    return _append_fields(tuple(base), atom, extra_fields)


def project_signature(signature: ContractSignature, method: str, extra_fields: Sequence[str] = ()) -> frozenset[tuple[str, ...]]:
    return frozenset(project_atom(atom, method, extra_fields) for atom in signature)


def false_equivalence_witnesses(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    method: str,
) -> list[tuple[str, str, tuple[str, str], tuple[str, str]]]:
    """Return witnesses that are unequal exactly but equal after projection."""
    pairs = list(itertools.combinations(engines, 2))
    projected = {key: project_signature(signature, method) for key, signature in maps.items()}
    witnesses: list[tuple[str, str, tuple[str, str], tuple[str, str]]] = []
    empty: ContractSignature = frozenset()
    for probe in probes:
        for left, right in pairs:
            left_key = (left, probe)
            right_key = (right, probe)
            left_sig = maps.get(left_key, empty)
            right_sig = maps.get(right_key, empty)
            if left_sig != right_sig and projected.get(left_key, frozenset()) == projected.get(right_key, frozenset()):
                witnesses.append((method, probe, left_key, right_key))
    return witnesses
