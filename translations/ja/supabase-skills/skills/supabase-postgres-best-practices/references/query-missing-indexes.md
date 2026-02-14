---
title: WHERE と JOIN 列にインデックスを追加する
impact: CRITICAL
impactDescription: 大規模テーブルでクエリを 100-1000 倍高速化
tags: indexes, performance, sequential-scan, query-optimization
---

## WHERE と JOIN 列にインデックスを追加する

インデックスのない列でフィルタや結合を行うと全表走査になります。テーブルが大きくなるほど急激に遅くなります。

**誤り（大規模テーブルで sequential scan）:**

```sql
-- No index on customer_id causes full table scan
select * from orders where customer_id = 123;

-- EXPLAIN shows: Seq Scan on orders (cost=0.00..25000.00 rows=100 width=85)
```

**正しい例（index scan）:**

```sql
-- Create index on frequently filtered column
create index orders_customer_id_idx on orders (customer_id);

select * from orders where customer_id = 123;

-- EXPLAIN shows: Index Scan using orders_customer_id_idx (cost=0.42..8.44 rows=100 width=85)
```

JOIN 列では、常に外部キー側にインデックスを張ります:

```sql
-- Index the referencing column
create index orders_customer_id_idx on orders (customer_id);

select c.name, o.total
from customers c
join orders o on o.customer_id = c.id;
```

Reference: [Query Optimization](https://supabase.com/docs/guides/database/query-optimization)
