.PHONY: verify deep paper baselines external frontier claims tests repository coverage proofs replay manifest clean package-check clean-gate artifact-archive
export PYTHONPATH := $(CURDIR):$(CURDIR)/scripts$(if $(PYTHONPATH),:$(PYTHONPATH))

verify:
	./run_mainline_checks.sh

deep:
	./run_deep_checks.sh

paper:
	python scripts/check_latex_compile.py && python scripts/check_pdf_integrity.py && python scripts/check_format_compliance.py && python scripts/check_visual_latex_style.py

baselines:
	python scripts/compute_baseline_portfolio.py && python scripts/compute_projection_mutation_suite.py && python scripts/check_projection_mutation_suite.py

external:
	python scripts/compute_external_benchmark_crosswalk.py && python scripts/compute_external_benchmark_suite.py && python scripts/check_external_benchmark_suite.py

frontier:
	python scripts/compute_semantic_frontier.py && python scripts/compute_counterfactual_repair_ablation.py && python scripts/check_counterfactual_repair_ablation.py

claims:
	python scripts/build_claim_metric_summary.py && python scripts/build_claim_ledger.py && python scripts/build_claim_evidence_graph.py && python scripts/check_claim_evidence_graph.py

proofs:
	python scripts/build_proof_carrying_semantics.py && python scripts/check_proof_carrying_semantics.py && python scripts/compute_formal_obligations.py && python scripts/check_formal_obligations.py

coverage:
	python scripts/compute_probe_coverage_matrix.py && python scripts/check_probe_coverage_depth.py && python scripts/compute_engine_pair_matrix.py && python scripts/check_engine_pair_matrix.py

replay:
	python scripts/build_replay_plan.py && python scripts/check_replay_plan.py && python scripts/check_cli_smoke.py

tests:
	python scripts/run_unit_tests.py && python scripts/check_core_library_contract.py

repository:
	python scripts/check_repository_quality.py && python scripts/check_codebase_scale.py && python scripts/compute_code_quality.py && python scripts/check_code_quality.py && python scripts/check_artifact_registry.py

manifest:
	python scripts/build_package_manifest.py && python scripts/check_package_manifest.py

package-check:
	python scripts/check_makefile_targets.py && python scripts/check_package_integrity.py && python scripts/check_source_witness_support.py && python scripts/check_side_balanced_witness_support.py

clean-gate:
	OPTSEMC_REQUIRE_CLEAN_GIT=1 python scripts/check_git_tree_state.py && python scripts/check_artifact_hygiene.py && python scripts/check_package_cleanliness.py && python scripts/check_repository_quality.py && python scripts/check_certificate_freshness.py

artifact-archive:
	OPTSEMC_REQUIRE_CLEAN_GIT=1 python scripts/check_git_tree_state.py && python scripts/build_anonymous_archive.py

clean:
	find .. -type d \( -name __pycache__ -o -name .pytest_cache -o -name '*.egg-info' \) -prune -exec rm -rf {} +
	find .. -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
	find ../Paper/latex -maxdepth 1 -type f \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' -o -name '*.bbl' -o -name '*.blg' -o -name '*.fls' -o -name '*.fdb_latexmk' \) -delete

audit-all: verify tests paper package-check manifest
	python scripts/check_package_snapshot.py && python scripts/run_integrity_suite.py
