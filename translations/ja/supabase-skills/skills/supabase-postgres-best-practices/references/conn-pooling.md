---
title: すべてのアプリでコネクションプーリングを使う
impact: CRITICAL
impactDescription: 同時接続ユーザー数を 10-100 倍拡張
tags: connection-pooling, pgbouncer, performance, scalability
---

## すべてのアプリでコネクションプーリングを使う

Postgres の接続は高コストです（1 接続あたり 1-3MB RAM）。プーリングがないと高負荷時に接続枠を使い切ります。

**誤り（リクエストごとに新規接続）:**

```sql
-- Each request creates a new connection
-- Application code: db.connect() per request
-- Result: 500 concurrent users = 500 connections = crashed database

-- Check current connections
select count(*) from pg_stat_activity;  -- 487 connections!
```

**正しい例（コネクションプーリング）:**

```sql
-- Use a pooler like PgBouncer between app and database
-- Application connects to pooler, pooler reuses a small pool to Postgres

-- Configure pool_size based on: (CPU cores * 2) + spindle_count
-- Example for 4 cores: pool_size = 10

-- Result: 500 concurrent users share 10 actual connections
select count(*) from pg_stat_activity;  -- 10 connections
```

プールモード:

- **Transaction mode**: 各トランザクション後に接続を返却（大半のアプリに最適）
- **Session mode**: セッション全体で接続を保持（prepared statement や一時テーブルに必要）

Reference: [Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)
