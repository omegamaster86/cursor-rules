---
title: OFFSET ではなくカーソルベースのページングを使う
impact: MEDIUM-HIGH
impactDescription: ページが深くても常に O(1) の性能
tags: pagination, cursor, keyset, offset, performance
---

## OFFSET ではなくカーソルベースのページングを使う

OFFSET ベースのページングはスキップした行をすべて走査するため、ページが深いほど遅くなります。カーソルページングは O(1) です。

**Incorrect (OFFSET ページング):**

```sql
-- 1 ページ目: 20 行を走査
select * from products order by id limit 20 offset 0;

-- 100 ページ目: 1980 行をスキップするため 2000 行を走査
select * from products order by id limit 20 offset 1980;

-- 10000 ページ目: 200,000 行を走査!
select * from products order by id limit 20 offset 199980;
```

**Correct (カーソル/キーセットページング):**

```sql
-- 1 ページ目: 最初の 20 件
select * from products order by id limit 20;
-- アプリ側で last_id = 20 を保持

-- 2 ページ目: last_id 以降
select * from products where id > 20 order by id limit 20;
-- インデックスを使い、ページが深くても常に高速

-- 10000 ページ目: 1 ページ目と同じ速度
select * from products where id > 199980 order by id limit 20;
```

複数カラムでのソート:

```sql
-- カーソルはソート列すべてを含む
select * from products
where (created_at, id) > ('2024-01-15 10:00:00', 12345)
order by created_at, id
limit 20;
```

Reference: [Pagination](https://supabase.com/docs/guides/database/pagination)
