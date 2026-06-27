#!/usr/bin/env python3
"""Compile external benchmark motifs into probe-coverage certificates."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "artifact"))
from optsemc.benchmark_compiler import load_suite_requirements, load_probe_features, compute_motif_coverage, suite_summary, greedy_probe_cover, redundancy_rows
from optsemc.io import write_csv
A = ROOT / "artifact"
E = A / "evaluation"
motifs = load_suite_requirements(A / "external/benchmark_suites.yaml")
probes = load_probe_features(A / "benchmark/generated_probes.jsonl")
coverage = compute_motif_coverage(motifs, probes)
write_csv(E / "benchmark_motif_coverage.csv", [row.as_row() for row in coverage], ["suite_id", "suite_name", "motif_id", "requirements", "matching_probes", "representative_probe", "covered"])
write_csv(E / "benchmark_compiler_summary.csv", suite_summary(coverage), ["suite_id", "suite_name", "motifs", "covered_motifs", "coverage_rate", "matching_probes"])
write_csv(E / "benchmark_minimal_probe_cover.csv", greedy_probe_cover(coverage), ["rank", "probe_id", "new_motifs_covered", "motifs"])
write_csv(E / "benchmark_motif_redundancy.csv", redundancy_rows(coverage), ["suite_id", "motif_id", "matching_probes", "redundancy_level", "covered"])
print(f"Benchmark motif compiler: motifs={len(coverage)} covered={sum(row.covered for row in coverage)}")
