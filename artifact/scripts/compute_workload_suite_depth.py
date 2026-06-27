#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.corpus import load_probe_objects
from optsemc.workloads import load_workload_suites, suite_coverage_matrix, suite_depth_summary, representative_probe_set
from optsemc.io import write_csv
probes=load_probe_objects(ART); suites=load_workload_suites(ART/'external'/'benchmark_suites.yaml')
write_csv(ART/'evaluation'/'workload_suite_matrix.csv', suite_coverage_matrix(suites, probes), ['suite_id','suite_name','motif_id','requirements','covered','matching_probes','example_probe'])
write_csv(ART/'evaluation'/'workload_suite_depth.csv', suite_depth_summary(suites, probes), ['suite_id','motifs','min_hits','median_hits','max_hits','total_hits'])
write_csv(ART/'evaluation'/'workload_representative_probes.csv', representative_probe_set(suites, probes), ['suite_id','motif_id','probe_id','alternatives'])
print(f'Workload suite depth: suites={len(suites)}')
