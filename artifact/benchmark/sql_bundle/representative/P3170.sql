-- OptSemBench-C probe P3170
-- features: adaptivity_trigger=none, aggregation=none, connector_capability=not_applicable, control_surface=spark_aqe_disabled, distribution_trigger=none, join_shape=snowflake, join_type=inner, order_limit=none, predicate_class=none, reuse_structure=none, source_boundary=local, statistics_need=low
SELECT f.key, d1.attr, d2.attr, SUM(f.measure)
FROM fact f JOIN dim1 d1 ON f.k1=d1.k JOIN dim2 d2 ON f.k2=d2.k;
