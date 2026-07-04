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
    ("baseline_portfolio", "baselines/baseline_catalog.yaml", "baseline comparison vocabulary"),
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
