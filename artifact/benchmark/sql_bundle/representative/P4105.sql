-- OptSemBench-C probe P4105
-- features: adaptivity_trigger=stage_boundary, aggregation=none, connector_capability=not_applicable, control_surface=explain_analyze, distribution_trigger=shuffle, join_shape=none, join_type=none, order_limit=none, predicate_class=none, reuse_structure=none, source_boundary=local, statistics_need=low
SELECT custkey, name
FROM customer d1;
