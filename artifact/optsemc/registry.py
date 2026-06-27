"""Central registry of packaged artifact files and minimum validators."""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

@dataclass(frozen=True)
class ArtifactSpec:
    path: str
    kind: str
    min_rows: int = 1
    required: bool = True

    def as_row(self) -> dict[str, str]:
        return {"path": self.path, "kind": self.kind, "min_rows": str(self.min_rows), "required": str(self.required).lower()}

@dataclass(frozen=True)
class ArtifactValidation:
    path: str
    passed: bool
    rows: int
    details: str

    def as_row(self) -> dict[str, str]:
        return {"path": self.path, "passed": str(self.passed).lower(), "rows": str(self.rows), "details": self.details}

def _row_count(path: Path, kind: str) -> int:
    if not path.exists():
        return 0
    if kind == "jsonl":
        return sum(1 for line in path.open(encoding="utf-8") if line.strip())
    if kind == "csv":
        with path.open(newline="", encoding="utf-8") as handle:
            return len(list(csv.DictReader(handle)))
    if kind == "json":
        json.loads(path.read_text(encoding="utf-8"))
        return 1
    if kind in {"yaml", "text", "python"}:
        return sum(1 for line in path.open(encoding="utf-8", errors="ignore") if line.strip())
    return 1

def validate_spec(root: Path, spec: ArtifactSpec) -> ArtifactValidation:
    path = root / spec.path
    if not path.exists():
        return ArtifactValidation(spec.path, not spec.required, 0, "missing" if spec.required else "optional missing")
    try:
        rows = _row_count(path, spec.kind)
    except Exception as exc:
        return ArtifactValidation(spec.path, False, 0, type(exc).__name__)
    return ArtifactValidation(spec.path, rows >= spec.min_rows, rows, f"min_rows={spec.min_rows}")

