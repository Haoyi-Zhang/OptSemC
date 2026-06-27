#!/usr/bin/env python3
"""Audit repository-level reproducibility packaging."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifact"
EVAL = ART / "evaluation"
sys.path.insert(0, str(ART))
from optsemc.io import write_csv

OUT = EVAL / "reproducibility_package.csv"
REQUIRED = [
    "artifact/README.md",
    "artifact/REPRODUCIBILITY.md",
    "artifact/CITATION.cff",
    "artifact/LICENSE",
    "artifact/Makefile",
    "artifact/pyproject.toml",
    "artifact/requirements.txt",
    "artifact/run_mainline_checks.sh",
    "artifact/run_deep_checks.sh",
    "artifact/optsemc/__init__.py",
    "artifact/baselines/baseline_catalog.yaml",
    "artifact/external/workload_motifs.yaml",
]
TEXT_EXT = {".md", ".txt", ".toml", ".yml", ".yaml", ".sh", ".py", ".tex", ".csv", ".bib", ".cff"}
BANNED_PATTERNS = [
    re.compile(r"/mnt/data/"),
    re.compile(r"/tmp/optsem"),
    re.compile(r"NEXT_WINDOW_HANDOFF", re.I),
    re.compile(r"CURRENT_STATUS", re.I),
    re.compile(r"LICENSE_PENDING", re.I),
    re.compile(r"GITHUB_SYNC", re.I),
]


def scan_text_files() -> list[str]:
    offenders = []
    checker_allowlist = {"check_reproducibility_package.py", "check_artifact_hygiene.py"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix not in TEXT_EXT:
            continue
        if path.name in checker_allowlist or path == OUT:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pat in BANNED_PATTERNS:
            if pat.search(text):
                offenders.append(f"{path.relative_to(ROOT)}:{pat.pattern}")
                break
    return offenders


def main() -> None:
    rows = []
    def add(check: str, ok: bool, details: str = "") -> None:
        rows.append({"check": check, "passed": str(bool(ok)).lower(), "details": details})
    missing = [rel for rel in REQUIRED if not (ROOT / rel).exists()]
    add("required_reproducibility_files_present", not missing, "|".join(missing))
    makefile = (ART / "Makefile").read_text(encoding="utf-8") if (ART / "Makefile").exists() else ""
    add("makefile_has_verify_deep_paper_targets", all(f"{target}:" in makefile for target in ["verify", "deep", "paper", "baselines"]), "")
    pyproject = (ART / "pyproject.toml").read_text(encoding="utf-8") if (ART / "pyproject.toml").exists() else ""
    add("pyproject_declares_optsemc_package", "name = \"optsemc\"" in pyproject and "package-dir" in pyproject and "optsemc" in pyproject, "")
    offenders = scan_text_files()
    add("no_local_or_handoff_paths_in_text_package", not offenders, "|".join(offenders[:10]))
    write_csv(OUT, rows, ["check", "passed", "details"])
    passed = sum(r["passed"] == "true" for r in rows)
    print(f"Reproducibility package: {passed}/{len(rows)} checks passed")
    if passed != len(rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
