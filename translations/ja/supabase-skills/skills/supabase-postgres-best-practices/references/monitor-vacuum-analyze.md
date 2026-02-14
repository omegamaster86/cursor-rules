---
title: VACUUM と ANALYZE でテーブル統計を維持する
impact: MEDIUM
impactDescription: 正確な統計によりクエリプランを 2-10 倍改善
tags: vacuum, analyze, statistics, maintenance, autovacuum
---

## VACUUM と ANALYZE でテーブル統計を維持する

統計情報が古いと、クエリプランナが誤った判断をします。VACUUM は領域回収、ANALYZE は統計更新を行います。

**誤り（統計が古い）:**

```sql
-- Table has 1M rows but stats say 1000
-- Query planner chooses wrong strategy
explain select * from orders where status = 'pending';
-- Shows: Seq Scan (because stats show small table)
-- Actually: Index Scan would be much faster
```

**正しい例（統計を新鮮に保つ）:**

```sql
-- Manually analyze after large data changes
analyze orders;

-- Analyze specific columns used in WHERE clauses
analyze orders (status, created_at);

-- Check when tables were last analyzed
select
  relname,
  last_vacuum,
  last_autovacuum,
  last_analyze,
  last_autoanalyze
from pg_stat_user_tables
order by last_analyze nulls first;
```

高更新テーブル向けの autovacuum 調整:

```sql
-- Increase frequency for high-churn tables
alter table orders set (
  autovacuum_vacuum_scale_factor = 0.05,     -- Vacuum at 5% dead tuples (default 20%)
  autovacuum_analyze_scale_factor = 0.02     -- Analyze at 2% changes (default 10%)
);

-- Check autovacuum status
select * from pg_stat_progress_vacuum;
```

Reference: [VACUUM](https://supabase.com/docs/guides/database/database-size#vacuum-operations)
