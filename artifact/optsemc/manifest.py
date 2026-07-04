"""Deterministic package-manifest construction and verification."""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

IGNORED_DIRS = frozenset({".git", ".reference_guard_cache", "__pycache__", ".pytest_cache", ".mypy_cache", "build", "dist", "tmp", "zenodo_artifact"})
TRANSIENT_SUFFIXES = (".aux", ".log", ".out", ".toc", ".bbl", ".blg", ".compile.stdout", ".backup")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def count_lines(path: Path) -> int:
    try:
        with path.open("rb") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return 0


def classify_path(path: Path) -> str:
    parts = path.parts
    suffix = path.suffix.lower()
    if parts[:1] == ("Paper",):
        return "paper"
    if parts[:2] == ("artifact", "grounded"):
        return "grounded-data"
    if parts[:2] == ("artifact", "benchmark"):
        return "benchmark-data"
    if parts[:2] == ("artifact", "evaluation"):
        return "generated-evaluation"
    if parts[:2] == ("artifact", "optsemc"):
        return "library-code"
    if parts[:2] == ("artifact", "scripts"):
        return "script-code"
    if parts[:2] == ("artifact", "tests"):
        return "test-code"
    if suffix in {".md", ".txt", ".cff"}:
        return "documentation"
    if suffix in {".yml", ".yaml", ".json"}:
        return "configuration"
    return "other"


def should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if any(part in IGNORED_DIRS or part.endswith(".egg-info") for part in rel.parts):
        return True
    if path.name.startswith(".") and path.name not in {".gitignore"}:
        return False
    if path.name.endswith(TRANSIENT_SUFFIXES):
        return True
    if path.name.startswith("paper_build"):
        return True
    if path.name.startswith("package_manifest") and path.parent.name == "evaluation":
        return True
    if path.parent.name == "evaluation" and path.name in {"package_files.csv", "package_fingerprint_summary.csv", "package_snapshot_check.csv", "integrity_suite.csv", "fast_mainline_results.csv", "optsemc-artifact.sha256", "reference_guard_audit_latest.json", "reference_guard_audit_latest.md", "git_tree_status.txt"}:
        return True
    return False


@dataclass(frozen=True)
class ManifestRow:
    path: str
    sha256: str
    bytes: int
    lines: int
    category: str

    def as_row(self) -> dict[str, str]:
        return {"path": self.path, "sha256": self.sha256, "bytes": str(self.bytes), "lines": str(self.lines), "category": self.category}


def build_manifest(root: Path) -> list[ManifestRow]:
    rows: list[ManifestRow] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if should_skip(path, root):
            continue
        rel = path.relative_to(root).as_posix()
        rows.append(ManifestRow(rel, sha256_file(path), path.stat().st_size, count_lines(path), classify_path(Path(rel))))
    return rows


def manifest_fingerprint(rows: Sequence[ManifestRow]) -> str:
    payload = "\n".join(f"{row.path}\t{row.sha256}\t{row.bytes}" for row in rows)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def manifest_summary(rows: Sequence[ManifestRow]) -> list[dict[str, str]]:
    buckets: dict[str, dict[str, int]] = {}
    for row in rows:
        bucket = buckets.setdefault(row.category, {"files": 0, "bytes": 0, "lines": 0})
        bucket["files"] += 1
        bucket["bytes"] += row.bytes
        bucket["lines"] += row.lines
    result = []
    for category in sorted(buckets):
        bucket = buckets[category]
        result.append({"category": category, "files": str(bucket["files"]), "bytes": str(bucket["bytes"]), "lines": str(bucket["lines"])})
    return result


def transient_files(root: Path) -> list[str]:
    offenders = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part in IGNORED_DIRS or part.endswith(".egg-info") for part in rel.parts):
            continue
        if path.is_file() and (path.name.startswith("paper_build") or path.name.endswith(TRANSIENT_SUFFIXES)):
            offenders.append(rel.as_posix())
    return sorted(offenders)
