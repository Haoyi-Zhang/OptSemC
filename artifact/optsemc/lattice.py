"""Projection-resolution lattice utilities.

The lattice module treats a comparison vocabulary as a set of optimizer-contract
fields retained from each evidence atom.  It is intentionally small and
side-effect free so that result-generation scripts, tests, and paper checks can
share the same semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import log2
from statistics import median
from typing import FrozenSet, Iterable, Mapping, Sequence

from .semantics import ActionAtom, ContractSignature, FIELDS

FIELD_UNIVERSE: tuple[str, ...] = FIELDS
EMPTY_TOKEN = "_evidenced_"


@dataclass(frozen=True, order=True)
class FieldSubset:
    """A deterministic representation of a field subset."""

    fields: tuple[str, ...]

    @property
    def key(self) -> str:
        return "+".join(self.fields) if self.fields else "none"

    @property
    def size(self) -> int:
        return len(self.fields)


@dataclass(frozen=True)
class ProjectionCounts:
    fields: FieldSubset
    comparisons: int
    projected_equivalences: int
    true_equivalences: int
    false_equivalences: int
    projected_classes: int
    exact_classes: int
    entropy_retained: float

    @property
    def safe(self) -> bool:
        return self.false_equivalences == 0

    @property
    def conditional_false_rate(self) -> float:
        if self.projected_equivalences == 0:
            return 0.0
        return self.false_equivalences / self.projected_equivalences

    @property
    def kernel_inflation(self) -> float:
        if self.true_equivalences == 0:
            return 0.0
        return self.projected_equivalences / self.true_equivalences


def enumerate_field_subsets(field_universe: Sequence[str] = FIELD_UNIVERSE) -> tuple[FieldSubset, ...]:
    """Enumerate all field subsets in cardinality, then lexicographic order."""
    universe = tuple(field_universe)
    out: list[FieldSubset] = []
    for size in range(len(universe) + 1):
        for combo in combinations(universe, size):
            out.append(FieldSubset(tuple(combo)))
    return tuple(out)


def project_atom_fields(atom: ActionAtom, fields: Sequence[str]) -> tuple[str, ...]:
    if not fields:
        return (EMPTY_TOKEN,)
    return tuple(atom.field(field) for field in fields)


def project_signature_fields(signature: ContractSignature, fields: Sequence[str]) -> frozenset[tuple[str, ...]]:
    if not signature:
        return frozenset()
    return frozenset(project_atom_fields(atom, fields) for atom in signature)


def entropy_of_signatures(signatures: Iterable[object]) -> float:
    counts: dict[object, int] = {}
    total = 0
    for sig in signatures:
        counts[sig] = counts.get(sig, 0) + 1
        total += 1
    if total == 0:
        return 0.0
    return -sum((count / total) * log2(count / total) for count in counts.values())


def pairwise_counts_for_projected(
    exact: Mapping[tuple[str, str], ContractSignature],
    projected: Mapping[tuple[str, str], frozenset[tuple[str, ...]]],
    engines: Sequence[str],
    probes: Sequence[str],
) -> tuple[int, int, int, int]:
    comparisons = projected_equivalences = true_equivalences = false_equivalences = 0
    empty_exact: ContractSignature = frozenset()
    empty_projected: frozenset[tuple[str, ...]] = frozenset()
    for probe in probes:
        for i, left in enumerate(engines):
            left_key = (left, probe)
            left_exact = exact.get(left_key, empty_exact)
            left_projected = projected.get(left_key, empty_projected)
            for right in engines[i + 1 :]:
                comparisons += 1
                right_key = (right, probe)
                right_exact = exact.get(right_key, empty_exact)
                right_projected = projected.get(right_key, empty_projected)
                exact_equal = left_exact == right_exact
                projected_equal = left_projected == right_projected
                if exact_equal:
                    true_equivalences += 1
                if projected_equal:
                    projected_equivalences += 1
                    if not exact_equal:
                        false_equivalences += 1
    return comparisons, projected_equivalences, true_equivalences, false_equivalences


def count_field_projection(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    fields: FieldSubset,
    exact_entropy: float | None = None,
    exact_classes: int | None = None,
) -> ProjectionCounts:
    projected = {key: project_signature_fields(sig, fields.fields) for key, sig in maps.items()}
    comparisons, projected_equivalences, true_equivalences, false_equivalences = pairwise_counts_for_projected(
        maps, projected, engines, probes
    )
    h_exact = exact_entropy if exact_entropy is not None else entropy_of_signatures(maps.values())
    h_projected = entropy_of_signatures(projected.values())
    retained = 1.0 if h_exact == 0 else h_projected / h_exact
    return ProjectionCounts(
        fields=fields,
        comparisons=comparisons,
        projected_equivalences=projected_equivalences,
        true_equivalences=true_equivalences,
        false_equivalences=false_equivalences,
        projected_classes=len(set(projected.values())),
        exact_classes=exact_classes if exact_classes is not None else len(set(maps.values())),
        entropy_retained=retained,
    )




@dataclass(frozen=True)
class FieldProjectionFrontier:
    """Antichain certificate for a finite field-projection lattice."""

    counts: tuple[ProjectionCounts, ...]

    @property
    def safe_counts(self) -> tuple[ProjectionCounts, ...]:
        return tuple(row for row in self.counts if row.safe)

    @property
    def unsafe_counts(self) -> tuple[ProjectionCounts, ...]:
        return tuple(row for row in self.counts if not row.safe)

    @property
    def minimal_safe_counts(self) -> tuple[ProjectionCounts, ...]:
        safe = self.safe_counts
        out: list[ProjectionCounts] = []
        for row in safe:
            fields = set(row.fields.fields)
            if not any(set(other.fields.fields) < fields for other in safe):
                out.append(row)
        return tuple(sorted(out, key=lambda r: (r.fields.size, r.fields.key)))

    @property
    def maximal_unsafe_counts(self) -> tuple[ProjectionCounts, ...]:
        unsafe = self.unsafe_counts
        out: list[ProjectionCounts] = []
        for row in unsafe:
            fields = set(row.fields.fields)
            if not any(fields < set(other.fields.fields) for other in unsafe):
                out.append(row)
        return tuple(sorted(out, key=lambda r: (r.fields.size, r.fields.key)))

    def monotone_safe(self) -> bool:
        by_fields = {frozenset(row.fields.fields): row.safe for row in self.counts}
        return all(not (left_safe and not by_fields[right] and left <= right) for left, left_safe in by_fields.items() for right in by_fields)

    def monotone_unsafe(self) -> bool:
        by_fields = {frozenset(row.fields.fields): row.safe for row in self.counts}
        return all(not ((not by_fields[left]) and by_fields[right] and right <= left) for left in by_fields for right in by_fields)

    def every_safe_covered(self) -> bool:
        minima = tuple(frozenset(row.fields.fields) for row in self.minimal_safe_counts)
        return all(any(minimum <= frozenset(row.fields.fields) for minimum in minima) for row in self.safe_counts)

    def every_unsafe_covered(self) -> bool:
        maxima = tuple(frozenset(row.fields.fields) for row in self.maximal_unsafe_counts)
        return all(any(frozenset(row.fields.fields) <= maximum for maximum in maxima) for row in self.unsafe_counts)


def field_projection_frontier(counts: Iterable[ProjectionCounts], *, include_variant: bool = True) -> FieldProjectionFrontier:
    """Return frontier antichains for an evaluated retained-field lattice."""
    rows = []
    for row in counts:
        if include_variant or "variant" not in row.fields.fields:
            rows.append(row)
    return FieldProjectionFrontier(tuple(rows))


def summarize_by_size(counts: Iterable[ProjectionCounts]) -> list[dict[str, object]]:
    grouped: dict[int, list[ProjectionCounts]] = {}
    for row in counts:
        grouped.setdefault(row.fields.size, []).append(row)
    out: list[dict[str, object]] = []
    for size in sorted(grouped):
        rows = grouped[size]
        false_counts = [r.false_equivalences for r in rows]
        best = min(rows, key=lambda r: (r.false_equivalences, -r.entropy_retained, r.fields.key))
        worst = max(rows, key=lambda r: (r.false_equivalences, -r.entropy_retained, r.fields.key))
        out.append(
            {
                "subset_size": size,
                "subsets": len(rows),
                "safe_subsets": sum(r.safe for r in rows),
                "unsafe_subsets": sum(not r.safe for r in rows),
                "min_false_equivalences": min(false_counts),
                "median_false_equivalences": median(false_counts),
                "max_false_equivalences": max(false_counts),
                "best_fields": best.fields.key,
                "best_entropy_retained": best.entropy_retained,
                "worst_fields": worst.fields.key,
            }
        )
    return out

# Backwards-compatible finite field-lattice helpers used by proof-carrying
# certificate builders.  They operate on repair witnesses, where each witness
# carries the baseline projection method and two exact signatures.
@dataclass(frozen=True)
class LatticePoint:
    fields: tuple[str, ...]
    safe: bool

    @property
    def label(self) -> str:
        return subset_key(self.fields)


@dataclass(frozen=True)
class LatticeSummary:
    universe: tuple[str, ...]
    points: tuple[LatticePoint, ...]

    @property
    def safe_points(self) -> tuple[LatticePoint, ...]:
        return tuple(p for p in self.points if p.safe)

    @property
    def unsafe_points(self) -> tuple[LatticePoint, ...]:
        return tuple(p for p in self.points if not p.safe)

    @property
    def minimum_safe_points(self) -> tuple[LatticePoint, ...]:
        safe = self.safe_points
        if not safe:
            return tuple()
        size = min(len(p.fields) for p in safe)
        return tuple(p for p in safe if len(p.fields) == size)

    @property
    def maximal_unsafe_points(self) -> tuple[LatticePoint, ...]:
        unsafe = self.unsafe_points
        out = []
        for point in unsafe:
            fields = set(point.fields)
            if not any(fields < set(other.fields) for other in unsafe):
                out.append(point)
        return tuple(out)

    def monotonicity_violations(self) -> tuple[tuple[str, str], ...]:
        safe_by_set = {frozenset(p.fields): p.safe for p in self.points}
        violations: list[tuple[str, str]] = []
        for left, left_safe in safe_by_set.items():
            for right, right_safe in safe_by_set.items():
                if left <= right and left_safe and not right_safe:
                    violations.append((subset_key(tuple(sorted(left))), subset_key(tuple(sorted(right)))))
        return tuple(violations)


def powerset(items: Sequence[str]) -> tuple[tuple[str, ...], ...]:
    universe = tuple(items)
    return tuple(combo for size in range(len(universe) + 1) for combo in combinations(universe, size))


def subset_key(items: Iterable[str]) -> str:
    fields = tuple(items)
    return "+".join(fields) if fields else "empty"


def repair_separates_witness(witness, maps: Mapping[tuple[str, str], ContractSignature], fields: Sequence[str]) -> bool:
    from .projections import project_signature

    method, _probe, left, right = witness
    return project_signature(maps[left], method, fields) != project_signature(maps[right], method, fields)


def evaluate_lattice(witnesses, maps: Mapping[tuple[str, str], ContractSignature], universe: Sequence[str]) -> LatticeSummary:
    pts = []
    for subset in powerset(universe):
        safe = all(repair_separates_witness(w, maps, subset) for w in witnesses)
        pts.append(LatticePoint(tuple(subset), safe))
    return LatticeSummary(tuple(universe), tuple(pts))


def minimum_hitting_sets(separator_sets: Sequence[Iterable[str]], universe: Sequence[str]) -> list[tuple[str, ...]]:
    families = [set(s) for s in separator_sets]
    if not families:
        return [tuple()]
    for size in range(1, len(universe) + 1):
        good = []
        for subset in combinations(universe, size):
            ss = set(subset)
            if all(ss & family for family in families):
                good.append(tuple(subset))
        if good:
            return good
    return []
