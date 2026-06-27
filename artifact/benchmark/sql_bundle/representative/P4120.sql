-- OptSemBench-C probe P4120
-- features: adaptivity_trigger=stage_boundary, aggregation=none, connector_capability=not_applicable, control_surface=materialized_hint, distribution_trigger=shuffle, join_shape=none, join_type=none, order_limit=none, predicate_class=none, reuse_structure=single_cte, source_boundary=local, statistics_need=low
WITH cte AS MATERIALIZED (SELECT custkey, COUNT(*) AS n FROM orders GROUP BY custkey)
SELECT c1.custkey FROM cte c1 JOIN cte c2 ON c1.custkey = c2.custkey WHERE c1.n > 1;
