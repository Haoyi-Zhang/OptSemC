#!/usr/bin/env python3
"""Compute side-balanced public-source support for headline false witnesses."""
from __future__ import annotations
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.evidence_balance import side_balanced_summary, side_balanced_witness_records
from optsemc.io import write_csv

records = side_balanced_witness_records(ROOT)
summary = side_balanced_summary(records)
write_csv(ROOT / "evaluation" / "side_balanced_witness_support.csv", [r.as_row() for r in records])
write_csv(ROOT / "evaluation" / "side_balanced_witness_support_summary.csv", summary)
labels = {"keyword": "Keyword", "operator_only": "Operator-only", "yesno": "Yes/No"}
paper_rows = []
for row in summary:
    paper_rows.append({
        "projection": labels.get(row["projection"], row["projection"]),
        "false_witnesses": row["false_witnesses"],
        "both_sides_supported": row["both_sides_supported"],
        "distinct_sources": row["distinct_sources"],
        "min_left_right_sources": f"{row['min_left_sources']}/{row['min_right_sources']}",
        "zero_shared_source_witnesses": row["zero_shared_source_witnesses"],
    })
write_csv(ROOT / "evaluation" / "side_balanced_witness_support_paper.csv", paper_rows)
print(f"Side-balanced witness support: {len(records)} witnesses across {len(summary)} projections")
