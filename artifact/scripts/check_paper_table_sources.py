#!/usr/bin/env python3
"""Check that every paper table declared in the manifest has a table file and all source files."""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "artifact" / "evaluation" / "paper_table_manifest.csv"
OUT = ROOT / "artifact" / "evaluation"
rows = []
all_ok = True
with MANIFEST.open(newline="") as f:
    for row in csv.DictReader(f):
        latex_file = ROOT / row["latex_file"]
        srcs = [s.strip() for s in row.get("source_files", "").split(";") if s.strip()]
        missing = []
        if not latex_file.exists():
            missing.append(row["latex_file"])
        for src in srcs:
            if not (ROOT / src).exists():
                missing.append(src)
        ok = not missing
        all_ok &= ok
        rows.append({
            "paper_table": row["paper_table"],
            "latex_file": row["latex_file"],
            "source_count": len(srcs),
            "missing_count": len(missing),
            "missing_paths": "|".join(missing),
            "passed": str(ok).lower(),
        })

with (OUT / "paper_table_source_check.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["paper_table","latex_file","source_count","missing_count","missing_paths","passed"])
    writer.writeheader()
    writer.writerows(rows)
with (OUT / "paper_table_source_check_summary.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["metric","value"])
    writer.writeheader()
    writer.writerow({"metric":"tables", "value":len(rows)})
    writer.writerow({"metric":"passed", "value":sum(1 for r in rows if r["passed"]=="true")})
    writer.writerow({"metric":"failed", "value":sum(1 for r in rows if r["passed"]!="true")})
print(f"Paper-table source check: {sum(1 for r in rows if r['passed']=='true')}/{len(rows)} passed")
if not all_ok:
    raise SystemExit(1)
