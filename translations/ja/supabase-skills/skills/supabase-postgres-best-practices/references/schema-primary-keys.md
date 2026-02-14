---
title: 最適な主キー戦略を選ぶ
impact: HIGH
impactDescription: インデックス局所性を改善し、断片化を削減
tags: primary-key, identity, uuid, serial, schema
---

## 最適な主キー戦略を選ぶ

主キーの選択は、INSERT 性能、インデックスサイズ、レプリケーション効率に影響します。

**誤り（問題のある主キー選択）:**

```sql
-- identity is the SQL-standard approach
create table users (
  id serial primary key  -- Works, but IDENTITY is recommended
);

-- Random UUIDs (v4) cause index fragmentation
create table orders (
  id uuid default gen_random_uuid() primary key  -- UUIDv4 = random = scattered inserts
);
```

**正しい例（最適な主キー戦略）:**

```sql
-- Use IDENTITY for sequential IDs (SQL-standard, best for most cases)
create table users (
  id bigint generated always as identity primary key
);

-- For distributed systems needing UUIDs, use UUIDv7 (time-ordered)
-- Requires pg_uuidv7 extension: create extension pg_uuidv7;
create table orders (
  id uuid default uuid_generate_v7() primary key  -- Time-ordered, no fragmentation
);

-- Alternative: time-prefixed IDs for sortable, distributed IDs (no extension needed)
create table events (
  id text default concat(
    to_char(now() at time zone 'utc', 'YYYYMMDDHH24MISSMS'),
    gen_random_uuid()::text
  ) primary key
);
```

ガイドライン:

- 単一 DB: `bigint identity`（連番、8 バイト、SQL 標準）
- 分散/外部公開 ID: UUIDv7（pg_uuidv7 必須）または ULID（時系列順、断片化しにくい）
- `serial` も動作するが、新規アプリでは SQL 標準の `identity` を推奨
- 大規模テーブルの主キーにランダム UUIDv4 は避ける（インデックス断片化の原因）

Reference:
[Identity Columns](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-PARMS-GENERATED-IDENTITY)
