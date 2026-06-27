#!/usr/bin/env python3
from optsemc.statistics import mean, variance, stddev, quantile, wilson, cohen_h, deterministic_sample, stratified_counts

def test_statistics_case_1_1():
    values = [float(x) for x in range(1, 6)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_2():
    values = [float(x) for x in range(1, 7)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_3():
    values = [float(x) for x in range(1, 8)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_4():
    values = [float(x) for x in range(1, 9)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_5():
    values = [float(x) for x in range(1, 10)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_6():
    values = [float(x) for x in range(1, 11)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_7():
    values = [float(x) for x in range(1, 12)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_8():
    values = [float(x) for x in range(1, 13)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_9():
    values = [float(x) for x in range(1, 5)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_10():
    values = [float(x) for x in range(1, 6)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_11():
    values = [float(x) for x in range(1, 7)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_12():
    values = [float(x) for x in range(1, 8)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_13():
    values = [float(x) for x in range(1, 9)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_14():
    values = [float(x) for x in range(1, 10)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_15():
    values = [float(x) for x in range(1, 11)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_16():
    values = [float(x) for x in range(1, 12)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_17():
    values = [float(x) for x in range(1, 13)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_18():
    values = [float(x) for x in range(1, 5)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_19():
    values = [float(x) for x in range(1, 6)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_20():
    values = [float(x) for x in range(1, 7)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_21():
    values = [float(x) for x in range(1, 8)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_22():
    values = [float(x) for x in range(1, 9)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_23():
    values = [float(x) for x in range(1, 10)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_24():
    values = [float(x) for x in range(1, 11)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_25():
    values = [float(x) for x in range(1, 12)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_26():
    values = [float(x) for x in range(1, 13)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_27():
    values = [float(x) for x in range(1, 5)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_28():
    values = [float(x) for x in range(1, 6)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_29():
    values = [float(x) for x in range(1, 7)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_30():
    values = [float(x) for x in range(1, 8)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_31():
    values = [float(x) for x in range(1, 9)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_32():
    values = [float(x) for x in range(1, 10)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_33():
    values = [float(x) for x in range(1, 11)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_34():
    values = [float(x) for x in range(1, 12)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_35():
    values = [float(x) for x in range(1, 13)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_36():
    values = [float(x) for x in range(1, 5)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_37():
    values = [float(x) for x in range(1, 6)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_38():
    values = [float(x) for x in range(1, 7)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_39():
    values = [float(x) for x in range(1, 8)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_40():
    values = [float(x) for x in range(1, 9)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_41():
    values = [float(x) for x in range(1, 10)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_42():
    values = [float(x) for x in range(1, 11)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_43():
    values = [float(x) for x in range(1, 12)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

def test_statistics_case_1_44():
    values = [float(x) for x in range(1, 13)]
    assert mean(values) > 0
    assert variance(values) >= 0
    assert stddev(values) >= 0
    assert min(values) <= quantile(values, 0.5) <= max(values)
    ci = wilson(1, 2)
    assert 0 <= ci.lower <= ci.estimate <= ci.upper <= 1
    sample = deterministic_sample(tuple(range(10)), 3, seed=1)
    assert len(sample) == 3

