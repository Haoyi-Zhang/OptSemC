-- OptSemBench-C probe P4057
-- features: adaptivity_trigger=stage_boundary, aggregation=none, connector_capability=not_applicable, control_surface=clickhouse_join_algorithm_full_sorting_merge, distribution_trigger=shuffle, join_shape=binary, join_type=inner, order_limit=none, predicate_class=none, reuse_structure=none, source_boundary=local, statistics_need=low
SELECT d1.custkey, f.orderkey
FROM customer d1 JOIN orders f ON d1.custkey = f.custkey;
