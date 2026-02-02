---
title: データに適したインデックス種別を選ぶ
impact: HIGH
impactDescription: 正しいインデックス種別で 10-100x 改善
tags: indexes, btree, gin, brin, hash, index-types
---

## データに適したインデックス種別を選ぶ

インデックス種別はクエリパターンごとに得意分野が異なります。デフォルトの B-tree が常に最適とは限りません。

**Incorrect (JSONB の包含に B-tree):**

```sql
-- B-tree は包含演算子を最適化できない
create index products_attrs_idx on products (attributes);
select * from products where attributes @> '{"color": "red"}';
-- 全表スキャン - B-tree は @> をサポートしない
```

**Correct (JSONB には GIN):**

```sql
-- GIN は @>, ?, ?&, ?| をサポート
create index products_attrs_idx on products using gin (attributes);
select * from products where attributes @> '{"color": "red"}';
```

インデックス種別の指針:

```sql
-- B-tree（デフォルト）: =, <, >, BETWEEN, IN, IS NULL
create index users_created_idx on users (created_at);

-- GIN: 配列、JSONB、全文検索
create index posts_tags_idx on posts using gin (tags);

-- BRIN: 大きな時系列テーブル（10-100x 小さい）
create index events_time_idx on events using brin (created_at);

-- Hash: 等価比較のみ（= に限り B-tree より少し速い）
create index sessions_token_idx on sessions using hash (token);
```

Reference: [Index Types](https://www.postgresql.org/docs/current/indexes-types.html)
