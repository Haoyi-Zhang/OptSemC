#!/usr/bin/env python3
"""Read-only artifact certificate verifier.

This script intentionally does not rewrite evaluation CSVs, regenerate figures,
delete caches, or rebuild manifests. It is a lightweight reviewer entry point
for checking that the existing certificate files are present and internally
passing before running the mutating replay scripts in a separate workspace.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "artifact" / "evaluation"
PAPER = ROOT / "Paper" / "latex" / "paper.pdf"
HAS_PAPER_TREE = (ROOT / "Paper").exists()

ARTIFACT_CERTIFICATE_FILES = [
    "cli_smoke_check.csv",
    "real_engine_validation_check.csv",
    "source_density_hotspots_check.csv",
    "claim_severity_check.csv",
    "package_manifest_check.csv",
    "package_cleanliness.csv",
    "repository_quality.csv",
]

PAPER_CERTIFICATE_FILES = [
    "latex_compile_check.csv",
    "pdf_integrity.csv",
    "format_compliance.csv",
    "visual_latex_style.csv",
    "reference_quality.csv",
    "paper_quality.csv",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def rows_pass(rows: list[dict[str, str]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    if "passed" in rows[0]:
        bad = [row for row in rows if row.get("passed", "").lower() != "true"]
        return not bad, f"{len(rows) - len(bad)}/{len(rows)} true"
    if "status" in rows[0]:
        bad = [row for row in rows if row.get("status", "").upper() != "PASS"]
        return not bad, f"{len(rows) - len(bad)}/{len(rows)} PASS"
    return False, "no pass/status column"


def key_values(path: Path) -> dict[str, str]:
    return {row.get("key", ""): row.get("value", "") for row in read_rows(path)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release",
        action="store_true",
        help="also require the recorded git-tree certificate to be clean",
    )
    args = parser.parse_args()

    checks: list[tuple[str, bool, str]] = []
    if HAS_PAPER_TREE:
        checks.append(("paper_pdf_present", PAPER.exists() and PAPER.stat().st_size > 1000, str(PAPER)))
    else:
        checks.append(("paper_pdf_not_packaged_ok", True, "artifact-only archive"))

    certificate_files = list(ARTIFACT_CERTIFICATE_FILES)
    if HAS_PAPER_TREE:
        certificate_files.extend(PAPER_CERTIFICATE_FILES)

    for name in certificate_files:
        path = EVAL / name
        if not path.exists():
            checks.append((f"{name}:present", False, "missing"))
            continue
        try:
            ok, detail = rows_pass(read_rows(path))
        except Exception as exc:
            ok, detail = False, type(exc).__name__
        checks.append((f"{name}:passing", ok, detail))

    tree_state = EVAL / "git_tree_state.csv"
    if tree_state.exists():
        try:
            state = key_values(tree_state)
            cleanish = (
                state.get("tracked_dirty_count") == "0"
                and state.get("untracked_count") == "0"
                and state.get("ignored_boundary_count") == "0"
            )
            checks.append(("git_tree_state_recorded", True, state.get("tree_state_intent", "")))
            if args.release:
                checks.append(("release_git_tree_clean", cleanish, str(state)))
        except Exception as exc:
            checks.append(("git_tree_state_recorded", False, type(exc).__name__))
    else:
        checks.append(("git_tree_state_recorded", False, "missing"))

    cache_dirs = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("__pycache__")
        if ".git" not in path.parts
    ]
    checks.append(("no_python_cache_dirs_visible", not cache_dirs, ";".join(cache_dirs[:20])))

    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"Read-only certificate check: {passed}/{len(checks)} passed")
    for name, ok, detail in checks:
        if not ok:
            print(f"FAIL {name}: {detail}")
    if passed != len(checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
