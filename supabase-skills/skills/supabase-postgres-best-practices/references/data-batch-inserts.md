---
title: バルクデータは INSERT をバッチ化する
impact: MEDIUM
impactDescription: バルク挿入が 10-50x 高速化
tags: batch, insert, bulk, performance, copy
---

## バルクデータは INSERT をバッチ化する

個別の INSERT はオーバーヘッドが大きいです。複数行を 1 つのステートメントにまとめるか、COPY を使ってください。

**Incorrect (個別 INSERT):**

```sql
-- 各 INSERT が別トランザクションと往復になる
insert into events (user_id, action) values (1, 'click');
insert into events (user_id, action) values (1, 'view');
insert into events (user_id, action) values (2, 'click');
-- ... さらに 1000 件

-- 1000 INSERT = 1000 往復 = 遅い
```

**Correct (バッチ INSERT):**

```sql
-- 1 文に複数行
insert into events (user_id, action) values
  (1, 'click'),
  (1, 'view'),
  (2, 'click'),
  -- ... 1 バッチあたり ~1000 行まで
  (999, 'view');

-- 1000 行でも往復は 1 回
```

大量投入は COPY を使う:

```sql
-- COPY がバルクロード最速
copy events (user_id, action, created_at)
from '/path/to/data.csv'
with (format csv, header true);

-- アプリから stdin 経由でも可
copy events (user_id, action) from stdin with (format csv);
1,click
1,view
2,click
\.
```

Reference: [COPY](https://www.postgresql.org/docs/current/sql-copy.html)
