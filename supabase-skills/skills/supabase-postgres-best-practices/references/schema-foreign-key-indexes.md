---
title: 外部キー列にインデックスを付ける
impact: HIGH
impactDescription: JOIN と CASCADE が 10-100x 高速化
tags: foreign-key, indexes, joins, schema
---

## 外部キー列にインデックスを付ける

Postgres は外部キー列に自動でインデックスを作りません。欠落すると JOIN や CASCADE が遅くなります。

**Incorrect (外部キーにインデックスがない):**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- customer_id にインデックスがない
-- JOIN と ON DELETE CASCADE が全表スキャンになる
select * from orders where customer_id = 123;  -- Seq Scan
delete from customers where id = 123;          -- テーブルロック＋全件スキャン
```

**Correct (外部キーにインデックスを付ける):**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- 外部キー列には必ずインデックス
create index orders_customer_id_idx on orders (customer_id);

-- JOIN とカスケードが高速に
select * from orders where customer_id = 123;  -- Index Scan
delete from customers where id = 123;          -- インデックス使用で高速
```

外部キーのインデックス不足を検出:

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