def default_artifact_registry() -> tuple[ArtifactSpec, ...]:
    specs = [
        ArtifactSpec('grounded/verified_rules.jsonl', 'jsonl', 1),
        ArtifactSpec('grounded/verified_segments.jsonl', 'jsonl', 1),
        ArtifactSpec('grounded/verified_sources.csv', 'csv', 1),
        ArtifactSpec('benchmark/generated_probes.jsonl', 'jsonl', 1),
        ArtifactSpec('evaluation/grounded_contract_maps.jsonl', 'jsonl', 1),
        ArtifactSpec('evaluation/grounded_conflicts.jsonl', 'jsonl', 0),
        ArtifactSpec('evaluation/grounded/baseline_portfolio.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/semantic_frontier.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/repair_certificate_summary.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/repair_hitting_sets.csv', 'csv', 1),
        ArtifactSpec('evaluation/projection_mutation_suite.csv', 'csv', 1),
        ArtifactSpec('evaluation/counterfactual_repair_ablation.csv', 'csv', 1),
        ArtifactSpec('evaluation/external_benchmark_suite.csv', 'csv', 1),
        ArtifactSpec('evaluation/probe_coverage_matrix.csv', 'csv', 1),
        ArtifactSpec('evaluation/provenance_deep_audit.csv', 'csv', 1),
        ArtifactSpec('evaluation/provenance_graph_edges.csv', 'csv', 1),
        ArtifactSpec('evaluation/formal_obligations.csv', 'csv', 1),
        ArtifactSpec('evaluation/proof_carrying_semantics.json', 'json', 1),
        ArtifactSpec('evaluation/repository_audit.csv', 'csv', 1),
        ArtifactSpec('evaluation/repository_quality.csv', 'csv', 1),
        ArtifactSpec('evaluation/package_manifest.csv', 'csv', 1),
        ArtifactSpec('evaluation/package_manifest_summary.csv', 'csv', 1),
        ArtifactSpec('evaluation/engine_pair_false_portability_matrix.csv', 'csv', 1),
        ArtifactSpec('evaluation/claim_ledger_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/theorem_ledger.csv', 'csv', 1),
        ArtifactSpec('evaluation/package_snapshot_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/integrity_suite.csv', 'csv', 1),
        ArtifactSpec('evaluation/core_library_contract.csv', 'csv', 1),
        ArtifactSpec('evaluation/reproducibility_package.csv', 'csv', 1),
        ArtifactSpec('evaluation/schema_coverage_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/cli_smoke_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/codebase_scale_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/projection_contract_semantics_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/projection_proof_obligations.csv', 'csv', 1),
        ArtifactSpec('evaluation/repair_hitting_set_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/semantic_frontier_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/external_benchmark_crosswalk_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/baseline_portfolio_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/public_provenance_summary.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded_summary_consistency.csv', 'csv', 1),
        ArtifactSpec('evaluation/paper_table_source_check_summary.csv', 'csv', 1),
        ArtifactSpec('evaluation/paper_quality.csv', 'csv', 1),
        ArtifactSpec('evaluation/pdf_integrity.csv', 'csv', 1),
        ArtifactSpec('evaluation/reference_quality.csv', 'csv', 1),
        ArtifactSpec('evaluation/latex_compile_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/artifact_hygiene.csv', 'csv', 1),
        ArtifactSpec('evaluation/stale_diagnostic_outputs.csv', 'csv', 1),
        ArtifactSpec('evaluation/semantic_field_attribution_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/shapley_attribution_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/projection_lattice_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/data_contracts.csv', 'csv', 1),
        ArtifactSpec('evaluation/data_contracts_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/data_contract_cross_file.csv', 'csv', 1),
        ArtifactSpec('evaluation/claim_evidence_graph.csv', 'csv', 1),
        ArtifactSpec('evaluation/claim_evidence_graph_nodes.csv', 'csv', 1),
        ArtifactSpec('evaluation/claim_evidence_graph_claims.csv', 'csv', 1),
        ArtifactSpec('evaluation/claim_evidence_graph_summary.csv', 'csv', 1),
        ArtifactSpec('evaluation/claim_evidence_graph_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/claim_evidence_gate_cover.csv', 'csv', 1),
        ArtifactSpec('evaluation/metamorphic_projection_tests.csv', 'csv', 1),
        ArtifactSpec('evaluation/metamorphic_projection_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/benchmark_motif_coverage.csv', 'csv', 1),
        ArtifactSpec('evaluation/benchmark_compiler_summary.csv', 'csv', 1),
        ArtifactSpec('evaluation/benchmark_compiler_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/benchmark_minimal_probe_cover.csv', 'csv', 1),
        ArtifactSpec('evaluation/benchmark_motif_redundancy.csv', 'csv', 1),
        ArtifactSpec('evaluation/differential_reproducibility.csv', 'csv', 1),
        ArtifactSpec('evaluation/differential_reproducibility_check.csv', 'csv', 1),
        ArtifactSpec('evaluation/package_files.csv', 'csv', 1),
        ArtifactSpec('evaluation/package_fingerprint_summary.csv', 'csv', 1),
        ArtifactSpec('evaluation/unit_test_results.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/projection_lattice_summary.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/benchmark_efficiency_summary.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/source_robustness_summary.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/repair_basis_stability.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/semantic_field_shapley.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/diagnostic_probe_order.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/repair_generalization_summary.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/trap_rate.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/conditional_trap_rate.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/pair_false_portability.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/mechanism_taxonomy.csv', 'csv', 1),
        ArtifactSpec('evaluation/grounded/projection_false_equivalence_analysis.csv', 'csv', 1),
        ArtifactSpec('external/workload_motifs.yaml', 'yaml', 1),
        ArtifactSpec('external/benchmark_suites.yaml', 'yaml', 1),
        ArtifactSpec('baselines/baseline_catalog.yaml', 'yaml', 1),
        ArtifactSpec('schema/action_domain.yaml', 'yaml', 1),
        ArtifactSpec('schema/contract_rule.schema.json', 'json', 1),
        ArtifactSpec('schema/query_probe.schema.json', 'json', 1),
        ArtifactSpec('optsemc/semantics.py', 'python', 1),
        ArtifactSpec('optsemc/projections.py', 'python', 1),
        ArtifactSpec('optsemc/repair.py', 'python', 1),
        ArtifactSpec('optsemc/corpus.py', 'python', 1),
        ArtifactSpec('optsemc/domain.py', 'python', 1),
        ArtifactSpec('optsemc/lattice.py', 'python', 1),
        ArtifactSpec('optsemc/certificates.py', 'python', 1),
        ArtifactSpec('optsemc/metrics.py', 'python', 1),
        ArtifactSpec('optsemc/coverage.py', 'python', 1),
        ArtifactSpec('optsemc/provenance.py', 'python', 1),
        ArtifactSpec('optsemc/manifest.py', 'python', 1),
        ArtifactSpec('optsemc/repository.py', 'python', 1),
        ArtifactSpec('optsemc/formal.py', 'python', 1),
        ArtifactSpec('optsemc/workloads.py', 'python', 1),
        ArtifactSpec('optsemc/relations.py', 'python', 1),
        ArtifactSpec('optsemc/minimization.py', 'python', 1),
        ArtifactSpec('optsemc/statistics.py', 'python', 1),
        ArtifactSpec('optsemc/replay.py', 'python', 1),
        ArtifactSpec('optsemc/sql_render.py', 'python', 1),
        ArtifactSpec('optsemc/reporting.py', 'python', 1),
        ArtifactSpec('optsemc/quality.py', 'python', 1),
        ArtifactSpec('optsemc/data_contracts.py', 'python', 1),
        ArtifactSpec('optsemc/claim_graph.py', 'python', 1),
        ArtifactSpec('optsemc/metamorphic.py', 'python', 1),
        ArtifactSpec('optsemc/benchmark_compiler.py', 'python', 1),
        ArtifactSpec('optsemc/differential.py', 'python', 1),
        ArtifactSpec('optsemc/package_builder.py', 'python', 1),
    ]
    return tuple(specs)

def validate_registry(root: Path, specs: Sequence[ArtifactSpec] | None = None) -> tuple[ArtifactValidation, ...]:
    return tuple(validate_spec(root, spec) for spec in (specs or default_artifact_registry()))

def registry_rows(specs: Sequence[ArtifactSpec] | None = None) -> list[dict[str, str]]:
    return [spec.as_row() for spec in (specs or default_artifact_registry())]

def registry_summary(validations: Sequence[ArtifactValidation]) -> list[dict[str, str]]:
    total = len(validations)
    passed = sum(1 for item in validations if item.passed)
    return [
        {"metric": "registered_artifacts", "value": str(total)},
        {"metric": "passed_artifacts", "value": str(passed)},
        {"metric": "failed_artifacts", "value": str(total - passed)},
    ]
