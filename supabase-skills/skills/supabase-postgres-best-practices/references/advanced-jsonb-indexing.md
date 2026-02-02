---
title: JSONB カラムにインデックスを付けて効率的に検索する
impact: MEDIUM
impactDescription: 適切なインデックスで JSONB クエリが 10-100x 高速化
tags: jsonb, gin, indexes, json
---

## JSONB カラムにインデックスを付けて効率的に検索する

インデックスがない JSONB クエリは全表スキャンになります。包含クエリには GIN インデックスを使ってください。

**Incorrect (JSONB にインデックスなし):**

```sql
create table products (
  id bigint primary key,
  attributes jsonb
);

-- すべてのクエリが全表スキャン
select * from products where attributes @> '{"color": "red"}';
select * from products where attributes->>'brand' = 'Nike';
```

**Correct (JSONB に GIN インデックス):**

```sql
-- 包含演算子 (@>, ?, ?&, ?|) 用の GIN インデックス
create index products_attrs_gin on products using gin (attributes);

-- 包含クエリがインデックスを使用
select * from products where attributes @> '{"color": "red"}';

-- 特定キーの検索には式インデックスを使用
create index products_brand_idx on products ((attributes->>'brand'));
select * from products where attributes->>'brand' = 'Nike';
```

適切なオペレータクラスを選ぶ:

```sql
-- jsonb_ops (デフォルト): すべての演算子をサポート、インデックスは大きめ
create index idx1 on products using gin (attributes);

-- jsonb_path_ops: @> のみだがインデックスは 2-3x 小さい
create index idx2 on products using gin (attributes jsonb_path_ops);
```

Reference: [JSONB Indexes](https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING)
