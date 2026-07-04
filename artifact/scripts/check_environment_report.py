#!/usr/bin/env python3
"""Check that the replay environment report contains the minimum audit fields."""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "evaluation" / "environment.csv"
OUT = ROOT / "evaluation" / "environment_check.csv"
rows: list[dict[str, str]] = []


def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})


if IN.exists():
    with IN.open(newline="", encoding="utf-8") as handle:
        data = {row.get("key", ""): row.get("value", "") for row in csv.DictReader(handle)}
else:
    data = {}

required = ["scope", "python", "platform", "machine", "python_executable_name", "pyyaml", "duckdb", "psycopg", "postgres", "git_head", "git_dirty_count", "artifact_readme_sha256"]
missing = [key for key in required if not data.get(key)]
add("environment_report_present", IN.exists(), str(IN.relative_to(ROOT)) if IN.exists() else "missing")
add("required_environment_fields", not missing, ";".join(missing))
add("python_version_recorded", "Python" not in data.get("python", "") and len(data.get("python", "")) > 5, data.get("python", ""))
add("scope_is_known", data.get("scope") in {"full-repository", "artifact-only"}, data.get("scope", ""))
path_re = re.compile(r"(?i)(/data/|/tmp/|[A-Z]:[\\/]+Users[\\/]+)")
path_leaks = [key for key, value in data.items() if path_re.search(value)]
add("environment_values_are_redacted", not path_leaks, ";".join(path_leaks))

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
    writer.writeheader()
    writer.writerows(rows)
passed = sum(row["passed"] == "true" for row in rows)
print(f"Environment report check: {passed}/{len(rows)} passed")
for row in rows:
    if row["passed"] != "true":
        print("FAIL", row)
if passed != len(rows):
    sys.exit(1)
