#!/usr/bin/env python3
"""Compute source-support diagnostics for false-portability witnesses."""
from __future__ import annotations
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.io import write_csv
from optsemc.source_support import witness_source_records, witness_source_summary

projections = ("keyword", "yesno", "operator_only")
records = witness_source_records(ROOT, projections)
write_csv(ROOT / "evaluation" / "source_witness_support.csv", [record.as_row() for record in records])
summary = witness_source_summary(records)
write_csv(ROOT / "evaluation" / "source_witness_support_summary.csv", summary)
# Paper table uses conventional display labels.
labels = {"keyword": "Keyword", "yesno": "Yes/No", "operator_only": "Operator-only"}
paper_rows = []
for row in summary:
    paper_rows.append({
        "projection": labels.get(row["projection"], row["projection"]),
        "false_witnesses": row["false_witnesses"],
        "distinct_sources": row["distinct_sources"],
        "min_sources_per_witness": row["min_sources_per_witness"],
        "median_sources_per_witness": row["median_sources_per_witness"],
        "cross_source_witnesses": row["cross_source_witnesses"],
    })
write_csv(ROOT / "evaluation" / "source_witness_support_paper.csv", paper_rows)
print(f"Source witness support: {len(records)} witnesses across {len(summary)} projections")
