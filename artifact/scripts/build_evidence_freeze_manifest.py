#!/usr/bin/env python3
"""Record the frozen evidence inputs used before witness counting."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evaluation"

FROZEN_INPUTS = [
    ("schema", "schema/action_domain.yaml", "canonical action fields and states"),
    ("schema", "schema/contract_rule.schema.json", "rule admission schema"),
    ("schema", "schema/query_probe.schema.json", "probe admission schema"),
    ("feature_space", "benchmark/feature_domain.yaml", "query-feature universe"),
    ("source_manifest", "grounded/verified_sources.csv", "public source set"),
    ("evidence_spans", "grounded/verified_segments.jsonl", "source-backed evidence spans"),
    ("admitted_rules", "grounded/verified_rules.jsonl", "source-linked contract rules"),
    ("projection_portfolio", "config/practice_projection_surfaces.csv", "public comparison surfaces"),
    ("external_motifs", "external/workload_motifs.yaml", "published workload motif requirements"),
    ("projection_surface_portfolio", "baselines/baseline_catalog.yaml", "comparison-surface vocabulary"),
    ("executable_logic", "optsemc/baselines.py", "projection-surface portfolio implementation"),
    ("environment_lock", "constraints.txt", "pinned Python build and runtime constraints"),
    ("executable_logic", "optsemc/projections.py", "projection-kernel witness implementation"),
    ("executable_logic", "optsemc/repair_stability.py", "repair-basis stability implementation"),
    ("executable_logic", "optsemc/algorithmic_scaling.py", "finite replay scaling implementation"),
    ("compute_script", "scripts/compute_anti_overfit_audit.py", "anti-overfitting audit construction"),
    ("compute_script", "scripts/compute_grounded_source_robustness.py", "source-removal robustness and witness-identity tracking"),
    ("compute_script", "scripts/compute_resource_profile.py", "cloud replay resource-profile measurement"),
    ("compute_script", "scripts/compute_repair_generalization.py", "probe-fold repair-stability measurement"),
    ("check_script", "scripts/check_anti_overfit_audit.py", "anti-overfitting audit gate"),
    ("check_script", "scripts/check_resource_profile.py", "resource-profile gate"),
    ("check_script", "scripts/check_real_engine_noninterference.py", "real-engine non-interference gate"),
    ("check_script", "scripts/check_evidence_freeze_manifest.py", "freeze-manifest hash gate"),
    ("release_gate", "scripts/check_git_tree_state.py", "clean-source-tree release gate"),
    ("release_gate", "scripts/build_anonymous_archive.py", "anonymous archive construction gate"),
    ("replay_entrypoint", "run_deep_checks.sh", "cloud replay and paper-gate entry point"),
    ("replay_entrypoint", "recompute_grounded_mainline.sh", "from-grounded replay entry point"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_records(path: Path) -> int:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            return max(0, sum(1 for _ in csv.reader(handle)) - 1)
    if suffix in {".jsonl", ".yaml", ".yml", ".json"}:
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    return len(path.read_bytes())


def main() -> int:
    rows = []
    for role, rel, description in FROZEN_INPUTS:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"missing frozen input: {rel}")
        rows.append(
            {
                "role": role,
                "path": rel,
                "sha256": sha256(path),
                "records_or_lines": str(count_records(path)),
                "freeze_point": "before_projection_witness_counting",
                "forbidden_after_freeze": "schema_or_source_or_projection_change_without_full_replay",
                "description": description,
            }
        )

    E.mkdir(parents=True, exist_ok=True)
    out = E / "evidence_freeze_manifest.csv"
    fields = [
        "role",
        "path",
        "sha256",
        "records_or_lines",
        "freeze_point",
        "forbidden_after_freeze",
        "description",
    ]
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Evidence freeze manifest: {len(rows)} frozen inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
