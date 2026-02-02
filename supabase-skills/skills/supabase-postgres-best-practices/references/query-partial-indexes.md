---
title: フィルタ付きクエリには部分インデックスを使う
impact: HIGH
impactDescription: インデックスが 5-20x 小さくなり、書き込み/クエリが高速化
tags: indexes, partial-index, query-optimization, storage
---

## フィルタ付きクエリには部分インデックスを使う

部分インデックスは WHERE 条件に一致する行だけを含むため、同じ条件で常にフィルタするクエリに対して小さく高速になります。

**Incorrect (無関係な行まで含むフルインデックス):**

```sql
-- インデックスが全行を含む（論理削除も含む）
create index users_email_idx on users (email);

-- クエリは常にアクティブユーザーのみ
select * from users where email = 'user@example.com' and deleted_at is null;
```

**Correct (クエリ条件に一致する部分インデックス):**

```sql
-- アクティブユーザーのみを含む
create index users_active_email_idx on users (email)
where deleted_at is null;

-- 小さく速いインデックスが使われる
select * from users where email = 'user@example.com' and deleted_at is null;
```

部分インデックスのよくある用途:

```sql
-- 未処理の注文のみ（完了後はほぼ変更されない）
create index orders_pending_idx on orders (created_at)
where status = 'pending';

-- NULL 以外だけ
create index products_sku_idx on products (sku)
where sku is not null;
```

Reference: [Partial Indexes](https://www.postgresql.org/docs/current/indexes-partial.html)
