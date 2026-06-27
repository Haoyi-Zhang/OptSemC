"""Differential reproducibility checks for generated OptSem-C metrics."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from .corpus import load_contract_maps
from .io import read_csv
from .metrics import equivalence_metrics
from .projections import false_equivalence_witnesses


@dataclass(frozen=True)
class DifferentialRow:
    claim: str
    frozen_value: str
    recomputed_value: str
    method: str
    passed: bool
    details: str = ""

    def as_row(self) -> dict[str, str]:
        return {
            "claim": self.claim,
            "frozen_value": self.frozen_value,
            "recomputed_value": self.recomputed_value,
            "method": self.method,
            "passed": str(self.passed).lower(),
            "details": self.details,
        }


def _lookup(rows: Sequence[Mapping[str, str]], key: str, value: str) -> Mapping[str, str] | None:
    for row in rows:
        if row.get(key) == value:
            return row
    return None


def compare_projection_metrics(root: Path) -> list[DifferentialRow]:
    artifact = root / "artifact"
    cm = load_contract_maps(artifact)
    frozen_baselines = read_csv(artifact / "evaluation/grounded/baseline_portfolio.csv")
    frozen_mutations = read_csv(artifact / "evaluation/projection_mutation_suite.csv")
    rows: list[DifferentialRow] = []
    projections = ["strict", "keyword", "yesno", "operator_only", "kind_only", "layer_only", "operator_kind_surface"]
    for projection in projections:
        recomputed = equivalence_metrics(cm.maps, cm.engines, cm.probes, projection)
        frozen = _lookup(frozen_baselines, "projection", projection) or _lookup(frozen_mutations, "projection", projection)
        if frozen is None:
            rows.append(DifferentialRow(f"{projection}.presence", "missing", "present", "equivalence_metrics", False))
            continue
        for frozen_field, attr in [
            ("false_equivalences", "false_equivalences"),
            ("projected_equivalences", "projected_equivalences"),
            ("declared_equivalences", "projected_equivalences"),
        ]:
            if frozen_field not in frozen:
                continue
            frozen_value = str(frozen.get(frozen_field, ""))
            recomputed_value = str(getattr(recomputed, attr))
            rows.append(DifferentialRow(f"{projection}.{frozen_field}", frozen_value, recomputed_value, "equivalence_metrics", frozen_value == recomputed_value))
    return rows


def compare_witness_counts(root: Path) -> list[DifferentialRow]:
    artifact = root / "artifact"
    cm = load_contract_maps(artifact)
    rows: list[DifferentialRow] = []
    trap = read_csv(artifact / "evaluation/grounded/trap_rate.csv")
    for projection in ("keyword", "yesno", "operator_only"):
        frozen = _lookup(trap, "method", projection)
        witness_count = len(false_equivalence_witnesses(cm.maps, cm.engines, cm.probes, projection))
        frozen_value = str(frozen.get("false_equivalence", "")) if frozen else "missing"
        rows.append(DifferentialRow(f"{projection}.witness_count", frozen_value, str(witness_count), "false_equivalence_witnesses", frozen_value == str(witness_count)))
    return rows


def compare_cross_file_headlines(root: Path) -> list[DifferentialRow]:
    artifact = root / "artifact"
    rows: list[DifferentialRow] = []
    files = [
        artifact / "evaluation/grounded/baseline_portfolio.csv",
        artifact / "evaluation/projection_mutation_suite.csv",
        artifact / "evaluation/grounded/trap_rate.csv",
        artifact / "evaluation/grounded/repair_certificate_summary.csv",
    ]
    tables = [read_csv(path) for path in files]
    for projection in ("keyword", "yesno", "operator_only"):
        values: list[str] = []
        for table in tables:
            row = _lookup(table, "projection", projection) or _lookup(table, "method", projection)
            if row:
                values.append(str(row.get("false_equivalences", row.get("false_equivalence", ""))))
        passed = len(set(values)) == 1 and len(values) == len(files)
        rows.append(DifferentialRow(f"{projection}.cross_table_false_equivalence", ";".join(values), values[0] if values else "", "cross_file_headline", passed, details=f"tables={len(values)}/{len(files)}"))
    return rows


def run_differential_reproducibility(root: Path) -> list[DifferentialRow]:
    rows: list[DifferentialRow] = []
    rows.extend(compare_projection_metrics(root))
    rows.extend(compare_witness_counts(root))
    rows.extend(compare_cross_file_headlines(root))
    return rows
