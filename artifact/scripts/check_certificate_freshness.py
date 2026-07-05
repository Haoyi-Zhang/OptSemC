#!/usr/bin/env python3
"""Check that key certificates are present, current, and bound to evidence hashes."""
from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifact"
E = ART / "evaluation"
OUT = E / "certificate_freshness_check.csv"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def newest(paths: list[Path]) -> float:
    existing = [path.stat().st_mtime for path in paths if path.exists()]
    return max(existing) if existing else 0.0


def oldest(paths: list[Path]) -> float:
    existing = [path.stat().st_mtime for path in paths if path.exists()]
    return min(existing) if existing else 0.0


rows: list[dict[str, str]] = []


def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})


def outputs_current(name: str, outputs: list[Path], inputs: list[Path]) -> None:
    missing_outputs = [path.relative_to(ROOT).as_posix() for path in outputs if not path.exists()]
    missing_inputs = [path.relative_to(ROOT).as_posix() for path in inputs if not path.exists()]
    if missing_outputs or missing_inputs:
        add(name, False, f"missing_outputs={';'.join(missing_outputs)};missing_inputs={';'.join(missing_inputs)}")
        return
    add(name, oldest(outputs) >= newest(inputs), f"outputs={len(outputs)};inputs={len(inputs)}")


def paper_table_source_inputs() -> list[Path]:
    manifest = E / "paper_table_manifest.csv"
    inputs = [manifest, ART / "scripts" / "check_paper_table_sources.py"]
    if not manifest.exists():
        return inputs
    try:
        for row in read_csv(manifest):
            for key in ("latex_file", "source_files"):
                value = row.get(key, "")
                for item in [part.strip() for part in value.split(";") if part.strip()]:
                    inputs.append(ROOT / item)
    except Exception:
        return inputs
    return inputs


outputs_current(
    "practice_projection_surface_outputs_current",
    [E / "practice_projection_surfaces.csv", E / "practice_projection_surface_summary.csv", E / "practice_projection_surfaces_check.csv"],
    [ART / "config" / "practice_projection_surfaces.csv", ART / "scripts" / "compute_practice_projection_surfaces.py", ART / "scripts" / "check_practice_projection_surfaces.py"],
)
outputs_current(
    "claim_ledger_outputs_current",
    [E / "paper_claim_ledger.csv", E / "claim_ledger_check.csv"],
    [
        ART / "scripts" / "build_claim_ledger.py",
        E / "practice_projection_surfaces_check.csv",
        E / "real_engine_validation_check.csv",
        E / "real_engine_noninterference_check.csv",
        E / "resource_profile_end_to_end.csv",
        E / "anti_overfit_audit.csv",
        E / "grounded" / "source_robustness_identity_summary.csv",
    ],
)
outputs_current(
    "source_robustness_outputs_current",
    [
        E / "grounded" / "source_robustness.csv",
        E / "grounded" / "source_robustness_summary.csv",
        E / "grounded" / "source_robustness_identity.csv",
        E / "grounded" / "source_robustness_identity_summary.csv",
    ],
    [
        ART / "scripts" / "compute_grounded_source_robustness.py",
        ART / "grounded" / "verified_rules.jsonl",
        E / "grounded_applicable_rules.jsonl",
    ],
)
outputs_current(
    "anti_overfit_outputs_current",
    [E / "anti_overfit_audit.csv", E / "anti_overfit_audit_check.csv"],
    [
        ART / "scripts" / "compute_anti_overfit_audit.py",
        ART / "scripts" / "check_anti_overfit_audit.py",
        E / "grounded" / "source_robustness_summary.csv",
        E / "grounded" / "source_robustness_identity_summary.csv",
        E / "feature_holdout_repair_summary.csv",
        E / "engine_family_stress_summary.csv",
        E / "grounded" / "probe_subsample_robustness.csv",
        E / "grounded" / "repair_enginepair_generalization_summary.csv",
    ],
)
outputs_current(
    "environment_outputs_current",
    [E / "environment.csv", E / "environment_check.csv"],
    [ART / "scripts" / "build_environment_report.py", ART / "scripts" / "check_environment_report.py"],
)
outputs_current(
    "real_engine_validation_check_current",
    [E / "real_engine_validation_check.csv", E / "real_engine_validation_environment.csv", E / "real_engine_noninterference_check.csv"],
    [
        ART / "scripts" / "check_real_engine_validation.py",
        ART / "scripts" / "check_real_engine_noninterference.py",
        E / "environment.csv",
        E / "real_engine_probe_validation_full.csv",
        E / "real_engine_probe_validation_full_summary.csv",
        E / "real_engine_probe_validation_motif.csv",
        E / "real_engine_probe_validation_motif_summary.csv",
        E / "sql_probe_execution.csv",
        E / "sql_probe_execution_summary.csv",
        E / "sql_probe_execution_check.csv",
        E / "sql_probe_multicatalog_summary.csv",
        E / "sql_probe_multicatalog_totals.csv",
        E / "sql_probe_multicatalog_check.csv",
        E / "paper_table_manifest.csv",
        E / "paper_table_source_check.csv",
    ],
)
outputs_current(
    "resource_profile_outputs_current",
    [E / "resource_profile.csv", E / "resource_profile_scale.csv", E / "resource_profile_end_to_end.csv", E / "resource_profile_check.csv"],
    [ART / "scripts" / "compute_resource_profile.py", ART / "scripts" / "check_resource_profile.py"],
)
outputs_current(
    "claim_graph_outputs_current",
    [E / "claim_evidence_graph.csv", E / "claim_evidence_graph_check.csv", E / "claim_evidence_gate_cover.csv"],
    [ART / "scripts" / "build_claim_evidence_graph.py", ART / "scripts" / "check_claim_evidence_graph.py"],
)
outputs_current(
    "repair_generalization_outputs_current",
    [
        E / "grounded" / "repair_generalization_folds.csv",
        E / "grounded" / "repair_generalization_summary.csv",
        E / "repair_generalization_summary.csv",
        E / "repair_generalization_check.csv",
    ],
    [
        ART / "scripts" / "compute_repair_generalization.py",
        ART / "scripts" / "check_repair_generalization.py",
        E / "grounded_contract_maps.jsonl",
    ],
)
outputs_current(
    "git_tree_state_outputs_current",
    [E / "git_tree_state.csv", E / "git_tree_porcelain.txt", E / "git_tree_state_check.csv"],
    [ART / "scripts" / "check_git_tree_state.py"],
)
outputs_current(
    "package_manifest_outputs_current",
    [E / "package_manifest.csv", E / "package_manifest_summary.csv", E / "package_manifest_check.csv"],
    [ART / "scripts" / "build_package_manifest.py", ART / "optsemc" / "manifest.py"],
)
outputs_current(
    "package_fingerprint_outputs_current",
    [E / "package_files.csv", E / "package_fingerprint_summary.csv"],
    [ART / "scripts" / "build_package_fingerprint.py", ART / "optsemc" / "package_builder.py"],
)
outputs_current(
    "repository_quality_outputs_current",
    [E / "repository_audit.csv", E / "repository_quality.csv", E / "repository_quality_check.csv"],
    [ART / "scripts" / "run_repository_audit.py", ART / "scripts" / "check_repository_quality.py", ART / "optsemc" / "repository.py"],
)

