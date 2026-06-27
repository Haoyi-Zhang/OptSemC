"""Finite OptSem-C contract semantics.

The code mirrors the formal evidence-atom model in the paper: an action atom is
(operator, kind, variant, layer, placement, decision_time, observability, state),
and a contract signature is the evidence-supported set of such atoms.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, Iterable, Mapping, Tuple

FIELDS: tuple[str, ...] = (
    "operator",
    "kind",
    "variant",
    "layer",
    "placement",
    "decision_time",
    "observability",
    "state",
)
SUPPORTED_STATES = {"MUST", "MAY", "MUST_NOT"}
UNSPEC = "UNSPEC"


@dataclass(frozen=True, order=True)
class ActionAtom:
    operator: str
    kind: str
    variant: str
    layer: str
    placement: str
    decision_time: str
    observability: str
    state: str

    def as_tuple(self) -> tuple[str, str, str, str, str, str, str, str]:
        return (
            self.operator,
            self.kind,
            self.variant,
            self.layer,
            self.placement,
            self.decision_time,
            self.observability,
            self.state,
        )

    def field(self, name: str) -> str:
        if name not in FIELDS:
            raise KeyError(f"unknown OptSem-C atom field: {name}")
        return self.as_tuple()[FIELDS.index(name)]


ContractSignature = FrozenSet[ActionAtom]


def parse_action_key(action_key: str, state: str) -> ActionAtom:
    """Parse action-key encodings used in frozen contract maps.

    Older corpus files used a compact action key; current packages use the full key.
    including variant.  Supporting both keeps the public artifact replayable.
    """
    parts = action_key.split("|")
    if len(parts) == 6:
        operator, kind, layer, placement, decision_time, observability = parts
        variant = ""
    else:
        parts = (parts + [""] * 7)[:7]
        operator, kind, variant, layer, placement, decision_time, observability = parts
    return ActionAtom(operator, kind, variant, layer, placement, decision_time, observability, state)


def evidence_signature(actions: Mapping[str, str]) -> ContractSignature:
    """Return the evidence-supported signature, excluding UNSPEC actions."""
    return frozenset(parse_action_key(key, state) for key, state in actions.items() if state != UNSPEC)


def stable_signature_payload(signature: Iterable[ActionAtom]) -> list[list[str]]:
    return [list(atom.as_tuple()) for atom in sorted(signature)]


STATE_JOIN: dict[str, dict[str, str]] = {
    "UNSPEC": {"UNSPEC": "UNSPEC", "MAY": "MAY", "MUST": "MUST", "MUST_NOT": "MUST_NOT"},
    "MAY": {"UNSPEC": "MAY", "MAY": "MAY", "MUST": "MUST", "MUST_NOT": "CONFLICT"},
    "MUST": {"UNSPEC": "MUST", "MAY": "MUST", "MUST": "MUST", "MUST_NOT": "CONFLICT"},
    "MUST_NOT": {"UNSPEC": "MUST_NOT", "MAY": "CONFLICT", "MUST": "CONFLICT", "MUST_NOT": "MUST_NOT"},
}


def join_state(left: str, right: str) -> str:
    if left == "CONFLICT" or right == "CONFLICT":
        return "CONFLICT"
    try:
        return STATE_JOIN[left][right]
    except KeyError as exc:
        raise ValueError(f"unknown state join: {left} sqcup {right}") from exc
