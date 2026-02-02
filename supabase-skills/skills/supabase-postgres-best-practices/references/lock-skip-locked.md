---
title: ブロッキングしないキュー処理に SKIP LOCKED を使う
impact: MEDIUM-HIGH
impactDescription: ワーカーキューのスループットが 10x
tags: skip-locked, queue, workers, concurrency
---

## ブロッキングしないキュー処理に SKIP LOCKED を使う

複数ワーカーでキューを処理する場合、SKIP LOCKED を使うと待ちを発生させずに別々の行を処理できます。

**Incorrect (ワーカー同士がブロック):**

```sql
-- Worker 1 と Worker 2 が同時に次のジョブを取得
begin;
select * from jobs where status = 'pending' order by created_at limit 1 for update;
-- Worker 2 は Worker 1 のロック解放を待つ
```

**Correct (SKIP LOCKED による並列処理):**

```sql
-- 各ワーカーはロック済み行をスキップして次を取得
begin;
select * from jobs
where status = 'pending'
order by created_at
limit 1
for update skip locked;

-- Worker 1 は job 1、Worker 2 は job 2（待ちなし）

update jobs set status = 'processing' where id = $1;
commit;
```

完全なキューパターン:

```sql
-- 1 文で原子的に取得と更新
update jobs
set status = 'processing', worker_id = $1, started_at = now()
where id = (
  select id from jobs
  where status = 'pending'
  order by created_at
  limit 1
  for update skip locked
)
returning *;
```

Reference: [SELECT FOR UPDATE SKIP LOCKED](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE)
