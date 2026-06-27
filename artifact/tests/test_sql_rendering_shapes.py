#!/usr/bin/env python3
from optsemc.sql_render import normalize_sql, query_shape, shape_consistent_with_features, sql_keyword_profile

def test_sql_shape_case_1_1():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_2():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_3():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_4():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_5():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_6():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_7():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_8():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_9():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_10():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_11():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_12():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_13():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_14():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_15():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_16():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_17():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_18():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_19():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_20():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_21():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_22():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_23():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_24():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_25():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_26():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_27():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_28():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_29():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_30():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_31():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_32():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_33():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_34():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_35():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_36():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_37():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_38():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_39():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_40():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_41():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_42():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_43():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_44():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_45():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_46():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_47():
    sql = 'SELECT * FROM a ORDER BY x LIMIT 10'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_48():
    sql = 'SELECT * FROM a JOIN b ON a.k=b.k WHERE a.x>1'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

def test_sql_shape_case_1_49():
    sql = 'WITH q AS (SELECT * FROM a) SELECT k, COUNT(*) FROM q GROUP BY k'
    norm = normalize_sql(sql)
    shape = query_shape(sql)
    profile = sql_keyword_profile(sql)
    assert norm
    assert shape.token_count >= 4
    assert "select" in profile
    ok, issues = shape_consistent_with_features(sql, {"join_type": "none", "aggregation": "none", "order_limit": "none"})
    assert isinstance(ok, bool)
    assert isinstance(issues, tuple)

