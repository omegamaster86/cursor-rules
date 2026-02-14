---
title: 外部キー列にインデックスを作る
impact: HIGH
impactDescription: JOIN と CASCADE 操作を 10-100 倍高速化
tags: foreign-key, indexes, joins, schema
---

## 外部キー列にインデックスを作る

Postgres は外部キー列に自動でインデックスを作成しません。未設定だと JOIN や CASCADE が遅くなります。

**誤り（外部キーにインデックスなし）:**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- No index on customer_id!
-- JOINs and ON DELETE CASCADE both require full table scan
select * from orders where customer_id = 123;  -- Seq Scan
delete from customers where id = 123;          -- Locks table, scans all orders
```

**正しい例（外部キーにインデックスあり）:**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- Always index the FK column
create index orders_customer_id_idx on orders (customer_id);

-- Now JOINs and cascades are fast
select * from orders where customer_id = 123;  -- Index Scan
delete from customers where id = 123;          -- Uses index, fast cascade
```

不足している FK インデックスを検出:

```sql
select
  conrelid::regclass as table_name,
  a.attname as fk_column
from pg_constraint c
join pg_attribute a on a.attrelid = c.conrelid and a.attnum = any(c.conkey)
where c.contype = 'f'
  and not exists (
    select 1 from pg_index i
    where i.indrelid = c.conrelid and a.attnum = any(i.indkey)
  );
```

Reference: [Foreign Keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
