---
title: バッチロードで N+1 クエリを解消する
impact: MEDIUM-HIGH
impactDescription: データベース往復回数を 10-100 倍削減
tags: n-plus-one, batch, performance, queries
---

## バッチロードで N+1 クエリを解消する

N+1 クエリはループ内で 1 件ずつ問い合わせます。配列や JOIN を使って 1 クエリにまとめます。

**誤り（N+1 クエリ）:**

```sql
-- First query: get all users
select id from users where active = true;  -- Returns 100 IDs

-- Then N queries, one per user
select * from orders where user_id = 1;
select * from orders where user_id = 2;
select * from orders where user_id = 3;
-- ... 97 more queries!

-- Total: 101 round trips to database
```

**正しい例（単一のバッチクエリ）:**

```sql
-- Collect IDs and query once with ANY
select * from orders where user_id = any(array[1, 2, 3, ...]);

-- Or use JOIN instead of loop
select u.id, u.name, o.*
from users u
left join orders o on o.user_id = u.id
where u.active = true;

-- Total: 1 round trip
```

アプリ側パターン:

```sql
-- Instead of looping in application code:
-- for user in users: db.query("SELECT * FROM orders WHERE user_id = $1", user.id)

-- Pass array parameter:
select * from orders where user_id = any($1::bigint[]);
-- Application passes: [1, 2, 3, 4, 5, ...]
```

Reference: [N+1 Query Problem](https://supabase.com/docs/guides/database/query-optimization)
