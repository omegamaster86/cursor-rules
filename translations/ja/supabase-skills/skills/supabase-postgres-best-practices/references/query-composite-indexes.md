---
title: 複数列クエリには複合インデックスを作る
impact: HIGH
impactDescription: 複数列クエリを 5-10 倍高速化
tags: indexes, composite-index, multi-column, query-optimization
---

## 複数列クエリには複合インデックスを作る

複数列で絞り込むクエリでは、単一列インデックスを複数持つより、複合インデックスの方が効率的です。

**誤り（単一列インデックスの組み合わせ）:**

```sql
-- Two separate indexes
create index orders_status_idx on orders (status);
create index orders_created_idx on orders (created_at);

-- Query must combine both indexes (slower)
select * from orders where status = 'pending' and created_at > '2024-01-01';
```

**正しい例（複合インデックス）:**

```sql
-- Single composite index (leftmost column first for equality checks)
create index orders_status_created_idx on orders (status, created_at);

-- Query uses one efficient index scan
select * from orders where status = 'pending' and created_at > '2024-01-01';
```

**列順は重要**: 等価条件の列を先頭、範囲条件の列を後ろに置きます。

```sql
-- Good: status (=) before created_at (>)
create index idx on orders (status, created_at);

-- Works for: WHERE status = 'pending'
-- Works for: WHERE status = 'pending' AND created_at > '2024-01-01'
-- Does NOT work for: WHERE created_at > '2024-01-01' (leftmost prefix rule)
```

Reference: [Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
