#!/usr/bin/env python3
"""Check external benchmark motif compiler outputs."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
E = ROOT / "artifact" / "evaluation"

def read(path: Path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))
coverage = read(E / "benchmark_motif_coverage.csv")
summary = read(E / "benchmark_compiler_summary.csv")
cover = read(E / "benchmark_minimal_probe_cover.csv")
redundancy = read(E / "benchmark_motif_redundancy.csv")
checks = [
    {"check": "motif_denominator_large", "passed": str(len(coverage) >= 59).lower(), "details": f"motifs={len(coverage)}"},
    {"check": "all_motifs_covered", "passed": str(bool(coverage) and all(r.get('covered') == 'true' for r in coverage)).lower(), "details": f"{sum(r.get('covered')=='true' for r in coverage)}/{len(coverage)}"},
    {"check": "all_suites_complete", "passed": str(bool(summary) and all(float(r.get('coverage_rate', 0)) >= 1.0 for r in summary)).lower(), "details": f"suites={len(summary)}"},
    {"check": "greedy_cover_compact", "passed": str(bool(cover) and len(cover) <= len(coverage)).lower(), "details": f"cover={len(cover)};motifs={len(coverage)}"},
    {"check": "no_zero_redundancy", "passed": str(bool(redundancy) and all(int(r.get('matching_probes', 0)) > 0 for r in redundancy)).lower(), "details": ""},
]
with (E / "benchmark_compiler_check.csv").open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"]); writer.writeheader(); writer.writerows(checks)
print(f"Benchmark compiler check: {sum(r['passed']=='true' for r in checks)}/{len(checks)} passed")
if not all(r['passed'] == 'true' for r in checks):
    sys.exit(1)
