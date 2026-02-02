---
title: 複数カラムクエリには複合インデックスを作成する
impact: HIGH
impactDescription: 複数カラムのクエリが 5-10x 高速化
tags: indexes, composite-index, multi-column, query-optimization
---

## 複数カラムクエリには複合インデックスを作成する

複数カラムでフィルタするクエリでは、単一カラムのインデックスを複数使うより複合インデックスのほうが効率的です。

**Incorrect (別々のインデックスはビットマップスキャンが必要):**

```sql
-- 2 つの単一インデックス
create index orders_status_idx on orders (status);
create index orders_created_idx on orders (created_at);

-- クエリは 2 つのインデックスを合成（遅い）
select * from orders where status = 'pending' and created_at > '2024-01-01';
```

**Correct (複合インデックス):**

```sql
-- 1 つの複合インデックス（等価条件の列を左側に）
create index orders_status_created_idx on orders (status, created_at);

-- 単一の効率的なインデックススキャン
select * from orders where status = 'pending' and created_at > '2024-01-01';
```

**列の順序が重要** - 等価条件を先、範囲条件を後に:

```sql
-- 良い例: status (=) を created_at (>) より先に
create index idx on orders (status, created_at);

-- 対応: WHERE status = 'pending'
-- 対応: WHERE status = 'pending' AND created_at > '2024-01-01'
-- 非対応: WHERE created_at > '2024-01-01'（左端一致のルール）
```

Reference: [Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
