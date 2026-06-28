"""Stability diagnostics for projection and repair claims.

Strict readers often ask whether a false-equivalence result is caused by a
single engine, a single deployment family, or a post-hoc repair field.  This
module evaluates the same public-contract comparison after removing each engine
or family, while checking that the repair vocabulary still separates every false
projected equivalence that remains in scope.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from .projections import project_signature
from .scalability import ENGINE_FAMILIES
from .semantics import ContractSignature

EMPTY_SIGNATURE: ContractSignature = frozenset()


@dataclass(frozen=True)
class StabilityRow:
    """One leave-out stability measurement for a projection vocabulary."""

    scope_kind: str
    omitted: str
    projection: str
    engines: int
    engine_pairs: int
    probes: int
    comparisons: int
    projected_equivalences: int
    true_equivalences: int
    false_equivalences: int
    repaired_by_layer_placement: int
    unresolved_after_layer_placement: int

    def as_row(self) -> dict[str, str]:
        return {
            "scope_kind": self.scope_kind,
            "omitted": self.omitted,
            "projection": self.projection,
            "engines": str(self.engines),
            "engine_pairs": str(self.engine_pairs),
            "probes": str(self.probes),
            "comparisons": str(self.comparisons),
            "projected_equivalences": str(self.projected_equivalences),
            "true_equivalences": str(self.true_equivalences),
            "false_equivalences": str(self.false_equivalences),
            "repaired_by_layer_placement": str(self.repaired_by_layer_placement),
            "unresolved_after_layer_placement": str(self.unresolved_after_layer_placement),
        }


@dataclass(frozen=True)
class StabilitySummary:
    """Projection-level summary across leave-out scopes."""

    projection: str
    scope_kind: str
    cases: int
    all_scope_false_equivalences: int
    min_false_equivalences: int
    max_false_equivalences: int
    scopes_with_false_equivalences: int
    max_unresolved_after_layer_placement: int
    repair_stable: bool

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "scope_kind": self.scope_kind,
            "cases": str(self.cases),
            "all_scope_false_equivalences": str(self.all_scope_false_equivalences),
            "min_false_equivalences": str(self.min_false_equivalences),
            "max_false_equivalences": str(self.max_false_equivalences),
            "scopes_with_false_equivalences": str(self.scopes_with_false_equivalences),
            "max_unresolved_after_layer_placement": str(self.max_unresolved_after_layer_placement),
            "repair_stable": str(self.repair_stable).lower(),
        }


def _pair_scopes(engines: Sequence[str]) -> list[tuple[str, str, tuple[str, ...]]]:
    ordered = tuple(engines)
    scopes: list[tuple[str, str, tuple[str, ...]]] = [("all", "none", ordered)]
    for engine in ordered:
        remaining = tuple(e for e in ordered if e != engine)
        if len(remaining) >= 2:
            scopes.append(("leave_engine", engine, remaining))
    for family in sorted(set(ENGINE_FAMILIES.get(e, "other") for e in ordered)):
        remaining = tuple(e for e in ordered if ENGINE_FAMILIES.get(e, "other") != family)
        if len(remaining) >= 2:
            scopes.append(("leave_family", family, remaining))
    return scopes


def _count_for_scope(
    maps: Mapping[tuple[str, str], ContractSignature],
    probes: Sequence[str],
    projection: str,
    engines: Sequence[str],
    projected: Mapping[tuple[str, str], frozenset[tuple[str, ...]]],
    repaired_projected: Mapping[tuple[str, str], frozenset[tuple[str, ...]]],
    scope_kind: str,
    omitted: str,
) -> StabilityRow:
    engine_pairs = tuple(itertools.combinations(engines, 2))
    projected_equivalences = true_equivalences = false_equivalences = 0
    repaired = unresolved = 0
    for probe in probes:
        for left, right in engine_pairs:
            left_key, right_key = (left, probe), (right, probe)
            left_sig = maps.get(left_key, EMPTY_SIGNATURE)
            right_sig = maps.get(right_key, EMPTY_SIGNATURE)
            if projected.get(left_key, frozenset()) != projected.get(right_key, frozenset()):
                continue
            projected_equivalences += 1
            if left_sig == right_sig:
                true_equivalences += 1
                continue
            false_equivalences += 1
            if repaired_projected.get(left_key, frozenset()) != repaired_projected.get(right_key, frozenset()):
                repaired += 1
            else:
                unresolved += 1
    return StabilityRow(
        scope_kind=scope_kind,
        omitted=omitted,
        projection=projection,
        engines=len(engines),
        engine_pairs=len(engine_pairs),
        probes=len(probes),
        comparisons=len(probes) * len(engine_pairs),
        projected_equivalences=projected_equivalences,
        true_equivalences=true_equivalences,
        false_equivalences=false_equivalences,
        repaired_by_layer_placement=repaired,
        unresolved_after_layer_placement=unresolved,
    )


def leave_out_stability_profile(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projections: Sequence[str],
) -> tuple[StabilityRow, ...]:
    """Evaluate projection and repair stability after engine/family removal."""
    scopes = _pair_scopes(tuple(engines))
    rows: list[StabilityRow] = []
    for projection in projections:
        projected = {key: project_signature(sig, projection) for key, sig in maps.items()}
        repaired_projected = {key: project_signature(sig, projection, ("layer", "placement")) for key, sig in maps.items()}
        for scope_kind, omitted, retained in scopes:
            rows.append(_count_for_scope(maps, probes, projection, retained, projected, repaired_projected, scope_kind, omitted))
    return tuple(rows)


def summarize_stability(rows: Iterable[StabilityRow]) -> tuple[StabilitySummary, ...]:
    """Summarize rows by projection and leave-out kind."""
    grouped: dict[tuple[str, str], list[StabilityRow]] = {}
    for row in rows:
        grouped.setdefault((row.projection, row.scope_kind), []).append(row)
    summaries: list[StabilitySummary] = []
    for (projection, scope_kind), subset in sorted(grouped.items()):
        all_row = next((r for r in subset if r.scope_kind == "all"), None)
        false_counts = [r.false_equivalences for r in subset]
        summaries.append(
            StabilitySummary(
                projection=projection,
                scope_kind=scope_kind,
                cases=len(subset),
                all_scope_false_equivalences=all_row.false_equivalences if all_row else -1,
                min_false_equivalences=min(false_counts) if false_counts else 0,
                max_false_equivalences=max(false_counts) if false_counts else 0,
                scopes_with_false_equivalences=sum(1 for r in subset if r.false_equivalences > 0),
                max_unresolved_after_layer_placement=max((r.unresolved_after_layer_placement for r in subset), default=0),
                repair_stable=all(r.unresolved_after_layer_placement == 0 for r in subset),
            )
        )
    return tuple(summaries)


def compact_paper_rows(rows: Iterable[StabilityRow], projections: Sequence[str]) -> list[dict[str, str]]:
    """Return compact rows used by the manuscript table."""
    by_projection = {projection: [r for r in rows if r.projection == projection] for projection in projections}
    paper: list[dict[str, str]] = []
    for projection in projections:
        subset = by_projection[projection]
        all_row = next(r for r in subset if r.scope_kind == "all")
        leave_engine = [r for r in subset if r.scope_kind == "leave_engine"]
        leave_family = [r for r in subset if r.scope_kind == "leave_family"]
        paper.append({
            "projection": projection,
            "all_false": str(all_row.false_equivalences),
            "leave_engine_false_range": f"{min(r.false_equivalences for r in leave_engine)}--{max(r.false_equivalences for r in leave_engine)}" if leave_engine else "n/a",
            "leave_family_false_range": f"{min(r.false_equivalences for r in leave_family)}--{max(r.false_equivalences for r in leave_family)}" if leave_family else "n/a",
            "max_unresolved_after_repair": str(max(r.unresolved_after_layer_placement for r in subset)),
        })
    return paper
