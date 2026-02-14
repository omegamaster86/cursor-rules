---
title: 一貫したロック順序でデッドロックを防ぐ
impact: MEDIUM-HIGH
impactDescription: デッドロックエラーを排除し、信頼性を向上
tags: deadlocks, locking, transactions, ordering
---

## 一貫したロック順序でデッドロックを防ぐ

トランザクションが異なる順序でリソースをロックするとデッドロックが発生します。常に同じ順序でロックを取得します。

**誤り（ロック順序が不一致）:**

```sql
-- Transaction A                    -- Transaction B
begin;                              begin;
update accounts                     update accounts
set balance = balance - 100         set balance = balance - 50
where id = 1;                       where id = 2;  -- B locks row 2

update accounts                     update accounts
set balance = balance + 100         set balance = balance + 50
where id = 2;  -- A waits for B     where id = 1;  -- B waits for A

-- DEADLOCK! Both waiting for each other
```

**正しい例（先に同一順でロック取得）:**

```sql
-- Explicitly acquire locks in ID order before updating
begin;
select * from accounts where id in (1, 2) order by id for update;

-- Now perform updates in any order - locks already held
update accounts set balance = balance - 100 where id = 1;
update accounts set balance = balance + 100 where id = 2;
commit;
```

別案: 単一文で原子的に更新:

```sql
-- Single statement acquires all locks atomically
begin;
update accounts
set balance = balance + case id
  when 1 then -100
  when 2 then 100
end
where id in (1, 2);
commit;
```

ログからデッドロックを検出:

```sql
-- Check for recent deadlocks
select * from pg_stat_database where deadlocks > 0;

-- Enable deadlock logging
set log_lock_waits = on;
set deadlock_timeout = '1s';
```

Reference:
[Deadlocks](https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-DEADLOCKS)
