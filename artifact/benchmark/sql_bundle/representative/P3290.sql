-- OptSemBench-C probe P3290
-- features: adaptivity_trigger=none, aggregation=none, connector_capability=not_applicable, control_surface=trino_join_distribution_partitioned, distribution_trigger=none, join_shape=binary, join_type=semi, order_limit=none, predicate_class=none, reuse_structure=none, source_boundary=local, statistics_need=unavailable
SELECT d1.custkey, f.orderkey
FROM customer d1 JOIN orders f ON d1.custkey = f.custkey;
