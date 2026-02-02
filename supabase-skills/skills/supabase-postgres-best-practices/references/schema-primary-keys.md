---
title: 最適な主キー戦略を選ぶ
impact: HIGH
impactDescription: インデックス局所性の改善と断片化の低減
tags: primary-key, identity, uuid, serial, schema
---

## 最適な主キー戦略を選ぶ

主キーの選択は、挿入性能・インデックスサイズ・レプリケーション効率に影響します。

**Incorrect (問題のある PK 選択):**

```sql
-- identity が SQL 標準のアプローチ
create table users (
  id serial primary key  -- 動作するが IDENTITY が推奨
);

-- ランダム UUID（v4）はインデックス断片化を引き起こす
create table orders (
  id uuid default gen_random_uuid() primary key  -- UUIDv4 = ランダム = 挿入が散る
);
```

**Correct (最適な PK 戦略):**

```sql
-- 連番 ID は IDENTITY を使用（SQL 標準でほとんどのケースに最適）
create table users (
  id bigint generated always as identity primary key
);

-- 分散システムで UUID が必要なら UUIDv7（時間順）
-- pg_uuidv7 拡張が必要: create extension pg_uuidv7;
create table orders (
  id uuid default uuid_generate_v7() primary key  -- 時間順で断片化しにくい
);

-- 代替: 時刻プレフィックス ID（並び替え可能、分散向き、拡張不要）
create table events (
  id text default concat(
    to_char(now() at time zone 'utc', 'YYYYMMDDHH24MISSMS'),
    gen_random_uuid()::text
  ) primary key
);
```

ガイドライン:

- 単一 DB: `bigint identity`（連番、8 バイト、SQL 標準）
- 分散/公開 ID: UUIDv7（pg_uuidv7 必須）または ULID（時間順で断片化なし）
- `serial` は動作するが、`identity` が SQL 標準で新規アプリに推奨
- 大規模テーブルの主キーにランダム UUID (v4) を使わない（断片化の原因）

Reference:
[Identity Columns](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-PARMS-GENERATED-IDENTITY)
