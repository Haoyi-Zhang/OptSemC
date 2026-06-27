"""Claim-to-evidence graph utilities for paper-code drift prevention.

A reader should be able to ask: every important claim in the paper is backed
by which computed files, which gate validates those files, and which upstream
source objects feed the computation?  This module builds a lightweight directed
artifact graph and reports reachability, missing gates, and minimal gate covers.
"""
from __future__ import annotations

import csv
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from .io import read_csv


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    kind: str
    label: str
    path: str = ""

    def as_row(self) -> dict[str, str]:
        return {"node_id": self.node_id, "kind": self.kind, "label": self.label, "path": self.path}


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    relation: str

    def as_row(self) -> dict[str, str]:
        return {"source": self.source, "target": self.target, "relation": self.relation}


@dataclass(frozen=True)
class ClaimGraph:
    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]

    @property
    def by_id(self) -> dict[str, GraphNode]:
        return {node.node_id: node for node in self.nodes}

    @property
    def outgoing(self) -> dict[str, list[GraphEdge]]:
        out: dict[str, list[GraphEdge]] = defaultdict(list)
        for edge in self.edges:
            out[edge.source].append(edge)
        return out

    @property
    def incoming(self) -> dict[str, list[GraphEdge]]:
        inc: dict[str, list[GraphEdge]] = defaultdict(list)
        for edge in self.edges:
            inc[edge.target].append(edge)
        return inc

    def reachable(self, start: str, *, kinds: set[str] | None = None) -> tuple[str, ...]:
        out = self.outgoing
        seen = {start}
        q = deque([start])
        reached: list[str] = []
        by_id = self.by_id
        while q:
            current = q.popleft()
            for edge in out.get(current, []):
                if edge.target in seen:
                    continue
                seen.add(edge.target)
                node = by_id.get(edge.target)
                if node and (kinds is None or node.kind in kinds):
                    reached.append(edge.target)
                q.append(edge.target)
        return tuple(sorted(reached))

    def claims(self) -> tuple[GraphNode, ...]:
        return tuple(node for node in self.nodes if node.kind == "claim")

    def gates(self) -> tuple[GraphNode, ...]:
        return tuple(node for node in self.nodes if node.kind == "gate")

    def files(self) -> tuple[GraphNode, ...]:
        return tuple(node for node in self.nodes if node.kind == "file")


def _node_id(prefix: str, label: str) -> str:
    safe = "".join(ch if ch.isalnum() else "_" for ch in label).strip("_")
    while "__" in safe:
        safe = safe.replace("__", "_")
    return f"{prefix}:{safe[:96]}"


def _claim_path_candidates(row: Mapping[str, str]) -> list[str]:
    candidates: list[str] = []
    for key in ("source_file", "generated_file", "evidence", "file", "path", "artifact_path", "artifact_support", "support"):
        value = row.get(key, "")
        if value:
            for piece in str(value).replace(";", "|").split("|"):
                piece = piece.strip()
                if piece and ("/" in piece or piece.endswith((".csv", ".json", ".jsonl", ".yaml", ".tex"))):
                    candidates.append(piece)
    return candidates


