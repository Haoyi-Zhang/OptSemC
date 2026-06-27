-- OptSemBench-C probe P1190
-- features: adaptivity_trigger=none, aggregation=expression_aggregate, connector_capability=supports_aggregate_pushdown, control_surface=none_control, distribution_trigger=none, join_shape=binary, join_type=inner, order_limit=none, predicate_class=none, reuse_structure=none, source_boundary=cross_connector, statistics_need=low
SELECT d1.nationkey, SUM(d1.acctbal * 1.08)
FROM remote_pg.customer d1 JOIN hive.orders f ON d1.custkey = f.custkey GROUP BY d1.nationkey;
