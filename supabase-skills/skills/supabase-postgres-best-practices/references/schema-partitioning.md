---
title: 大きなテーブルはパーティション分割する
impact: MEDIUM-HIGH
impactDescription: 大規模テーブルのクエリとメンテナンスが 5-20x 高速化
tags: partitioning, large-tables, time-series, performance
---

## 大きなテーブルはパーティション分割する

パーティショニングは大きなテーブルを小さな断片に分割し、クエリ性能とメンテナンスを改善します。

**Incorrect (単一の巨大テーブル):**

```sql
create table events (
  id bigint generated always as identity,
  created_at timestamptz,
  data jsonb
);

-- 5 億行、クエリは全体を走査
select * from events where created_at > '2024-01-01';  -- 遅い
vacuum events;  -- 数時間かかりテーブルをロック
```

**Correct (時間範囲でパーティション化):**

```sql
create table events (
  id bigint generated always as identity,
  created_at timestamptz not null,
  data jsonb
) partition by range (created_at);

-- 月ごとにパーティションを作成
create table events_2024_01 partition of events
  for values from ('2024-01-01') to ('2024-02-01');

create table events_2024_02 partition of events
  for values from ('2024-02-01') to ('2024-03-01');

-- 関連パーティションだけを走査
select * from events where created_at > '2024-01-15';  -- events_2024_01+ のみ

-- 古いデータを即時削除
drop table events_2023_01;  -- DELETE の数時間に比べ瞬時
```

パーティションの目安:

- 1 億行以上のテーブル
- 日付ベースで検索する時系列データ
- 古いデータを効率的に削除したい

Reference: [Table Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
