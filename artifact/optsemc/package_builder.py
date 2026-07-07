"""Repository packaging helpers used by the package gates."""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

TEXT_SUFFIXES = {".py", ".md", ".txt", ".tex", ".bib", ".csv", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".sh", ".cff", ""}
EXCLUDE_DIRS = {
    ".git",
    ".reference_guard_cache",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "build",
    "dist",
    "tmp",
    "zenodo_artifact",
}
TRANSIENT_SUFFIXES = {
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".bbl",
    ".blg",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
    ".pyc",
    ".pyo",
}
GENERATED_SELF_CHECKS = {
    "artifact/evaluation/package_files.csv",
    "artifact/evaluation/package_fingerprint_summary.csv",
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
    "artifact/evaluation/git_tree_state.csv",
    "artifact/evaluation/git_tree_state_check.csv",
    "artifact/evaluation/git_tree_porcelain.txt",
}
REVIEW_LOG_PREFIXES = (
    "external_opus_blind_review_round",
    "dual_blind_review_round",
)
CHUNK_SIZE = 1024 * 1024
TEXT_PROBE_BYTES = 16 * 1024


@dataclass(frozen=True)
class PackageFile:
    path: str
    size: int
    sha256: str
    text: bool
    category: str

    def as_row(self) -> dict[str, str]:
        return {"path": self.path, "size": str(self.size), "sha256": self.sha256, "text": str(self.text).lower(), "category": self.category}


def artifact_only_requested(root: Path) -> bool:
    return os.environ.get("ANONYMOUS_ARTIFACT_ONLY", "0") == "1" or not (root / "Paper").exists()


def should_include(root: Path, rel: Path, path: Path) -> bool:
    if artifact_only_requested(root) and rel.parts[:1] == ("Paper",):
        return False
    parts = set(rel.parts)
    if parts & EXCLUDE_DIRS:
        return False
    rel_posix = rel.as_posix()
    if rel_posix == "reference_guard_audit.md":
        return False
    if rel.parts[:2] == ("artifact", "evaluation") and (
        any(path.name.startswith(prefix) for prefix in REVIEW_LOG_PREFIXES)
        or path.name.endswith("_disposition.md")
    ):
        return False
    if rel_posix in GENERATED_SELF_CHECKS:
        return False
    if path.suffix in TRANSIENT_SUFFIXES:
        return False
    return path.is_file()


def file_sha256(path: Path) -> str:
    """Return a SHA-256 digest without materializing large generated outputs."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    try:
        sample = path.read_bytes()[:TEXT_PROBE_BYTES]
        sample.decode("utf-8")
        return True
    except (UnicodeDecodeError, OSError):
        return False


def categorize(path: Path) -> str:
    rel = path.as_posix()
    if rel.startswith("artifact/optsemc/"):
        return "library"
    if rel.startswith("artifact/scripts/"):
        return "scripts"
    if rel.startswith("artifact/tests/"):
        return "tests"
    if rel.startswith("artifact/evaluation/"):
        return "evaluation"
    if rel.startswith("artifact/grounded/"):
        return "grounded-data"
    if rel.startswith("artifact/benchmark/"):
        return "benchmark-data"
    if rel.startswith("artifact/external/"):
        return "external-denominator"
    if rel.startswith("Paper/"):
        return "paper"
    if rel.startswith(".github/"):
        return "ci"
    return "root"


def package_files(root: Path) -> tuple[PackageFile, ...]:
    """Enumerate package files with bounded memory.

    Large generated contract relations can exceed tens of megabytes.  The
    manifest should therefore be a streaming pass over files, not an accidental
    memory benchmark.  This keeps reader replay stable on small machines.
    """
    rows: list[PackageFile] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if not should_include(root, rel, path):
            continue
        rows.append(PackageFile(rel.as_posix(), path.stat().st_size, file_sha256(path), is_text_file(path), categorize(rel)))
    return tuple(rows)


def package_summary(files: Sequence[PackageFile]) -> list[dict[str, str]]:
    by_category: dict[str, list[PackageFile]] = {}
    for row in files:
        by_category.setdefault(row.category, []).append(row)
    out = []
    for category in sorted(by_category):
        rows = by_category[category]
        out.append({"category": category, "files": str(len(rows)), "bytes": str(sum(row.size for row in rows)), "text_files": str(sum(row.text for row in rows))})
    out.append({"category": "ALL", "files": str(len(files)), "bytes": str(sum(row.size for row in files)), "text_files": str(sum(row.text for row in files))})
    return out


def package_fingerprint(files: Sequence[PackageFile]) -> str:
    payload = [{"path": row.path, "size": row.size, "sha256": row.sha256} for row in files]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
