"""SQL-skeleton normalization and lightweight query-shape diagnostics."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Mapping, Sequence

SQL_KEYWORDS = ("select", "from", "where", "join", "group by", "order by", "limit", "with", "union", "intersect", "except")
JOIN_RE = re.compile(r"\bjoin\b", re.I)
WHERE_RE = re.compile(r"\bwhere\b", re.I)
GROUP_RE = re.compile(r"\bgroup\s+by\b", re.I)
ORDER_RE = re.compile(r"\border\s+by\b", re.I)
LIMIT_RE = re.compile(r"\blimit\b", re.I)
CTE_RE = re.compile(r"^\s*with\b", re.I)


@dataclass(frozen=True)
class QueryShape:
    has_join: bool
    join_count: int
    has_filter: bool
    has_group: bool
    has_order: bool
    has_limit: bool
    has_cte: bool
    token_count: int

    def as_row(self, probe_id: str) -> dict[str, str]:
        return {"probe_id": probe_id, "has_join": str(self.has_join).lower(), "join_count": str(self.join_count), "has_filter": str(self.has_filter).lower(), "has_group": str(self.has_group).lower(), "has_order": str(self.has_order).lower(), "has_limit": str(self.has_limit).lower(), "has_cte": str(self.has_cte).lower(), "token_count": str(self.token_count)}


def normalize_sql(sql: str) -> str:
    return re.sub(r"\s+", " ", sql.strip()).lower()


def sql_hash(sql: str) -> str:
    return hashlib.sha256(normalize_sql(sql).encode("utf-8")).hexdigest()


def query_shape(sql: str) -> QueryShape:
    norm = normalize_sql(sql)
    return QueryShape(bool(JOIN_RE.search(norm)), len(JOIN_RE.findall(norm)), bool(WHERE_RE.search(norm)), bool(GROUP_RE.search(norm)), bool(ORDER_RE.search(norm)), bool(LIMIT_RE.search(norm)), bool(CTE_RE.search(norm)), len(norm.split()))


def shape_consistent_with_features(sql: str, features: Mapping[str, str]) -> tuple[bool, tuple[str, ...]]:
    shape = query_shape(sql)
    issues = []
    if features.get("join_type") not in {None, "none"} and not shape.has_join:
        issues.append("feature declares join but SQL has no JOIN")
    if features.get("aggregation") not in {None, "none", "distinct"} and not shape.has_group:
        issues.append("feature declares grouped aggregation but SQL has no GROUP BY")
    if features.get("order_limit") in {"order_by", "topn", "window_order"} and not shape.has_order:
        issues.append("feature declares ordering but SQL has no ORDER BY")
    if features.get("order_limit") in {"limit", "topn"} and not shape.has_limit:
        issues.append("feature declares limit/topn but SQL has no LIMIT")
    return not issues, tuple(issues)


def shape_rows(probes: Sequence[object]) -> list[dict[str, str]]:
    rows = []
    for probe in probes:
        rows.append(query_shape(probe.sql_skeleton).as_row(probe.probe_id))
    return rows


def sql_keyword_profile(sql: str) -> dict[str, str]:
    norm = normalize_sql(sql)
    return {keyword.replace(" ", "_"): str(keyword in norm).lower() for keyword in SQL_KEYWORDS}

