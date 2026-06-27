#!/usr/bin/env python3
"""Compute guard-support and guard-overlap diagnostics for grounded rules."""
from __future__ import annotations
import csv
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_probe_objects, load_rule_objects
from optsemc.guards import invalid_guard_dimensions, overlap_rows, overlap_summary, support_summary, support_table

E = ROOT / 'evaluation'

def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

rules = load_rule_objects(ROOT)
probes = load_probe_objects(ROOT)
supports = support_table(rules, probes)
support_rows = [
    {
        'rule_id': s.rule_id,
        'engine': s.engine,
        'state': s.state,
        'action_key': s.action_key,
        'guard_width': s.guard_width,
        'expanded_guard_width': s.expanded_guard_width,
        'support_count': s.support_count,
        'total_probes': s.total_probes,
        'support_share': f'{s.support_share:.6f}',
        'support_class': s.support_class,
    }
    for s in supports
]
write_csv(E/'guard_support.csv', support_rows, ['rule_id','engine','state','action_key','guard_width','expanded_guard_width','support_count','total_probes','support_share','support_class'])
summary = support_summary(supports)
summary_rows = [{'metric': key, 'value': f'{value:.6f}' if isinstance(value, float) else str(value)} for key, value in summary.items()]
write_csv(E/'guard_quality_summary.csv', summary_rows, ['metric','value'])
issues = invalid_guard_dimensions(rules, probes)
write_csv(E/'guard_dimension_issues.csv', issues, ['rule_id','field','issue','value'])
overlap = overlap_rows(rules, probes)
write_csv(E/'guard_overlap.csv', overlap, ['left_rule_id','right_rule_id','engine','state','action_key','overlap_type','intersection_support','left_support','right_support','guard_containment'])
ovsum = overlap_summary(overlap)
write_csv(E/'guard_overlap_summary.csv', [{'metric': k, 'value': str(v)} for k,v in ovsum.items()], ['metric','value'])
paper_rows = [
    {'check': 'grounded rules', 'value': str(summary['rules']), 'interpretation': 'finite public-contract relation'},
    {'check': 'rules with probe support', 'value': f"{summary['triggered_rules']}/{summary['rules']}", 'interpretation': 'no admitted rule is outside the generated denominator'},
    {'check': 'guarded non-global rules', 'value': str(summary['non_global_guarded_rules']), 'interpretation': 'query-conditional contracts rather than engine-level labels'},
    {'check': 'median probe support', 'value': str(int(summary['median_support'])), 'interpretation': 'guards range from narrow motifs to global observability'},
    {'check': 'same-action guard containments', 'value': str(ovsum['guard_containment_pairs']), 'interpretation': 'finite overlap, explicitly audited'},
    {'check': 'invalid guard dimensions', 'value': str(len(issues)), 'interpretation': 'guard values are inside the benchmark feature domain'},
]
write_csv(E/'guard_quality_paper.csv', paper_rows, ['check','value','interpretation'])
print(f"Guard quality: {summary['triggered_rules']}/{summary['rules']} rules have support; invalid_guard_dimensions={len(issues)}")
