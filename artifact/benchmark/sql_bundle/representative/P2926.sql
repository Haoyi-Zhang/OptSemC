-- OptSemBench-C probe P2926
-- features: adaptivity_trigger=none, aggregation=none, connector_capability=not_applicable, control_surface=pg_enable_memoize_off, distribution_trigger=none, join_shape=none, join_type=none, order_limit=none, predicate_class=disjunctive, reuse_structure=none, source_boundary=local, statistics_need=low
SELECT custkey, name
FROM customer d1
WHERE (d1.flag = 1 OR d1.region = 'EU');
