"""Adversarial artifact-audit model for OptSem-C."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Sequence


@dataclass(frozen=True)
class Attack:
    attack_id: str
    reader: str
    claim: str
    required_evidence: tuple[str, ...]
    resolution: str


@dataclass(frozen=True)
class AttackResolution:
    attack_id: str
    passed: bool
    missing: tuple[str, ...]
    resolution: str

    def as_row(self) -> dict[str, str]:
        return {
            "attack_id": self.attack_id,
            "passed": str(self.passed).lower(),
            "missing_evidence": ";".join(self.missing),
            "resolution": self.resolution,
        }


DEFAULT_ATTACKS = (
    Attack("A1-code-dump", "artifact reader", "Repository is a frozen dump, not reusable code.", ("artifact/optsemc", "pyproject.toml", "Makefile"), "Reusable package, CLI, tests, and checks separate semantics from scripts."),
    Attack("A2-stale-paper-code", "systems reader", "Paper claims may drift from generated outputs.", ("artifact/evaluation/paper_claim_ledger.csv", "artifact/evaluation/claim_ledger_check.csv"), "Claim ledger binds reported numbers to regenerated outputs."),
    Attack("A3-baseline-cherry-pick", "benchmark reader", "Only weak baselines are shown.", ("artifact/evaluation/grounded/baseline_portfolio.csv", "artifact/evaluation/projection_mutation_suite.csv"), "Baseline portfolio and mutation suite enumerate weak, adversarial, ablation, and strengthened projections."),
    Attack("A4-repair-posthoc", "theory reader", "Repair fields are post-hoc choices.", ("artifact/evaluation/grounded/semantic_frontier.csv", "artifact/evaluation/proof_carrying_semantics.json"), "Field lattice and hitting-set certificates prove minimum repair frontiers."),
    Attack("A5-benchmark-arbitrary", "benchmark reader", "Generated probes are arbitrary feature tuples.", ("artifact/evaluation/external_benchmark_suite.csv", "artifact/evaluation/probe_coverage_matrix.csv"), "Probe suite is checked against optimizer benchmark motifs and coverage matrices."),
    Attack("A6-public-evidence-weak", "data reader", "Rules are not grounded in auditable evidence.", ("artifact/evaluation/provenance_graph_edges.csv", "artifact/evaluation/provenance_deep_audit.csv"), "Rules link to public source/segment hashes and evidence DAG."),
    Attack("A7-no-formal-depth", "theory reader", "The formal section is too obvious.", ("artifact/evaluation/formal_obligations.csv", "artifact/evaluation/theorem_ledger.csv"), "Finite obligations cover state algebra, projection kernels, lattice monotonicity, and repair certificates."),
    Attack("A8-unreproducible", "artifact reader", "The repository requires hidden state.", ("artifact/evaluation/package_manifest.csv", "artifact/evaluation/audit_access_hygiene.csv"), "Deterministic manifest and hygiene gates reject hidden/local dependencies."),
    Attack("A9-low-code-quality", "systems reader", "Code is thin or script-only.", ("artifact/evaluation/repository_audit.csv", "artifact/evaluation/repository_quality.csv"), "Repository audit gate enforces package scale, tests, CLI, CI, and reuse."),
)


def resolve_attacks(root: Path, attacks: Sequence[Attack] = DEFAULT_ATTACKS) -> list[AttackResolution]:
    rows: list[AttackResolution] = []
    for attack in attacks:
        missing = tuple(path for path in attack.required_evidence if not (root / path).exists())
        rows.append(AttackResolution(attack.attack_id, not missing, missing, attack.resolution))
    return rows

