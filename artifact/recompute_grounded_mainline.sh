#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/scripts${PYTHONPATH:+:$PYTHONPATH}"
python scripts/generate_probes.py --rules grounded/verified_rules.jsonl
python scripts/verify_generated_probes.py
python scripts/match_rules.py --rules grounded/verified_rules.jsonl --probes benchmark/generated_probes.jsonl --out evaluation/grounded_applicable_rules.jsonl
python scripts/merge_contracts.py --applicable evaluation/grounded_applicable_rules.jsonl --out evaluation/grounded_contract_maps.jsonl --support evaluation/grounded_contract_support.jsonl --conflicts evaluation/grounded_conflicts.jsonl
python scripts/compute_metrics.py --rules grounded/verified_rules.jsonl --probes benchmark/generated_probes.jsonl --applicable evaluation/grounded_applicable_rules.jsonl --maps evaluation/grounded_contract_maps.jsonl --outdir evaluation/grounded
python scripts/compute_grounded_conditional_traps.py --maps evaluation/grounded_contract_maps.jsonl --out evaluation/grounded/conditional_trap_rate.csv --examples-out evaluation/grounded/conditional_trap_examples.jsonl
python scripts/analyze_grounded_projection_loss.py --maps evaluation/grounded_contract_maps.jsonl --outdir evaluation/grounded
python scripts/compute_grounded_repair_certificates.py
python scripts/compute_grounded_semantic_repair_basis.py
python scripts/compute_grounded_repair_curve.py --maps evaluation/grounded_contract_maps.jsonl --out evaluation/grounded/semantic_repair_curve.csv
python scripts/compute_grounded_pair_failures.py --maps evaluation/grounded_contract_maps.jsonl --out evaluation/grounded/pair_false_portability.csv
python scripts/compute_workload_sensitivity.py --probes benchmark/generated_probes.jsonl --maps evaluation/grounded_contract_maps.jsonl --out evaluation/grounded/workload_sensitivity.csv
python scripts/compute_benchmark_efficiency.py
(cd .. && python artifact/scripts/generate_grounded_case_studies.py)
python scripts/audit_grounded_core.py
python scripts/check_grounded_readiness.py
python scripts/check_grounded_traceability.py
python scripts/check_mainline_grounded_only.py
python scripts/check_paper_table_sources.py
python scripts/check_stale_diagnostic_outputs.py
python scripts/run_unit_tests.py

python scripts/compute_repair_basis_stability.py
python scripts/compute_baseline_portfolio.py
python scripts/compute_external_benchmark_crosswalk.py

python scripts/compute_repair_hitting_sets.py
python scripts/check_projection_proof_obligations.py
python scripts/compute_projection_lattice.py
python scripts/check_projection_lattice.py
python scripts/compute_semantic_frontier.py
python scripts/compute_projection_resolution_lattice.py
python scripts/check_projection_resolution_lattice.py

python scripts/check_theorem_ledger.py
python scripts/build_claim_metric_summary.py
python scripts/build_claim_ledger.py
python scripts/build_adversarial_audit_matrix.py

python scripts/export_sql_probe_bundle.py
python scripts/check_sql_probe_bundle.py
python scripts/execute_sql_probe_suite.py
python scripts/check_sql_probe_execution.py
python scripts/compile_benchmark_motifs.py
python scripts/check_benchmark_compiler.py
python scripts/compute_benchmark_motif_difficulty.py
python scripts/check_benchmark_motif_difficulty.py
python scripts/compute_external_benchmark_suite.py
python scripts/check_external_benchmark_suite.py
python scripts/execute_external_motif_suite.py
python scripts/check_external_motif_execution.py
python scripts/check_no_cache_package.py
python scripts/compute_incremental_update_stress.py
python scripts/check_incremental_update_stress.py
python scripts/compute_leave_out_stability.py
python scripts/check_leave_out_stability.py
python scripts/compute_witness_diversity.py
python scripts/check_witness_diversity.py
python scripts/compute_witness_dispersion.py
python scripts/check_witness_dispersion.py
python scripts/compute_algorithmic_scaling.py
python scripts/check_algorithmic_scaling.py
python scripts/compute_scalability_regression.py
python scripts/check_scalability_regression.py
python scripts/compute_incremental_audit.py
python scripts/check_incremental_audit.py
python scripts/render_scaling_and_incremental_tables.py
python scripts/check_paper_numeric_claims.py