if (ROOT / "Paper").exists():
    tex_inputs = sorted((ROOT / "Paper" / "latex").rglob("*.tex"))
    bib_inputs = sorted((ROOT / "Paper" / "latex").rglob("*.bib"))
    outputs_current(
        "python_figure_outputs_current",
        [
            E / "python_figure_renderers.csv",
            E / "paper_figure_manifest.csv",
            ROOT / "Paper" / "latex" / "generated_figures" / "fig_projection_information.pdf",
            ROOT / "Paper" / "latex" / "generated_figures" / "fig_external_motifs.pdf",
            ROOT / "Paper" / "latex" / "generated_figures" / "fig_semantic_frontier.pdf",
            ROOT / "Paper" / "latex" / "generated_figures" / "fig_sql_execution.pdf",
        ],
        [
            ART / "scripts" / "render_python_figures.py",
            E / "projection_information_paper.csv",
            E / "benchmark_motif_difficulty_paper.csv",
            E / "grounded" / "semantic_frontier.csv",
            E / "sql_probe_execution_summary.csv",
        ],
    )
    outputs_current(
        "pdf_certificate_current",
        [E / "latex_compile_check.csv", E / "pdf_integrity.csv"],
        tex_inputs + bib_inputs + [
            ART / "scripts" / "check_latex_compile.py",
            ART / "scripts" / "check_pdf_integrity.py",
            E / "python_figure_renderers.csv",
        ],
    )
    outputs_current(
        "paper_table_source_check_current",
        [E / "paper_table_source_check.csv", E / "paper_table_source_check_summary.csv"],
        paper_table_source_inputs(),
    )

real_engine_files = [
    E / "real_engine_probe_validation_full.csv",
    E / "real_engine_probe_validation_full_summary.csv",
    E / "real_engine_probe_validation_motif.csv",
    E / "real_engine_probe_validation_motif_summary.csv",
    E / "real_engine_validation_check.csv",
    E / "real_engine_validation_environment.csv",
    E / "real_engine_noninterference_check.csv",
    ART / "benchmark" / "generated_probes.jsonl",
]
missing = [path.relative_to(ROOT).as_posix() for path in real_engine_files if not path.exists()]
if missing:
    add("real_engine_evidence_hashes_bound", False, ";".join(missing))
else:
    digests = [sha256_file(path)[:12] for path in real_engine_files]
    full_rows = len(read_csv(E / "real_engine_probe_validation_full.csv"))
    motif_rows = len(read_csv(E / "real_engine_probe_validation_motif.csv"))
    add("real_engine_evidence_hashes_bound", full_rows == 8432 and motif_rows == 142, f"digests={','.join(digests)};rows={full_rows}/{motif_rows}")

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader()
    writer.writerows(rows)
passed = sum(row["passed"] == "true" for row in rows)
print(f"Certificate freshness check: {passed}/{len(rows)} passed")
for row in rows:
    if row["passed"] != "true":
        print("FAIL", row)
if passed != len(rows):
    sys.exit(1)
