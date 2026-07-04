#!/usr/bin/env python3
"""Build an anonymous artifact-only archive for long-term public storage."""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifact"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "Paper",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".reference_guard_cache",
    "build",
    "dist",
}
EXCLUDED_FILE_NAMES = {
    "build_anonymous_archive.py",
    "check_format_compliance.py",
    "check_latex_compile.py",
    "check_manuscript_style.py",
    "check_paper_numeric_citations.py",
    "check_paper_numeric_claims.py",
    "check_paper_quality.py",
    "check_paper_table_sources.py",
    "check_pdf_integrity.py",
    "check_reference_quality.py",
    "check_visual_latex_style.py",
    "render_paper_tables.py",
    "format_compliance.csv",
    "latex_compile_check.csv",
    "manuscript_style.csv",
    "package_coherence.csv",
    "package_files.csv",
    "paper_claim_ledger.csv",
    "paper_numeric_claims.csv",
    "paper_quality.csv",
    "paper_table_manifest.csv",
    "paper_table_renderers.csv",
    "paper_table_source_check.csv",
    "paper_table_source_check_summary.csv",
    "pdf_integrity.csv",
    "reference_quality.csv",
    "visual_latex_style.csv",
    "optsemc-artifact.sha256",
    "reference_guard_audit_latest.json",
    "reference_guard_audit_latest.md",
    "git_tree_status.txt",
}
EXCLUDED_SUFFIXES = {
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
}
MANIFEST_SKIP = {
    "artifact/evaluation/package_manifest.csv",
    "artifact/evaluation/package_manifest_summary.csv",
    "artifact/evaluation/package_manifest_check.csv",
    "artifact/evaluation/package_snapshot_check.csv",
    "artifact/evaluation/integrity_suite.csv",
    "artifact/evaluation/fast_mainline_results.csv",
    "artifact/evaluation/optsemc-artifact.sha256",
    "artifact/evaluation/reference_guard_audit_latest.json",
    "artifact/evaluation/reference_guard_audit_latest.md",
    "artifact/evaluation/git_tree_status.txt",
}
SOURCE_STATE_FILE = "artifact/evaluation/git_tree_state.csv"
TEXT_SUFFIXES = {
    ".bib",
    ".cff",
    ".csv",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".sh",
    ".tex",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"\b(?!(?:127\.0\.0\.1|0\.0\.0\.0|255\.255\.255\.255)\b)(?:\d{1,3}\.){3}\d{1,3}\b"),
    re.compile(r"\b(?:password|passwd|secret|api[_-]?key|auth[_-]?token|access[_-]?token)\b\s*[:=]\s*[\"']?[^\"'\s]{8,}", re.I),
    re.compile(r"\b(?:anthropic|openai|zenodo|github)[A-Z0-9_.:/_-]*(?:token|key|secret)\b\s*[:=]", re.I),
    re.compile(r"github\.com/[^/\s,]+/OptSemC", re.I),
    re.compile(r"\\(?:author|affiliation|institution|city|country)\b|\borcid\b", re.I),
    re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s,;:]+", re.I),
]


