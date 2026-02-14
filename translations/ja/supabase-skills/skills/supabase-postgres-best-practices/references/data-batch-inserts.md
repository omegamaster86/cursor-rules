---
title: バルクデータは INSERT をバッチ化する
impact: MEDIUM
impactDescription: バルク INSERT を 10-50 倍高速化
tags: batch, insert, bulk, performance, copy
---

## バルクデータは INSERT をバッチ化する

個別の INSERT はオーバーヘッドが大きくなります。複数行を 1 文にまとめるか、COPY を使います。

**誤り（個別 INSERT）:**

```sql
-- Each insert is a separate transaction and round trip
insert into events (user_id, action) values (1, 'click');
insert into events (user_id, action) values (1, 'view');
insert into events (user_id, action) values (2, 'click');
-- ... 1000 more individual inserts

-- 1000 inserts = 1000 round trips = slow
```

**正しい例（バッチ INSERT）:**

```sql
-- Multiple rows in single statement
insert into events (user_id, action) values
  (1, 'click'),
  (1, 'view'),
  (2, 'click'),
  -- ... up to ~1000 rows per batch
  (999, 'view');

-- One round trip for 1000 rows
```

大量投入では COPY を使う:

```sql
-- COPY is fastest for bulk loading
copy events (user_id, action, created_at)
from '/path/to/data.csv'
with (format csv, header true);

-- Or from stdin in application
copy events (user_id, action) from stdin with (format csv);
1,click
1,view
2,click
\.
```

Reference: [COPY](https://www.postgresql.org/docs/current/sql-copy.html)
