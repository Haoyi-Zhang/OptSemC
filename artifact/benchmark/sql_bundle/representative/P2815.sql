-- OptSemBench-C probe P2815
-- features: adaptivity_trigger=none, aggregation=none, connector_capability=not_applicable, control_surface=pg_enable_incremental_sort_off, distribution_trigger=none, join_shape=binary, join_type=outer, order_limit=none, predicate_class=none, reuse_structure=none, source_boundary=local, statistics_need=unavailable
SELECT d1.custkey, f.orderkey
FROM customer d1 JOIN orders f ON d1.custkey = f.custkey;
