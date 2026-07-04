#!/usr/bin/env python3
"""Check that every paper table declared in the manifest has a table file and all source files."""
from __future__ import annotations
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "artifact" / "evaluation" / "paper_table_manifest.csv"
OUT = ROOT / "artifact" / "evaluation"
rows = []
all_ok = True


def sha256_prefix(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def record_count(path: Path) -> int:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            return sum(1 for _ in csv.DictReader(handle))
    with path.open(encoding="utf-8", errors="ignore") as handle:
        lines = [line for line in handle if line.strip()]
    if suffix == ".jsonl":
        return len(lines)
    if suffix == ".sql":
        return max(1, sum(line.count(";") for line in lines)) if lines else 0
    return len(lines)


def allows_zero_records(path: Path) -> bool:
    lowered = path.name.lower()
    return any(token in lowered for token in ("conflict", "failure", "violation", "negative"))


with MANIFEST.open(newline="") as f:
    for row in csv.DictReader(f):
        latex_file = ROOT / row["latex_file"]
        srcs = [s.strip() for s in row.get("source_files", "").split(";") if s.strip()]
        missing = []
        empty = []
        source_counts = []
        source_digests = []
        if not latex_file.exists():
            missing.append(row["latex_file"])
        else:
            try:
                if record_count(latex_file) <= 0:
                    empty.append(row["latex_file"])
            except Exception as exc:
                empty.append(f"{row['latex_file']}:{type(exc).__name__}")
        for src in srcs:
            path = ROOT / src
            if not path.exists():
                missing.append(src)
                continue
            try:
                count = record_count(path)
                source_counts.append(f"{src}={count}")
                source_digests.append(f"{src}={sha256_prefix(path)}")
                if count <= 0 and not allows_zero_records(path):
                    empty.append(src)
            except Exception as exc:
                empty.append(f"{src}:{type(exc).__name__}")
        ok = not missing and not empty and bool(srcs)
        all_ok &= ok
        rows.append({
            "paper_table": row["paper_table"],
            "latex_file": row["latex_file"],
            "source_count": len(srcs),
            "missing_count": len(missing),
            "missing_paths": "|".join(missing),
            "empty_or_unreadable_paths": "|".join(empty),
            "source_records": "|".join(source_counts),
            "source_sha256_12": "|".join(source_digests),
            "passed": str(ok).lower(),
        })

with (OUT / "paper_table_source_check.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["paper_table","latex_file","source_count","missing_count","missing_paths","empty_or_unreadable_paths","source_records","source_sha256_12","passed"])
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
