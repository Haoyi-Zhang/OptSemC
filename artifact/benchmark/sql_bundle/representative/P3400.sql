-- OptSemBench-C probe P3400
-- features: adaptivity_trigger=none, aggregation=none, connector_capability=supports_join_pushdown, control_surface=none_control, distribution_trigger=none, join_shape=binary, join_type=inner, order_limit=none, predicate_class=none, reuse_structure=none, source_boundary=same_connector, statistics_need=high
SELECT d1.custkey, f.orderkey
FROM remote_pg.customer d1 JOIN remote_pg.orders f ON d1.custkey = f.custkey;
