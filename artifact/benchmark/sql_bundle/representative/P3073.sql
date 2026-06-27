-- OptSemBench-C probe P3073
-- features: adaptivity_trigger=none, aggregation=none, connector_capability=not_applicable, control_surface=pg_join_collapse_1, distribution_trigger=none, join_shape=none, join_type=none, order_limit=window_order, predicate_class=none, reuse_structure=none, source_boundary=local, statistics_need=low
SELECT *, ROW_NUMBER() OVER (ORDER BY 1) AS rn FROM (SELECT custkey, name
FROM customer d1) s;
