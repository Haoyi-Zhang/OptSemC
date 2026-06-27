-- OptSemBench-C probe P0963
-- features: adaptivity_trigger=none, aggregation=distinct, connector_capability=not_applicable, control_surface=pg_enable_hashagg_off, distribution_trigger=none, join_shape=none, join_type=none, order_limit=none, predicate_class=none, reuse_structure=single_cte, source_boundary=local, statistics_need=low
SELECT DISTINCT custkey, name
FROM customer d1;
