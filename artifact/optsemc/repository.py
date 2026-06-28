"""Repository-level audit and scoring utilities."""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from .manifest import build_manifest, manifest_summary, transient_files

PY_SUFFIXES = {".py"}
DOC_SUFFIXES = {".md", ".txt", ".cff"}
DATA_SUFFIXES = {".csv", ".jsonl", ".json", ".yaml", ".yml"}
STALE_VERSION_RE = re.compile(r"(?i)(\bfinal\b|\brelease\s+candidate\b|version\s*=\s*[\"'][0-9])")
SECRET_RE = re.compile(r"(?i)(api[_-]?key|password|private[_-]?key)\s*[:=]\s*[\'\"]?[^\'\"\s]{8,}")
LOCAL_PATH_RE = re.compile(r"/mnt/data|/home/oai|C:\\\\Users")


@dataclass(frozen=True)
class AuditCheck:
    check: str
    passed: bool
    score: int
    weight: int
    details: str

    def as_row(self) -> dict[str, str]:
        return {"check": self.check, "passed": str(self.passed).lower(), "score": str(self.score), "weight": str(self.weight), "details": self.details}


def python_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.py") if ".git" not in path.parts and "__pycache__" not in path.parts)


def python_loc(root: Path) -> int:
    total = 0
    for path in python_files(root):
        try:
            total += sum(1 for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip() and not line.lstrip().startswith("#"))
        except OSError:
            continue
    return total


def public_classes_and_functions(root: Path) -> tuple[int, int]:
    classes = functions = 0
    for path in python_files(root):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
                classes += 1
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                functions += 1
    return classes, functions


def import_edges(root: Path) -> list[tuple[str, str]]:
    edges = []
    for path in python_files(root):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        rel = path.relative_to(root).as_posix()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                edges.append((rel, node.module))
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    edges.append((rel, alias.name))
    return edges


def stale_package_tokens(root: Path) -> list[str]:
    offenders = []
    allow = {"CHANGELOG.md", "CITATION.cff"}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in DOC_SUFFIXES | {".toml", ".yml", ".yaml"}:
            continue
        rel = path.relative_to(root).as_posix()
        if path.name in allow:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if STALE_VERSION_RE.search(text):
            offenders.append(rel)
    return sorted(offenders)


