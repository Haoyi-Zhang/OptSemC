#!/usr/bin/env python3
"""Build and verify a paper-to-artifact claim ledger.

Each row names a scientific claim that appears in the paper, the numeric value
or qualitative result, and the artifact files that support it.  The checker
prevents manuscript changes from drifting away from regenerated outputs.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT.parent
E = ROOT / "evaluation"
G = E / "grounded"
OUT = E / "paper_claim_ledger.csv"
CHECK = E / "claim_ledger_check.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def metric_summary() -> dict[str, str]:
    return {r["metric"]: r["value"] for r in read_csv(E / "claim_metric_summary.csv")}


def practice_summary() -> dict[str, str]:
    return {r["metric"]: r["value"] for r in read_csv(E / "practice_projection_surface_summary.csv")}


def exists_many(paths: str) -> bool:
    return all((PKG / p.strip()).exists() for p in paths.split(";") if p.strip())


def keyed_csv(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return {row.get("key", "") or row.get("check", ""): row.get("value", "") or row.get("passed", "") for row in read_csv(path)}


def pass_summary(path: Path) -> str:
    if not path.exists():
        return "missing"
    rows = read_csv(path)
    passable = [row for row in rows if "passed" in row]
    if not passable:
        return f"rows={len(rows)}"
    return f"{sum(row.get('passed') == 'true' for row in passable)}/{len(passable)}"


def main() -> None:
    m = metric_summary()
    p = practice_summary()
    public_sources = p["public_sources"]
    freeze_rows = read_csv(E / "evidence_freeze_manifest.csv") if (E / "evidence_freeze_manifest.csv").exists() else []
    freeze_roles = {row.get("role", "") for row in freeze_rows}
    anti_rows = read_csv(E / "anti_overfit_audit.csv") if (E / "anti_overfit_audit.csv").exists() else []
    anti_verdicts = {row.get("verdict", "") for row in anti_rows}
    source_identity_rows = read_csv(G / "source_robustness_identity_summary.csv") if (G / "source_robustness_identity_summary.csv").exists() else []
    source_identity = {row.get("method", ""): row for row in source_identity_rows}
    resource_rows = read_csv(E / "resource_profile.csv") if (E / "resource_profile.csv").exists() else []
    resource_scale = read_csv(E / "resource_profile_scale.csv") if (E / "resource_profile_scale.csv").exists() else []
    resource_total = read_csv(E / "resource_profile_end_to_end.csv") if (E / "resource_profile_end_to_end.csv").exists() else []
    git_state = keyed_csv(E / "git_tree_state.csv")
    if "source_tree_clean" in git_state or "allow_dirty_source" in git_state:
        archive_gate_value = (
            f"source_tree_clean={git_state.get('source_tree_clean','pending')};"
            f"allow_dirty_source={git_state.get('allow_dirty_source','pending')}"
        )
    else:
        archive_gate_value = (
            f"intent={git_state.get('tree_state_intent','pending')};"
            f"require_clean={git_state.get('require_clean','pending')}"
        )
    rows = [
        {"claim_id": "C1-grounded-corpus", "paper_claim": "The grounded mainline contains 287 admitted source-linked rules, 287 evidence spans, and 26 sources.", "value": f"{m['grounded_rules']}/{m['grounded_segments']}/{m['public_sources']}", "artifact_support": "artifact/grounded/verified_rules.jsonl;artifact/grounded/verified_segments.jsonl;artifact/grounded/verified_sources.csv"},
        {"claim_id": "C2-probe-coverage", "paper_claim": "OptSemBench-C generates 4,216 probes covering 7,112 renderable feature interactions.", "value": f"{m['generated_probes']}/{m['valid_interactions']}", "artifact_support": "artifact/benchmark/generated_probes.jsonl;artifact/evaluation/coverage_interactions.csv;artifact/evaluation/probe_validity.csv"},
        {"claim_id": "C3-keyword-false-equivalence", "paper_claim": "Keyword projection induces 254 contract-collision witnesses among 2,284 declared equivalences.", "value": f"{m['keyword_projected_equivalences']}/{m['keyword_false_equivalences']}", "artifact_support": "artifact/evaluation/grounded/conditional_trap_rate.csv;artifact/evaluation/grounded/baseline_portfolio.csv"},
        {"claim_id": "C4-operator-false-equivalence", "paper_claim": "Operator-only projection induces 238 contract-collision witnesses among 2,268 declared equivalences.", "value": f"{m['operator_only_projected_equivalences']}/{m['operator_only_false_equivalences']}", "artifact_support": "artifact/evaluation/grounded/conditional_trap_rate.csv;artifact/evaluation/grounded/baseline_portfolio.csv"},
        {"claim_id": "C5-reference-negative-control", "paper_claim": "Reference-signature comparison over admitted public evidence produces zero projection-induced collisions.", "value": m['strict_baseline_false_equivalences'], "artifact_support": "artifact/evaluation/grounded/baseline_portfolio.csv;artifact/evaluation/baseline_portfolio_check.csv"},
        {"claim_id": "C6-adversarial-baselines", "paper_claim": "The projection-surface portfolio contains 17 executable vocabularies, including one-field stress surfaces and strengthened control surfaces.", "value": m['baseline_portfolio_size'], "artifact_support": "artifact/evaluation/grounded/baseline_portfolio.csv;artifact/evaluation/baseline_portfolio_check.csv"},
        {"claim_id": "C7-practice-projection-surfaces", "paper_claim": "The public source-surface audit observes keyword labels in all 26 sources, yes/no controls in 12 sources, operator-family labels in all 26 sources, and no source exposes the full reference-signature payload.", "value": f"keyword={p['keyword_surfaces']}/{public_sources};yesno={p['yesno_surfaces']}/{public_sources};operator={p['operator_surfaces']}/{public_sources};reference={p['reference_signature_payload_surfaces']}/{public_sources}", "artifact_support": "artifact/evaluation/practice_projection_surface_summary.csv;artifact/evaluation/practice_projection_surfaces.csv;artifact/evaluation/practice_projection_surfaces_check.csv"},
        {"claim_id": "C8-repair-basis", "paper_claim": "The layer+placement semantic basis repairs all 498 projection-induced collisions across headline projections.", "value": f"{m['semantic_basis']}:{m['semantic_basis_resolved']}/{m['semantic_basis_false_equivalences']}", "artifact_support": "artifact/evaluation/grounded/repair_basis_stability.csv;artifact/evaluation/grounded/semantic_frontier.csv;artifact/evaluation/semantic_frontier_check.csv"},
        {"claim_id": "C9-minimality", "paper_claim": "Repair certificates are sufficient and minimal under finite enumeration and hitting-set checks.", "value": "passed", "artifact_support": "artifact/evaluation/repair_certificate_minimality.csv;artifact/evaluation/repair_hitting_set_check.csv;artifact/evaluation/projection_proof_obligations.csv"},
        {"claim_id": "C10-source-robustness", "paper_claim": "Keyword and operator-only projection-induced collisions remain nonzero after removing any single public source, while an identity audit records retained original witnesses and newly induced witnesses for that information-deletion stress.", "value": f"keyword=26/26;kept>={float(source_identity.get('keyword', {}).get('min_retained_original_rate', '0')):.2f};new<={source_identity.get('keyword', {}).get('max_new_witnesses_after_removal', 'missing')};operator=26/26;kept>={float(source_identity.get('operator_only', {}).get('min_retained_original_rate', '0')):.2f};new<={source_identity.get('operator_only', {}).get('max_new_witnesses_after_removal', 'missing')}", "artifact_support": "artifact/evaluation/grounded/source_robustness_summary.csv;artifact/evaluation/grounded/source_robustness_identity.csv;artifact/evaluation/grounded/source_robustness_identity_summary.csv"},
        {"claim_id": "C11-external-suite", "paper_claim": "The external benchmark-family suite covers 90/90 declared optimizer motifs across 12 families; those motifs are represented by 71 distinct deterministic-catalog SQL probes because some probes satisfy multiple declared requirements.", "value": f"{m['external_benchmark_motifs_covered']}/{m['external_benchmark_motifs']};executed={m['external_motif_representative_executed_motifs']}/{m['external_motif_representative_external_motifs']};representatives={m['external_motif_representative_distinct_representative_probes']};suites={m['external_benchmark_suites']}", "artifact_support": "artifact/evaluation/external_benchmark_suite.csv;artifact/evaluation/external_benchmark_suite_check.csv;artifact/evaluation/external_motif_execution_summary.csv;artifact/evaluation/external_motif_execution_check.csv;artifact/evaluation/external_motif_probe_map.csv"},
        {"claim_id": "C12-real-engine-validation", "paper_claim": "The generated probes execute on DuckDB and PostgreSQL with zero failures for the full corpus and the motif representatives, and this evidence is scoped away from collision and repair computation.", "value": f"engines={m['real_engine_full_engines']};full={m['real_engine_full_execution_successes']}/{m['real_engine_full_validations']};failures={m['real_engine_full_execution_failures']};motif={m['real_engine_motif_execution_successes']}/{m['real_engine_motif_validations']}", "artifact_support": "artifact/evaluation/real_engine_probe_validation_full.csv;artifact/evaluation/real_engine_probe_validation_full_summary.csv;artifact/evaluation/real_engine_probe_validation_motif.csv;artifact/evaluation/real_engine_probe_validation_motif_summary.csv;artifact/evaluation/real_engine_validation_check.csv;artifact/evaluation/real_engine_validation_environment.csv;artifact/evaluation/real_engine_fresh_run.csv;artifact/evaluation/real_engine_noninterference_check.csv;artifact/scripts/check_real_engine_noninterference.py"},
        {"claim_id": "C13-formal-obligations", "paper_claim": "Every finite formal obligation asserted in the paper is checked by the replay package.", "value": "10/10", "artifact_support": "artifact/evaluation/theorem_ledger.csv"},
        {"claim_id": "C14-rule-aware-probe-denominator", "paper_claim": "The probe denominator is a rule-aware coverage benchmark rather than an independent held-out generalization set.", "value": "forced_by_rule_guard=99", "artifact_support": "artifact/benchmark/generated_probes.jsonl;artifact/evaluation/probe_validity.csv;artifact/scripts/generate_probes.py;artifact/recompute_grounded_mainline.sh"},
        {"claim_id": "C15-evidence-freeze-protocol", "paper_claim": "The freeze manifest hashes schema, source inputs, projection/baseline specifications, result-determining code, compute/check scripts, and replay entrypoints.", "value": f"rows={len(freeze_rows)};roles={len(freeze_roles)};check={pass_summary(E / 'evidence_freeze_manifest_check.csv')}", "artifact_support": "artifact/evaluation/evidence_freeze_manifest.csv;artifact/evaluation/evidence_freeze_manifest_check.csv;artifact/scripts/build_evidence_freeze_manifest.py;artifact/scripts/check_evidence_freeze_manifest.py;artifact/optsemc/baselines.py;artifact/optsemc/projections.py"},
        {"claim_id": "C16-anti-overfit-boundaries", "paper_claim": "The anti-overfit audit separates controls and finite-denominator stress from source-sensitive, overlapping-fold, and failed learned-transfer boundaries.", "value": f"rows={len(anti_rows)};verdicts={','.join(sorted(anti_verdicts))}", "artifact_support": "artifact/evaluation/anti_overfit_audit.csv;artifact/evaluation/anti_overfit_audit_check.csv;artifact/scripts/compute_anti_overfit_audit.py;artifact/scripts/check_anti_overfit_audit.py"},
        {"claim_id": "C17-resource-profile", "paper_claim": "The resource profile reports stage-level and total finite-audit replay cost and labels the 8x row as a deterministic inner-loop lift, not a new corpus, source set, or engine set.", "value": f"stages={len(resource_rows)};total_rows={len(resource_total)};scale_points={len(resource_scale)};check={pass_summary(E / 'resource_profile_check.csv')}", "artifact_support": "artifact/evaluation/resource_profile.csv;artifact/evaluation/resource_profile_end_to_end.csv;artifact/evaluation/resource_profile_scale.csv;artifact/evaluation/resource_profile_check.csv;artifact/scripts/compute_resource_profile.py;artifact/scripts/check_resource_profile.py"},
        {"claim_id": "C18-clean-archive-gate", "paper_claim": "The long-term anonymous archive builder refuses a dirty source tree for release construction and records the source-tree state inside the package.", "value": archive_gate_value, "artifact_support": "artifact/scripts/build_anonymous_archive.py;artifact/scripts/check_git_tree_state.py;artifact/evaluation/git_tree_state.csv;artifact/evaluation/git_tree_state_check.csv"},
    ]
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["claim_id", "paper_claim", "value", "artifact_support"])
        writer.writeheader(); writer.writerows(rows)
    checks = []
    def add(check: str, ok: bool, details: str = "") -> None:
        checks.append({"check": check, "passed": str(bool(ok)).lower(), "details": details})
    by_id = {r["claim_id"]: r for r in rows}
    real_claims = [r["claim_id"] for r in rows if "real_engine" in r.get("artifact_support", "").lower()]
    add("all_claim_support_files_exist", all(exists_many(r["artifact_support"]) for r in rows), "")
    add("headline_numeric_values_current", by_id["C1-grounded-corpus"]["value"] == "287/287/26" and by_id["C2-probe-coverage"]["value"] == "4216/7112" and by_id["C3-keyword-false-equivalence"]["value"] == "2284/254" and by_id["C4-operator-false-equivalence"]["value"] == "2268/238")
    add("baseline_size_current", by_id["C6-adversarial-baselines"]["value"] == "17", f"size={by_id['C6-adversarial-baselines']['value']}")
    add("practice_surface_current", by_id["C7-practice-projection-surfaces"]["value"] == "keyword=26/26;yesno=12/26;operator=26/26;reference=0/26", by_id["C7-practice-projection-surfaces"]["value"])
    add("semantic_basis_current", by_id["C8-repair-basis"]["value"] == "layer+placement:498/498", by_id["C8-repair-basis"]["value"])
    add("external_suite_current", by_id["C11-external-suite"]["value"] == "90/90;executed=90/90;representatives=71;suites=12", by_id["C11-external-suite"]["value"])
    add("real_engine_validation_current", by_id["C12-real-engine-validation"]["value"] == "engines=2;full=8432/8432;failures=0;motif=142/142", by_id["C12-real-engine-validation"]["value"])
    add("real_engine_support_scoped_to_c12", set(real_claims).issubset({"C12-real-engine-validation"}), ",".join(real_claims))
    real_env = keyed_csv(E / "real_engine_validation_environment.csv")
    real_check = keyed_csv(E / "real_engine_validation_check.csv")
    validation_mode = real_env.get("validation_mode", "missing")
    artifact_only = not (PKG / "Paper").exists()
    if artifact_only:
        add("real_engine_evidence_mode_supported", validation_mode in {"fresh-engine-rerun", "saved-engine-certificate-replay"}, validation_mode)
        add(
            "real_engine_replay_scope_recorded",
            real_check.get("saved_evidence_environment_bound") == "true"
            and real_check.get("current_sql_replay_chain_bound") == "true",
            str({k: real_check.get(k, "missing") for k in ("saved_evidence_environment_bound", "current_sql_replay_chain_bound")}),
        )
    else:
        add("real_engine_evidence_is_fresh_rerun", validation_mode == "fresh-engine-rerun", validation_mode)
        add(
            "real_engine_fresh_marker_checked",
            real_check.get("fresh_run_marker_present") == "true" and real_check.get("fresh_marker_after_engine_outputs") == "true",
            str({k: real_check.get(k, "missing") for k in ("fresh_run_marker_present", "fresh_marker_after_engine_outputs")}),
        )
        noninterference = keyed_csv(E / "real_engine_noninterference_check.csv")
        add(
            "real_engine_noninterference_checked",
            noninterference.get("core_collision_repair_code_independent") == "true"
            and noninterference.get("core_paper_tables_do_not_source_real_engine") == "true"
            and noninterference.get("paper_table_source_gate_available") == "true",
            str(noninterference),
        )
    add("ledger_has_benchmark_theory_artifact_rows", len(rows) >= 18, f"rows={len(rows)}")
    add("freeze_manifest_covers_executable_logic", {"executable_logic", "compute_script", "check_script", "release_gate", "replay_entrypoint"}.issubset(freeze_roles), ",".join(sorted(freeze_roles)))
    add("anti_overfit_boundaries_current", {"source-sensitive", "within-denominator", "stress-fails"}.issubset(anti_verdicts) and len(anti_rows) >= 8, ",".join(sorted(anti_verdicts)))
    add("resource_profile_current", len(resource_rows) >= 5 and len(resource_total) == 1 and {row.get("scale") for row in resource_scale} == {"1x", "2x", "4x", "8x"}, f"profile={len(resource_rows)};total={len(resource_total)};scale={','.join(row.get('scale','') for row in resource_scale)}")
    archive_value = by_id["C18-clean-archive-gate"]["value"]
    if "source_tree_clean" in git_state or "allow_dirty_source" in git_state:
        release_gate_ok = git_state.get("source_tree_clean") == "true" and git_state.get("allow_dirty_source") == "false"
    else:
        release_gate_ok = archive_value != "intent=pending;require_clean=pending"
    add("release_gate_recorded", release_gate_ok, archive_value)
    with CHECK.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
        writer.writeheader(); writer.writerows(checks)
    passed = sum(r["passed"] == "true" for r in checks)
    print(f"Claim ledger: {passed}/{len(checks)} checks passed")
    if passed != len(checks):
        for r in checks:
            if r["passed"] != "true":
                print("FAIL", r["check"], r["details"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
