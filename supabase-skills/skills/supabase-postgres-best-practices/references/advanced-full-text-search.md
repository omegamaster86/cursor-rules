---
title: 全文検索に tsvector を使う
impact: MEDIUM
impactDescription: LIKE より 100x 高速、ランキングにも対応
tags: full-text-search, tsvector, gin, search
---

## 全文検索に tsvector を使う

ワイルドカード付きの LIKE はインデックスを使えません。tsvector を使った全文検索は桁違いに高速です。

**Incorrect (LIKE によるパターン一致):**

```sql
-- インデックスを使えず、全行スキャン
select * from articles where content like '%postgresql%';

-- 大文字小文字を無視するとさらに悪化
select * from articles where lower(content) like '%postgresql%';
```

**Correct (tsvector による全文検索):**

```sql
-- tsvector カラムとインデックスを追加
alter table articles add column search_vector tsvector
  generated always as (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,''))) stored;

create index articles_search_idx on articles using gin (search_vector);

-- 高速な全文検索
select * from articles
where search_vector @@ to_tsquery('english', 'postgresql & performance');

-- ランキング付き
select *, ts_rank(search_vector, query) as rank
from articles, to_tsquery('english', 'postgresql') query
where search_vector @@ query
order by rank desc;
```

複数語の検索:

```sql
-- AND: 両方の語が必要
to_tsquery('postgresql & performance')

-- OR: どちらか一方
to_tsquery('postgresql | mysql')

-- 前方一致
to_tsquery('post:*')
```

Reference: [Full Text Search](https://supabase.com/docs/guides/database/full-text-search)