def should_skip(rel: Path) -> bool:
    parts = set(rel.parts)
    if parts & EXCLUDED_DIRS:
        return True
    if rel.name in EXCLUDED_FILE_NAMES:
        return True
    rel_posix = rel.as_posix()
    if rel_posix.startswith("artifact/evaluation/") and rel.name in EXCLUDED_FILE_NAMES:
        return True
    if rel.name.startswith(".") and rel.name not in {".gitignore"}:
        return True
    if any(rel_posix.endswith(suffix) for suffix in EXCLUDED_SUFFIXES):
        return True
    if rel.name.endswith(".backup"):
        return True
    return False


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def git(args: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            ["git", "-C", str(ROOT), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
    except Exception as exc:
        return 127, f"unavailable:{type(exc).__name__}"
    return proc.returncode, proc.stdout


def collect_source_tree_state(allow_dirty: bool) -> list[dict[str, str]]:
    head_code, head = git(["rev-parse", "--short=12", "HEAD"])
    status_code, status = git(["status", "--porcelain=v1", "--untracked-files=all"])
    diff_code, diff = git(["diff", "--no-ext-diff", "--binary"])
    cached_code, cached = git(["diff", "--cached", "--no-ext-diff", "--binary"])
    if head_code != 0 or status_code != 0 or diff_code != 0 or cached_code != 0:
        raise RuntimeError("git state unavailable; refusing to build release archive")
    tracked_or_untracked = [line for line in status.splitlines() if line.strip() and not line.startswith("!! ")]
    if tracked_or_untracked and not allow_dirty:
        preview = "\n".join(tracked_or_untracked[:40])
        raise RuntimeError(
            "source tree is dirty; commit or clean before building the release archive\n"
            + preview
        )
    return [
        {"key": "git_head", "value": head.strip()},
        {"key": "source_tree_clean", "value": str(not tracked_or_untracked).lower()},
        {"key": "tracked_or_untracked_count", "value": str(len(tracked_or_untracked))},
        {"key": "allow_dirty_source", "value": str(bool(allow_dirty)).lower()},
        {"key": "status_sha256", "value": sha256_text(status)},
        {"key": "diff_sha256", "value": sha256_text(diff)},
        {"key": "cached_diff_sha256", "value": sha256_text(cached)},
    ]


def copy_tree(stage: Path) -> None:
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    (stage / "artifact").mkdir()
    shutil.copy2(ART / "README.md", stage / "README.md")
    for path in sorted(ART.rglob("*")):
        rel = path.relative_to(ROOT)
        if should_skip(rel):
            continue
        dest = stage / rel
        if path.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)


def write_manifest(stage: Path) -> None:
    rows: list[dict[str, str]] = []
    for path in sorted(p for p in stage.rglob("*") if p.is_file()):
        rel = path.relative_to(stage).as_posix()
        if rel in MANIFEST_SKIP:
            continue
        rows.append(
            {
                "path": rel,
                "sha256": sha256_file(path),
                "bytes": str(path.stat().st_size),
            }
        )
    eval_dir = stage / "artifact" / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)
    manifest = eval_dir / "package_manifest.csv"
    with manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "sha256", "bytes"])
        writer.writeheader()
        writer.writerows(rows)
    summary: dict[str, int] = {}
    for row in rows:
        category = row["path"].split("/", 2)[1] if row["path"].startswith("artifact/") and "/" in row["path"] else "root"
        summary[category] = summary.get(category, 0) + 1
    with (eval_dir / "package_manifest_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["category", "files"])
        writer.writeheader()
        for category in sorted(summary):
            writer.writerow({"category": category, "files": str(summary[category])})


def write_source_tree_state(stage: Path, rows: list[dict[str, str]]) -> None:
    out = stage / SOURCE_STATE_FILE
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "value"])
        writer.writeheader()
        writer.writerows(rows)


def prime_stage_checks(stage: Path) -> None:
    env = os.environ.copy()
    artifact = stage / "artifact"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(artifact) + os.pathsep + str(artifact / "scripts")
    commands = [
        "check_package_cleanliness.py",
        "check_package_integrity.py",
        "compute_practice_projection_surfaces.py",
        "check_practice_projection_surfaces.py",
        "build_environment_report.py",
        "check_environment_report.py",
        "check_real_engine_validation.py",
        "compute_repair_generalization.py",
        "check_repair_generalization.py",
        "build_claim_metric_summary.py",
        "build_claim_ledger.py",
        "build_claim_evidence_graph.py",
        "check_claim_evidence_graph.py",
        "run_repository_audit.py",
        "check_repository_quality.py",
        "check_git_tree_state.py",
        "check_artifact_registry.py",
        "build_package_fingerprint.py",
        "build_package_manifest.py",
        "check_package_manifest.py",
        "check_certificate_freshness.py",
        "build_package_fingerprint.py",
        "build_package_manifest.py",
        "check_package_manifest.py",
        "check_package_snapshot.py",
        "run_integrity_suite.py",
    ]
    for script in commands:
        subprocess.run(
            [sys.executable, str(artifact / "scripts" / script)],
            cwd=str(artifact),
            env=env,
            check=True,
            stdout=subprocess.DEVNULL,
        )


