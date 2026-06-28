"""Severity metrics for contract-level false-equivalence witnesses.

Counts tell how often a projected comparison fabricates equivalence.  Severity
measures how far apart the exact public-contract signatures are when that
happens.  The metric is intentionally finite and deterministic: signatures are
sets of evidence-supported atoms, so the exact distance is the Jaccard distance
on those sets, and the atom delta is the size of the symmetric difference.
"""
from __future__ import annotations

import itertools
from collections import Counter
from dataclasses import dataclass
from statistics import mean, median
from typing import Mapping, Sequence

from .projections import project_signature
from .semantics import ActionAtom, ContractSignature, FIELDS


def jaccard_distance(left: ContractSignature, right: ContractSignature) -> float:
    """Return set Jaccard distance between exact contract signatures."""
    union = left | right
    if not union:
        return 0.0
    return 1.0 - (len(left & right) / len(union))


def symmetric_atom_delta(left: ContractSignature, right: ContractSignature) -> int:
    """Return number of exact evidence atoms present in exactly one signature."""
    return len(left ^ right)


def _atom_field_signature(atom: ActionAtom, fields: Sequence[str]) -> tuple[str, ...]:
    return tuple(atom.field(field) for field in fields)


def field_value_delta(left: ContractSignature, right: ContractSignature, fields: Sequence[str] = FIELDS) -> Counter[str]:
    """Approximate which semantic fields differ between two signatures.

    The comparison is deliberately conservative: for each field, compare the set
    of observed field values in the two signatures.  A field counts as different
    when the public evidence exposes different values on that semantic axis.
    """
    out: Counter[str] = Counter()
    for field in fields:
        if {a.field(field) for a in left} != {a.field(field) for a in right}:
            out[field] += 1
    return out


@dataclass(frozen=True)
class FalsePortabilitySeverity:
    projection: str
    false_equivalences: int
    mean_exact_distance: float
    median_exact_distance: float
    p90_exact_distance: float
    max_exact_distance: float
    mean_atom_delta: float
    median_atom_delta: float
    max_atom_delta: int
    pairs_with_distance_ge_half: int
    dominant_field_delta: str

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "false_equivalences": str(self.false_equivalences),
            "mean_exact_distance": f"{self.mean_exact_distance:.6f}",
            "median_exact_distance": f"{self.median_exact_distance:.6f}",
            "p90_exact_distance": f"{self.p90_exact_distance:.6f}",
            "max_exact_distance": f"{self.max_exact_distance:.6f}",
            "mean_atom_delta": f"{self.mean_atom_delta:.6f}",
            "median_atom_delta": f"{self.median_atom_delta:.6f}",
            "max_atom_delta": str(self.max_atom_delta),
            "pairs_with_distance_ge_half": str(self.pairs_with_distance_ge_half),
            "dominant_field_delta": self.dominant_field_delta,
        }


def _p90(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(0.9 * (len(ordered) - 1)))
    return ordered[index]


def false_portability_severity(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projection: str,
) -> FalsePortabilitySeverity:
    """Summarize severity among pairs falsely equated by a projection."""
    projected_cache = {key: project_signature(sig, projection) for key, sig in maps.items()}
    empty: ContractSignature = frozenset()
    distances: list[float] = []
    deltas: list[int] = []
    fields: Counter[str] = Counter()
    for probe in probes:
        for left_engine, right_engine in itertools.combinations(engines, 2):
            left_key, right_key = (left_engine, probe), (right_engine, probe)
            left_sig, right_sig = maps.get(left_key, empty), maps.get(right_key, empty)
            if left_sig == right_sig:
                continue
            if projected_cache.get(left_key, frozenset()) != projected_cache.get(right_key, frozenset()):
                continue
            dist = jaccard_distance(left_sig, right_sig)
            delta = symmetric_atom_delta(left_sig, right_sig)
            distances.append(dist)
            deltas.append(delta)
            fields.update(field_value_delta(left_sig, right_sig))
    if not distances:
        return FalsePortabilitySeverity(projection, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, "none")
    dominant = fields.most_common(1)[0][0] if fields else "none"
    return FalsePortabilitySeverity(
        projection=projection,
        false_equivalences=len(distances),
        mean_exact_distance=mean(distances),
        median_exact_distance=median(distances),
        p90_exact_distance=_p90(distances),
        max_exact_distance=max(distances),
        mean_atom_delta=mean(deltas),
        median_atom_delta=median(deltas),
        max_atom_delta=max(deltas),
        pairs_with_distance_ge_half=sum(1 for d in distances if d >= 0.5),
        dominant_field_delta=dominant,
    )
