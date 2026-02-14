---
title: JSONB 列にインデックスを作成して効率的に検索する
impact: MEDIUM
impactDescription: 適切なインデックスで JSONB クエリを 10-100 倍高速化
tags: jsonb, gin, indexes, json
---

## JSONB 列にインデックスを作成して効率的に検索する

インデックスのない JSONB クエリは全表走査になります。包含検索には GIN インデックスを使います。

**誤り（JSONB にインデックスなし）:**

```sql
create table products (
  id bigint primary key,
  attributes jsonb
);

-- Full table scan for every query
select * from products where attributes @> '{"color": "red"}';
select * from products where attributes->>'brand' = 'Nike';
```

**正しい例（JSONB 用 GIN インデックス）:**

```sql
-- GIN index for containment operators (@>, ?, ?&, ?|)
create index products_attrs_gin on products using gin (attributes);

-- Now containment queries use the index
select * from products where attributes @> '{"color": "red"}';

-- For specific key lookups, use expression index
create index products_brand_idx on products ((attributes->>'brand'));
select * from products where attributes->>'brand' = 'Nike';
```

適切な operator class を選択:

```sql
-- jsonb_ops (default): supports all operators, larger index
create index idx1 on products using gin (attributes);

-- jsonb_path_ops: only @> operator, but 2-3x smaller index
create index idx2 on products using gin (attributes jsonb_path_ops);
```

Reference: [JSONB Indexes](https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING)
