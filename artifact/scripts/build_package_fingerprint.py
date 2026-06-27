#!/usr/bin/env python3
"""Build package fingerprint independent of the older manifest module."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "artifact"))
from optsemc.package_builder import package_files, package_summary, package_fingerprint
from optsemc.io import write_csv
E = ROOT / "artifact" / "evaluation"
files = package_files(ROOT)
write_csv(E / "package_files.csv", [row.as_row() for row in files], ["path", "size", "sha256", "text", "category"])
summary = package_summary(files)
summary.append({"category": "FINGERPRINT", "files": str(len(files)), "bytes": package_fingerprint(files), "text_files": ""})
write_csv(E / "package_fingerprint_summary.csv", summary, ["category", "files", "bytes", "text_files"])
print(f"package fingerprint: files={len(files)} sha256={package_fingerprint(files)[:12]}")
