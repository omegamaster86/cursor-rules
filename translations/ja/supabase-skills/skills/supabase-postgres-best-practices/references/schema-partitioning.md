---
title: 大規模テーブルはパーティショニングで性能を上げる
impact: MEDIUM-HIGH
impactDescription: 大規模テーブルで検索と保守を 5-20 倍高速化
tags: partitioning, large-tables, time-series, performance
---

## 大規模テーブルはパーティショニングで性能を上げる

パーティショニングは巨大テーブルを小さな断片に分割し、クエリ性能と保守性を改善します。

**誤り（単一の巨大テーブル）:**

```sql
create table events (
  id bigint generated always as identity,
  created_at timestamptz,
  data jsonb
);

-- 500M rows, queries scan everything
select * from events where created_at > '2024-01-01';  -- Slow
vacuum events;  -- Takes hours, locks table
```

**正しい例（期間で分割）:**

```sql
create table events (
  id bigint generated always as identity,
  created_at timestamptz not null,
  data jsonb
) partition by range (created_at);

-- Create partitions for each month
create table events_2024_01 partition of events
  for values from ('2024-01-01') to ('2024-02-01');

create table events_2024_02 partition of events
  for values from ('2024-02-01') to ('2024-03-01');

-- Queries only scan relevant partitions
select * from events where created_at > '2024-01-15';  -- Only scans events_2024_01+

-- Drop old data instantly
drop table events_2023_01;  -- Instant vs DELETE taking hours
```

パーティション導入の目安:

- テーブル行数が 1 億超
- 日付ベースで問い合わせる時系列データ
- 古いデータを効率的に削除したい

Reference: [Table Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
