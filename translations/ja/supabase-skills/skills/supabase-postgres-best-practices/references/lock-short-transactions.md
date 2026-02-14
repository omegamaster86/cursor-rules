---
title: ロック競合を減らすためトランザクションを短く保つ
impact: MEDIUM-HIGH
impactDescription: スループット 3-5 倍改善、デッドロック減少
tags: transactions, locking, contention, performance
---

## ロック競合を減らすためトランザクションを短く保つ

長時間トランザクションはロックを保持し続け、他クエリをブロックします。できるだけ短く保ちます。

**誤り（外部呼び出しを含む長いトランザクション）:**

```sql
begin;
select * from orders where id = 1 for update;  -- Lock acquired

-- Application makes HTTP call to payment API (2-5 seconds)
-- Other queries on this row are blocked!

update orders set status = 'paid' where id = 1;
commit;  -- Lock held for entire duration
```

**正しい例（最小限のトランザクション範囲）:**

```sql
-- Validate data and call APIs outside transaction
-- Application: response = await paymentAPI.charge(...)

-- Only hold lock for the actual update
begin;
update orders
set status = 'paid', payment_id = $1
where id = $2 and status = 'pending'
returning *;
commit;  -- Lock held for milliseconds
```

`statement_timeout` で暴走クエリを防止:

```sql
-- Abort queries running longer than 30 seconds
set statement_timeout = '30s';

-- Or per-session
set local statement_timeout = '5s';
```

Reference: [Transaction Management](https://www.postgresql.org/docs/current/tutorial-transactions.html)
