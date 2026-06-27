-- OptSemBench-C probe P3708
-- features: adaptivity_trigger=none, aggregation=none, connector_capability=supports_topn_pushdown, control_surface=none_control, distribution_trigger=none, join_shape=binary, join_type=inner, order_limit=topn, predicate_class=correlated, reuse_structure=none, source_boundary=cross_connector, statistics_need=low
SELECT d1.custkey, f.orderkey
FROM remote_pg.customer d1 JOIN hive.orders f ON d1.custkey = f.custkey
WHERE f.custkey IN (SELECT x.custkey FROM aux x WHERE x.custkey = f.custkey)
ORDER BY 1 LIMIT 10;
