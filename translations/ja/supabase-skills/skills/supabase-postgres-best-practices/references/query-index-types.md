---
title: データに合ったインデックス種別を選ぶ
impact: HIGH
impactDescription: 適切なインデックス種別で 10-100 倍改善
tags: indexes, btree, gin, gist, brin, hash, index-types
---

## データに合ったインデックス種別を選ぶ

インデックス種別ごとに得意なクエリパターンが異なります。既定の B-tree が常に最適とは限りません。

**誤り（JSONB 包含検索に B-tree）:**

```sql
-- B-tree cannot optimize containment operators
create index products_attrs_idx on products (attributes);
select * from products where attributes @> '{"color": "red"}';
-- Full table scan - B-tree doesn't support @> operator
```

**正しい例（JSONB には GIN）:**

```sql
-- GIN supports @>, ?, ?&, ?| operators
create index products_attrs_idx on products using gin (attributes);
select * from products where attributes @> '{"color": "red"}';
```

インデックス種別の目安:

```sql
-- B-tree (default): =, <, >, BETWEEN, IN, IS NULL
create index users_created_idx on users (created_at);

-- GIN: arrays, JSONB, full-text search
create index posts_tags_idx on posts using gin (tags);

-- GiST: geometric data, range types, nearest-neighbor (KNN) queries
create index locations_idx on places using gist (location);

-- BRIN: large time-series tables (10-100x smaller)
create index events_time_idx on events using brin (created_at);

-- Hash: equality-only (slightly faster than B-tree for =)
create index sessions_token_idx on sessions using hash (token);
```

Reference: [Index Types](https://www.postgresql.org/docs/current/indexes-types.html)
