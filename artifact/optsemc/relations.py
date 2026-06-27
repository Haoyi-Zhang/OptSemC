"""Finite relation algebra for optimizer-contract comparisons."""
from __future__ import annotations

import itertools
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Hashable, Iterable, Mapping, Sequence, TypeVar

T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class Relation:
    """A finite binary relation over hashable objects."""

    nodes: tuple[T, ...]
    edges: frozenset[tuple[T, T]]

    @classmethod
    def empty(cls, nodes: Iterable[T]) -> "Relation[T]":
        return cls(tuple(sorted(set(nodes), key=str)), frozenset())

    @classmethod
    def identity(cls, nodes: Iterable[T]) -> "Relation[T]":
        ordered = tuple(sorted(set(nodes), key=str))
        return cls(ordered, frozenset((node, node) for node in ordered))

    @classmethod
    def complete(cls, nodes: Iterable[T]) -> "Relation[T]":
        ordered = tuple(sorted(set(nodes), key=str))
        return cls(ordered, frozenset(itertools.product(ordered, repeat=2)))

    def contains(self, left: T, right: T) -> bool:
        return (left, right) in self.edges

    def with_edge(self, left: T, right: T) -> "Relation[T]":
        nodes = tuple(sorted(set(self.nodes) | {left, right}, key=str))
        return Relation(nodes, frozenset(set(self.edges) | {(left, right)}))

    def union(self, other: "Relation[T]") -> "Relation[T]":
        return Relation(tuple(sorted(set(self.nodes) | set(other.nodes), key=str)), self.edges | other.edges)

    def intersection(self, other: "Relation[T]") -> "Relation[T]":
        return Relation(tuple(sorted(set(self.nodes) | set(other.nodes), key=str)), self.edges & other.edges)

    def difference(self, other: "Relation[T]") -> "Relation[T]":
        return Relation(self.nodes, frozenset(edge for edge in self.edges if edge not in other.edges))

    def converse(self) -> "Relation[T]":
        return Relation(self.nodes, frozenset((b, a) for a, b in self.edges))

    def compose(self, other: "Relation[T]") -> "Relation[T]":
        right_by_left: dict[T, set[T]] = defaultdict(set)
        for a, b in other.edges:
            right_by_left[a].add(b)
        composed = set()
        for a, b in self.edges:
            for c in right_by_left.get(b, set()):
                composed.add((a, c))
        return Relation(tuple(sorted(set(self.nodes) | set(other.nodes), key=str)), frozenset(composed))

    def is_reflexive(self) -> bool:
        return all((node, node) in self.edges for node in self.nodes)

    def is_symmetric(self) -> bool:
        return all((b, a) in self.edges for a, b in self.edges)

    def is_transitive(self) -> bool:
        edge_set = set(self.edges)
        for a, b in edge_set:
            for c, d in edge_set:
                if b == c and (a, d) not in edge_set:
                    return False
        return True

    def is_equivalence(self) -> bool:
        return self.is_reflexive() and self.is_symmetric() and self.is_transitive()

    def equivalence_classes(self) -> tuple[tuple[T, ...], ...]:
        if not self.is_equivalence():
            raise ValueError("equivalence_classes requires an equivalence relation")
        seen: set[T] = set()
        classes = []
        for node in self.nodes:
            if node in seen:
                continue
            cls = tuple(sorted((other for other in self.nodes if (node, other) in self.edges), key=str))
            seen.update(cls)
            classes.append(cls)
        return tuple(classes)

    def density(self) -> float:
        denom = len(self.nodes) * len(self.nodes)
        return len(self.edges) / denom if denom else 0.0


def equivalence_relation(items: Iterable[T], key: Callable[[T], Hashable]) -> Relation[T]:
    ordered = tuple(sorted(set(items), key=str))
    buckets: dict[Hashable, list[T]] = defaultdict(list)
    for item in ordered:
        buckets[key(item)].append(item)
    edges = set()
    for bucket in buckets.values():
        for left, right in itertools.product(bucket, repeat=2):
            edges.add((left, right))
    return Relation(ordered, frozenset(edges))


def partition_refines(fine: Sequence[Sequence[T]], coarse: Sequence[Sequence[T]]) -> bool:
    coarse_owner: dict[T, int] = {}
    for idx, block in enumerate(coarse):
        for item in block:
            coarse_owner[item] = idx
    for block in fine:
        owners = {coarse_owner.get(item) for item in block}
        if len(owners) > 1:
            return False
    return True


def quotient_map(items: Iterable[T], key: Callable[[T], Hashable]) -> dict[Hashable, tuple[T, ...]]:
    buckets: dict[Hashable, list[T]] = defaultdict(list)
    for item in items:
        buckets[key(item)].append(item)
    return {k: tuple(sorted(v, key=str)) for k, v in sorted(buckets.items(), key=lambda kv: str(kv[0]))}


def quotient_statistics(items: Iterable[T], exact_key: Callable[[T], Hashable], projected_key: Callable[[T], Hashable]) -> dict[str, str]:
    values = tuple(items)
    exact = quotient_map(values, exact_key)
    projected = quotient_map(values, projected_key)
    nontrivial = 0
    false_classes = 0
    max_class = 0
    for block in projected.values():
        max_class = max(max_class, len(block))
        exact_values = {exact_key(item) for item in block}
        if len(block) > 1:
            nontrivial += 1
        if len(exact_values) > 1:
            false_classes += 1
    return {
        "items": str(len(values)),
        "exact_classes": str(len(exact)),
        "projected_classes": str(len(projected)),
        "nontrivial_projected_classes": str(nontrivial),
        "false_projected_classes": str(false_classes),
        "max_projected_class_size": str(max_class),
    }


def transitive_closure(relation: Relation[T]) -> Relation[T]:
    closure = set(relation.edges)
    changed = True
    while changed:
        changed = False
        new_edges = set(closure)
        for a, b in closure:
            for c, d in closure:
                if b == c and (a, d) not in new_edges:
                    new_edges.add((a, d)); changed = True
        closure = new_edges
    return Relation(relation.nodes, frozenset(closure))


def symmetric_closure(relation: Relation[T]) -> Relation[T]:
    return relation.union(relation.converse())


def reflexive_closure(relation: Relation[T]) -> Relation[T]:
    return relation.union(Relation.identity(relation.nodes))


def equivalence_closure(relation: Relation[T]) -> Relation[T]:
    return transitive_closure(symmetric_closure(reflexive_closure(relation)))


def relation_summary(relation: Relation[T]) -> dict[str, str]:
    return {
        "nodes": str(len(relation.nodes)),
        "edges": str(len(relation.edges)),
        "density": f"{relation.density():.6f}",
        "reflexive": str(relation.is_reflexive()).lower(),
        "symmetric": str(relation.is_symmetric()).lower(),
        "transitive": str(relation.is_transitive()).lower(),
        "equivalence": str(relation.is_equivalence()).lower(),
    }

