---
title: マイグレーションで制約を安全に追加する
impact: HIGH
impactDescription: マイグレーション失敗を防ぎ、冪等なスキーマ変更を実現
tags: constraints, migrations, schema, alter-table
---

## マイグレーションで制約を安全に追加する

PostgreSQL は `ADD CONSTRAINT IF NOT EXISTS` をサポートしていません。この構文を使うマイグレーションは失敗します。

**誤り（構文エラーを引き起こす）:**

```sql
-- ERROR: syntax error at or near "not" (SQLSTATE 42601)
alter table public.profiles
add constraint if not exists profiles_birthchart_id_unique unique (birthchart_id);
```

**正しい例（冪等な制約作成）:**

```sql
-- Use DO block to check before adding
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'profiles_birthchart_id_unique'
    and conrelid = 'public.profiles'::regclass
  ) then
    alter table public.profiles
    add constraint profiles_birthchart_id_unique unique (birthchart_id);
  end if;
end $$;
```

すべての制約種別に適用可能:

```sql
-- Check constraints
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'check_age_positive'
  ) then
    alter table users add constraint check_age_positive check (age > 0);
  end if;
end $$;

-- Foreign keys
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'profiles_birthchart_id_fkey'
  ) then
    alter table profiles
    add constraint profiles_birthchart_id_fkey
    foreign key (birthchart_id) references birthcharts(id);
  end if;
end $$;
```

制約の存在確認:

```sql
-- Query to check constraint existence
select conname, contype, pg_get_constraintdef(oid)
from pg_constraint
where conrelid = 'public.profiles'::regclass;

-- contype values:
-- 'p' = PRIMARY KEY
-- 'f' = FOREIGN KEY
-- 'u' = UNIQUE
-- 'c' = CHECK
```

Reference: [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
