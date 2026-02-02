---
title: マルチテナントデータでは行レベルセキュリティを有効化する
impact: CRITICAL
impactDescription: DB でテナント分離を強制し、データ漏洩を防ぐ
tags: rls, row-level-security, multi-tenant, security
---

## マルチテナントデータでは行レベルセキュリティを有効化する

Row Level Security（RLS）は DB レベルでアクセス制御を行い、ユーザーが自分のデータだけを見るよう保証します。

**Incorrect (アプリ側のフィルタに依存):**

```sql
-- アプリだけでフィルタ
select * from orders where user_id = $current_user_id;

-- バグや回避で全データが露出!
select * from orders;  -- 全注文が返る
```

**Correct (DB で RLS を強制):**

```sql
-- テーブルで RLS を有効化
alter table orders enable row level security;

-- ユーザーが自分の注文だけ見られるポリシー
create policy orders_user_policy on orders
  for all
  using (user_id = current_setting('app.current_user_id')::bigint);

-- テーブル所有者にも RLS を強制
alter table orders force row level security;

-- ユーザー文脈を設定してクエリ
set app.current_user_id = '123';
select * from orders;  -- ユーザー 123 の注文だけが返る
```

認証ロール向けポリシー:

```sql
create policy orders_user_policy on orders
  for all
  to authenticated
  using (user_id = auth.uid());
```

Reference: [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