def _read_if_exists(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        return read_csv(path)
    except Exception:
        return []


def build_claim_graph(root: Path) -> ClaimGraph:
    evaluation = root / "artifact" / "evaluation"
    nodes: dict[str, GraphNode] = {}
    edges: list[GraphEdge] = []

    def add_node(node: GraphNode) -> None:
        nodes.setdefault(node.node_id, node)

    def add_file(path: str) -> str:
        fid = _node_id("file", path)
        add_node(GraphNode(fid, "file", path, path))
        return fid

    def add_gate(name: str, path: str) -> str:
        gid = _node_id("gate", name)
        add_node(GraphNode(gid, "gate", name, path))
        return gid

    def resolve_support_path(piece: str) -> list[str]:
        piece = piece.strip()
        if not piece:
            return []
        prefixes = ("artifact/", "Paper/", ".github/")
        patterns: list[str] = []
        if piece.startswith(prefixes):
            patterns.append(piece)
        elif "/" in piece:
            patterns.append("artifact/" + piece)
            patterns.append(piece)
        else:
            patterns.extend([
                "artifact/evaluation/" + piece,
                "artifact/evaluation/grounded/" + piece,
                "artifact/grounded/" + piece,
                "artifact/benchmark/" + piece,
                "artifact/" + piece,
                piece,
            ])
        resolved: list[str] = []
        for pattern in patterns:
            if "*" in pattern:
                resolved.extend(match.relative_to(root).as_posix() for match in sorted(root.glob(pattern)) if match.is_file())
            else:
                candidate = root / pattern
                if candidate.exists():
                    resolved.append(candidate.relative_to(root).as_posix())
        if not resolved and "/" not in piece and "*" not in piece:
            resolved.extend(match.relative_to(root).as_posix() for match in sorted(root.rglob(piece)) if match.is_file() and ".git" not in match.parts)
        if resolved:
            return sorted(dict.fromkeys(resolved))
        # Preserve unresolved labels so the graph check exposes drift rather than
        # silently dropping a claimed evidence target.
        if piece.startswith(prefixes):
            return [piece]
        return ["artifact/" + piece]

    def add_support_edges(source_id: str, raw_value: str, relation: str = "supported_by") -> None:
        for piece in str(raw_value).replace(";", "|").split("|"):
            piece = piece.strip()
            if not piece:
                continue
            if not ("/" in piece or "*" in piece or piece.endswith((".csv", ".json", ".jsonl", ".yaml", ".yml", ".tex"))):
                continue
            for path in resolve_support_path(piece):
                edges.append(GraphEdge(source_id, add_file(path), relation))

    # Paper claim ledger: explicit claim rows.
    for i, row in enumerate(_read_if_exists(evaluation / "paper_claim_ledger.csv"), 1):
        label = row.get("paper_claim", "") or row.get("claim", "") or row.get("claim_id", "") or f"claim_{i}"
        cid = _node_id("claim", row.get("claim_id", label))
        add_node(GraphNode(cid, "claim", label))
        for key in ("artifact_support", "source_file", "generated_file", "evidence", "file", "path", "artifact_path"):
            if row.get(key):
                add_support_edges(cid, row[key])
        edges.append(GraphEdge(cid, add_gate(f"claim_row_{i}_checked", "artifact/evaluation/claim_ledger_check.csv"), "checked_by"))

    # Theorem ledger: formal claims with executable evidence files.
    for i, row in enumerate(_read_if_exists(evaluation / "theorem_ledger.csv"), 1):
        label = row.get("theorem_or_claim", "") or row.get("theorem", "") or row.get("obligation", "") or f"theorem_{i}"
        cid = _node_id("claim", f"theorem:{label}")
        add_node(GraphNode(cid, "claim", label))
        for key in ("support", "evidence", "checker", "artifact"):
            if row.get(key):
                add_support_edges(cid, row[key])
        edges.append(GraphEdge(cid, add_gate(f"theorem_row_{i}_checked", "artifact/evaluation/theorem_ledger.csv"), "checked_by"))

    # Registry: every registered artifact should be produced by at least one gate.
    registry = _read_if_exists(evaluation / "artifact_registry.csv")
    for row in registry:
        path = row.get("path", "") or row.get("artifact", "")
        check = row.get("check", "") or row.get("producer", "") or row.get("category", "")
        if not path:
            continue
        for resolved in resolve_support_path(path):
            fid = add_file(resolved)
            if check:
                gid = add_gate(check, resolved)
                edges.append(GraphEdge(gid, fid, "produces"))

    # Grounded roots: make provenance/source support explicit.
    root_files = [
        "artifact/grounded/verified_rules.jsonl",
        "artifact/grounded/verified_segments.jsonl",
        "artifact/grounded/verified_sources.csv",
        "artifact/benchmark/generated_probes.jsonl",
        "artifact/evaluation/grounded_contract_maps.jsonl",
    ]
    for path in root_files:
        root_node = _node_id("root", path)
        add_node(GraphNode(root_node, "root", path, path))
        add_file(path)
        edges.append(GraphEdge(root_node, _node_id("file", path), "materializes"))

    return ClaimGraph(tuple(sorted(nodes.values(), key=lambda n: n.node_id)), tuple(sorted(edges, key=lambda e: (e.source, e.target, e.relation))))

def graph_metrics(graph: ClaimGraph, root: Path | None = None) -> list[dict[str, str]]:
    by_id = graph.by_id
    claim_rows: list[dict[str, str]] = []
    for claim in graph.claims():
        files = graph.reachable(claim.node_id, kinds={"file"})
        gates = graph.reachable(claim.node_id, kinds={"gate"})
        existing = 0
        if root is not None:
            existing = sum(1 for fid in files if (root / by_id[fid].path).exists())
        else:
            existing = len(files)
        claim_rows.append({
            "claim_id": claim.node_id,
            "claim": claim.label,
            "supporting_files": str(len(files)),
            "existing_supporting_files": str(existing),
            "checking_gates": str(len(gates)),
            "passed": str(len(files) > 0 and existing == len(files) and len(gates) > 0).lower(),
        })
    return claim_rows


def graph_summary(graph: ClaimGraph, root: Path | None = None) -> list[dict[str, str]]:
    claim_rows = graph_metrics(graph, root)
    files = graph.files()
    existing_files = len(files)
    if root is not None:
        existing_files = sum(1 for file in files if (root / file.path).exists())
    gates = graph.gates()
    return [
        {"metric": "nodes", "value": str(len(graph.nodes))},
        {"metric": "edges", "value": str(len(graph.edges))},
        {"metric": "claims", "value": str(len(graph.claims()))},
        {"metric": "claim_rows_passed", "value": str(sum(row["passed"] == "true" for row in claim_rows))},
        {"metric": "files", "value": str(len(files))},
        {"metric": "existing_files", "value": str(existing_files)},
        {"metric": "gates", "value": str(len(gates))},
    ]


def gate_cover_rows(graph: ClaimGraph) -> list[dict[str, str]]:
    """Return a small greedy gate cover for claim support obligations."""
    claim_to_gates = {claim.node_id: set(graph.reachable(claim.node_id, kinds={"gate"})) for claim in graph.claims()}
    uncovered = {claim for claim, gates in claim_to_gates.items() if gates}
    chosen: list[str] = []
    while uncovered:
        counts: dict[str, int] = defaultdict(int)
        for claim in uncovered:
            for gate in claim_to_gates[claim]:
                counts[gate] += 1
        best = max(counts, key=lambda key: (counts[key], key))
        chosen.append(best)
        uncovered = {claim for claim in uncovered if best not in claim_to_gates[claim]}
    by_id = graph.by_id
    rows: list[dict[str, str]] = []
    for rank, gate in enumerate(chosen, 1):
        covered = sum(1 for claim, gates in claim_to_gates.items() if gate in gates)
        node = by_id[gate]
        rows.append({"rank": str(rank), "gate_id": gate, "gate": node.label, "path": node.path, "claims_covered": str(covered)})
    return rows
