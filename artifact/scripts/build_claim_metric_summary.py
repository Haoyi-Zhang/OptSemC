#!/usr/bin/env python3
"""Build a compact, machine-readable summary of headline grounded metrics.

The summary is used by the traceability checks so that headline numbers in the
paper and claim matrix are regenerated from the same evaluation outputs that
feed the tables.
"""
from __future__ import annotations
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evaluation'
G = E / 'grounded'
OUT = E / 'claim_metric_summary.csv'

def count_lines(path):
    with path.open(encoding='utf-8') as f:
        return sum(1 for line in f if line.strip())

def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def metric_rows():
    rows=[]
    def add(metric, value, source):
        rows.append({'metric': metric, 'value': str(value), 'source': source})
    add('grounded_rules', count_lines(ROOT/'grounded/verified_rules.jsonl'), 'grounded/verified_rules.jsonl')
    add('grounded_segments', count_lines(ROOT/'grounded/verified_segments.jsonl'), 'grounded/verified_segments.jsonl')
    add('public_sources', max(0, count_lines(ROOT/'grounded/verified_sources.csv')-1), 'grounded/verified_sources.csv')
    add('generated_probes', count_lines(ROOT/'benchmark/generated_probes.jsonl'), 'benchmark/generated_probes.jsonl')
    # coverage interactions: unique interaction row is easiest to parse by label.
    for r in read_csv(E/'coverage_interactions.csv'):
        if r.get('coverage_target') in {'all_unique_interactions', 'ALL'}:
            add('valid_interactions', r.get('valid_interactions', r.get('covered_interactions','')), 'evaluation/coverage_interactions.csv')
    for r in read_csv(G/'conditional_trap_rate.csv'):
        method = r.get('method') or r.get('projection')
        if method in {'keyword','yesno','operator_only'}:
            add(f'{method}_projected_equivalences', r['projected_equivalences'], 'evaluation/grounded/conditional_trap_rate.csv')
            add(f'{method}_false_equivalences', r['false_equivalences'], 'evaluation/grounded/conditional_trap_rate.csv')
            add(f'{method}_conditional_false_rate', r['conditional_false_equivalence_rate'], 'evaluation/grounded/conditional_trap_rate.csv')
    for r in read_csv(G/'repair_certificate_summary.csv'):
        method = r['method']
        add(f'{method}_repair_sets', r['repair_sets'], 'evaluation/grounded/repair_certificate_summary.csv')
        add(f'{method}_minimal_repair_size', r['minimal_universal_repair_size'], 'evaluation/grounded/repair_certificate_summary.csv')
    for r in read_csv(G/'repair_basis_stability.csv'):
        if r.get('scope') == 'all_projections':
            add('semantic_basis', r['basis'], 'evaluation/grounded/repair_basis_stability.csv')
            add('semantic_basis_resolved', r['resolved'], 'evaluation/grounded/repair_basis_stability.csv')
            add('semantic_basis_false_equivalences', r['false_equivalences'], 'evaluation/grounded/repair_basis_stability.csv')
    for r in read_csv(G/'repair_generalization_summary.csv'):
        method = r.get('method') or r.get('projection')
        add(f'{method}_heldout_false_equivalences', r.get('heldout_false_equivalence', r.get('heldout_false_equivalences','')), 'evaluation/grounded/repair_generalization_summary.csv')
        add(f'{method}_heldout_resolved', r.get('resolved_by_learned_repair', r.get('heldout_resolved','')), 'evaluation/grounded/repair_generalization_summary.csv')
    try:
        for r in read_csv(E/'repair_certificate_minimality.csv'):
            add(f'{r["method"]}_repair_minimality_passed', r['passed'], 'evaluation/repair_certificate_minimality.csv')
    except FileNotFoundError:
        pass
    try:
        bench = {r['metric']: r['value'] for r in read_csv(G/'benchmark_efficiency_summary.csv')}
        for key in ['generated_full_rule_coverage_budget','diagnostic_full_rule_coverage_budget','generated_budget50_rule_coverage','diagnostic_budget50_rule_coverage','generated_budget100_rule_coverage','diagnostic_budget100_rule_coverage','random_mean_at_100','random_p95_at_100']:
            if key in bench:
                add(key, bench[key], 'evaluation/grounded/benchmark_efficiency_summary.csv')
    except FileNotFoundError:
        pass
    try:
        proof = read_csv(E/'projection_proof_obligations.csv')
        add('projection_proof_obligations_passed', sum(1 for r in proof if r.get('passed') == 'true'), 'evaluation/projection_proof_obligations.csv')
        add('projection_proof_obligations_total', len(proof), 'evaluation/projection_proof_obligations.csv')
    except FileNotFoundError:
        pass
    try:
        baseline = {r['projection']: r for r in read_csv(G/'baseline_portfolio.csv')}
        for method in ['strict','keyword','yesno','operator_only']:
            if method in baseline:
                add(f'{method}_baseline_false_equivalences', baseline[method]['false_equivalences'], 'evaluation/grounded/baseline_portfolio.csv')
                add(f'{method}_baseline_projected_equivalences', baseline[method]['projected_equivalences'], 'evaluation/grounded/baseline_portfolio.csv')
        add('baseline_portfolio_size', len(baseline), 'evaluation/grounded/baseline_portfolio.csv')
    except FileNotFoundError:
        pass
    try:
        anchor_crosswalk = read_csv(G/'external_benchmark_crosswalk.csv')
        add('external_anchor_motifs', len(anchor_crosswalk), 'evaluation/grounded/external_benchmark_crosswalk.csv')
        add('external_anchor_requirements', sum(int(r['total_requirements']) for r in anchor_crosswalk), 'evaluation/grounded/external_benchmark_crosswalk.csv')
        add('external_anchor_requirements_covered', sum(int(r['covered_requirements']) for r in anchor_crosswalk), 'evaluation/grounded/external_benchmark_crosswalk.csv')
    except FileNotFoundError:
        pass
    try:
        suite_rows = read_csv(E/'external_benchmark_suite.csv')
        add('external_benchmark_suites', len(suite_rows), 'evaluation/external_benchmark_suite.csv')
        add('external_benchmark_motifs', sum(int(r['motifs']) for r in suite_rows), 'evaluation/external_benchmark_suite.csv')
        add('external_benchmark_motifs_covered', sum(int(r['covered_motifs']) for r in suite_rows), 'evaluation/external_benchmark_suite.csv')
        add('external_benchmark_matching_probes', sum(int(r['matching_probes']) for r in suite_rows), 'evaluation/external_benchmark_suite.csv')
    except FileNotFoundError:
        pass
    try:
        exec_summary = {r['metric']: r['value'] for r in read_csv(E/'external_motif_execution_summary.csv')}
        for key in ['external_motifs', 'matched_motifs', 'executed_motifs', 'execution_failures', 'suites']:
            if key in exec_summary:
                add(f'external_motif_representative_{key}', exec_summary[key], 'evaluation/external_motif_execution_summary.csv')
    except FileNotFoundError:
        pass

    for subset in ['motif', 'full']:
        try:
            real_rows = read_csv(E/f'real_engine_probe_validation_{subset}_summary.csv')
            total_probes = sum(int(r['probes']) for r in real_rows)
            total_success = sum(int(r['execution_successes']) for r in real_rows)
            total_failures = sum(int(r['execution_failures']) for r in real_rows)
            min_match = min(float(r['mean_visible_match_rate']) for r in real_rows) if real_rows else 0.0
            add(f'real_engine_{subset}_engines', len(real_rows), f'evaluation/real_engine_probe_validation_{subset}_summary.csv')
            add(f'real_engine_{subset}_validations', total_probes, f'evaluation/real_engine_probe_validation_{subset}_summary.csv')
            add(f'real_engine_{subset}_execution_successes', total_success, f'evaluation/real_engine_probe_validation_{subset}_summary.csv')
            add(f'real_engine_{subset}_execution_failures', total_failures, f'evaluation/real_engine_probe_validation_{subset}_summary.csv')
            add(f'real_engine_{subset}_min_visible_match_rate', f'{min_match:.6f}', f'evaluation/real_engine_probe_validation_{subset}_summary.csv')
            for r in real_rows:
                engine = r['engine']
                add(f'real_engine_{subset}_{engine}_probes', r['probes'], f'evaluation/real_engine_probe_validation_{subset}_summary.csv')
                add(f'real_engine_{subset}_{engine}_execution_successes', r['execution_successes'], f'evaluation/real_engine_probe_validation_{subset}_summary.csv')
                add(f'real_engine_{subset}_{engine}_distinct_plan_hashes', r['distinct_plan_hashes'], f'evaluation/real_engine_probe_validation_{subset}_summary.csv')
        except FileNotFoundError:
            pass

    try:
        scale = {r['metric']: r['value'] for r in read_csv(E/'scalability_stress_summary.csv')}
        for key in ['full_pairwise_comparisons_per_projection','full_min_comparisons_per_second','full_elapsed_ms_total']:
            if key in scale:
                add(key, scale[key], 'evaluation/scalability_stress_summary.csv')
    except FileNotFoundError:
        pass
    try:
        family = {r['projection']: r for r in read_csv(E/'engine_family_stress_summary.csv')}
        for method in ['keyword','operator_only','operator_kind_surface']:
            if method in family:
                add(f'{method}_family_false_equivalences', family[method]['false_equivalences'], 'evaluation/engine_family_stress_summary.csv')
                add(f'{method}_families_with_false_equivalence', family[method]['families_with_false_equivalence'], 'evaluation/engine_family_stress_summary.csv')
                add(f'{method}_family_unresolved_after_layer_placement', family[method]['unresolved_after_layer_placement'], 'evaluation/engine_family_stress_summary.csv')
    except FileNotFoundError:
        pass

    try:
        stale = read_csv(E/'stale_diagnostic_outputs.csv')
        add('stale_diagnostic_checks_passed', sum(1 for r in stale if r.get('passed') == 'true'), 'evaluation/stale_diagnostic_outputs.csv')
        add('stale_diagnostic_checks_total', len(stale), 'evaluation/stale_diagnostic_outputs.csv')
    except FileNotFoundError:
        pass
    return rows

rows=metric_rows()
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['metric','value','source']); w.writeheader(); w.writerows(rows)
print(f'Wrote claim metric summary with {len(rows)} metrics')
