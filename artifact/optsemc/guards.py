"""Guard semantics and corpus-quality diagnostics for public contracts.

Grounded contract rules use finite guards over benchmark feature vectors.  Most
rules have scalar guards, while a small number of public documentation statements
cover a finite disjunction encoded as a list literal.  This module gives those
records a single evaluator so benchmark triggering, corpus audits, and paper
summaries use the same guard semantics.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from statistics import mean, median
from typing import Iterable, Mapping, Sequence

from .domain import ContractRule, Probe

DEFAULT_FEATURE_VALUES = frozenset({"none", "local", "not_applicable", "low", "none_control"})


@dataclass(frozen=True)
class GuardSupport:
    """Support statistics for one grounded rule over a finite probe set."""

    rule_id: str
    engine: str
    action_key: str
    state: str
    guard_width: int
    expanded_guard_width: int
    support_count: int
    total_probes: int

    @property
    def support_share(self) -> float:
        return self.support_count / self.total_probes if self.total_probes else 0.0

    @property
    def support_class(self) -> str:
        if self.support_count == 0:
            return "zero"
        if self.support_count == self.total_probes:
            return "global"
        if self.support_count >= 1000:
            return "broad"
        if self.support_count >= 100:
            return "medium"
        return "narrow"


def parse_guard_values(value: object) -> tuple[str, ...]:
    """Parse a guard value into a finite accepted-value tuple.

    Existing packages encode disjunctive values as strings such as
    ``"['simple', 'conjunctive']"``.  Treat those as finite disjunctions rather
    than opaque values.  Scalar strings remain singleton guards.
    """
    if value is None:
        return tuple()
    if isinstance(value, (list, tuple, set, frozenset)):
        return tuple(sorted(str(v) for v in value))
    text = str(value).strip()
    if not text:
        return tuple()
    try:
        parsed = ast.literal_eval(text)
    except (SyntaxError, ValueError):
        return (text,)
    if isinstance(parsed, (list, tuple, set, frozenset)):
        return tuple(sorted(str(v) for v in parsed))
    return (text,)


def guard_value_accepts(guard_value: object, feature_value: object) -> bool:
    return str(feature_value) in parse_guard_values(guard_value)


def guard_applies(guard: Mapping[str, object], feature_vector: Mapping[str, object]) -> bool:
    """Return whether a probe feature vector satisfies a finite guard."""
    for name, accepted in guard.items():
        if str(feature_vector.get(name, "")) not in parse_guard_values(accepted):
            return False
    return True


def probe_satisfies_rule(rule: ContractRule, probe: Probe | Mapping[str, object]) -> bool:
    feature_vector = probe.feature_vector if isinstance(probe, Probe) else probe.get("feature_vector", probe)
    return guard_applies(rule.guard, feature_vector)


def support_for_rule(rule: ContractRule, probes: Sequence[Probe]) -> GuardSupport:
    total = len(probes)
    support = sum(1 for probe in probes if probe_satisfies_rule(rule, probe))
    expanded = sum(len(parse_guard_values(value)) for value in rule.guard.values())
    return GuardSupport(
        rule_id=rule.rule_id,
        engine=rule.engine,
        action_key=rule.action_key,
        state=rule.state,
        guard_width=len(rule.guard),
        expanded_guard_width=expanded,
        support_count=support,
        total_probes=total,
    )


def support_table(rules: Sequence[ContractRule], probes: Sequence[Probe]) -> list[GuardSupport]:
    return [support_for_rule(rule, probes) for rule in rules]


def support_summary(supports: Sequence[GuardSupport]) -> dict[str, object]:
    counts = [s.support_count for s in supports]
    classes: dict[str, int] = {"zero": 0, "narrow": 0, "medium": 0, "broad": 0, "global": 0}
    for support in supports:
        classes[support.support_class] += 1
    return {
        "rules": len(supports),
        "zero_support_rules": classes["zero"],
        "triggered_rules": len(supports) - classes["zero"],
        "global_rules": classes["global"],
        "non_global_guarded_rules": len(supports) - classes["global"],
        "narrow_rules": classes["narrow"],
        "medium_rules": classes["medium"],
        "broad_rules": classes["broad"],
        "min_support": min(counts) if counts else 0,
        "median_support": median(counts) if counts else 0,
        "mean_support": mean(counts) if counts else 0.0,
        "max_support": max(counts) if counts else 0,
    }


def feature_domain(probes: Sequence[Probe]) -> dict[str, tuple[str, ...]]:
    values: dict[str, set[str]] = {}
    for probe in probes:
        for key, value in probe.feature_vector.items():
            values.setdefault(key, set()).add(str(value))
    return {key: tuple(sorted(vals)) for key, vals in sorted(values.items())}


def invalid_guard_dimensions(rules: Sequence[ContractRule], probes: Sequence[Probe]) -> list[dict[str, str]]:
    domains = feature_domain(probes)
    issues: list[dict[str, str]] = []
    for rule in rules:
        for key, value in rule.guard.items():
            if key not in domains:
                issues.append({"rule_id": rule.rule_id, "field": key, "issue": "unknown_feature", "value": str(value)})
                continue
            accepted = parse_guard_values(value)
            missing = [v for v in accepted if v not in domains[key]]
            if missing:
                issues.append({"rule_id": rule.rule_id, "field": key, "issue": "value_not_in_domain", "value": ";".join(missing)})
    return issues


def guard_items(rule: ContractRule) -> frozenset[tuple[str, tuple[str, ...]]]:
    return frozenset((key, parse_guard_values(value)) for key, value in sorted(rule.guard.items()))


def support_set(rule: ContractRule, probes: Sequence[Probe]) -> frozenset[str]:
    return frozenset(probe.probe_id for probe in probes if probe_satisfies_rule(rule, probe))


def overlap_rows(rules: Sequence[ContractRule], probes: Sequence[Probe]) -> list[dict[str, object]]:
    """Compare same-engine/action/state guards for redundancy and overlap."""
    support_cache = {rule.rule_id: support_set(rule, probes) for rule in rules}
    rows: list[dict[str, object]] = []
    for i, left in enumerate(rules):
        left_items = guard_items(left)
        left_support = support_cache[left.rule_id]
        for right in rules[i + 1 :]:
            if (left.engine, left.action_key, left.state) != (right.engine, right.action_key, right.state):
                continue
            right_items = guard_items(right)
            right_support = support_cache[right.rule_id]
            inter = left_support & right_support
            if not inter:
                overlap_type = "disjoint"
            elif left_support == right_support:
                overlap_type = "identical_support"
            elif left_support <= right_support or right_support <= left_support:
                overlap_type = "support_containment"
            else:
                overlap_type = "partial_overlap"
            guard_containment = left_items <= right_items or right_items <= left_items
            rows.append(
                {
                    "left_rule_id": left.rule_id,
                    "right_rule_id": right.rule_id,
                    "engine": left.engine,
                    "state": left.state,
                    "action_key": left.action_key,
                    "overlap_type": overlap_type,
                    "intersection_support": len(inter),
                    "left_support": len(left_support),
                    "right_support": len(right_support),
                    "guard_containment": str(bool(guard_containment)).lower(),
                }
            )
    return rows


def overlap_summary(rows: Sequence[Mapping[str, object]]) -> dict[str, int]:
    counts = {
        "same_action_state_pairs": len(rows),
        "disjoint_pairs": 0,
        "partial_overlap_pairs": 0,
        "support_containment_pairs": 0,
        "identical_support_pairs": 0,
        "guard_containment_pairs": 0,
    }
    for row in rows:
        typ = str(row["overlap_type"])
        if typ == "disjoint":
            counts["disjoint_pairs"] += 1
        elif typ == "partial_overlap":
            counts["partial_overlap_pairs"] += 1
        elif typ == "support_containment":
            counts["support_containment_pairs"] += 1
        elif typ == "identical_support":
            counts["identical_support_pairs"] += 1
        if str(row.get("guard_containment", "false")).lower() == "true":
            counts["guard_containment_pairs"] += 1
    return counts
