#!/usr/bin/env python3
"""Compute multi-strength feature coverage diagnostics for generated probes."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.io import read_yaml, write_csv
from optsemc.corpus import load_probe_objects
from optsemc.coverage import coverage_summary, feature_value_counts, declared_interactions, greedy_probe_cover
probes=load_probe_objects(ART)
feature_domain=read_yaml(ART/'benchmark'/'feature_domain.yaml') or {}
rows=[]
for strength in (1,2,3):
    try:
        rows.append(coverage_summary(probes, feature_domain, strength).as_row())
    except Exception as exc:
        rows.append({'strength':str(strength),'covered':'0','required':'0','coverage_rate':'0.000000','probes':str(len(probes)),'error':type(exc).__name__})
write_csv(ART/'evaluation'/'probe_coverage_matrix.csv', rows, ['strength','covered','required','coverage_rate','probes'])
write_csv(ART/'evaluation'/'probe_feature_value_counts.csv', feature_value_counts(probes), ['feature','value','probe_count'])
cover=greedy_probe_cover(probes, declared_interactions(probes), max_steps=50)
write_csv(ART/'evaluation'/'probe_greedy_cover_prefix.csv', cover, ['step','probe_id','new_interactions','remaining_interactions','sql_skeleton_hash'])
print(f"Probe coverage matrix: strengths={len(rows)}; probes={len(probes)}; greedy_prefix={len(cover)}")

