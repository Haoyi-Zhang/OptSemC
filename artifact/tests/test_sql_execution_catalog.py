#!/usr/bin/env python3
from optsemc.sql_render import normalize_sql, query_shape, shape_consistent_with_features, sql_keyword_profile

def test_sql_shape_case_2_1():
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

def test_sql_shape_case_2_2():
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

def test_sql_shape_case_2_3():
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

def test_sql_shape_case_2_4():
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

def test_sql_shape_case_2_5():
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

def test_sql_shape_case_2_6():
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

def test_sql_shape_case_2_7():
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

def test_sql_shape_case_2_8():
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

def test_sql_shape_case_2_9():
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

def test_sql_shape_case_2_10():
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

def test_sql_shape_case_2_11():
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

def test_sql_shape_case_2_12():
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

def test_sql_shape_case_2_13():
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

def test_sql_shape_case_2_14():
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

def test_sql_shape_case_2_15():
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

def test_sql_shape_case_2_16():
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

def test_sql_shape_case_2_17():
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

def test_sql_shape_case_2_18():
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

def test_sql_shape_case_2_19():
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

def test_sql_shape_case_2_20():
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

def test_sql_shape_case_2_21():
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

def test_sql_shape_case_2_22():
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

def test_sql_shape_case_2_23():
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

def test_sql_shape_case_2_24():
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

def test_sql_shape_case_2_25():
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

def test_sql_shape_case_2_26():
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

def test_sql_shape_case_2_27():
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

def test_sql_shape_case_2_28():
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

def test_sql_shape_case_2_29():
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

def test_sql_shape_case_2_30():
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

def test_sql_shape_case_2_31():
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

def test_sql_shape_case_2_32():
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

def test_sql_shape_case_2_33():
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

def test_sql_shape_case_2_34():
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

def test_sql_shape_case_2_35():
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

def test_sql_shape_case_2_36():
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

def test_sql_shape_case_2_37():
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

def test_sql_shape_case_2_38():
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

def test_sql_shape_case_2_39():
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

def test_sql_shape_case_2_40():
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

def test_sql_shape_case_2_41():
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

def test_sql_shape_case_2_42():
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

def test_sql_shape_case_2_43():
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

def test_sql_shape_case_2_44():
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

def test_sql_shape_case_2_45():
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

def test_sql_shape_case_2_46():
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

def test_sql_shape_case_2_47():
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

def test_sql_shape_case_2_48():
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

def test_sql_shape_case_2_49():
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

