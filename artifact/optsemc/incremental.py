"""Incremental maintenance and corpus-influence diagnostics for OptSem-C.

The public-contract relation is finite, but a reader still needs to know how a
new or corrected public source affects the derived comparison denominator.  The
routines here compute source-local update footprints over grounded applicable
rules without re-reading large derived maps into memory.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .io import read_csv, read_jsonl

TOTAL_ENGINES = 7
TOTAL_PROBES = 4216
TOTAL_MAP_ROWS = TOTAL_ENGINES * TOTAL_PROBES


@dataclass(frozen=True)
class SourceInfluenceRow:
    """Influence footprint for one public source record."""

    source_id: str
    engine: str
    source_class: str
    rules: int
    rule_share: float
    affected_maps: int
    affected_map_share: float
    affected_probes: int
    applicable_actions: int
    max_actions_per_map: int

    def as_row(self) -> dict[str, str]:
        return {
            "source_id": self.source_id,
            "engine": self.engine,
            "source_class": self.source_class,
            "rules": str(self.rules),
            "rule_share": f"{self.rule_share:.6f}",
            "affected_maps": str(self.affected_maps),
            "affected_map_share": f"{self.affected_map_share:.6f}",
            "affected_probes": str(self.affected_probes),
            "applicable_actions": str(self.applicable_actions),
            "max_actions_per_map": str(self.max_actions_per_map),
        }


@dataclass(frozen=True)
class IncrementalSummary:
    """Corpus-level summary for source-local incremental updates."""

    sources: int
    rules: int
    max_source_rules: int
    max_source_rule_share: float
    median_affected_maps: float
    max_affected_maps: int
    max_affected_map_share: float
    total_map_rows: int
    total_applicable_actions: int

    def as_rows(self) -> list[dict[str, str]]:
        return [
            {"metric": "sources", "value": str(self.sources)},
            {"metric": "rules", "value": str(self.rules)},
            {"metric": "max_source_rules", "value": str(self.max_source_rules)},
            {"metric": "max_source_rule_share", "value": f"{self.max_source_rule_share:.6f}"},
            {"metric": "median_affected_maps", "value": f"{self.median_affected_maps:.1f}"},
            {"metric": "max_affected_maps", "value": str(self.max_affected_maps)},
            {"metric": "max_affected_map_share", "value": f"{self.max_affected_map_share:.6f}"},
            {"metric": "total_map_rows", "value": str(self.total_map_rows)},
            {"metric": "total_applicable_actions", "value": str(self.total_applicable_actions)},
        ]


def _median(values: Sequence[int]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def source_influence(root: Path) -> tuple[list[SourceInfluenceRow], IncrementalSummary]:
    """Compute source-local update footprints from grounded rules and applicability.

    A source update can only affect maps for its own engine, but the number of
    probes touched depends on guards.  This footprint is therefore a practical
    bound on incremental recomputation work for public-contract refreshes.
    """

    sources = {r["source_id"]: r for r in read_csv(root / "grounded" / "verified_sources.csv")}
    rule_source: dict[str, str] = {}
    rules_per_source: Counter[str] = Counter()
    total_rules = 0
    for rule in read_jsonl(root / "grounded" / "verified_rules.jsonl"):
        source_id = rule["evidence"]["source_id"]
        rule_id = rule["rule_id"]
        rule_source[rule_id] = source_id
        rules_per_source[source_id] += 1
        total_rules += 1

    affected_keys: dict[str, set[tuple[str, str]]] = defaultdict(set)
    affected_probes: dict[str, set[str]] = defaultdict(set)
    actions_per_key: dict[str, Counter[tuple[str, str]]] = defaultdict(Counter)
    applicable_actions: Counter[str] = Counter()
    for app in read_jsonl(root / "evaluation" / "grounded_applicable_rules.jsonl"):
        source_id = rule_source.get(app["rule_id"])
        if source_id is None:
            continue
        key = (app["engine"], app["probe_id"])
        affected_keys[source_id].add(key)
        affected_probes[source_id].add(app["probe_id"])
        actions_per_key[source_id][key] += 1
        applicable_actions[source_id] += 1

    rows: list[SourceInfluenceRow] = []
    for source_id in sorted(sources):
        src = sources[source_id]
        affected = len(affected_keys[source_id])
        rows.append(
            SourceInfluenceRow(
                source_id=source_id,
                engine=src.get("engine", ""),
                source_class=src.get("source_class", ""),
                rules=rules_per_source[source_id],
                rule_share=rules_per_source[source_id] / max(1, total_rules),
                affected_maps=affected,
                affected_map_share=affected / TOTAL_MAP_ROWS,
                affected_probes=len(affected_probes[source_id]),
                applicable_actions=applicable_actions[source_id],
                max_actions_per_map=max(actions_per_key[source_id].values(), default=0),
            )
        )
    affected_counts = [row.affected_maps for row in rows]
    max_rules = max((row.rules for row in rows), default=0)
    summary = IncrementalSummary(
        sources=len(rows),
        rules=total_rules,
        max_source_rules=max_rules,
        max_source_rule_share=max((row.rule_share for row in rows), default=0.0),
        median_affected_maps=_median(affected_counts),
        max_affected_maps=max(affected_counts, default=0),
        max_affected_map_share=max((row.affected_map_share for row in rows), default=0.0),
        total_map_rows=TOTAL_MAP_ROWS,
        total_applicable_actions=sum(applicable_actions.values()),
    )
    return rows, summary

# Streaming projection-count maintenance -------------------------------------------------------
# This section is intentionally independent of source-local influence diagnostics above.
import itertools
import time
from typing import Mapping

from .projections import project_signature
from .scalability import EMPTY_SIGNATURE, natural_probe_key
from .semantics import ContractSignature


@dataclass(frozen=True)
class ProbeDelta:
    """Projected-equivalence contribution of one probe under one projection."""

    projection: str
    probe_id: str
    comparisons: int
    projected_equivalences: int
    true_equivalences: int
    false_equivalences: int

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "probe_id": self.probe_id,
            "comparisons": str(self.comparisons),
            "projected_equivalences": str(self.projected_equivalences),
            "true_equivalences": str(self.true_equivalences),
            "false_equivalences": str(self.false_equivalences),
        }


@dataclass(frozen=True)
class IncrementalAuditRow:
    """Budget-level parity between incremental and full recomputation."""

    projection: str
    probes: int
    engine_pairs: int
    comparisons: int
    incremental_projected_equivalences: int
    full_projected_equivalences: int
    incremental_true_equivalences: int
    full_true_equivalences: int
    incremental_false_equivalences: int
    full_false_equivalences: int
    drift: int
    elapsed_incremental_ms: float
    elapsed_full_ms: float
    repeated_prefix_work_units: int
    incremental_work_units: int
    work_reduction_factor: float

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "probes": str(self.probes),
            "engine_pairs": str(self.engine_pairs),
            "comparisons": str(self.comparisons),
            "incremental_projected_equivalences": str(self.incremental_projected_equivalences),
            "full_projected_equivalences": str(self.full_projected_equivalences),
            "incremental_true_equivalences": str(self.incremental_true_equivalences),
            "full_true_equivalences": str(self.full_true_equivalences),
            "incremental_false_equivalences": str(self.incremental_false_equivalences),
            "full_false_equivalences": str(self.full_false_equivalences),
            "drift": str(self.drift),
            "elapsed_incremental_ms": f"{self.elapsed_incremental_ms:.3f}",
            "elapsed_full_ms": f"{self.elapsed_full_ms:.3f}",
            "repeated_prefix_work_units": str(self.repeated_prefix_work_units),
            "incremental_work_units": str(self.incremental_work_units),
            "work_reduction_factor": f"{self.work_reduction_factor:.2f}",
        }


def probe_delta(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probe_id: str,
    projection: str,
) -> ProbeDelta:
    """Count projected/true/false equivalences contributed by one probe."""
    projected = {
        (engine, probe_id): project_signature(maps.get((engine, probe_id), EMPTY_SIGNATURE), projection)
        for engine in engines
    }
    projected_eq = true_eq = false_eq = 0
    comparisons = 0
    for left, right in itertools.combinations(engines, 2):
        comparisons += 1
        left_key = (left, probe_id)
        right_key = (right, probe_id)
        left_sig = maps.get(left_key, EMPTY_SIGNATURE)
        right_sig = maps.get(right_key, EMPTY_SIGNATURE)
        if projected[left_key] == projected[right_key]:
            projected_eq += 1
            if left_sig == right_sig:
                true_eq += 1
            else:
                false_eq += 1
    return ProbeDelta(projection, probe_id, comparisons, projected_eq, true_eq, false_eq)


def incremental_audit(
    maps: Mapping[tuple[str, str], ContractSignature],
    engines: Sequence[str],
    probes: Sequence[str],
    projections: Sequence[str],
    budgets: Sequence[int],
) -> tuple[tuple[IncrementalAuditRow, ...], tuple[ProbeDelta, ...]]:
    """Compare streaming maintenance against full prefix recomputation."""
    ordered_probes = tuple(sorted(probes, key=natural_probe_key))
    budget_set = {min(b, len(ordered_probes)) for b in budgets}
    engine_pairs = len(tuple(itertools.combinations(engines, 2)))
    rows: list[IncrementalAuditRow] = []
    deltas: list[ProbeDelta] = []
    for projection in projections:
        projected_acc = true_acc = false_acc = 0
        incremental_started = time.perf_counter()
        for index, probe_id in enumerate(ordered_probes, 1):
            delta = probe_delta(maps, engines, probe_id, projection)
            deltas.append(delta)
            projected_acc += delta.projected_equivalences
            true_acc += delta.true_equivalences
            false_acc += delta.false_equivalences
            if index not in budget_set:
                continue
            elapsed_incremental_ms = (time.perf_counter() - incremental_started) * 1000.0
            prefix = ordered_probes[:index]
            full_started = time.perf_counter()
            full_projected = full_true = full_false = 0
            for prefix_probe_id in prefix:
                prefix_delta = probe_delta(maps, engines, prefix_probe_id, projection)
                full_projected += prefix_delta.projected_equivalences
                full_true += prefix_delta.true_equivalences
                full_false += prefix_delta.false_equivalences
            elapsed_full_ms = (time.perf_counter() - full_started) * 1000.0
            drift = abs(projected_acc - full_projected) + abs(true_acc - full_true) + abs(false_acc - full_false)
            incremental_work = index * engine_pairs
            repeated_prefix_work = engine_pairs * (index * (index + 1) // 2)
            rows.append(
                IncrementalAuditRow(
                    projection=projection,
                    probes=index,
                    engine_pairs=engine_pairs,
                    comparisons=incremental_work,
                    incremental_projected_equivalences=projected_acc,
                    full_projected_equivalences=full_projected,
                    incremental_true_equivalences=true_acc,
                    full_true_equivalences=full_true,
                    incremental_false_equivalences=false_acc,
                    full_false_equivalences=full_false,
                    drift=drift,
                    elapsed_incremental_ms=elapsed_incremental_ms,
                    elapsed_full_ms=elapsed_full_ms,
                    repeated_prefix_work_units=repeated_prefix_work,
                    incremental_work_units=incremental_work,
                    work_reduction_factor=repeated_prefix_work / max(1, incremental_work),
                )
            )
    return tuple(rows), tuple(deltas)
