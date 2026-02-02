---
title: VACUUM と ANALYZE で統計情報を保つ
impact: MEDIUM
impactDescription: 正確な統計でクエリプランが 2-10x 改善
tags: vacuum, analyze, statistics, maintenance, autovacuum
---

## VACUUM と ANALYZE で統計情報を保つ

古い統計情報はプランナの判断を誤らせます。VACUUM は領域を回収し、ANALYZE は統計を更新します。

**Incorrect (統計が古い):**

```sql
-- テーブルは 100 万行だが統計は 1000 行
-- プランナが誤った戦略を選ぶ
explain select * from orders where status = 'pending';
-- Seq Scan が選ばれる（小さいテーブルと誤認）
-- 実際は Index Scan のほうが高速
```

**Correct (統計を最新に保つ):**

```sql
-- 大きなデータ変更後に手動で ANALYZE
analyze orders;

-- WHERE で使う列を対象にする
analyze orders (status, created_at);

-- 最終 ANALYZE の時刻を確認
select
  relname,
  last_vacuum,
  last_autovacuum,
  last_analyze,
  last_autoanalyze
from pg_stat_user_tables
order by last_analyze nulls first;
```

高更新テーブル向けの autovacuum チューニング:

```sql
-- 更新頻度が高いテーブルで頻度を上げる
alter table orders set (
  autovacuum_vacuum_scale_factor = 0.05,     -- 5% の死行で VACUUM（デフォルト 20%）
  autovacuum_analyze_scale_factor = 0.02     -- 2% の変更で ANALYZE（デフォルト 10%）
);

-- autovacuum の状態確認
select * from pg_stat_progress_vacuum;
```

Reference: [VACUUM](https://supabase.com/docs/guides/database/database-size#vacuum-operations)
