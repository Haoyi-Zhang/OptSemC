#!/usr/bin/env python3
"""Verify the deterministic package manifest against the current tree."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "artifact"))
from optsemc.manifest import build_manifest, manifest_fingerprint, transient_files
from optsemc.io import write_csv
OUT = ROOT / "artifact" / "evaluation" / "package_manifest_check.csv"
manifest = ROOT / "artifact" / "evaluation" / "package_manifest.csv"
rows=[]
def add(check, passed, details=""):
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": str(details)})
current = build_manifest(ROOT)
add("manifest_file_present", manifest.exists(), str(manifest.relative_to(ROOT)))
if manifest.exists():
    old = list(csv.DictReader(manifest.open(newline='', encoding='utf-8')))
    current_map = {r.path: r for r in current}
    old_map = {r['path']: r for r in old}
    missing = sorted(set(current_map) - set(old_map))
    stale = sorted(set(old_map) - set(current_map))
    changed = sorted(path for path in set(old_map) & set(current_map) if old_map[path]['sha256'] != current_map[path].sha256)
    add("manifest_complete", not missing, ";".join(missing[:10]))
    add("manifest_no_stale_entries", not stale, ";".join(stale[:10]))
    add("manifest_hashes_current", not changed, ";".join(changed[:10]))
    add("manifest_fingerprint_nonempty", bool(manifest_fingerprint(current)), manifest_fingerprint(current)[:12])
else:
    add("manifest_complete", False, "missing manifest")
    add("manifest_no_stale_entries", False, "missing manifest")
    add("manifest_hashes_current", False, "missing manifest")
    add("manifest_fingerprint_nonempty", False, "missing manifest")
transient = transient_files(ROOT)
add("no_transient_build_artifacts", not transient, ";".join(transient[:10]))
write_csv(OUT, rows, ["check", "passed", "details"])
passed=sum(r['passed']=='true' for r in rows)
print(f"Package manifest check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)
