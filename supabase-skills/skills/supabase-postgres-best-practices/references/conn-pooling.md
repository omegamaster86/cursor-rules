---
title: すべてのアプリで接続プーリングを使う
impact: CRITICAL
impactDescription: 同時ユーザーを 10-100x 多く処理可能
tags: connection-pooling, pgbouncer, performance, scalability
---

## すべてのアプリで接続プーリングを使う

Postgres の接続は高コスト（1-3MB RAM/接続）です。プーリングなしだと負荷時に接続が枯渇します。

**Incorrect (リクエストごとに新規接続):**

```sql
-- 各リクエストが新しい接続を作成
-- アプリコード: リクエストごとに db.connect()
-- 結果: 同時 500 ユーザー = 500 接続 = DB がクラッシュ

-- 現在の接続数を確認
select count(*) from pg_stat_activity;  -- 487 connections!
```

**Correct (接続プーリング):**

```sql
-- アプリと DB の間に PgBouncer などのプーラを使う
-- アプリはプーラに接続し、プーラが少数の接続を再利用

-- pool_size の目安: (CPU コア数 * 2) + ディスク本数
-- 例: 4 コアなら pool_size = 10

-- 結果: 同時 500 ユーザーが 10 接続を共有
select count(*) from pg_stat_activity;  -- 10 connections
```

プールモード:

- **Transaction mode**: トランザクション終了ごとに接続を返却（多くのアプリに最適）
- **Session mode**: セッション全体で接続を保持（プリペアドステートメント、テンポラリテーブルが必要な場合）

Reference: [Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)
