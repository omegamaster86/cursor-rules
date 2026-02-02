---
title: WHERE/JOIN 列にインデックスを付ける
impact: CRITICAL
impactDescription: 大規模テーブルでクエリが 100-1000x 高速化
tags: indexes, performance, sequential-scan, query-optimization
---

## WHERE/JOIN 列にインデックスを付ける

インデックスのない列でフィルタや結合を行うと全表スキャンになり、テーブルが大きくなるほど遅くなります。

**Incorrect (大きなテーブルの順次スキャン):**

```sql
-- customer_id にインデックスがなく全表スキャン
select * from orders where customer_id = 123;

-- EXPLAIN: Seq Scan on orders (cost=0.00..25000.00 rows=100 width=85)
```

**Correct (インデックススキャン):**

```sql
-- よくフィルタする列にインデックスを作成
create index orders_customer_id_idx on orders (customer_id);

select * from orders where customer_id = 123;

-- EXPLAIN: Index Scan using orders_customer_id_idx (cost=0.42..8.44 rows=100 width=85)
```

JOIN 列は外部キー側に必ずインデックス:

```sql
-- 参照側の列にインデックス
create index orders_customer_id_idx on orders (customer_id);

select c.name, o.total
from customers c
join orders o on o.customer_id = c.id;
```

Reference: [Query Optimization](https://supabase.com/docs/guides/database/query-optimization)
