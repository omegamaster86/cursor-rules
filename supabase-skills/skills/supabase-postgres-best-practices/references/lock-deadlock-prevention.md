---
title: 一貫したロック順序でデッドロックを防ぐ
impact: MEDIUM-HIGH
impactDescription: デッドロックエラーを排除し、信頼性を向上
tags: deadlocks, locking, transactions, ordering
---

## 一貫したロック順序でデッドロックを防ぐ

デッドロックはトランザクションが異なる順序でリソースをロックすると発生します。常に一貫した順序でロックを取得してください。

**Incorrect (ロック順序が不一致):**

```sql
-- Transaction A                    -- Transaction B
begin;                              begin;
update accounts                     update accounts
set balance = balance - 100         set balance = balance - 50
where id = 1;                       where id = 2;  -- B が行 2 をロック

update accounts                     update accounts
set balance = balance + 100         set balance = balance + 50
where id = 2;  -- A が B を待つ     where id = 1;  -- B が A を待つ

-- DEADLOCK! お互いに待ち続ける
```

**Correct (先に行を一貫した順序でロック):**

```sql
-- ID 順で明示的にロック取得
begin;
select * from accounts where id in (1, 2) order by id for update;

-- すでにロック済みなので更新順は任意
update accounts set balance = balance - 100 where id = 1;
update accounts set balance = balance + 100 where id = 2;
commit;
```

代替: 単一ステートメントで原子的に更新:

```sql
-- 単一文で全ロックを原子的に取得
begin;
update accounts
set balance = balance + case id
  when 1 then -100
  when 2 then 100
end
where id in (1, 2);
commit;
```

ログでデッドロックを検出:

```sql
-- 直近のデッドロックを確認
select * from pg_stat_database where deadlocks > 0;

-- デッドロックログを有効化
set log_lock_waits = on;
set deadlock_timeout = '1s';
```

Reference:
[Deadlocks](https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-DEADLOCKS)
