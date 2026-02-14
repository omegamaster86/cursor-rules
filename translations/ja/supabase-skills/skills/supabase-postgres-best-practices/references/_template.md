---
title: 明確でアクション指向のタイトル（例: "フィルタ条件付きクエリには部分インデックスを使う"）
impact: MEDIUM
impactDescription: フィルタ付きクエリで 5-20 倍の高速化
tags: indexes, query-optimization, performance
---

## [ルールタイトル]

[問題点と重要性を 1-2 文で説明。性能への影響に焦点を当てる。]

**誤り（問題のあるパターン）:**

```sql
-- Comment explaining what makes this slow/problematic
CREATE INDEX users_email_idx ON users(email);

SELECT * FROM users WHERE email = 'user@example.com' AND deleted_at IS NULL;
-- This scans deleted records unnecessarily
```

**正しい例（解決策）:**

```sql
-- Comment explaining why this is better
CREATE INDEX users_active_email_idx ON users(email) WHERE deleted_at IS NULL;

SELECT * FROM users WHERE email = 'user@example.com' AND deleted_at IS NULL;
-- Only indexes active users, 10x smaller index, faster queries
```

[任意: 追加の文脈、エッジケース、トレードオフ]

Reference: [Postgres Docs](https://www.postgresql.org/docs/current/)
