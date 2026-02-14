---
title: テーブル参照を避けるためカバリングインデックスを使う
impact: MEDIUM-HIGH
impactDescription: ヒープフェッチ排除でクエリを 2-5 倍高速化
tags: indexes, covering-index, include, index-only-scan
---

## テーブル参照を避けるためカバリングインデックスを使う

カバリングインデックスはクエリに必要な列をすべて含み、テーブル本体を読まない index-only scan を可能にします。

**誤り（インデックス走査 + ヒープフェッチ）:**

```sql
create index users_email_idx on users (email);

-- Must fetch name and created_at from table heap
select email, name, created_at from users where email = 'user@example.com';
```

**正しい例（INCLUDE を使う index-only scan）:**

```sql
-- Include non-searchable columns in the index
create index users_email_idx on users (email) include (name, created_at);

-- All columns served from index, no table access needed
select email, name, created_at from users where email = 'user@example.com';
```

INCLUDE は、絞り込みには使わないが SELECT で必要な列に使います:

```sql
-- Searching by status, but also need customer_id and total
create index orders_status_idx on orders (status) include (customer_id, total);

select status, customer_id, total from orders where status = 'shipped';
```

Reference: [Index-Only Scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
