from pathlib import Path
from optsemc.benchmark_compiler import (
    MotifRequirement, ProbeFeature, load_suite_requirements, load_probe_features,
    compute_motif_coverage, suite_summary, greedy_probe_cover, redundancy_rows,
)

ROOT = Path(__file__).resolve().parents[1]


def test_motif_requirement_matches_feature_vector():
    motif = MotifRequirement('S', 'Suite', 'm', (('join_shape', 'star'), ('join_type', 'inner')))
    assert motif.matches({'join_shape': 'star', 'join_type': 'inner'})


def test_motif_requirement_rejects_missing_feature():
    motif = MotifRequirement('S', 'Suite', 'm', (('join_shape', 'star'), ('join_type', 'inner')))
    assert not motif.matches({'join_shape': 'star'})


def test_load_suite_requirements_count():
    motifs = load_suite_requirements(ROOT / 'external/benchmark_suites.yaml')
    assert len(motifs) == 90


def test_load_probe_features_count():
    probes = load_probe_features(ROOT / 'benchmark/generated_probes.jsonl')
    assert len(probes) == 4216


def test_all_motifs_have_requirements():
    motifs = load_suite_requirements(ROOT / 'external/benchmark_suites.yaml')
    assert all(motif.requirements for motif in motifs)


def test_compute_motif_coverage_complete():
    motifs = load_suite_requirements(ROOT / 'external/benchmark_suites.yaml')
    probes = load_probe_features(ROOT / 'benchmark/generated_probes.jsonl')
    coverage = compute_motif_coverage(motifs, probes)
    assert all(row.covered for row in coverage)


def test_suite_summary_has_twelve_suites():
    motifs = load_suite_requirements(ROOT / 'external/benchmark_suites.yaml')
    probes = load_probe_features(ROOT / 'benchmark/generated_probes.jsonl')
    summary = suite_summary(compute_motif_coverage(motifs, probes))
    assert len(summary) == 12


def test_suite_summary_full_coverage_rates():
    motifs = load_suite_requirements(ROOT / 'external/benchmark_suites.yaml')
    probes = load_probe_features(ROOT / 'benchmark/generated_probes.jsonl')
    summary = suite_summary(compute_motif_coverage(motifs, probes))
    assert all(float(row['coverage_rate']) == 1.0 for row in summary)


def test_greedy_probe_cover_covers_some_motifs_per_row():
    motifs = load_suite_requirements(ROOT / 'external/benchmark_suites.yaml')
    probes = load_probe_features(ROOT / 'benchmark/generated_probes.jsonl')
    rows = greedy_probe_cover(compute_motif_coverage(motifs, probes))
    assert rows and all(int(row['new_motifs_covered']) >= 1 for row in rows)


def test_redundancy_rows_are_all_covered():
    motifs = load_suite_requirements(ROOT / 'external/benchmark_suites.yaml')
    probes = load_probe_features(ROOT / 'benchmark/generated_probes.jsonl')
    rows = redundancy_rows(compute_motif_coverage(motifs, probes))
    assert all(row['covered'] == 'true' for row in rows)
