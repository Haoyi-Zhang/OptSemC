-- OptSemBench-C probe P1535
-- features: adaptivity_trigger=none, aggregation=group_by_after_join, connector_capability=not_applicable, control_surface=spark_shuffle_replicate_nl_hint, distribution_trigger=none, join_shape=binary, join_type=inner, order_limit=none, predicate_class=none, reuse_structure=reused_cte, source_boundary=local, statistics_need=low
WITH cte AS (SELECT custkey, COUNT(*) AS n FROM orders GROUP BY custkey)
SELECT c1.custkey FROM cte c1 JOIN cte c2 ON c1.custkey = c2.custkey WHERE c1.n > 1;
