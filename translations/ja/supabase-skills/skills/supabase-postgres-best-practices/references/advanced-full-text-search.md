---
title: 全文検索には tsvector を使う
impact: MEDIUM
impactDescription: LIKE より 100 倍高速で、ランキングにも対応
tags: full-text-search, tsvector, gin, search
---

## 全文検索には tsvector を使う

ワイルドカード付き LIKE はインデックスを使えません。tsvector を使った全文検索は桁違いに高速です。

**誤り（LIKE パターンマッチ）:**

```sql
-- Cannot use index, scans all rows
select * from articles where content like '%postgresql%';

-- Case-insensitive makes it worse
select * from articles where lower(content) like '%postgresql%';
```

**正しい例（tsvector を使った全文検索）:**

```sql
-- Add tsvector column and index
alter table articles add column search_vector tsvector
  generated always as (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,''))) stored;

create index articles_search_idx on articles using gin (search_vector);

-- Fast full-text search
select * from articles
where search_vector @@ to_tsquery('english', 'postgresql & performance');

-- With ranking
select *, ts_rank(search_vector, query) as rank
from articles, to_tsquery('english', 'postgresql') query
where search_vector @@ query
order by rank desc;
```

複数語の検索:

```sql
-- AND: both terms required
to_tsquery('postgresql & performance')

-- OR: either term
to_tsquery('postgresql | mysql')

-- Prefix matching
to_tsquery('post:*')
```

Reference: [Full Text Search](https://supabase.com/docs/guides/database/full-text-search)
