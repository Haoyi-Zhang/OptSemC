#!/usr/bin/env python3
"""Export a reader-friendly SQL bundle for generated OptSemBench-C probes."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_probes
from optsemc.io import read_csv, write_csv
from optsemc.sql_bundle import bundle_manifest_rows, export_sql_bundle


def main() -> None:
    probes = load_probes(ROOT)
    cover_path = ROOT / "evaluation" / "benchmark_minimal_probe_cover.csv"
    representative_ids = []
    if cover_path.exists():
        representative_ids = [r['probe_id'] for r in read_csv(cover_path)]
    out_dir = ROOT / "benchmark" / "sql_bundle"
    summary = export_sql_bundle(probes, out_dir, representative_ids)
    manifest = bundle_manifest_rows(probes)
    write_csv(out_dir / "full_probe_manifest.csv", manifest)
    rows = [{"metric":"generated_probe_sql_queries", "value": summary['bundle_queries']},
            {"metric":"representative_sql_files", "value": summary['representative_files']},
            {"metric":"full_probe_bundle_sha256", "value": summary['bundle_sha256']},
            {"metric":"shape_invalid_queries", "value": str(sum(1 for r in manifest if r['shape_valid'] != 'true'))}]
    write_csv(ROOT / "evaluation" / "sql_probe_bundle_summary.csv", rows)
    print(f"SQL probe bundle: {summary['bundle_queries']} queries; representative={summary['representative_files']}")

if __name__ == "__main__":
    main()
