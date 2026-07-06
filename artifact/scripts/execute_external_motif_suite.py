#!/usr/bin/env python3
"""Execute one matched OptSemBench-C SQL probe for every external benchmark motif."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_probes
from optsemc.io import read_yaml, write_csv
from optsemc.sql_execution import SyntheticOptimizerCatalog, select_first_matching_probe

probes = load_probes(ROOT)
suites = (read_yaml(ROOT / 'external' / 'benchmark_suites.yaml') or {}).get('suites') or []
catalog = SyntheticOptimizerCatalog(rows_per_table=5)
rows=[]
try:
    for suite in suites:
        for motif in suite.get('motifs') or []:
            req = {str(k): str(v) for k, v in dict(motif.get('requirements') or {}).items()}
            probe = select_first_matching_probe(probes, req)
            if probe is None:
                rows.append({'suite_id':str(suite.get('suite_id','')), 'motif_id':str(motif.get('motif_id','')), 'requirements':str(req), 'matched':'false', 'probe_id':'', 'plan_ok':'false', 'exec_ok':'false', 'row_count':'0', 'plan_steps':'0', 'error':'no matching probe'})
                continue
            rec = catalog.execute(str(probe.get('probe_id','')), str(probe.get('sql_skeleton','')))
            rows.append({'suite_id':str(suite.get('suite_id','')), 'motif_id':str(motif.get('motif_id','')), 'requirements':str(req), 'matched':'true', 'probe_id':rec.probe_id, 'plan_ok':str(rec.plan_ok).lower(), 'exec_ok':str(rec.exec_ok).lower(), 'row_count':str(rec.row_count), 'plan_steps':str(rec.plan_steps), 'error':rec.error})
finally:
    catalog.close()
write_csv(ROOT / 'evaluation' / 'external_motif_execution.csv', rows, ['suite_id','motif_id','requirements','matched','probe_id','plan_ok','exec_ok','row_count','plan_steps','error'])
matched_rows = [r for r in rows if r['matched'] == 'true']
probe_to_motifs: dict[str, list[str]] = {}
for row in matched_rows:
    probe_to_motifs.setdefault(row['probe_id'], []).append(f"{row['suite_id']}:{row['motif_id']}")
probe_rows = [
    {
        'probe_id': probe_id,
        'motif_count': str(len(motifs)),
        'motifs': ';'.join(sorted(motifs)),
    }
    for probe_id, motifs in sorted(probe_to_motifs.items())
]
write_csv(ROOT / 'evaluation' / 'external_motif_probe_map.csv', probe_rows, ['probe_id','motif_count','motifs'])
motif_counts = [len(motifs) for motifs in probe_to_motifs.values()]
summary=[
    {'metric':'external_motifs', 'value':str(len(rows))},
    {'metric':'matched_motifs', 'value':str(sum(r['matched']=='true' for r in rows))},
    {'metric':'executed_motifs', 'value':str(sum(r['exec_ok']=='true' for r in rows))},
    {'metric':'execution_failures', 'value':str(sum(r['exec_ok']!='true' for r in rows))},
    {'metric':'distinct_representative_probes', 'value':str(len(probe_to_motifs))},
    {'metric':'motifs_per_representative_min', 'value':str(min(motif_counts) if motif_counts else 0)},
    {'metric':'motifs_per_representative_max', 'value':str(max(motif_counts) if motif_counts else 0)},
    {'metric':'shared_representative_probes', 'value':str(sum(1 for count in motif_counts if count > 1))},
    {'metric':'suites', 'value':str(len(suites))},
]
write_csv(ROOT / 'evaluation' / 'external_motif_execution_summary.csv', summary, ['metric','value'])
print(f"External motif execution: {summary[2]['value']}/{summary[0]['value']} motifs, {len(probe_to_motifs)} representatives across {len(suites)} suites")
if any(r['exec_ok']!='true' for r in rows):
    raise SystemExit(1)
