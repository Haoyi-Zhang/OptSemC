-- OptSemBench-C probe P2575
-- features: adaptivity_trigger=none, aggregation=none, connector_capability=not_applicable, control_surface=none_control, distribution_trigger=none, join_shape=none, join_type=none, order_limit=none, predicate_class=conjunctive, reuse_structure=none, source_boundary=local, statistics_need=medium
SELECT custkey, name
FROM customer d1
WHERE d1.flag = 1;