def secret_or_local_path_offenders(root: Path) -> list[str]:
    offenders = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel_parts = path.relative_to(root).parts
        if len(rel_parts) >= 2 and rel_parts[0] == "artifact" and rel_parts[1] == "evaluation":
            continue
        if path.suffix.lower() not in DOC_SUFFIXES | DATA_SUFFIXES | {".toml", ".sh", ".tex", ".bib"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if SECRET_RE.search(text) or LOCAL_PATH_RE.search(text):
            offenders.append(path.relative_to(root).as_posix())
    return sorted(offenders)


def duplicate_markdown_titles(root: Path) -> list[str]:
    titles: dict[str, list[str]] = {}
    for path in root.glob("*.md"):
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        title = next((line.strip() for line in lines if line.startswith("# ")), path.stem)
        titles.setdefault(title.lower(), []).append(path.name)
    return [";".join(paths) for title, paths in titles.items() if len(paths) > 1]


def repository_audit(root: Path) -> list[AuditCheck]:
    checks: list[AuditCheck] = []
    classes, funcs = public_classes_and_functions(root)
    scripts = list((root / "artifact" / "scripts").glob("*.py")) if (root / "artifact" / "scripts").exists() else []
    tests = list((root / "artifact" / "tests").glob("test_*.py")) if (root / "artifact" / "tests").exists() else []
    modules = list((root / "artifact" / "optsemc").glob("*.py")) if (root / "artifact" / "optsemc").exists() else []
    manifest = build_manifest(root)
    categories = {row["category"]: int(row["files"]) for row in manifest_summary(manifest)}
    imports = import_edges(root)
    package_importing_scripts = sum(1 for src, dst in imports if src.startswith("artifact/scripts/") and (dst.startswith("optsemc") or dst.startswith(".")))
    stale = stale_package_tokens(root)
    secrets = secret_or_local_path_offenders(root)
    transient = transient_files(root)
    dup_docs = duplicate_markdown_titles(root)
    ci = root / ".github" / "workflows" / "ci.yml"
    if not ci.exists():
        ci = root / "artifact" / ".github" / "workflows" / "ci.yml"
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        pyproject = root / "artifact" / "pyproject.toml"
    makefile = root / "Makefile"
    if not makefile.exists():
        makefile = root / "artifact" / "Makefile"
    required_replay = [
        root / "artifact" / "run_mainline_checks.sh",
        root / "artifact" / "run_deep_checks.sh",
        root / "artifact" / "run_from_scratch_no_cache.sh",
        root / "artifact" / "recompute_grounded_mainline.sh",
    ]
    required_grounded = [
        root / "artifact" / "grounded" / "verified_rules.jsonl",
        root / "artifact" / "grounded" / "verified_segments.jsonl",
        root / "artifact" / "grounded" / "verified_sources.csv",
    ]
    required_claim = [
        root / "artifact" / "evaluation" / "claim_evidence_graph.csv",
        root / "artifact" / "evaluation" / "paper_claim_ledger.csv",
        root / "artifact" / "evaluation" / "paper_table_manifest.csv",
    ]
    required_categories = {"paper", "grounded-data", "benchmark-data", "generated-evaluation", "library-code", "script-code", "test-code"}
    present_categories = set(categories)
    checks.append(AuditCheck("project_entrypoints_present", (root / "README.md").exists() and (root / "Paper").is_dir() and (root / "artifact").is_dir(), 10 if (root / "README.md").exists() and (root / "Paper").is_dir() and (root / "artifact").is_dir() else 5, 10, "root README, Paper, artifact"))
    checks.append(AuditCheck("replay_entrypoints_present", all(path.exists() for path in required_replay), 10 if all(path.exists() for path in required_replay) else 4, 10, ";".join(str(path.relative_to(root)) for path in required_replay if not path.exists())))
    checks.append(AuditCheck("grounded_provenance_present", all(path.exists() for path in required_grounded), 10 if all(path.exists() for path in required_grounded) else 4, 10, ";".join(str(path.relative_to(root)) for path in required_grounded if not path.exists())))
    checks.append(AuditCheck("claim_evidence_outputs_present", all(path.exists() for path in required_claim), 10 if all(path.exists() for path in required_claim) else 4, 10, ";".join(str(path.relative_to(root)) for path in required_claim if not path.exists())))
    checks.append(AuditCheck("semantic_library_reused_by_scripts", modules and package_importing_scripts > 0 and classes > 0 and funcs > 0, 10 if modules and package_importing_scripts > 0 and classes > 0 and funcs > 0 else 5, 10, f"modules={len(modules)};classes={classes};functions={funcs};script_import_edges={package_importing_scripts}"))
    checks.append(AuditCheck("unit_test_entrypoints_present", bool(tests) and (root / "artifact" / "scripts" / "run_unit_tests.py").exists(), 10 if bool(tests) and (root / "artifact" / "scripts" / "run_unit_tests.py").exists() else 5, 10, f"tests={len(tests)}"))
    checks.append(AuditCheck("ci_and_cli", ci.exists() and pyproject.exists() and makefile.exists(), 10 if ci.exists() and pyproject.exists() and makefile.exists() else 5, 10, "ci, pyproject, makefile present"))
    checks.append(AuditCheck("package_manifest_covers_research_artifacts", required_categories <= present_categories, 10 if required_categories <= present_categories else 5, 10, f"missing={';'.join(sorted(required_categories - present_categories))}"))
    checks.append(AuditCheck("no_hardcoded_release_tokens", not stale, 10 if not stale else 2, 10, ";".join(stale[:8])))
    checks.append(AuditCheck("no_secret_or_local_path_tokens", not secrets, 10 if not secrets else 0, 10, ";".join(secrets[:8])))
    checks.append(AuditCheck("no_transient_build_artifacts", not transient, 10 if not transient else 3, 10, ";".join(transient[:8])))
    checks.append(AuditCheck("no_duplicate_top_level_docs", not dup_docs, 10 if not dup_docs else 6, 10, ";".join(dup_docs)))
    return checks


def score(checks: Sequence[AuditCheck]) -> tuple[int, int, float]:
    weighted = sum(check.score for check in checks)
    total = sum(check.weight for check in checks)
    return weighted, total, 100.0 * weighted / total if total else 0.0


def score_row(checks: Sequence[AuditCheck]) -> dict[str, str]:
    weighted, total, pct = score(checks)
    return {"metric": "repository_quality_score", "score": str(weighted), "max_score": str(total), "percent": f"{pct:.2f}", "passed": str(pct >= 95.0).lower()}
