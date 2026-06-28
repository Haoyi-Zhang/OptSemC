"""Side-balanced evidence support for contract-level false-equivalence witnesses.

A false-equivalence witness is only convincing if both sides of the comparison
are grounded by public evidence.  The source-support module checks the union of
sources for a witness; this module checks each side separately and verifies that
no headline witness is merely a one-sided annotation artifact.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from .corpus import load_contract_maps
from .projections import false_equivalence_witnesses
from .source_support import contract_support_index, rule_source_index


@dataclass(frozen=True)
class SideBalancedWitnessRecord:
    """Evidence support for the left and right sides of one false witness."""

    projection: str
    probe_id: str
    engine_left: str
    engine_right: str
    left_sources: tuple[str, ...]
    right_sources: tuple[str, ...]
    left_rules: int
    right_rules: int

    @property
    def both_sides_supported(self) -> bool:
        """Return whether both compared signatures have public evidence support."""
        return bool(self.left_sources) and bool(self.right_sources)

    @property
    def shared_sources(self) -> tuple[str, ...]:
        """Return public sources shared by both sides of the comparison."""
        return tuple(sorted(set(self.left_sources) & set(self.right_sources)))

    @property
    def all_sources(self) -> tuple[str, ...]:
        """Return public sources supporting either side."""
        return tuple(sorted(set(self.left_sources) | set(self.right_sources)))

    def as_row(self) -> dict[str, str]:
        return {
            "projection": self.projection,
            "probe_id": self.probe_id,
            "engine_left": self.engine_left,
            "engine_right": self.engine_right,
            "left_source_count": str(len(self.left_sources)),
            "right_source_count": str(len(self.right_sources)),
            "left_sources": ";".join(self.left_sources),
            "right_sources": ";".join(self.right_sources),
            "shared_source_count": str(len(self.shared_sources)),
            "shared_sources": ";".join(self.shared_sources),
            "left_supporting_rules": str(self.left_rules),
            "right_supporting_rules": str(self.right_rules),
            "both_sides_supported": str(self.both_sides_supported).lower(),
        }


def _side_sources(
    key: tuple[str, str],
    support: Mapping[tuple[str, str], Mapping[str, Sequence[str]]],
    rule_sources: Mapping[str, str],
) -> tuple[tuple[str, ...], int]:
    """Return source IDs and rule count supporting one engine-probe signature."""
    sources: set[str] = set()
    rules_seen: set[str] = set()
    for rules in support.get(key, {}).values():
        for rule_id in rules:
            if rule_id in rule_sources:
                sources.add(rule_sources[rule_id])
                rules_seen.add(rule_id)
    return tuple(sorted(sources)), len(rules_seen)


def side_balanced_witness_records(
    artifact_root: Path,
    projections: Sequence[str] = ("keyword", "yesno", "operator_only"),
) -> list[SideBalancedWitnessRecord]:
    """Compute side-balanced evidence records for headline false witnesses."""
    maps = load_contract_maps(artifact_root)
    support = contract_support_index(artifact_root)
    rule_sources = rule_source_index(artifact_root)
    records: list[SideBalancedWitnessRecord] = []
    for projection in projections:
        for method, probe_id, left_key, right_key in false_equivalence_witnesses(
            maps.maps, maps.engines, maps.probes, projection
        ):
            left_sources, left_rules = _side_sources(left_key, support, rule_sources)
            right_sources, right_rules = _side_sources(right_key, support, rule_sources)
            records.append(
                SideBalancedWitnessRecord(
                    projection=method,
                    probe_id=probe_id,
                    engine_left=left_key[0],
                    engine_right=right_key[0],
                    left_sources=left_sources,
                    right_sources=right_sources,
                    left_rules=left_rules,
                    right_rules=right_rules,
                )
            )
    return records


def side_balanced_summary(records: Sequence[SideBalancedWitnessRecord]) -> list[dict[str, str]]:
    """Aggregate side-balanced support by projection."""
    rows: list[dict[str, str]] = []
    for projection in sorted({record.projection for record in records}):
        group = [record for record in records if record.projection == projection]
        distinct_sources = sorted({source for record in group for source in record.all_sources})
        both = sum(1 for record in group if record.both_sides_supported)
        left_counts = [len(record.left_sources) for record in group]
        right_counts = [len(record.right_sources) for record in group]
        shared_zero = sum(1 for record in group if len(record.shared_sources) == 0)
        rows.append(
            {
                "projection": projection,
                "false_witnesses": str(len(group)),
                "both_sides_supported": str(both),
                "both_sides_supported_share": f"{(both / len(group)) if group else 0.0:.6f}",
                "min_left_sources": str(min(left_counts) if left_counts else 0),
                "min_right_sources": str(min(right_counts) if right_counts else 0),
                "distinct_sources": str(len(distinct_sources)),
                "zero_shared_source_witnesses": str(shared_zero),
                "zero_shared_source_share": f"{(shared_zero / len(group)) if group else 0.0:.6f}",
            }
        )
    return rows
