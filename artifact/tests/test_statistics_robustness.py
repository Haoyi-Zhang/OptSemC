#!/usr/bin/env python3
from optsemc.statistics import mean, variance, stddev, quantile, wilson, cohen_h, deterministic_sample, stratified_counts

def test_statistics_case_2_1():
    values = [float(x) for x in range(1, 6)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_2():
    values = [float(x) for x in range(1, 7)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_3():
    values = [float(x) for x in range(1, 8)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_4():
    values = [float(x) for x in range(1, 9)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_5():
    values = [float(x) for x in range(1, 10)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_6():
    values = [float(x) for x in range(1, 11)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_7():
    values = [float(x) for x in range(1, 12)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_8():
    values = [float(x) for x in range(1, 13)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_9():
    values = [float(x) for x in range(1, 5)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_10():
    values = [float(x) for x in range(1, 6)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_11():
    values = [float(x) for x in range(1, 7)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_12():
    values = [float(x) for x in range(1, 8)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_13():
    values = [float(x) for x in range(1, 9)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_14():
    values = [float(x) for x in range(1, 10)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_15():
    values = [float(x) for x in range(1, 11)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_16():
    values = [float(x) for x in range(1, 12)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_17():
    values = [float(x) for x in range(1, 13)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_18():
    values = [float(x) for x in range(1, 5)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_19():
    values = [float(x) for x in range(1, 6)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_20():
    values = [float(x) for x in range(1, 7)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_21():
    values = [float(x) for x in range(1, 8)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_22():
    values = [float(x) for x in range(1, 9)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_23():
    values = [float(x) for x in range(1, 10)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_24():
    values = [float(x) for x in range(1, 11)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_25():
    values = [float(x) for x in range(1, 12)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_26():
    values = [float(x) for x in range(1, 13)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_27():
    values = [float(x) for x in range(1, 5)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_28():
    values = [float(x) for x in range(1, 6)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_29():
    values = [float(x) for x in range(1, 7)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_30():
    values = [float(x) for x in range(1, 8)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_31():
    values = [float(x) for x in range(1, 9)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_32():
    values = [float(x) for x in range(1, 10)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_33():
    values = [float(x) for x in range(1, 11)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_34():
    values = [float(x) for x in range(1, 12)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_35():
    values = [float(x) for x in range(1, 13)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_36():
    values = [float(x) for x in range(1, 5)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_37():
    values = [float(x) for x in range(1, 6)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_38():
    values = [float(x) for x in range(1, 7)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_39():
    values = [float(x) for x in range(1, 8)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_40():
    values = [float(x) for x in range(1, 9)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_41():
    values = [float(x) for x in range(1, 10)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_42():
    values = [float(x) for x in range(1, 11)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_43():
    values = [float(x) for x in range(1, 12)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_2_44():
    values = [float(x) for x in range(1, 13)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

