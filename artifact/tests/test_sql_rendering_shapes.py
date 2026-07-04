from optsemc.sql_render import (
    normalize_sql,
    query_shape,
    shape_consistent_with_features,
    sql_hash,
    sql_keyword_profile,
)


def test_normalize_sql_and_hash_are_whitespace_stable():
    left = " SELECT *\nFROM a WHERE x > 1 "
    right = "select * from a where x > 1"
    assert normalize_sql(left) == right
    assert sql_hash(left) == sql_hash(right)


def test_query_shape_detects_core_sql_features():
    shape = query_shape(
        "WITH q AS (SELECT * FROM a) "
        "SELECT b.k, COUNT(*) FROM q JOIN b ON q.k=b.k "
        "WHERE b.x > 1 GROUP BY b.k ORDER BY b.k LIMIT 5"
    )
    assert shape.has_cte
    assert shape.has_join and shape.join_count == 1
    assert shape.has_filter
    assert shape.has_group
    assert shape.has_order
    assert shape.has_limit


def test_shape_consistency_accepts_declared_features():
    ok, issues = shape_consistent_with_features(
        "SELECT a.k, COUNT(*) FROM a JOIN b ON a.k=b.k GROUP BY a.k ORDER BY a.k LIMIT 10",
        {"join_type": "inner", "aggregation": "group_by", "order_limit": "topn"},
    )
    assert ok
    assert issues == ()


def test_shape_consistency_reports_missing_join_group_and_limit():
    ok, issues = shape_consistent_with_features(
        "SELECT k FROM a ORDER BY k",
        {"join_type": "inner", "aggregation": "group_by", "order_limit": "topn"},
    )
    assert not ok
    assert "feature declares join but SQL has no JOIN" in issues
    assert "feature declares grouped aggregation but SQL has no GROUP BY" in issues
    assert "feature declares limit/topn but SQL has no LIMIT" in issues


def test_sql_keyword_profile_uses_stable_keys():
    profile = sql_keyword_profile("SELECT * FROM a ORDER BY k LIMIT 3")
    assert profile["select"] == "true"
    assert profile["order_by"] == "true"
    assert profile["limit"] == "true"
    assert profile["join"] == "false"
