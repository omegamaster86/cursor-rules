---
title: トランザクションを短く保ちロック競合を減らす
impact: MEDIUM-HIGH
impactDescription: スループットが 3-5x 向上し、デッドロックが減少
tags: transactions, locking, contention, performance
---

## トランザクションを短く保ちロック競合を減らす

長時間のトランザクションはロックを保持し、他のクエリをブロックします。トランザクションは可能な限り短くしてください。

**Incorrect (外部呼び出しを含む長いトランザクション):**

```sql
begin;
select * from orders where id = 1 for update;  -- ロック取得

-- アプリが支払い API に HTTP 呼び出し（2-5 秒）
-- 他のクエリがこの行でブロックされる

update orders set status = 'paid' where id = 1;
commit;  -- ロックを全期間保持
```

**Correct (最小限のトランザクション範囲):**

```sql
-- 検証と API 呼び出しはトランザクション外で実施
-- Application: response = await paymentAPI.charge(...)

-- 実際の更新だけをロック下で行う
begin;
update orders
set status = 'paid', payment_id = $1
where id = $2 and status = 'pending'
returning *;
commit;  -- ロックはミリ秒単位
```

`statement_timeout` で暴走トランザクションを防ぐ:

```sql
-- 30 秒超のクエリを中断
set statement_timeout = '30s';

-- セッション単位でも設定可
set local statement_timeout = '5s';
```

Reference: [Transaction Management](https://www.postgresql.org/docs/current/tutorial-transactions.html)
