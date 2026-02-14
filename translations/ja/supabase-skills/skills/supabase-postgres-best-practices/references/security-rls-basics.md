---
title: マルチテナントデータでは Row Level Security を有効化する
impact: CRITICAL
impactDescription: DB 強制のテナント分離でデータ漏えいを防止
tags: rls, row-level-security, multi-tenant, security
---

## マルチテナントデータでは Row Level Security を有効化する

Row Level Security（RLS）は DB レベルでアクセス制御を行い、ユーザーが自分のデータだけを見られるようにします。

**誤り（アプリ側フィルタのみ）:**

```sql
-- Relying only on application to filter
select * from orders where user_id = $current_user_id;

-- Bug or bypass means all data is exposed!
select * from orders;  -- Returns ALL orders
```

**正しい例（DB 強制 RLS）:**

```sql
-- Enable RLS on the table
alter table orders enable row level security;

-- Create policy for users to see only their orders
create policy orders_user_policy on orders
  for all
  using (user_id = current_setting('app.current_user_id')::bigint);

-- Force RLS even for table owners
alter table orders force row level security;

-- Set user context and query
set app.current_user_id = '123';
select * from orders;  -- Only returns orders for user 123
```

authenticated ロール向けポリシー:

```sql
create policy orders_user_policy on orders
  for all
  to authenticated
  using (user_id = auth.uid());
```

Reference: [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
