---
title: アプリレベルのロックにはアドバイザリロックを使う
impact: MEDIUM
impactDescription: 行ロックのオーバーヘッドなしで効率的に協調
tags: advisory-locks, coordination, application-locks
---

## アプリレベルのロックにはアドバイザリロックを使う

アドバイザリロックは、DB の行をロックせずにアプリ側の協調制御を提供します。

**Incorrect (ロックのための行を作成):**

```sql
-- ロック専用のダミー行を作成
create table resource_locks (
  resource_name text primary key
);

insert into resource_locks values ('report_generator');

-- 行を選択してロック
select * from resource_locks where resource_name = 'report_generator' for update;
```

**Correct (アドバイザリロック):**

```sql
-- セッションレベルのアドバイザリロック（切断または unlock で解除）
select pg_advisory_lock(hashtext('report_generator'));
-- ... 排他作業 ...
select pg_advisory_unlock(hashtext('report_generator'));

-- トランザクションレベル（commit/rollback で解除）
begin;
select pg_advisory_xact_lock(hashtext('daily_report'));
-- ... 作業 ...
commit;  -- ロックは自動解除
```

非ブロッキングの try-lock:

```sql
-- 待たずに true/false を返す
select pg_try_advisory_lock(hashtext('resource_name'));

-- アプリ側で利用
if (acquired) {
  -- 作業
  select pg_advisory_unlock(hashtext('resource_name'));
} else {
  -- スキップまたは後で再試行
}
```

Reference: [Advisory Locks](https://www.postgresql.org/docs/current/explicit-locking.html#ADVISORY-LOCKS)
