"""Exact and greedy finite minimization routines used by repository checks."""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Callable, FrozenSet, Hashable, Iterable, Mapping, Sequence, TypeVar

T = TypeVar("T", bound=Hashable)
S = TypeVar("S", bound=Hashable)


@dataclass(frozen=True)
class SetCoverSolution:
    universe_size: int
    selected: tuple[S, ...]
    covered: frozenset[T]
    optimal: bool

    @property
    def uncovered(self) -> int:
        return self.universe_size - len(self.covered)

    @property
    def cardinality(self) -> int:
        return len(self.selected)

    def as_row(self) -> dict[str, str]:
        return {"universe_size": str(self.universe_size), "selected": "+".join(map(str, self.selected)), "covered": str(len(self.covered)), "uncovered": str(self.uncovered), "optimal": str(self.optimal).lower()}


def greedy_set_cover(universe: Iterable[T], sets: Mapping[S, Iterable[T]]) -> SetCoverSolution[T, S]:
    remaining = set(universe)
    chosen: list[S] = []
    covered: set[T] = set()
    normalized = {key: set(value) for key, value in sets.items()}
    while remaining:
        best = None
        best_gain: set[T] = set()
        for key, value in normalized.items():
            if key in chosen:
                continue
            gain = value & remaining
            if len(gain) > len(best_gain) or (len(gain) == len(best_gain) and str(key) < str(best)):
                best = key; best_gain = gain
        if best is None or not best_gain:
            break
        chosen.append(best)
        covered.update(best_gain)
        remaining -= best_gain
    return SetCoverSolution(len(set(universe)), tuple(chosen), frozenset(covered), False)


def exact_set_cover(universe: Iterable[T], sets: Mapping[S, Iterable[T]], *, max_width: int | None = None) -> SetCoverSolution[T, S]:
    universe_set = set(universe)
    normalized = {key: set(value) for key, value in sets.items()}
    keys = tuple(sorted(normalized, key=str))
    width = len(keys) if max_width is None else min(max_width, len(keys))
    for size in range(width + 1):
        for combo in itertools.combinations(keys, size):
            covered = set().union(*(normalized[key] for key in combo)) if combo else set()
            if universe_set.issubset(covered):
                return SetCoverSolution(len(universe_set), tuple(combo), frozenset(covered), True)
    greedy = greedy_set_cover(universe_set, normalized)
    return SetCoverSolution(greedy.universe_size, greedy.selected, greedy.covered, False)


def exact_hitting_set(families: Sequence[Iterable[S]], universe: Sequence[S]) -> tuple[tuple[S, ...], ...]:
    fam = [set(item) for item in families]
    ordered = tuple(sorted(universe, key=str))
    if not fam:
        return (tuple(),)
    for size in range(1, len(ordered) + 1):
        result = []
        for combo in itertools.combinations(ordered, size):
            chosen = set(combo)
            if all(chosen & item for item in fam):
                result.append(combo)
        if result:
            return tuple(result)
    return tuple()


def greedy_hitting_set(families: Sequence[Iterable[S]], universe: Sequence[S]) -> tuple[S, ...]:
    remaining = [set(item) for item in families]
    chosen: list[S] = []
    universe_set = set(universe)
    while remaining:
        best = max(universe_set - set(chosen), key=lambda x: (sum(1 for family in remaining if x in family), str(x)), default=None)
        if best is None:
            break
        chosen.append(best)
        remaining = [family for family in remaining if best not in family]
    return tuple(chosen)


def delta_minimize(items: Sequence[T], predicate: Callable[[tuple[T, ...]], bool]) -> tuple[T, ...]:
    current = tuple(items)
    changed = True
    while changed:
        changed = False
        for item in list(current):
            candidate = tuple(x for x in current if x != item)
            if predicate(candidate):
                current = candidate
                changed = True
                break
    return current


def pareto_frontier(rows: Iterable[Mapping[str, float]], minimize: Sequence[str], maximize: Sequence[str] = ()) -> list[Mapping[str, float]]:
    values = list(rows)
    frontier = []
    for row in values:
        dominated = False
        for other in values:
            if other is row:
                continue
            no_worse = all(float(other[f]) <= float(row[f]) for f in minimize) and all(float(other[f]) >= float(row[f]) for f in maximize)
            strictly = any(float(other[f]) < float(row[f]) for f in minimize) or any(float(other[f]) > float(row[f]) for f in maximize)
            if no_worse and strictly:
                dominated = True
                break
        if not dominated:
            frontier.append(row)
    return frontier


def minimal_by_inclusion(items: Iterable[Iterable[S]]) -> tuple[tuple[S, ...], ...]:
    sets = [set(item) for item in items]
    result = []
    for item in sets:
        if not any(other < item for other in sets):
            result.append(tuple(sorted(item, key=str)))
    return tuple(sorted(set(result), key=lambda x: (len(x), x)))


def maximal_by_inclusion(items: Iterable[Iterable[S]]) -> tuple[tuple[S, ...], ...]:
    sets = [set(item) for item in items]
    result = []
    for item in sets:
        if not any(item < other for other in sets):
            result.append(tuple(sorted(item, key=str)))
    return tuple(sorted(set(result), key=lambda x: (len(x), x)))

