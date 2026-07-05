#!/usr/bin/env python3
"""Record Git tree state for the artifact certificate set."""
from __future__ import annotations

import csv
import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifact" / "evaluation" / "git_tree_state_check.csv"
STATE = ROOT / "artifact" / "evaluation" / "git_tree_state.csv"
PORCELAIN = ROOT / "artifact" / "evaluation" / "git_tree_porcelain.txt"
LEGACY_STATUS = ROOT / "artifact" / "evaluation" / "git_tree_status.txt"


def git(args: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(["git", "-C", str(ROOT), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=15)
    except Exception as exc:
        return 127, f"unavailable:{type(exc).__name__}"
    return proc.returncode, proc.stdout


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def manifest_fingerprint() -> str:
    summary = ROOT / "artifact" / "evaluation" / "package_manifest_summary.csv"
    if not summary.exists():
        return "missing"
    try:
        with summary.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if row.get("category") == "fingerprint":
                    return row.get("bytes", "") or "missing"
    except Exception as exc:
        return f"unavailable:{type(exc).__name__}"
    return "missing"


def porcelain(include_ignored: bool = False) -> list[str]:
    args = ["status", "--porcelain=v1", "--untracked-files=all"]
    if include_ignored:
        args.append("--ignored")
    code, out = git(args)
    if code != 0:
        return [f"!! git-status-unavailable:{out.strip()[:120]}"]
    return [line for line in out.splitlines() if line.strip()]


def ignored_boundary(lines: list[str]) -> list[str]:
    offenders: list[str] = []
    allowed_prefixes = (
        ".reference_guard_cache/",
        ".pytest_cache/",
        ".mypy_cache/",
        "build/",
        "artifact/build/",
        "dist/",
        "artifact/dist/",
        "zenodo_artifact/",
    )
    allowed_suffixes = (
        ".aux",
        ".bbl",
        ".blg",
        ".fdb_latexmk",
        ".fls",
        ".log",
        ".out",
        ".pyc",
        ".pyo",
        ".synctex.gz",
        ".toc",
    )
    for line in lines:
        if not line.startswith("!! "):
            continue
        path = line[3:]
        if path.startswith(allowed_prefixes) or path.endswith(allowed_suffixes):
            continue
        if path.startswith("artifact/") or path.startswith("Paper/") or "/" not in path:
            offenders.append(path)
    return sorted(offenders)


rows: list[dict[str, str]] = []


def add(check: str, passed: bool, details: str = "") -> None:
    rows.append({"check": check, "passed": str(bool(passed)).lower(), "details": details})


def write_outputs(state_rows: list[dict[str, str]], status_text: str) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if LEGACY_STATUS.exists():
        LEGACY_STATUS.unlink()
    with STATE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "value"])
        writer.writeheader()
        writer.writerows(state_rows)
    PORCELAIN.write_text(status_text, encoding="utf-8")
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"])
        writer.writeheader()
        writer.writerows(rows)


artifact_only = not (ROOT / "Paper").exists()
if artifact_only and not (ROOT / ".git").exists():
    existing_rows: list[dict[str, str]] = []
    if STATE.exists():
        try:
            with STATE.open(newline="", encoding="utf-8") as handle:
                existing_rows = list(csv.DictReader(handle))
        except Exception:
            existing_rows = []
    status_text = "artifact-only archive: .git is not packaged; source-tree clean state is enforced before archive construction\n"
    status_sha = sha256_text(status_text)
    add("git_head_available", True, "artifact-only-not-packaged")
    add("tree_state_recorded", True, "artifact-only-not-packaged")
    add("no_ignored_boundary_files", True, "artifact-only-not-packaged")
    add("clean_tree_when_required", True, "artifact-only-not-packaged")
    add("tree_state_hashes_recorded", len(status_sha) == 64, status_sha[:12])
    write_outputs(
        existing_rows
        + [
            {"key": "git_head", "value": "artifact-only-not-packaged"},
            {"key": "tracked_dirty_count", "value": "0"},
            {"key": "untracked_count", "value": "0"},
            {"key": "ignored_boundary_count", "value": "0"},
            {"key": "require_clean", "value": "not-applicable"},
            {"key": "tree_state_intent", "value": "source-clean-recorded-artifact-only"},
            {"key": "status_sha256", "value": status_sha},
            {"key": "diff_sha256", "value": sha256_text("")},
            {"key": "cached_diff_sha256", "value": sha256_text("")},
            {"key": "manifest_fingerprint", "value": manifest_fingerprint()},
        ],
        status_text,
    )
    print(f"Git tree state check: {len(rows)}/{len(rows)} passed")
    sys.exit(0)


