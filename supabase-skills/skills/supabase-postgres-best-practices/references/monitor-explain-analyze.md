---
title: 低速クエリの診断に EXPLAIN ANALYZE を使う
impact: LOW-MEDIUM
impactDescription: クエリ実行のボトルネックを特定
tags: explain, analyze, diagnostics, query-plan
---

## 低速クエリの診断に EXPLAIN ANALYZE を使う

EXPLAIN ANALYZE はクエリを実行し、実測時間を表示します。実際のボトルネックが分かります。

**Incorrect (推測で判断):**

```sql
-- クエリが遅いが理由が不明
select * from orders where customer_id = 123 and status = 'pending';
-- "インデックスが足りないはず" でもどれ？
```

**Correct (EXPLAIN ANALYZE を使う):**

```sql
explain (analyze, buffers, format text)
select * from orders where customer_id = 123 and status = 'pending';

-- 出力が原因を示す:
-- Seq Scan on orders (cost=0.00..25000.00 rows=50 width=100) (actual time=0.015..450.123 rows=50 loops=1)
--   Filter: ((customer_id = 123) AND (status = 'pending'::text))
--   Rows Removed by Filter: 999950
--   Buffers: shared hit=5000 read=15000
-- Planning Time: 0.150 ms
-- Execution Time: 450.500 ms
```

注目ポイント:

```sql
-- 大規模テーブルの Seq Scan = インデックス不足
-- Rows Removed by Filter = 選択性が低い/インデックス不足
-- Buffers: read >> hit = キャッシュ不足、メモリ拡張が必要
-- Nested Loop の loops が多い = JOIN 戦略の見直し
-- Sort Method: external merge = work_mem が小さい
```

Reference: [EXPLAIN](https://supabase.com/docs/guides/database/inspect)
