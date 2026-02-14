---
title: 適切なデータ型を選ぶ
impact: HIGH
impactDescription: ストレージを 50% 削減し、比較を高速化
tags: data-types, schema, storage, performance
---

## 適切なデータ型を選ぶ

正しいデータ型を選ぶと、ストレージ削減、クエリ性能向上、バグ防止につながります。

**誤り（不適切なデータ型）:**

```sql
create table users (
  id int,                    -- Will overflow at 2.1 billion
  email varchar(255),        -- Unnecessary length limit
  created_at timestamp,      -- Missing timezone info
  is_active varchar(5),      -- String for boolean
  price varchar(20)          -- String for numeric
);
```

**正しい例（適切なデータ型）:**

```sql
create table users (
  id bigint generated always as identity primary key,  -- 9 quintillion max
  email text,                     -- No artificial limit, same performance as varchar
  created_at timestamptz,         -- Always store timezone-aware timestamps
  is_active boolean default true, -- 1 byte vs variable string length
  price numeric(10,2)             -- Exact decimal arithmetic
);
```

主なガイドライン:

```sql
-- IDs: use bigint, not int (future-proofing)
-- Strings: use text, not varchar(n) unless constraint needed
-- Time: use timestamptz, not timestamp
-- Money: use numeric, not float (precision matters)
-- Enums: use text with check constraint or create enum type
```

Reference: [Data Types](https://www.postgresql.org/docs/current/datatype.html)