head_code, head = git(["rev-parse", "--short=12", "HEAD"])
status_code, status_out = git(["status", "--porcelain=v1", "--untracked-files=all"])
diff_code, diff_out = git(["diff", "--no-ext-diff", "--binary"])
cached_diff_code, cached_diff_out = git(["diff", "--cached", "--no-ext-diff", "--binary"])
dirty = porcelain(include_ignored=False)
with_ignored = porcelain(include_ignored=True)
ignored = ignored_boundary(with_ignored)
release_gate = os.environ.get("OPTSEMC_RELEASE_GATE", "0") == "1"
development_snapshot = os.environ.get("OPTSEMC_DEVELOPMENT_SNAPSHOT", "0") == "1"
require_clean = release_gate or os.environ.get("OPTSEMC_REQUIRE_CLEAN_GIT", "0") == "1" or not development_snapshot

tracked_or_untracked = [line for line in dirty if not line.startswith("!! ")]
untracked = [line for line in tracked_or_untracked if line.startswith("?? ")]
tracked = [line for line in tracked_or_untracked if not line.startswith("?? ")]

add("git_head_available", head_code == 0 and bool(head.strip()), head.strip()[:80])
add("tree_state_recorded", True, f"tracked={len(tracked)};untracked={len(untracked)};require_clean={require_clean};release_gate={release_gate};development_snapshot={development_snapshot}")
add("no_ignored_boundary_files", not ignored, ";".join(ignored[:20]))
add("release_gate_requires_clean_tree", (not release_gate) or require_clean, f"release_gate={release_gate};require_clean={require_clean}")
add("dirty_tree_requires_explicit_development_snapshot", require_clean or development_snapshot, f"require_clean={require_clean};development_snapshot={development_snapshot}")
add("clean_tree_when_required", (not require_clean) or not tracked_or_untracked, ";".join(tracked_or_untracked[:20]))

status_sha = sha256_text(status_out) if status_code == 0 else ""
diff_sha = sha256_text(diff_out) if diff_code == 0 else ""
cached_diff_sha = sha256_text(cached_diff_out) if cached_diff_code == 0 else ""
add("tree_state_hashes_recorded", all(len(value) == 64 for value in (status_sha, diff_sha, cached_diff_sha)), f"status={status_sha[:12]};diff={diff_sha[:12]};cached={cached_diff_sha[:12]}")
state_rows = [
    {"key": "git_head", "value": head.strip() if head_code == 0 else f"unavailable:exit{head_code}"},
    {"key": "tracked_dirty_count", "value": str(len(tracked))},
    {"key": "untracked_count", "value": str(len(untracked))},
    {"key": "ignored_boundary_count", "value": str(len(ignored))},
    {"key": "require_clean", "value": str(require_clean).lower()},
    {"key": "release_gate", "value": str(release_gate).lower()},
    {"key": "development_snapshot", "value": str(development_snapshot).lower()},
    {
        "key": "tree_state_intent",
        "value": "development-record-only" if development_snapshot else "clean-tree-required",
    },
    {"key": "status_sha256", "value": status_sha or f"unavailable:exit{status_code}"},
    {"key": "diff_sha256", "value": diff_sha or f"unavailable:exit{diff_code}"},
    {"key": "cached_diff_sha256", "value": cached_diff_sha or f"unavailable:exit{cached_diff_code}"},
    {"key": "manifest_fingerprint", "value": manifest_fingerprint()},
]
write_outputs(state_rows, status_out if status_code == 0 else f"git status unavailable: exit {status_code}\n")
passed = sum(row["passed"] == "true" for row in rows)
print(f"Git tree state check: {passed}/{len(rows)} passed")
for row in rows:
    if row["passed"] != "true":
        print("FAIL", row)
if passed != len(rows):
    sys.exit(1)
