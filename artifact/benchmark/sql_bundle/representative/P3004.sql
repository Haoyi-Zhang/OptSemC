-- OptSemBench-C probe P3004
-- features: adaptivity_trigger=none, aggregation=none, connector_capability=not_applicable, control_surface=pg_enable_nestloop_off, distribution_trigger=none, join_shape=none, join_type=none, order_limit=order_by, predicate_class=none, reuse_structure=none, source_boundary=local, statistics_need=low
SELECT custkey, name
FROM customer d1
ORDER BY 1;
