"""Code-quality metrics that avoid heavyweight external linters."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class PythonFileQuality:
    path: str
    functions: int
    classes: int
    imports: int
    max_function_lines: int
    syntax_ok: bool

    def as_row(self) -> dict[str, str]:
        return {"path": self.path, "functions": str(self.functions), "classes": str(self.classes), "imports": str(self.imports), "max_function_lines": str(self.max_function_lines), "syntax_ok": str(self.syntax_ok).lower()}


def analyze_python_file(path: Path, root: Path) -> PythonFileQuality:
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except Exception:
        return PythonFileQuality(path.relative_to(root).as_posix(), 0, 0, 0, 0, False)
    funcs = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    max_lines = 0
    for fn in funcs:
        if getattr(fn, "end_lineno", None) and getattr(fn, "lineno", None):
            max_lines = max(max_lines, fn.end_lineno - fn.lineno + 1)
    return PythonFileQuality(path.relative_to(root).as_posix(), len(funcs), len(classes), len(imports), max_lines, True)


def analyze_tree(root: Path) -> list[PythonFileQuality]:
    return [analyze_python_file(path, root) for path in sorted(root.rglob("*.py")) if ".git" not in path.parts and "__pycache__" not in path.parts]


def quality_summary(rows: Sequence[PythonFileQuality]) -> list[dict[str, str]]:
    return [
        {"metric": "python_files", "value": str(len(rows))},
        {"metric": "syntax_ok_files", "value": str(sum(1 for row in rows if row.syntax_ok))},
        {"metric": "functions", "value": str(sum(row.functions for row in rows))},
        {"metric": "classes", "value": str(sum(row.classes for row in rows))},
        {"metric": "max_function_lines", "value": str(max((row.max_function_lines for row in rows), default=0))},
        {"metric": "files_over_120_function_lines", "value": str(sum(1 for row in rows if row.max_function_lines > 120))},
    ]


def import_graph_rows(root: Path) -> list[dict[str, str]]:
    rows = []
    for path in sorted(root.rglob("*.py")):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        rel = path.relative_to(root).as_posix()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                rows.append({"source": rel, "target": node.module, "kind": "from"})
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    rows.append({"source": rel, "target": alias.name, "kind": "import"})
    return rows

