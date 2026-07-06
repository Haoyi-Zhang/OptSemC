#!/usr/bin/env python3
"""Build a compact, machine-readable summary of headline grounded metrics.

The summary is used by traceability checks so that headline numbers in the
paper and claim matrix are regenerated from the same evaluation outputs that
feed the tables.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"
G = E / "grounded"
OUT = E / "claim_metric_summary.csv"


def count_lines(path: Path) -> int:
    with path.open(encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def optional_csv(path: Path) -> list[dict[str, str]] | None:
    if not path.exists():
        return None
    return read_csv(path)


def add(rows: list[dict[str, str]], metric: str, value: object, source: str) -> None:
    rows.append({"metric": metric, "value": str(value), "source": source})


def add_core_counts(rows: list[dict[str, str]]) -> None:
    add(rows, "grounded_rules", count_lines(ROOT / "grounded/verified_rules.jsonl"), "grounded/verified_rules.jsonl")
    add(rows, "grounded_segments", count_lines(ROOT / "grounded/verified_segments.jsonl"), "grounded/verified_segments.jsonl")
    add(rows, "public_sources", max(0, count_lines(ROOT / "grounded/verified_sources.csv") - 1), "grounded/verified_sources.csv")
    add(rows, "generated_probes", count_lines(ROOT / "benchmark/generated_probes.jsonl"), "benchmark/generated_probes.jsonl")
    for row in read_csv(E / "coverage_interactions.csv"):
        if row.get("coverage_target") in {"all_unique_interactions", "ALL"}:
            add(rows, "valid_interactions", row.get("valid_interactions", row.get("covered_interactions", "")), "evaluation/coverage_interactions.csv")


def add_trap_and_repair_metrics(rows: list[dict[str, str]]) -> None:
    for row in read_csv(G / "conditional_trap_rate.csv"):
        method = row.get("method") or row.get("projection")
        if method in {"keyword", "yesno", "operator_only"}:
            add(rows, f"{method}_projected_equivalences", row["projected_equivalences"], "evaluation/grounded/conditional_trap_rate.csv")
            add(rows, f"{method}_false_equivalences", row["false_equivalences"], "evaluation/grounded/conditional_trap_rate.csv")
            add(rows, f"{method}_conditional_false_rate", row["conditional_false_equivalence_rate"], "evaluation/grounded/conditional_trap_rate.csv")
    for row in read_csv(G / "repair_certificate_summary.csv"):
        method = row["method"]
        add(rows, f"{method}_repair_sets", row["repair_sets"], "evaluation/grounded/repair_certificate_summary.csv")
        add(rows, f"{method}_minimal_repair_size", row["minimal_universal_repair_size"], "evaluation/grounded/repair_certificate_summary.csv")
    for row in read_csv(G / "repair_basis_stability.csv"):
        if row.get("scope") == "all_projections":
            add(rows, "semantic_basis", row["basis"], "evaluation/grounded/repair_basis_stability.csv")
            add(rows, "semantic_basis_resolved", row["resolved"], "evaluation/grounded/repair_basis_stability.csv")
            add(rows, "semantic_basis_false_equivalences", row["false_equivalences"], "evaluation/grounded/repair_basis_stability.csv")
    for row in read_csv(G / "repair_generalization_summary.csv"):
        method = row.get("method") or row.get("projection")
        add(rows, f"{method}_heldout_false_equivalences", row.get("heldout_false_equivalence", row.get("heldout_false_equivalences", "")), "evaluation/grounded/repair_generalization_summary.csv")
        add(rows, f"{method}_heldout_resolved", row.get("resolved_by_learned_repair", row.get("heldout_resolved", "")), "evaluation/grounded/repair_generalization_summary.csv")


def add_optional_certificates(rows: list[dict[str, str]]) -> None:
    for row in optional_csv(E / "repair_certificate_minimality.csv") or []:
        add(rows, f'{row["method"]}_repair_minimality_passed', row["passed"], "evaluation/repair_certificate_minimality.csv")
    bench = {row["metric"]: row["value"] for row in optional_csv(G / "benchmark_efficiency_summary.csv") or []}
    for key in [
        "generated_full_rule_coverage_budget",
        "diagnostic_full_rule_coverage_budget",
        "generated_budget50_rule_coverage",
        "diagnostic_budget50_rule_coverage",
        "generated_budget100_rule_coverage",
        "diagnostic_budget100_rule_coverage",
        "random_mean_at_100",
        "random_p95_at_100",
    ]:
        if key in bench:
            add(rows, key, bench[key], "evaluation/grounded/benchmark_efficiency_summary.csv")
    proof = optional_csv(E / "projection_proof_obligations.csv")
    if proof is not None:
        add(rows, "projection_proof_obligations_passed", sum(1 for row in proof if row.get("passed") == "true"), "evaluation/projection_proof_obligations.csv")
        add(rows, "projection_proof_obligations_total", len(proof), "evaluation/projection_proof_obligations.csv")


def add_baseline_and_external_metrics(rows: list[dict[str, str]]) -> None:
    baseline_rows = optional_csv(G / "baseline_portfolio.csv")
    baseline = {row["projection"]: row for row in baseline_rows or []}
    for method in ["strict", "keyword", "yesno", "operator_only"]:
        if method in baseline:
            add(rows, f"{method}_baseline_false_equivalences", baseline[method]["false_equivalences"], "evaluation/grounded/baseline_portfolio.csv")
            add(rows, f"{method}_baseline_projected_equivalences", baseline[method]["projected_equivalences"], "evaluation/grounded/baseline_portfolio.csv")
    if baseline_rows is not None:
        add(rows, "baseline_portfolio_size", len(baseline), "evaluation/grounded/baseline_portfolio.csv")

    anchor_crosswalk = optional_csv(G / "external_benchmark_crosswalk.csv")
    if anchor_crosswalk is not None:
        add(rows, "external_anchor_motifs", len(anchor_crosswalk), "evaluation/grounded/external_benchmark_crosswalk.csv")
        add(rows, "external_anchor_requirements", sum(int(row["total_requirements"]) for row in anchor_crosswalk), "evaluation/grounded/external_benchmark_crosswalk.csv")
        add(rows, "external_anchor_requirements_covered", sum(int(row["covered_requirements"]) for row in anchor_crosswalk), "evaluation/grounded/external_benchmark_crosswalk.csv")

    suite_rows = optional_csv(E / "external_benchmark_suite.csv")
    if suite_rows is not None:
        add(rows, "external_benchmark_suites", len(suite_rows), "evaluation/external_benchmark_suite.csv")
        add(rows, "external_benchmark_motifs", sum(int(row["motifs"]) for row in suite_rows), "evaluation/external_benchmark_suite.csv")
        add(rows, "external_benchmark_motifs_covered", sum(int(row["covered_motifs"]) for row in suite_rows), "evaluation/external_benchmark_suite.csv")
        add(rows, "external_benchmark_matching_probes", sum(int(row["matching_probes"]) for row in suite_rows), "evaluation/external_benchmark_suite.csv")

    exec_summary = {row["metric"]: row["value"] for row in optional_csv(E / "external_motif_execution_summary.csv") or []}
    for key in [
        "external_motifs",
        "matched_motifs",
        "executed_motifs",
        "execution_failures",
        "distinct_representative_probes",
        "motifs_per_representative_min",
        "motifs_per_representative_max",
        "shared_representative_probes",
        "suites",
    ]:
        if key in exec_summary:
            add(rows, f"external_motif_representative_{key}", exec_summary[key], "evaluation/external_motif_execution_summary.csv")


def add_real_engine_metrics(rows: list[dict[str, str]]) -> None:
    for subset in ["motif", "full"]:
        source_path = E / f"real_engine_probe_validation_{subset}_summary.csv"
        real_rows = optional_csv(source_path)
        if real_rows is None:
            continue
        source = f"evaluation/real_engine_probe_validation_{subset}_summary.csv"
        total_probes = sum(int(row["probes"]) for row in real_rows)
        total_success = sum(int(row["execution_successes"]) for row in real_rows)
        total_failures = sum(int(row["execution_failures"]) for row in real_rows)
        min_match = min((float(row["mean_visible_match_rate"]) for row in real_rows), default=0.0)
        add(rows, f"real_engine_{subset}_engines", len(real_rows), source)
        add(rows, f"real_engine_{subset}_validations", total_probes, source)
        add(rows, f"real_engine_{subset}_execution_successes", total_success, source)
        add(rows, f"real_engine_{subset}_execution_failures", total_failures, source)
        add(rows, f"real_engine_{subset}_min_visible_match_rate", f"{min_match:.6f}", source)
        for row in real_rows:
            engine = row["engine"]
            add(rows, f"real_engine_{subset}_{engine}_probes", row["probes"], source)
            add(rows, f"real_engine_{subset}_{engine}_execution_successes", row["execution_successes"], source)
            add(rows, f"real_engine_{subset}_{engine}_distinct_plan_hashes", row["distinct_plan_hashes"], source)


def add_scaling_and_diagnostic_metrics(rows: list[dict[str, str]]) -> None:
    scale = {row["metric"]: row["value"] for row in optional_csv(E / "scalability_stress_summary.csv") or []}
    for key in ["full_pairwise_comparisons_per_projection", "full_min_comparisons_per_second", "full_elapsed_ms_total"]:
        if key in scale:
            add(rows, key, scale[key], "evaluation/scalability_stress_summary.csv")

    family = {row["projection"]: row for row in optional_csv(E / "engine_family_stress_summary.csv") or []}
    for method in ["keyword", "operator_only", "operator_kind_surface"]:
        if method in family:
            add(rows, f"{method}_family_false_equivalences", family[method]["false_equivalences"], "evaluation/engine_family_stress_summary.csv")
            add(rows, f"{method}_families_with_false_equivalence", family[method]["families_with_false_equivalence"], "evaluation/engine_family_stress_summary.csv")
            add(rows, f"{method}_family_unresolved_after_layer_placement", family[method]["unresolved_after_layer_placement"], "evaluation/engine_family_stress_summary.csv")

    stale = optional_csv(E / "stale_diagnostic_outputs.csv")
    if stale is not None:
        add(rows, "stale_diagnostic_checks_passed", sum(1 for row in stale if row.get("passed") == "true"), "evaluation/stale_diagnostic_outputs.csv")
        add(rows, "stale_diagnostic_checks_total", len(stale), "evaluation/stale_diagnostic_outputs.csv")


def metric_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    add_core_counts(rows)
    add_trap_and_repair_metrics(rows)
    add_optional_certificates(rows)
    add_baseline_and_external_metrics(rows)
    add_real_engine_metrics(rows)
    add_scaling_and_diagnostic_metrics(rows)
    return rows


def main() -> None:
    rows = metric_rows()
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value", "source"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote claim metric summary with {len(rows)} metrics")


if __name__ == "__main__":
    main()
