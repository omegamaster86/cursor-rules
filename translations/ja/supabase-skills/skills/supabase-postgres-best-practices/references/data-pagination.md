---
title: OFFSET ではなくカーソルベースページネーションを使う
impact: MEDIUM-HIGH
impactDescription: ページ深度に依存しない一貫した O(1) 性能
tags: pagination, cursor, keyset, offset, performance
---

## OFFSET ではなくカーソルベースページネーションを使う

OFFSET ベースのページングはスキップ行を走査するため、深いページほど遅くなります。カーソル方式は O(1) です。

**誤り（OFFSET ページング）:**

```sql
-- Page 1: scans 20 rows
select * from products order by id limit 20 offset 0;

-- Page 100: scans 2000 rows to skip 1980
select * from products order by id limit 20 offset 1980;

-- Page 10000: scans 200,000 rows!
select * from products order by id limit 20 offset 199980;
```

**正しい例（カーソル/キーセットページング）:**

```sql
-- Page 1: get first 20
select * from products order by id limit 20;
-- Application stores last_id = 20

-- Page 2: start after last ID
select * from products where id > 20 order by id limit 20;
-- Uses index, always fast regardless of page depth

-- Page 10000: same speed as page 1
select * from products where id > 199980 order by id limit 20;
```

複数列ソートの場合:

```sql
-- Cursor must include all sort columns
select * from products
where (created_at, id) > ('2024-01-15 10:00:00', 12345)
order by created_at, id
limit 20;
```

Reference: [Pagination](https://supabase.com/docs/guides/database/pagination)
