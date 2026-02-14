---
title: RLS ポリシーを性能面で最適化する
impact: HIGH
impactDescription: 適切なパターンで RLS クエリを 5-10 倍高速化
tags: rls, performance, security, optimization
---

## RLS ポリシーを性能面で最適化する

不適切な RLS ポリシーは深刻な性能問題を引き起こします。サブクエリとインデックスを戦略的に使います。

**誤り（関数が行ごとに呼ばれる）:**

```sql
create policy orders_policy on orders
  using (auth.uid() = user_id);  -- auth.uid() called per row!

-- With 1M rows, auth.uid() is called 1M times
```

**正しい例（関数を SELECT でラップ）:**

```sql
create policy orders_policy on orders
  using ((select auth.uid()) = user_id);  -- Called once, cached

-- 100x+ faster on large tables
```

複雑な判定には security definer 関数を使う:

```sql
-- Create helper function (runs as definer, bypasses RLS)
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

-- Use in policy (indexed lookup, not per-row check)
create policy team_orders_policy on orders
  using ((select is_team_member(team_id)));
```

RLS ポリシーで使う列には必ずインデックスを追加:

```sql
create index orders_user_id_idx on orders (user_id);
```

Reference: [RLS Performance](https://supabase.com/docs/guides/database/postgres/row-level-security#rls-performance-recommendations)
