---
title: プーリング環境でプリペアドステートメントを正しく使う
impact: HIGH
impactDescription: プール環境でのプリペアドステートメント競合を回避
tags: prepared-statements, connection-pooling, transaction-mode
---

## プーリング環境でプリペアドステートメントを正しく使う

プリペアドステートメントは個々の DB 接続に紐づきます。トランザクションモードのプーリングでは接続が共有されるため競合が起きます。

**Incorrect (トランザクションプーリングで名前付きプリペアド):**

```sql
-- 名前付きプリペアドステートメント
prepare get_user as select * from users where id = $1;

-- トランザクションモードでは次のリクエストが別接続になる可能性
execute get_user(123);
-- ERROR: prepared statement "get_user" does not exist
```

**Correct (無名ステートメントかセッションモードを使用):**

```sql
-- 選択肢 1: 無名のプリペアドステートメントを使う（多くの ORM は自動対応）
-- クエリは 1 回のプロトコルメッセージで準備と実行が行われる

-- 選択肢 2: トランザクションモードでは使用後に解放
prepare get_user as select * from users where id = $1;
execute get_user(123);
deallocate get_user;

-- 選択肢 3: セッションモードのプーリングを使う（ポート 5432 vs 6543）
-- セッション全体で接続を保持し、プリペアドは維持される
```

ドライバ設定を確認:

```sql
-- 多くのドライバはデフォルトでプリペアドを使う
-- Node.js pg: { prepare: false } で無効化
-- JDBC: prepareThreshold=0 で無効化
```

Reference: [Prepared Statements with Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pool-modes)
