---
title: RLS ポリシーを性能最適化する
impact: HIGH
impactDescription: 適切なパターンで RLS クエリが 5-10x 高速化
tags: rls, performance, security, optimization
---

## RLS ポリシーを性能最適化する

RLS ポリシーの書き方が悪いと深刻な性能問題になります。サブクエリとインデックスを戦略的に使ってください。

**Incorrect (各行で関数を呼ぶ):**

```sql
create policy orders_policy on orders
  using (auth.uid() = user_id);  -- auth.uid() が各行で呼ばれる

-- 100 万行なら auth.uid() が 100 万回実行される
```

**Correct (SELECT でラップする):**

```sql
create policy orders_policy on orders
  using ((select auth.uid()) = user_id);  -- 1 回呼ばれキャッシュされる

-- 大規模テーブルで 100x+ 高速
```

複雑なチェックには security definer 関数を使う:

```sql
-- ヘルパー関数（definer 権限で実行、RLS をバイパス）
create or replace function is_team_member(team_id bigint)
returns boolean
language sql
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.team_members
    where team_id = $1 and user_id = (select auth.uid())
  );
$$;

-- ポリシーで使用（インデックス参照、行ごとチェックではない）
create policy team_orders_policy on orders
  using ((select is_team_member(team_id)));
```

RLS ポリシーで使う列には必ずインデックス:

```sql
create index orders_user_id_idx on orders (user_id);
```

Reference: [RLS Performance](https://supabase.com/docs/guides/database/postgres/row-level-security#rls-performance-recommendations)
