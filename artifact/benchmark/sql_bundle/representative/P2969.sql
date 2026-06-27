-- OptSemBench-C probe P2969
-- features: adaptivity_trigger=none, aggregation=none, connector_capability=not_applicable, control_surface=pg_enable_mergejoin_off, distribution_trigger=none, join_shape=none, join_type=none, order_limit=none, predicate_class=udf, reuse_structure=none, source_boundary=local, statistics_need=low
SELECT custkey, name
FROM customer d1
WHERE expensive_udf(d1.comment) = TRUE;
