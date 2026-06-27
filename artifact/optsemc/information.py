"""Information and kernel diagnostics for optimizer-contract projections.

These helpers quantify how much distinguishability a comparison vocabulary loses.
They are intentionally finite and deterministic: all quantities are computed over
observed engine-probe contract maps, not asymptotic assumptions.
"""
from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Mapping, Sequence

from .semantics import ContractSignature, stable_signature_payload
from .projections import project_signature


@dataclass(frozen=True)
class InformationProfile:
    projection: str
    maps: int
    exact_classes: int
    projected_classes: int
    projected_collision_classes: int
    max_exact_classes_per_projection: int
    exact_entropy_bits: float
    projected_entropy_bits: float
    entropy_retained: float
    pair_comparisons: int
    exact_equivalences: int
    projected_equivalences: int
    false_equivalences: int
    conditional_false_rate: float
    kernel_inflation: float

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "maps": str(self.maps),
            "exact_classes": str(self.exact_classes),
            "projected_classes": str(self.projected_classes),
            "projected_collision_classes": str(self.projected_collision_classes),
            "max_exact_classes_per_projection": str(self.max_exact_classes_per_projection),
            "exact_entropy_bits": f"{self.exact_entropy_bits:.6f}",
            "projected_entropy_bits": f"{self.projected_entropy_bits:.6f}",
            "entropy_retained": f"{self.entropy_retained:.6f}",
            "pair_comparisons": str(self.pair_comparisons),
            "exact_equivalences": str(self.exact_equivalences),
            "projected_equivalences": str(self.projected_equivalences),
            "false_equivalences": str(self.false_equivalences),
            "conditional_false_rate": f"{self.conditional_false_rate:.6f}",
            "kernel_inflation": f"{self.kernel_inflation:.6f}",
        }


def _payload_signature(signature: ContractSignature) -> tuple[tuple[str, ...], ...]:
    return tuple(tuple(row) for row in stable_signature_payload(signature))


def _payload_projected(signature: ContractSignature, projection: str) -> tuple[tuple[str, ...], ...]:
    return tuple(sorted(tuple(row) for row in project_signature(signature, projection)))


def entropy(counter: Counter[tuple]) -> float:
    total = sum(counter.values())
    if total == 0:
        return 0.0
    value = 0.0
    for count in counter.values():
        p = count / total
        value -= p * math.log2(p)
    return value


def projection_information_profile(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projection: str,
) -> InformationProfile:
    exact_payloads: dict[tuple[str, str], tuple[tuple[str, ...], ...]] = {key: _payload_signature(sig) for key, sig in maps.items()}
    projected_payloads: dict[tuple[str, str], tuple[tuple[str, ...], ...]] = {key: _payload_projected(sig, projection) for key, sig in maps.items()}
    exact_counts = Counter(exact_payloads.values())
    projected_counts = Counter(projected_payloads.values())
    bucket_to_exact: dict[tuple[tuple[str, ...], ...], set[tuple[tuple[str, ...], ...]]] = defaultdict(set)
    for key, projected in projected_payloads.items():
        bucket_to_exact[projected].add(exact_payloads[key])
    collision_sizes = [len(v) for v in bucket_to_exact.values()]
    projected_collision_classes = sum(1 for size in collision_sizes if size > 1)
    max_exact_classes_per_projection = max(collision_sizes) if collision_sizes else 0
    pair_comparisons = 0
    exact_equivalences = 0
    projected_equivalences = 0
    false_equivalences = 0
    empty: tuple[tuple[str, ...], ...] = tuple()
    for probe in probes:
        for i, left in enumerate(engines):
            for right in engines[i + 1 :]:
                pair_comparisons += 1
                lk = (left, probe); rk = (right, probe)
                e1 = exact_payloads.get(lk, empty); e2 = exact_payloads.get(rk, empty)
                p1 = projected_payloads.get(lk, empty); p2 = projected_payloads.get(rk, empty)
                if e1 == e2:
                    exact_equivalences += 1
                if p1 == p2:
                    projected_equivalences += 1
                    if e1 != e2:
                        false_equivalences += 1
    h_exact = entropy(exact_counts)
    h_projected = entropy(projected_counts)
    return InformationProfile(
        projection=projection,
        maps=len(exact_payloads),
        exact_classes=len(exact_counts),
        projected_classes=len(projected_counts),
        projected_collision_classes=projected_collision_classes,
        max_exact_classes_per_projection=max_exact_classes_per_projection,
        exact_entropy_bits=h_exact,
        projected_entropy_bits=h_projected,
        entropy_retained=(h_projected / h_exact) if h_exact else 1.0,
        pair_comparisons=pair_comparisons,
        exact_equivalences=exact_equivalences,
        projected_equivalences=projected_equivalences,
        false_equivalences=false_equivalences,
        conditional_false_rate=(false_equivalences / projected_equivalences) if projected_equivalences else 0.0,
        kernel_inflation=(projected_equivalences / exact_equivalences) if exact_equivalences else float("inf"),
    )


def profiles_for(projections: Sequence[str], maps: Mapping[tuple[str, str], ContractSignature], engines: Sequence[str], probes: Sequence[str]) -> list[InformationProfile]:
    return [projection_information_profile(maps, engines, probes, projection) for projection in projections]
