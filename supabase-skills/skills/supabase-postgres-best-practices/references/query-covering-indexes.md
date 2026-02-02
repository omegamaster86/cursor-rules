---
title: テーブル参照を避けるためにカバリングインデックスを使う
impact: MEDIUM-HIGH
impactDescription: ヒープフェッチを削減して 2-5x 高速化
tags: indexes, covering-index, include, index-only-scan
---

## テーブル参照を避けるためにカバリングインデックスを使う

カバリングインデックスはクエリに必要なすべての列を含み、テーブルを読まずに index-only scan を可能にします。

**Incorrect (インデックススキャン + ヒープフェッチ):**

```sql
create index users_email_idx on users (email);

-- name と created_at はテーブルから取得が必要
select email, name, created_at from users where email = 'user@example.com';
```

**Correct (INCLUDE 付き index-only scan):**

```sql
-- 検索に使わない列をインデックスに含める
create index users_email_idx on users (email) include (name, created_at);

-- すべての列をインデックスから返し、テーブルアクセス不要
select email, name, created_at from users where email = 'user@example.com';
```

検索対象ではないが SELECT に必要な列に INCLUDE を使う:

```sql
-- status で検索しつつ customer_id と total が必要
create index orders_status_idx on orders (status) include (customer_id, total);

select status, customer_id, total from orders where status = 'shipped';
```

Reference: [Index-Only Scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
