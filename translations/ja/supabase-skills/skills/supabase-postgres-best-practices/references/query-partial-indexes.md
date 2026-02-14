---
title: フィルタ付きクエリには部分インデックスを使う
impact: HIGH
impactDescription: インデックスを 5-20 倍小さくし、書き込みと検索を高速化
tags: indexes, partial-index, query-optimization, storage
---

## フィルタ付きクエリには部分インデックスを使う

部分インデックスは WHERE 条件に合致する行だけを含みます。同じ条件で繰り返し絞り込むクエリで小さく高速になります。

**誤り（不要な行まで含む全体インデックス）:**

```sql
-- Index includes all rows, even soft-deleted ones
create index users_email_idx on users (email);

-- Query always filters active users
select * from users where email = 'user@example.com' and deleted_at is null;
```

**正しい例（クエリ条件に一致する部分インデックス）:**

```sql
-- Index only includes active users
create index users_active_email_idx on users (email)
where deleted_at is null;

-- Query uses the smaller, faster index
select * from users where email = 'user@example.com' and deleted_at is null;
```

部分インデックスの代表例:

```sql
-- Only pending orders (status rarely changes once completed)
create index orders_pending_idx on orders (created_at)
where status = 'pending';

-- Only non-null values
create index products_sku_idx on products (sku)
where sku is not null;
```

Reference: [Partial Indexes](https://www.postgresql.org/docs/current/indexes-partial.html)
