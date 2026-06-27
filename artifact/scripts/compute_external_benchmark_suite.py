#!/usr/bin/env python3
"""Compute coverage of recognizable optimizer benchmark families by feature motifs."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifact"
sys.path.insert(0, str(ART))
from optsemc.io import read_yaml, write_csv
from optsemc.corpus import load_probe_objects
from optsemc.coverage import benchmark_suite_crosswalk
suite_file = ART / "external" / "benchmark_suites.yaml"
OUT = ART / "evaluation" / "external_benchmark_suite.csv"
probes = load_probe_objects(ART)
data = read_yaml(suite_file) or {}
suites = data.get('suites') or []
rows = benchmark_suite_crosswalk(probes, suites)
write_csv(OUT, rows, ["suite_id","suite_name","motifs","covered_motifs","coverage_rate","matching_probes"])
print(f"External benchmark suite: {sum(int(r['covered_motifs']) for r in rows)}/{sum(int(r['motifs']) for r in rows)} motifs covered across {len(rows)} suites")

