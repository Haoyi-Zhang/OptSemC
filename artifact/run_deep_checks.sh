#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/scripts${PYTHONPATH:+:$PYTHONPATH}"
clean_transients() {
  find .. -type d \( -name "__pycache__" -o -name ".pytest_cache" -o -name "*.egg-info" -o -name "build" -o -name "dist" \) -prune -exec rm -rf {} +
  find .. -type f \( -name "*.pyc" -o -name "*.pyo" -o -name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.bbl" -o -name "*.blg" -o -name "*.backup" \) -delete
  find .. -type f -name "git_tree_status.txt" -delete
}
clean_transients
PY_TIMEOUT=${PY_TIMEOUT:-600}
LATEX_TIMEOUT=${LATEX_TIMEOUT:-1200}
run_py() { echo "[deep] python $*"; timeout "$PY_TIMEOUT" python -u "$@"; }
run_py_latex() { echo "[deep] python $*"; timeout "$LATEX_TIMEOUT" python -u "$@"; }
run_real_engine_check() {
  if [[ "${RUN_LATEX_COMPILE:-0}" == "1" || "${OPTSEMC_REQUIRE_FRESH_REAL_ENGINE:-0}" == "1" ]]; then
    echo "[deep] OPTSEMC_REQUIRE_FRESH_REAL_ENGINE=1 python $*"
    OPTSEMC_REQUIRE_FRESH_REAL_ENGINE=1 timeout "$PY_TIMEOUT" python -u "$@"
  else
    run_py "$@"
  fi
}
run_real_engine_validation_gate() {
  if [[ "${RUN_LATEX_COMPILE:-0}" == "1" || "${OPTSEMC_REQUIRE_FRESH_REAL_ENGINE:-0}" == "1" ]]; then
    echo "[deep] bash run_cloud_real_engine_validation.sh"
    timeout "$PY_TIMEOUT" bash run_cloud_real_engine_validation.sh
  else
    run_py scripts/check_real_engine_validation.py
  fi
}
ARTIFACT_ONLY=0
if [[ ! -d ../Paper || "${ANONYMOUS_ARTIFACT_ONLY:-0}" == "1" ]]; then
  ARTIFACT_ONLY=1
fi
run_paper_py() {
  if [[ "$ARTIFACT_ONLY" == "1" ]]; then
    echo "[deep] skip paper-only python $*"
  else
    run_py "$@"
  fi
}
run_paper_py_latex() {
  if [[ "$ARTIFACT_ONLY" == "1" ]]; then
    echo "[deep] skip paper-only python $*"
  else
    run_py_latex "$@"
  fi
}

run_py scripts/hydrate_large_outputs.py
run_py scripts/build_evidence_freeze_manifest.py
run_py scripts/check_evidence_freeze_manifest.py
run_py scripts/compute_projection_information_profile.py
run_py scripts/check_projection_information_profile.py
run_py scripts/compute_false_equivalence_severity.py
run_py scripts/check_false_equivalence_severity.py
run_py scripts/compute_projection_resolution_lattice.py
run_py scripts/check_projection_resolution_lattice.py
run_py scripts/compute_projection_frontier_antichains.py
run_py scripts/check_projection_frontier_antichains.py
run_py scripts/compute_scalability_stress.py
run_py scripts/check_scalability_stress.py
run_py scripts/compute_witness_diversity.py
run_py scripts/check_witness_diversity.py
run_py scripts/compute_witness_dispersion.py
run_py scripts/check_witness_dispersion.py
run_py scripts/compute_algorithmic_scaling.py
run_py scripts/check_algorithmic_scaling.py
run_py scripts/compute_scalability_regression.py
run_py scripts/check_scalability_regression.py
run_py scripts/compute_incremental_audit.py
run_py scripts/check_incremental_audit.py
run_py scripts/compute_incremental_update_stress.py
run_py scripts/check_incremental_update_stress.py
run_py scripts/compute_grounded_statistical_robustness.py --boot 200
run_py scripts/check_statistical_robustness.py
run_py scripts/compute_leave_out_stability.py
run_py scripts/check_leave_out_stability.py
run_py scripts/compute_engine_family_stress.py
run_py scripts/check_engine_family_stress.py
run_py scripts/compute_guard_quality.py
run_py scripts/check_guard_quality.py
run_py scripts/compute_feature_holdout_repair.py
run_py scripts/check_feature_holdout_repair.py
run_py scripts/compute_repair_generalization.py
run_py scripts/check_repair_generalization.py
run_py scripts/compute_grounded_source_robustness.py
run_py scripts/compute_anti_overfit_audit.py
run_py scripts/check_anti_overfit_audit.py
run_py scripts/render_scaling_and_incremental_tables.py
run_paper_py scripts/check_paper_numeric_claims.py
run_py scripts/check_architecture_contract.py
run_py scripts/check_packaging_installability.py
clean_transients
run_py scripts/export_sql_probe_bundle.py
run_py scripts/check_sql_probe_bundle.py
run_py scripts/execute_sql_probe_suite.py
run_py scripts/check_sql_probe_execution.py
run_py scripts/execute_sql_probe_suite_multicatalog.py
run_py scripts/check_sql_probe_multicatalog_execution.py
run_py scripts/compute_resource_profile.py
run_py scripts/check_resource_profile.py
run_paper_py scripts/render_validity_resource_tables.py
run_paper_py scripts/render_python_figures.py
run_py scripts/compute_benchmark_motif_difficulty.py
run_py scripts/check_benchmark_motif_difficulty.py
run_py scripts/execute_external_motif_suite.py
run_py scripts/check_external_motif_execution.py
run_real_engine_validation_gate
run_py scripts/check_real_engine_noninterference.py
run_py scripts/check_no_cache_package.py
run_py scripts/refresh_grounded_summaries.py
run_py scripts/check_grounded_summary_consistency.py
run_py scripts/annotate_public_provenance.py
run_py scripts/check_public_provenance.py
run_py scripts/compute_baseline_portfolio.py
run_py scripts/compute_practice_projection_surfaces.py
run_py scripts/check_practice_projection_surfaces.py
run_py scripts/compute_external_benchmark_crosswalk.py
run_py scripts/compute_external_benchmark_suite.py
run_py scripts/check_external_benchmark_suite.py
run_py scripts/compute_workload_suite_depth.py
run_py scripts/check_workload_suite_depth.py
run_py scripts/compute_semantic_frontier.py
run_py scripts/render_baseline_external_tables.py
run_py scripts/check_core_library_contract.py
run_py scripts/build_data_contracts.py
run_py scripts/check_data_contracts.py
run_py scripts/build_claim_evidence_graph.py
run_py scripts/check_claim_evidence_graph.py
run_py scripts/compute_metamorphic_projection_tests.py
run_py scripts/check_metamorphic_projection_tests.py
run_py scripts/compile_benchmark_motifs.py
run_py scripts/check_benchmark_compiler.py
run_py scripts/compute_differential_reproducibility.py
run_py scripts/check_differential_reproducibility.py
run_py scripts/check_reproducibility_package.py
run_py scripts/check_package_integrity.py
run_paper_py scripts/check_package_coherence.py
if [[ "${RUN_LATEX_COMPILE:-0}" == "1" ]]; then
  run_paper_py_latex scripts/check_latex_compile.py
else
  run_paper_py scripts/check_latex_certificate.py
fi
run_py scripts/verify_generated_probes.py
run_py scripts/compute_sql_shape_diagnostics.py
run_py scripts/check_sql_shape_diagnostics.py
run_py scripts/check_stale_diagnostic_outputs.py
run_py scripts/check_mainline_grounded_only.py
if [[ "${RUN_EXPENSIVE_RECOMPUTE:-0}" == "1" ]]; then
  run_py scripts/compute_benchmark_efficiency.py
else
  run_py scripts/check_benchmark_efficiency_certificate.py
fi
run_py scripts/compute_probe_coverage_matrix.py
run_py scripts/check_probe_coverage_depth.py
run_py scripts/compute_engine_pair_matrix.py
run_py scripts/check_engine_pair_matrix.py
run_py scripts/compute_projection_mutation_suite.py
run_py scripts/check_projection_mutation_suite.py
run_py scripts/compute_counterfactual_repair_ablation.py
run_py scripts/check_counterfactual_repair_ablation.py
run_py scripts/build_proof_carrying_semantics.py
run_py scripts/check_proof_carrying_semantics.py
run_py scripts/build_provenance_deep_audit.py
run_py scripts/check_provenance_deep_audit.py
run_py scripts/compute_formal_obligations.py
run_py scripts/check_formal_obligations.py
run_py scripts/compute_relation_diagnostics.py
run_py scripts/check_relation_diagnostics.py
run_py scripts/compute_code_quality.py
run_py scripts/check_code_quality.py
run_py scripts/build_replay_plan.py
run_py scripts/check_replay_plan.py
run_py scripts/check_cli_smoke.py
run_py scripts/check_schema_coverage.py
run_py scripts/run_unit_tests.py
run_paper_py scripts/render_paper_tables.py
run_paper_py scripts/check_paper_table_sources.py
run_paper_py scripts/check_paper_quality.py
run_paper_py scripts/check_pdf_integrity.py
run_paper_py scripts/check_format_compliance.py
run_paper_py scripts/check_visual_latex_style.py
run_paper_py scripts/check_reference_quality.py
run_py scripts/check_shapley_attribution.py
run_py scripts/check_repair_certificate_minimality.py
run_py scripts/compute_repair_hitting_sets.py
run_py scripts/check_projection_proof_obligations.py
run_py scripts/check_projection_contract_semantics.py
run_py scripts/check_theorem_ledger.py
echo "[deep] OPTSEMC_DEVELOPMENT_SNAPSHOT=1 python scripts/check_git_tree_state.py"
OPTSEMC_DEVELOPMENT_SNAPSHOT=1 timeout "$PY_TIMEOUT" python -u scripts/check_git_tree_state.py
run_py scripts/build_claim_metric_summary.py
run_py scripts/build_claim_ledger.py
run_py scripts/check_artifact_hygiene.py
run_paper_py scripts/check_manuscript_style.py
clean_transients
run_py scripts/check_package_cleanliness.py
run_py scripts/run_repository_audit.py
run_py scripts/check_repository_quality.py
run_py scripts/check_codebase_scale.py
run_py scripts/check_artifact_registry.py
run_py scripts/build_environment_report.py
run_py scripts/check_environment_report.py
run_real_engine_check scripts/check_real_engine_validation.py
run_py scripts/check_real_engine_noninterference.py
run_py scripts/build_claim_metric_summary.py
run_py scripts/build_claim_ledger.py
run_py scripts/build_claim_evidence_graph.py
run_py scripts/check_claim_evidence_graph.py
echo "[deep] OPTSEMC_DEVELOPMENT_SNAPSHOT=1 python scripts/check_git_tree_state.py"
OPTSEMC_DEVELOPMENT_SNAPSHOT=1 timeout "$PY_TIMEOUT" python -u scripts/check_git_tree_state.py
run_py scripts/build_package_fingerprint.py
clean_transients
run_py scripts/build_package_manifest.py
run_py scripts/check_package_manifest.py
run_py scripts/check_certificate_freshness.py
run_py scripts/build_package_fingerprint.py
clean_transients
run_py scripts/build_package_manifest.py
run_py scripts/check_package_manifest.py
run_py scripts/check_package_snapshot.py
run_py scripts/run_integrity_suite.py
if [[ "${OPTSEMC_RELEASE_GATE:-0}" == "1" ]]; then
  echo "[deep] clean-tree assertion"
  OPTSEMC_RELEASE_GATE=1 timeout "$PY_TIMEOUT" python -u scripts/check_git_tree_state.py
  git -C .. diff --exit-code -- artifact/evaluation/git_tree_state.csv artifact/evaluation/git_tree_porcelain.txt artifact/evaluation/git_tree_state_check.csv
  test -z "$(git -C .. status --porcelain=v1 --untracked-files=all)"
fi
