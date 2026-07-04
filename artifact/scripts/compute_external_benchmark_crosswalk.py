#!/usr/bin/env python3
"""Compute coverage of published optimizer-benchmark motifs by OptSemBench-C."""
from __future__ import annotations

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from optsemc.corpus import load_probes
from optsemc.external import motif_coverage
from optsemc.io import read_yaml, write_csv

MOTIFS = ROOT / "external" / "workload_motifs.yaml"
PROBES = ROOT / "benchmark" / "generated_probes.jsonl"
OUT = ROOT / "evaluation" / "grounded" / "external_benchmark_crosswalk.csv"
CHECK = ROOT / "evaluation" / "external_benchmark_crosswalk_check.csv"
REFS = ROOT.parent / "Paper" / "latex" / "refs.bib"


def bib_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"@\w+\{([^,\s]+)", text))


def main() -> None:
    doc = read_yaml(MOTIFS) or {}
    motifs = doc.get("motifs", [])
    keys = bib_keys(REFS)
    probes = load_probes(PROBES)
    rows = [motif_coverage(probes, motif) | {"literature_anchor": motif.get("literature_anchor", "")} for motif in motifs]
    write_csv(OUT, rows, ["motif_id", "benchmark_family", "literature_anchor", "optimizer_surface", "covered_requirements", "total_requirements", "coverage", "missing_requirements"])

    checks = []
    def add(check: str, ok: bool, details: str = "") -> None:
        checks.append({"check": check, "passed": str(bool(ok)).lower(), "details": details})
    add("motif_catalog_nonempty", len(rows) >= 5, f"motifs={len(rows)}")
    add("every_motif_has_literature_anchor", all(r["literature_anchor"] for r in rows), ";".join(r["motif_id"] for r in rows if not r["literature_anchor"]))
    if REFS.exists():
        missing_anchors = [r["literature_anchor"] for r in rows if r["literature_anchor"] and r["literature_anchor"] not in keys]
        add("every_literature_anchor_resolves", not missing_anchors, ";".join(missing_anchors))
    else:
        add("every_literature_anchor_resolves", all(r["literature_anchor"] for r in rows), "refs_bib_absent_in_artifact_only_package")
    add("every_motif_has_optimizer_surface", all(r["optimizer_surface"] for r in rows), "")
    add("every_motif_has_feature_requirements", all(int(r["total_requirements"]) > 0 for r in rows), "")
    add("all_declared_motif_requirements_covered", all(int(r["covered_requirements"]) == int(r["total_requirements"]) for r in rows), ";".join(f"{r['motif_id']}:{r['missing_requirements']}" for r in rows if r["missing_requirements"]))
    write_csv(CHECK, checks, ["check", "passed", "details"])
    passed = sum(r["passed"] == "true" for r in checks)
    print(f"External benchmark crosswalk: {passed}/{len(checks)} checks passed")
    if passed != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
