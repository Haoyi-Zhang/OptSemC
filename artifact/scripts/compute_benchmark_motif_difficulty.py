#!/usr/bin/env python3
"""Summarize benchmark motif difficulty and redundancy from the executable crosswalk."""
from __future__ import annotations
import csv, statistics, sys
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from optsemc.io import write_csv

SRC = ROOT / "evaluation" / "benchmark_motif_coverage.csv"
OUT = ROOT / "evaluation" / "benchmark_motif_difficulty.csv"
PAPER = ROOT / "evaluation" / "benchmark_motif_difficulty_paper.csv"

def main() -> None:
    with SRC.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    by_suite = defaultdict(list)
    for r in rows:
        by_suite[r['suite_id']].append(int(r['matching_probes']))
    out=[]
    for suite, vals in sorted(by_suite.items()):
        vals_sorted=sorted(vals)
        out.append({
            'suite_id':suite,
            'motifs':str(len(vals)),
            'min_matching_probes':str(vals_sorted[0]),
            'median_matching_probes':f"{statistics.median(vals):.1f}",
            'max_matching_probes':str(vals_sorted[-1]),
            'single_probe_motifs':str(sum(1 for v in vals if v == 1)),
            'sparse_motifs_le_5':str(sum(1 for v in vals if v <= 5)),
        })
    write_csv(OUT, out)
    keep_order = ['TPC-H','TPC-DS','JOB','SSB','CEB-CardEst','Adaptive-Distributed','Federated-Lakehouse','Optimizer-Controls','PostgreSQL-Controls','DuckDB-Controls','ClickHouse-JoinAlgorithms','Spark-Trino-Distribution']
    out_by = {r['suite_id']: r for r in out}
    write_csv(PAPER, [out_by[k] for k in keep_order if k in out_by])
    print(f"Benchmark motif difficulty: {len(rows)} motifs across {len(out)} suites")

if __name__ == '__main__':
    main()
