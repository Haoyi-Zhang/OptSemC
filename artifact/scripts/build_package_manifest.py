#!/usr/bin/env python3
"""Build a deterministic manifest for the public package tree."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "artifact"))
from optsemc.io import write_csv
from optsemc.manifest import build_manifest, manifest_summary, manifest_fingerprint
OUT = ROOT / "artifact" / "evaluation" / "package_manifest.csv"
SUMMARY = ROOT / "artifact" / "evaluation" / "package_manifest_summary.csv"
rows = build_manifest(ROOT)
write_csv(OUT, [row.as_row() for row in rows], ["path", "sha256", "bytes", "lines", "category"])
summary = manifest_summary(rows)
summary.append({"category": "fingerprint", "files": str(len(rows)), "bytes": manifest_fingerprint(rows), "lines": ""})
write_csv(SUMMARY, summary, ["category", "files", "bytes", "lines"])
print(f"Package manifest: {len(rows)} files; fingerprint={manifest_fingerprint(rows)[:12]}")

