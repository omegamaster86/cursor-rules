---
title: 遅いクエリ診断に EXPLAIN ANALYZE を使う
impact: LOW-MEDIUM
impactDescription: クエリ実行の正確なボトルネックを特定
tags: explain, analyze, diagnostics, query-plan
---

## 遅いクエリ診断に EXPLAIN ANALYZE を使う

EXPLAIN ANALYZE はクエリを実行し、実測時間を表示します。真の性能ボトルネックを把握できます。

**誤り（性能問題を推測で判断）:**

```sql
-- Query is slow, but why?
select * from orders where customer_id = 123 and status = 'pending';
-- "It must be missing an index" - but which one?
```

**正しい例（EXPLAIN ANALYZE を使う）:**

```sql
explain (analyze, buffers, format text)
select * from orders where customer_id = 123 and status = 'pending';

-- Output reveals the issue:
-- Seq Scan on orders (cost=0.00..25000.00 rows=50 width=100) (actual time=0.015..450.123 rows=50 loops=1)
--   Filter: ((customer_id = 123) AND (status = 'pending'::text))
--   Rows Removed by Filter: 999950
--   Buffers: shared hit=5000 read=15000
-- Planning Time: 0.150 ms
-- Execution Time: 450.500 ms
```

注目ポイント:

```sql
-- Seq Scan on large tables = missing index
-- Rows Removed by Filter = poor selectivity or missing index
-- Buffers: read >> hit = data not cached, needs more memory
-- Nested Loop with high loops = consider different join strategy
-- Sort Method: external merge = work_mem too low
```

Reference: [EXPLAIN](https://supabase.com/docs/guides/database/inspect)
