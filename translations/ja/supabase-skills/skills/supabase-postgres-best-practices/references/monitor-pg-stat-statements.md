---
title: クエリ分析のために pg_stat_statements を有効化する
impact: LOW-MEDIUM
impactDescription: 最もリソースを消費するクエリを特定
tags: pg-stat-statements, monitoring, statistics, performance
---

## クエリ分析のために pg_stat_statements を有効化する

pg_stat_statements は全クエリの実行統計を記録し、遅いクエリや頻出クエリの特定に役立ちます。

**誤り（クエリ傾向が見えない）:**

```sql
-- Database is slow, but which queries are the problem?
-- No way to know without pg_stat_statements
```

**正しい例（pg_stat_statements を有効化して参照）:**

```sql
-- Enable the extension
create extension if not exists pg_stat_statements;

-- Find slowest queries by total time
select
  calls,
  round(total_exec_time::numeric, 2) as total_time_ms,
  round(mean_exec_time::numeric, 2) as mean_time_ms,
  query
from pg_stat_statements
order by total_exec_time desc
limit 10;

-- Find most frequent queries
select calls, query
from pg_stat_statements
order by calls desc
limit 10;

-- Reset statistics after optimization
select pg_stat_statements_reset();
```

監視すべき主要メトリクス:

```sql
-- Queries with high mean time (candidates for optimization)
select query, mean_exec_time, calls
from pg_stat_statements
where mean_exec_time > 100  -- > 100ms average
order by mean_exec_time desc;
```

Reference: [pg_stat_statements](https://supabase.com/docs/guides/database/extensions/pg_stat_statements)
