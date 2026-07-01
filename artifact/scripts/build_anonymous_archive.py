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
}
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


def prime_stage_checks(stage: Path) -> None:
    env = os.environ.copy()
    artifact = stage / "artifact"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(artifact) + os.pathsep + str(artifact / "scripts")
    subprocess.run(
        [sys.executable, str(artifact / "scripts" / "check_package_cleanliness.py")],
        cwd=str(artifact),
        env=env,
        check=True,
        stdout=subprocess.DEVNULL,
    )


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
            with path.open("rb") as handle:
                zf.writestr(info, handle.read())
    return sha256_file(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "zenodo_artifact" / "optsemc-artifact.zip")
    parser.add_argument("--stage", type=Path, default=ROOT / "zenodo_artifact" / "stage")
    args = parser.parse_args()
    copy_tree(args.stage)
    prime_stage_checks(args.stage)
    write_manifest(args.stage)
    offenders = scan_stage(args.stage)
    if offenders:
        for offender in offenders[:50]:
            print(f"LEAK {offender}", file=sys.stderr)
        raise SystemExit(1)
    digest = make_zip(args.stage, args.output)
    size = args.output.stat().st_size
    print(f"anonymous_archive={args.output}")
    print(f"anonymous_archive_sha256={digest}")
    print(f"anonymous_archive_bytes={size}")


if __name__ == "__main__":
    main()
