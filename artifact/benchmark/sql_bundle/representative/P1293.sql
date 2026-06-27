-- OptSemBench-C probe P1293
-- features: adaptivity_trigger=none, aggregation=group_by, connector_capability=not_applicable, control_surface=none_control, distribution_trigger=none, join_shape=none, join_type=none, order_limit=none, predicate_class=simple, reuse_structure=nested_view, source_boundary=local, statistics_need=low
SELECT d1.nationkey, COUNT(*)
FROM customer d1
WHERE d1.flag = 1 GROUP BY 1;
