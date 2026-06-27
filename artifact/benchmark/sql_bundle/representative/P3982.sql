-- OptSemBench-C probe P3982
-- features: adaptivity_trigger=skew, aggregation=none, connector_capability=not_applicable, control_surface=not_materialized_hint, distribution_trigger=skewed, join_shape=none, join_type=none, order_limit=none, predicate_class=none, reuse_structure=single_cte, source_boundary=local, statistics_need=low
WITH cte AS NOT MATERIALIZED (SELECT custkey, COUNT(*) AS n FROM orders GROUP BY custkey)
SELECT c1.custkey FROM cte c1 JOIN cte c2 ON c1.custkey = c2.custkey WHERE c1.n > 1;
