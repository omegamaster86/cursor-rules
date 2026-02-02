---
title: Insert-or-Update には UPSERT を使う
impact: MEDIUM
impactDescription: 原子的な操作で競合を排除
tags: upsert, on-conflict, insert, update
---

## Insert-or-Update には UPSERT を使う

SELECT の後に INSERT/UPDATE を別々に行うと競合が起きます。原子操作の INSERT ... ON CONFLICT を使ってください。

**Incorrect (チェック→挿入の競合):**

```sql
-- 競合: 2 つのリクエストが同時に確認
select * from settings where user_id = 123 and key = 'theme';
-- どちらも見つからない

-- どちらも挿入を試行
insert into settings (user_id, key, value) values (123, 'theme', 'dark');
-- 一方は成功、一方は重複キーエラーで失敗
```

**Correct (原子的な UPSERT):**

```sql
-- 単一の原子操作
insert into settings (user_id, key, value)
values (123, 'theme', 'dark')
on conflict (user_id, key)
do update set value = excluded.value, updated_at = now();

-- 挿入/更新された行を返す
insert into settings (user_id, key, value)
values (123, 'theme', 'dark')
on conflict (user_id, key)
do update set value = excluded.value
returning *;
```

Insert-or-ignore パターン:

```sql
-- 既存なら挿入しない（更新もしない）
insert into page_views (page_id, user_id)
values (1, 123)
on conflict (page_id, user_id) do nothing;
```

Reference: [INSERT ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT)
