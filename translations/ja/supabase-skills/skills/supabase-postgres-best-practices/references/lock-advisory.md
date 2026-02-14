---
title: アプリケーションレベルのロックには Advisory Lock を使う
impact: MEDIUM
impactDescription: 行ロックのオーバーヘッドなしで効率的に調停
tags: advisory-locks, coordination, application-locks
---

## アプリケーションレベルのロックには Advisory Lock を使う

Advisory Lock は、実テーブルの行をロックせずにアプリ側の排他制御を行えます。

**誤り（ロック専用行を作る）:**

```sql
-- Creating dummy rows to lock on
create table resource_locks (
  resource_name text primary key
);

insert into resource_locks values ('report_generator');

-- Lock by selecting the row
select * from resource_locks where resource_name = 'report_generator' for update;
```

**正しい例（Advisory Lock）:**

```sql
-- Session-level advisory lock (released on disconnect or unlock)
select pg_advisory_lock(hashtext('report_generator'));
-- ... do exclusive work ...
select pg_advisory_unlock(hashtext('report_generator'));

-- Transaction-level lock (released on commit/rollback)
begin;
select pg_advisory_xact_lock(hashtext('daily_report'));
-- ... do work ...
commit;  -- Lock automatically released
```

非ブロッキングの try-lock:

```sql
-- Returns immediately with true/false instead of waiting
select pg_try_advisory_lock(hashtext('resource_name'));

-- Use in application
if (acquired) {
  -- Do work
  select pg_advisory_unlock(hashtext('resource_name'));
} else {
  -- Skip or retry later
}
```

Reference: [Advisory Locks](https://www.postgresql.org/docs/current/explicit-locking.html#ADVISORY-LOCKS)
