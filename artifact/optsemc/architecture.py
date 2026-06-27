"""Static architecture checks for the OptSem-C artifact package."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ImportEdge:
    source: str
    target: str
    kind: str

    def as_row(self) -> dict[str, str]:
        return {"source": self.source, "target": self.target, "kind": self.kind}


def module_name(path: Path, root: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    return ".".join(rel.parts)


def import_edges(package_dir: Path) -> tuple[ImportEdge, ...]:
    root = package_dir.parent
    edges: list[ImportEdge] = []
    for path in sorted(package_dir.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        src = module_name(path, root)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("optsemc"):
                        edges.append(ImportEdge(src, alias.name, "import"))
            elif isinstance(node, ast.ImportFrom):
                if node.module is None:
                    continue
                if node.level:
                    base_parts = src.split(".")[:-node.level]
                    target = ".".join(base_parts + ([node.module] if node.module else []))
                else:
                    target = node.module
                if target.startswith("optsemc"):
                    edges.append(ImportEdge(src, target, "from"))
    return tuple(edges)


def internal_adjacency(edges: Iterable[ImportEdge], modules: Iterable[str]) -> dict[str, set[str]]:
    module_set = set(modules)
    adj = {m: set() for m in module_set}
    for edge in edges:
        target = edge.target
        if target in module_set:
            adj.setdefault(edge.source, set()).add(target)
    return adj


def strongly_connected_components(adj: dict[str, set[str]]) -> list[tuple[str, ...]]:
    index = 0
    stack: list[str] = []
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    on_stack: set[str] = set()
    sccs: list[tuple[str, ...]] = []

    def visit(v: str) -> None:
        nonlocal index
        indices[v] = index
        low[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in adj.get(v, set()):
            if w not in indices:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            comp: list[str] = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            if len(comp) > 1:
                sccs.append(tuple(sorted(comp)))
    for node in sorted(adj):
        if node not in indices:
            visit(node)
    return sccs


def has_module_docstring(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return ast.get_docstring(tree) is not None
