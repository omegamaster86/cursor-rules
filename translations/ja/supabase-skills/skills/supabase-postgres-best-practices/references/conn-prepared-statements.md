---
title: プーリング環境で Prepared Statement を正しく使う
impact: HIGH
impactDescription: プール環境での prepared statement 競合を回避
tags: prepared-statements, connection-pooling, transaction-mode
---

## プーリング環境で Prepared Statement を正しく使う

Prepared statement は個別の DB 接続に紐づきます。Transaction モードのプーリングでは接続が共有されるため、競合が発生します。

**誤り（Transaction プーリングで名前付き prepared statement）:**

```sql
-- Named prepared statement
prepare get_user as select * from users where id = $1;

-- In transaction mode pooling, next request may get different connection
execute get_user(123);
-- ERROR: prepared statement "get_user" does not exist
```

**正しい例（無名 statement または Session モードを使う）:**

```sql
-- Option 1: Use unnamed prepared statements (most ORMs do this automatically)
-- The query is prepared and executed in a single protocol message

-- Option 2: Deallocate after use in transaction mode
prepare get_user as select * from users where id = $1;
execute get_user(123);
deallocate get_user;

-- Option 3: Use session mode pooling (port 5432 vs 6543)
-- Connection is held for entire session, prepared statements persist
```

ドライバ設定を確認:

```sql
-- Many drivers use prepared statements by default
-- Node.js pg: { prepare: false } to disable
-- JDBC: prepareThreshold=0 to disable
```

Reference: [Prepared Statements with Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pool-modes)
