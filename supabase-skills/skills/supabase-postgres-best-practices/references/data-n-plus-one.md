---
title: バッチロードで N+1 クエリを解消する
impact: MEDIUM-HIGH
impactDescription: DB 往復を 10-100x 削減
tags: n-plus-one, batch, performance, queries
---

## バッチロードで N+1 クエリを解消する

N+1 クエリはループ内でアイテムごとに 1 クエリを実行します。配列や JOIN で 1 クエリにまとめてください。

**Incorrect (N+1 クエリ):**

```sql
-- まず全ユーザーを取得
select id from users where active = true;  -- 100 件の ID が返る

-- その後、ユーザーごとに N 回クエリ
select * from orders where user_id = 1;
select * from orders where user_id = 2;
select * from orders where user_id = 3;
-- ... さらに 97 件

-- 合計: DB への往復 101 回
```

**Correct (単一のバッチクエリ):**

```sql
-- ID をまとめて ANY で 1 回
select * from orders where user_id = any(array[1, 2, 3, ...]);

-- もしくはループではなく JOIN
select u.id, u.name, o.*
from users u
left join orders o on o.user_id = u.id
where u.active = true;

-- 合計: 往復 1 回
```

アプリ側のパターン:

```sql
-- アプリコードでループしない:
-- for user in users: db.query("SELECT * FROM orders WHERE user_id = $1", user.id)

-- 配列パラメータを渡す:
select * from orders where user_id = any($1::bigint[]);
-- アプリ側: [1, 2, 3, 4, 5, ...]
```

Reference: [N+1 Query Problem](https://supabase.com/docs/guides/database/query-optimization)
