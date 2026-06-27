"""Deterministic replay-plan model for artifact commands."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class ReplayStep:
    step_id: str
    command: str
    inputs: tuple[str, ...] = field(default_factory=tuple)
    outputs: tuple[str, ...] = field(default_factory=tuple)
    expensive: bool = False

    def as_row(self) -> dict[str, str]:
        return {"step_id": self.step_id, "command": self.command, "inputs": ";".join(self.inputs), "outputs": ";".join(self.outputs), "expensive": str(self.expensive).lower()}


def default_replay_steps() -> tuple[ReplayStep, ...]:
    return (
        ReplayStep("refresh-summaries", "python scripts/refresh_grounded_summaries.py", ("grounded/verified_rules.jsonl",), ("grounded/verified_core_summary.csv",)),
        ReplayStep("public-provenance", "python scripts/check_public_provenance.py", ("grounded/verified_segments.jsonl",), ("evaluation/public_provenance_summary.csv",)),
        ReplayStep("baseline-portfolio", "python scripts/compute_baseline_portfolio.py", ("evaluation/grounded_contract_maps.jsonl",), ("evaluation/grounded/baseline_portfolio.csv",)),
        ReplayStep("external-suite", "python scripts/compute_external_benchmark_suite.py", ("external/benchmark_suites.yaml", "benchmark/generated_probes.jsonl"), ("evaluation/external_benchmark_suite.csv",)),
        ReplayStep("projection-mutations", "python scripts/compute_projection_mutation_suite.py", ("evaluation/grounded_contract_maps.jsonl",), ("evaluation/projection_mutation_suite.csv",)),
        ReplayStep("semantic-frontier", "python scripts/compute_semantic_frontier.py", ("evaluation/grounded_contract_maps.jsonl",), ("evaluation/grounded/semantic_frontier.csv",)),
        ReplayStep("proof-carrying", "python scripts/build_proof_carrying_semantics.py", ("evaluation/grounded_contract_maps.jsonl",), ("evaluation/proof_carrying_semantics.json",)),
        ReplayStep("repository-audit", "python scripts/run_repository_audit.py", ("optsemc", "scripts"), ("evaluation/repository_audit.csv",)),
        ReplayStep("integrity-suite", "python scripts/run_integrity_suite.py", ("evaluation/package_snapshot_check.csv",), ("evaluation/integrity_suite.csv",)),
    )


def missing_inputs(root: Path, steps: Sequence[ReplayStep]) -> dict[str, tuple[str, ...]]:
    result = {}
    for step in steps:
        missing = tuple(item for item in step.inputs if not (root / item).exists())
        if missing:
            result[step.step_id] = missing
    return result


def produced_outputs(root: Path, steps: Sequence[ReplayStep]) -> dict[str, tuple[str, ...]]:
    return {step.step_id: tuple(item for item in step.outputs if (root / item).exists()) for step in steps}


def replay_plan_rows(steps: Sequence[ReplayStep]) -> list[dict[str, str]]:
    return [step.as_row() for step in steps]


def replay_state_rows(root: Path, steps: Sequence[ReplayStep]) -> list[dict[str, str]]:
    rows = []
    for step in steps:
        missing = tuple(item for item in step.inputs if not (root / item).exists())
        outputs = tuple(item for item in step.outputs if (root / item).exists())
        rows.append({"step_id": step.step_id, "ready": str(not missing).lower(), "missing_inputs": ";".join(missing), "current_outputs": ";".join(outputs)})
    return rows

