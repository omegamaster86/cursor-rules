---
title: クエリ分析のために pg_stat_statements を有効化する
impact: LOW-MEDIUM
impactDescription: リソース消費の大きいクエリを特定
tags: pg-stat-statements, monitoring, statistics, performance
---

## クエリ分析のために pg_stat_statements を有効化する

pg_stat_statements は全クエリの実行統計を追跡し、遅い/頻繁なクエリを特定できます。

**Incorrect (クエリパターンの可視化なし):**

```sql
-- DB が遅いが、どのクエリが原因か不明
-- pg_stat_statements がないと把握できない
```

**Correct (pg_stat_statements を有効化して参照):**

```sql
-- 拡張を有効化
create extension if not exists pg_stat_statements;

-- 総実行時間が長いクエリを抽出
select
  calls,
  round(total_exec_time::numeric, 2) as total_time_ms,
  round(mean_exec_time::numeric, 2) as mean_time_ms,
  query
from pg_stat_statements
order by total_exec_time desc
limit 10;

-- 実行回数が多いクエリ
select calls, query
from pg_stat_statements
order by calls desc
limit 10;

-- 最適化後に統計をリセット
select pg_stat_statements_reset();
```

監視すべき主な指標:

```sql
-- 平均実行時間が長いクエリ（最適化候補）
select query, mean_exec_time, calls
from pg_stat_statements
where mean_exec_time > 100  -- 平均 100ms 超
order by mean_exec_time desc;
```

Reference: [pg_stat_statements](https://supabase.com/docs/guides/database/extensions/pg_stat_statements)
