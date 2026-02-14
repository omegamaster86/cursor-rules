---
title: INSERT または UPDATE には UPSERT を使う
impact: MEDIUM
impactDescription: 原子的操作で競合状態を排除
tags: upsert, on-conflict, insert, update
---

## INSERT または UPDATE には UPSERT を使う

SELECT のあとに INSERT/UPDATE を分けると競合状態が起きます。`INSERT ... ON CONFLICT` により原子的に処理します。

**誤り（チェックしてから INSERT する競合）:**

```sql
-- Race condition: two requests check simultaneously
select * from settings where user_id = 123 and key = 'theme';
-- Both find nothing

-- Both try to insert
insert into settings (user_id, key, value) values (123, 'theme', 'dark');
-- One succeeds, one fails with duplicate key error!
```

**正しい例（原子的 UPSERT）:**

```sql
-- Single atomic operation
insert into settings (user_id, key, value)
values (123, 'theme', 'dark')
on conflict (user_id, key)
do update set value = excluded.value, updated_at = now();

-- Returns the inserted/updated row
insert into settings (user_id, key, value)
values (123, 'theme', 'dark')
on conflict (user_id, key)
do update set value = excluded.value
returning *;
```

Insert-or-ignore パターン:

```sql
-- Insert only if not exists (no update)
insert into page_views (page_id, user_id)
values (1, 123)
on conflict (page_id, user_id) do nothing;
```

Reference: [INSERT ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT)