def verify_stage_fingerprint(stage: Path) -> list[str]:
    eval_dir = stage / "artifact" / "evaluation"
    files_csv = eval_dir / "package_files.csv"
    summary_csv = eval_dir / "package_fingerprint_summary.csv"
    errors: list[str] = []
    if not files_csv.exists():
        return ["missing package_files.csv"]
    if not summary_csv.exists():
        return ["missing package_fingerprint_summary.csv"]
    with files_csv.open(newline="", encoding="utf-8") as handle:
        file_rows = list(csv.DictReader(handle))
    with summary_csv.open(newline="", encoding="utf-8") as handle:
        summary_rows = list(csv.DictReader(handle))
    if len(file_rows) < 100:
        errors.append(f"package_files_too_small:{len(file_rows)}")
    missing_paths = [
        row.get("path", "")
        for row in file_rows
        if row.get("path") and not (stage / row["path"]).is_file()
    ]
    if missing_paths:
        errors.append("listed_paths_missing:" + ",".join(missing_paths[:10]))
    by_category = {row.get("category", ""): row for row in summary_rows}
    all_row = by_category.get("ALL")
    fp_row = by_category.get("FINGERPRINT")
    if not all_row or int(all_row.get("files", "0") or 0) != len(file_rows):
        errors.append(f"summary_all_mismatch:{all_row}")
    if not fp_row or not re.fullmatch(r"[0-9a-f]{64}", fp_row.get("bytes", "")):
        errors.append(f"fingerprint_missing_or_invalid:{fp_row}")
    return errors


def scan_stage(stage: Path) -> list[str]:
    offenders: list[str] = []
    for path in sorted(p for p in stage.rglob("*") if p.is_file()):
        rel = path.relative_to(stage).as_posix()
        if rel.startswith("Paper/") or "/Paper/" in rel:
            offenders.append(f"{rel}:paper-tree")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                offenders.append(f"{rel}:{pattern.pattern}")
                break
    return offenders


def make_zip(stage: Path, output: Path) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in stage.rglob("*") if p.is_file()):
            rel = path.relative_to(stage).as_posix()
            info = zipfile.ZipInfo(rel)
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            mode = 0o755 if path.suffix == ".sh" else 0o644
            info.external_attr = mode << 16
            with path.open("rb") as handle:
                zf.writestr(info, handle.read())
    return sha256_file(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "zenodo_artifact" / "optsemc-artifact.zip")
    parser.add_argument("--stage", type=Path, default=ROOT / "zenodo_artifact" / "stage")
    parser.add_argument("--digest-output", type=Path, default=ROOT / "artifact" / "evaluation" / "optsemc-artifact.sha256")
    parser.add_argument("--keep-stage", action="store_true")
    parser.add_argument("--allow-dirty-source", action="store_true",
                        help="Development-only override. Release/Zenodo archives must leave this off.")
    args = parser.parse_args()
    source_state = collect_source_tree_state(args.allow_dirty_source)
    copy_tree(args.stage)
    write_source_tree_state(args.stage, source_state)
    prime_stage_checks(args.stage)
    fingerprint_errors = verify_stage_fingerprint(args.stage)
    if fingerprint_errors:
        for error in fingerprint_errors[:20]:
            print(f"FINGERPRINT {error}", file=sys.stderr)
        raise SystemExit(1)
    offenders = scan_stage(args.stage)
    if offenders:
        for offender in offenders[:50]:
            print(f"LEAK {offender}", file=sys.stderr)
        raise SystemExit(1)
    digest = make_zip(args.stage, args.output)
    size = args.output.stat().st_size
    args.digest_output.parent.mkdir(parents=True, exist_ok=True)
    args.digest_output.write_text(f"{digest}  {args.output.name}\n", encoding="utf-8")
    if not args.keep_stage:
        shutil.rmtree(args.stage, ignore_errors=True)
    print(f"anonymous_archive={args.output}")
    print(f"anonymous_archive_sha256={digest}")
    print(f"anonymous_archive_bytes={size}")


if __name__ == "__main__":
    main()
