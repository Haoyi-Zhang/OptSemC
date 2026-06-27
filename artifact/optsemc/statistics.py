"""Deterministic statistical helpers for artifact diagnostics."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable, Iterable, Sequence


@dataclass(frozen=True)
class Interval:
    lower: float
    estimate: float
    upper: float

    def as_row(self, metric: str) -> dict[str, str]:
        return {"metric": metric, "lower": f"{self.lower:.6f}", "estimate": f"{self.estimate:.6f}", "upper": f"{self.upper:.6f}"}


def mean(values: Iterable[float]) -> float:
    seq = list(values)
    return sum(seq) / len(seq) if seq else 0.0


def variance(values: Iterable[float], *, sample: bool = True) -> float:
    seq = list(values)
    if len(seq) <= (1 if sample else 0):
        return 0.0
    m = mean(seq)
    denom = len(seq) - 1 if sample else len(seq)
    return sum((x - m) ** 2 for x in seq) / denom


def stddev(values: Iterable[float], *, sample: bool = True) -> float:
    return math.sqrt(variance(values, sample=sample))


def quantile(values: Sequence[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos); hi = math.ceil(pos)
    if lo == hi:
        return ordered[int(pos)]
    return ordered[lo] * (hi - pos) + ordered[hi] * (pos - lo)


def percentile_interval(values: Sequence[float], lower: float = 0.025, upper: float = 0.975) -> Interval:
    return Interval(quantile(values, lower), mean(values), quantile(values, upper))


def bootstrap_interval(values: Sequence[float], statistic: Callable[[Sequence[float]], float] = lambda xs: mean(xs), *, iterations: int = 1000, seed: int = 0) -> Interval:
    if not values:
        return Interval(0.0, 0.0, 0.0)
    rng = random.Random(seed)
    samples = []
    n = len(values)
    for _ in range(iterations):
        draw = [values[rng.randrange(n)] for _ in range(n)]
        samples.append(statistic(draw))
    return Interval(quantile(samples, 0.025), statistic(values), quantile(samples, 0.975))


def jackknife_interval(values: Sequence[float], statistic: Callable[[Sequence[float]], float] = lambda xs: mean(xs), z: float = 1.96) -> Interval:
    n = len(values)
    if n <= 1:
        est = statistic(values) if values else 0.0
        return Interval(est, est, est)
    leave_one = [statistic(values[:i] + values[i + 1:]) for i in range(n)]
    est = statistic(values)
    se = math.sqrt((n - 1) / n * sum((x - mean(leave_one)) ** 2 for x in leave_one))
    return Interval(est - z * se, est, est + z * se)


def wilson(successes: int, trials: int, z: float = 1.96) -> Interval:
    if trials == 0:
        return Interval(0.0, 0.0, 0.0)
    p = successes / trials
    denom = 1 + z * z / trials
    centre = (p + z * z / (2 * trials)) / denom
    spread = z * math.sqrt((p * (1 - p) + z * z / (4 * trials)) / trials) / denom
    return Interval(max(0.0, centre - spread), p, min(1.0, centre + spread))


def cohen_h(p1: float, p2: float) -> float:
    return 2 * (math.asin(math.sqrt(p1)) - math.asin(math.sqrt(p2)))


def odds_ratio(a: int, b: int, c: int, d: int, correction: float = 0.5) -> float:
    aa, bb, cc, dd = a + correction, b + correction, c + correction, d + correction
    return (aa * dd) / (bb * cc)


def deterministic_sample(items: Sequence[object], k: int, seed: int = 0) -> list[object]:
    rng = random.Random(seed)
    if k >= len(items):
        return list(items)
    indices = sorted(rng.sample(range(len(items)), k))
    return [items[i] for i in indices]


def stratified_counts(labels: Sequence[str]) -> list[dict[str, str]]:
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    total = sum(counts.values())
    return [{"label": key, "count": str(count), "share": f"{count/total if total else 0.0:.6f}"} for key, count in sorted(counts.items())]

