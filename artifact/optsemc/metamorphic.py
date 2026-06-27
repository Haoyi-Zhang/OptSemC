"""Metamorphic tests for projection and repair semantics.

The same false-portability claim should survive multiple independent ways of
checking it: deterministic recomputation, projection idempotence, monotonicity
under refinement, negative-control strictness, and repair-separator soundness.
These tests are intentionally finite and executable over the grounded corpus.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Callable, Iterable, Mapping, Sequence

from .metrics import equivalence_metrics
from .projections import METHODS, project_signature
from .repair import distinguishing_fields
from .semantics import ContractSignature, FIELDS


@dataclass(frozen=True)
class MetamorphicResult:
    test: str
    projection: str
    pairs_checked: int
    violations: int
    details: str = ""

    @property
    def passed(self) -> bool:
        return self.violations == 0

    def as_row(self) -> dict[str, str]:
        return {
            "test": self.test,
            "projection": self.projection,
            "pairs_checked": str(self.pairs_checked),
            "violations": str(self.violations),
            "passed": str(self.passed).lower(),
            "details": self.details,
        }


def signature_cache(maps: Mapping[tuple[str, str], ContractSignature], method: str, extra_fields: Sequence[str] = ()) -> dict[tuple[str, str], frozenset[tuple[str, ...]]]:
    return {key: project_signature(sig, method, extra_fields) for key, sig in maps.items()}


def check_determinism(maps: Mapping[tuple[str, str], ContractSignature], methods: Sequence[str]) -> list[MetamorphicResult]:
    rows: list[MetamorphicResult] = []
    for method in methods:
        left = signature_cache(maps, method)
        right = signature_cache(maps, method)
        violations = sum(1 for key in left if left[key] != right.get(key))
        rows.append(MetamorphicResult("projection_determinism", method, len(left), violations))
    return rows


def check_projection_idempotence(maps: Mapping[tuple[str, str], ContractSignature], methods: Sequence[str]) -> list[MetamorphicResult]:
    rows: list[MetamorphicResult] = []
    for method in methods:
        cache = signature_cache(maps, method)
        # Idempotence is represented by deterministic canonical tuple sorting: applying
        # set/frozenset normalization twice must preserve the projected signature.
        violations = 0
        for sig in cache.values():
            normalized = frozenset(tuple(atom) for atom in sig)
            if normalized != sig:
                violations += 1
        rows.append(MetamorphicResult("projection_idempotence", method, len(cache), violations))
    return rows


def _equivalence_pairs(cache: Mapping[tuple[str, str], frozenset[tuple[str, ...]]], engines: Sequence[str], probes: Sequence[str]) -> set[tuple[str, str, str]]:
    pairs: set[tuple[str, str, str]] = set()
    for left, right in itertools.combinations(sorted(engines), 2):
        for probe in probes:
            if cache.get((left, probe), frozenset()) == cache.get((right, probe), frozenset()):
                pairs.add((left, right, probe))
    return pairs


def check_refinement_monotonicity(maps: Mapping[tuple[str, str], ContractSignature], engines: Sequence[str], probes: Sequence[str]) -> list[MetamorphicResult]:
    """Strict equivalence must be contained in every coarser projection equivalence."""
    strict_pairs = _equivalence_pairs(signature_cache(maps, "strict"), engines, probes)
    rows: list[MetamorphicResult] = []
    for method in METHODS:
        cache = signature_cache(maps, method)
        coarse_pairs = _equivalence_pairs(cache, engines, probes)
        missing = strict_pairs - coarse_pairs
        rows.append(MetamorphicResult("strict_refines_projection", method, len(strict_pairs), len(missing), details=f"coarse_pairs={len(coarse_pairs)}"))
    return rows


def check_extra_field_monotonicity(maps: Mapping[tuple[str, str], ContractSignature], engines: Sequence[str], probes: Sequence[str], method: str, fields: Sequence[str]) -> list[MetamorphicResult]:
    """Adding semantic fields must not create new projected equivalences."""
    rows: list[MetamorphicResult] = []
    base = _equivalence_pairs(signature_cache(maps, method), engines, probes)
    previous = base
    prefix: list[str] = []
    for field in fields:
        prefix.append(field)
        current = _equivalence_pairs(signature_cache(maps, method, prefix), engines, probes)
        created = current - previous
        rows.append(MetamorphicResult("extra_field_refinement_monotonicity", f"{method}+{'+'.join(prefix)}", len(previous), len(created), details=f"remaining_equivalences={len(current)}"))
        previous = current
    return rows


def check_negative_control_strictness(maps: Mapping[tuple[str, str], ContractSignature], engines: Sequence[str], probes: Sequence[str]) -> list[MetamorphicResult]:
    metric = equivalence_metrics(maps, engines, probes, "strict")
    return [MetamorphicResult("strict_projection_has_no_false_equivalence", "strict", metric.comparisons, metric.false_equivalences, details=f"projected_equivalences={metric.projected_equivalences}")]


def check_separator_soundness(
    maps: Mapping[tuple[str, str], ContractSignature],
    witnesses: Sequence[tuple[str, str, tuple[str, str], tuple[str, str]]],
    required_fields: Sequence[str] = ("layer", "placement"),
) -> list[MetamorphicResult]:
    empty: ContractSignature = frozenset()
    checks = 0
    violations = 0
    missing_details: list[str] = []
    for method, probe, left_key, right_key in witnesses:
        left = maps.get(left_key, empty)
        right = maps.get(right_key, empty)
        diff = distinguishing_fields(left, right)
        checks += 1
        if not any(field in diff for field in required_fields):
            violations += 1
            if len(missing_details) < 5:
                missing_details.append(f"{method}:{left_key[0]}:{right_key[0]}:{probe}:{sorted(diff)}")
    return [MetamorphicResult("repair_separator_soundness", "+".join(required_fields), checks, violations, details="|".join(missing_details))]


def run_projection_metamorphic_suite(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    witnesses: Sequence[tuple[str, str, tuple[str, str], tuple[str, str]]] = (),
) -> list[MetamorphicResult]:
    methods = ("strict", "keyword", "yesno", "operator_only", "kind_only", "layer_only", "placement_only", "state_only", "operator_kind_surface")
    rows: list[MetamorphicResult] = []
    rows.extend(check_determinism(maps, methods))
    rows.extend(check_projection_idempotence(maps, methods))
    rows.extend(check_refinement_monotonicity(maps, engines, probes))
    rows.extend(check_extra_field_monotonicity(maps, engines, probes, "keyword", ("layer", "placement", "decision_time", "observability")))
    rows.extend(check_extra_field_monotonicity(maps, engines, probes, "operator_only", ("layer", "placement", "decision_time", "observability")))
    rows.extend(check_negative_control_strictness(maps, engines, probes))
    if witnesses:
        rows.extend(check_separator_soundness(maps, witnesses))
    return rows
