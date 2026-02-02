---
title: 適切なデータ型を選ぶ
impact: HIGH
impactDescription: 50% の容量削減と比較の高速化
tags: data-types, schema, storage, performance
---

## 適切なデータ型を選ぶ

適切なデータ型はストレージを削減し、クエリ性能を向上させ、バグも防ぎます。

**Incorrect (不適切なデータ型):**

```sql
create table users (
  id int,                    -- 21 億でオーバーフロー
  email varchar(255),        -- 不要な長さ制限
  created_at timestamp,      -- タイムゾーン情報なし
  is_active varchar(5),      -- boolean に文字列
  price varchar(20)          -- 数値に文字列
);
```

**Correct (適切なデータ型):**

```sql
create table users (
  id bigint generated always as identity primary key,  -- 最大 900 兆
  email text,                     -- 不要な制限なし、varchar と同等性能
  created_at timestamptz,         -- 常にタイムゾーン付きで保持
  is_active boolean default true, -- 1 バイトで可変長文字列より小さい
  price numeric(10,2)             -- 正確な小数演算
);
```

主な指針:

```sql
-- ID: int ではなく bigint（将来の拡張に備える）
-- 文字列: 制約が不要なら varchar(n) ではなく text
-- 時刻: timestamp ではなく timestamptz
-- 金額: float ではなく numeric（精度が重要）
-- Enum: check 制約付き text か enum 型を作成
```

Reference: [Data Types](https://www.postgresql.org/docs/current/datatype.html)
