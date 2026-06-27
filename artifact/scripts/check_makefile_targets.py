#!/usr/bin/env python3
"""Validate that artifact Makefile targets match the two-folder package layout."""
from __future__ import annotations
from pathlib import Path
import csv, re, sys
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evaluation" / "makefile_targets_check.csv"
rows=[]
def add(check, passed, details=""):
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})
try:
    text=(ROOT/"Makefile").read_text(encoding="utf-8")
    add("makefile_present", True, "")
    add("no_nested_cd_artifact", "cd artifact" not in text, "")
    targets=set(re.findall(r"^([A-Za-z0-9_.-]+):", text, flags=re.M))
    required={"verify","deep","paper","baselines","external","frontier","claims","proofs","coverage","replay","tests","repository","manifest","package-check","audit-all","clean"}
    add("expected_targets_present", required.issubset(targets), ";".join(sorted(required-targets)))
    missing_scripts=[]
    for script in re.findall(r"python (scripts/[A-Za-z0-9_./-]+\.py)", text):
        if not (ROOT/script).exists():
            missing_scripts.append(script)
    add("referenced_scripts_exist", not missing_scripts, ";".join(missing_scripts[:20]))
    add("verify_uses_local_mainline", "./run_mainline_checks.sh" in text, "")
except Exception as exc:
    add("makefile_exception", False, type(exc).__name__ + ":" + str(exc))
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer=csv.DictWriter(handle, fieldnames=["check","passed","details"]); writer.writeheader(); writer.writerows(rows)
passed=sum(r["passed"]=="true" for r in rows)
print(f"Makefile target check: {passed}/{len(rows)} passed")
for r in rows:
    if r["passed"]!="true": print("FAIL", r["check"], r["details"])
if passed != len(rows): sys.exit(1)
