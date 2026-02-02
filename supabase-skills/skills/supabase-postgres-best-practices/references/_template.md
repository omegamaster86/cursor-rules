---
title: 明確で行動指向のタイトル（例: "フィルタ付きクエリに部分インデックスを使う"）
impact: MEDIUM
impactDescription: フィルタ付きクエリで 5-20x 高速化
tags: indexes, query-optimization, performance
---

## [ルールタイトル]

[問題と重要性を 1-2 文で説明。パフォーマンスへの影響に焦点を当てる。]

**Incorrect (問題の説明):**

```sql
-- 遅い/問題がある理由を説明するコメント
CREATE INDEX users_email_idx ON users(email);

SELECT * FROM users WHERE email = 'user@example.com' AND deleted_at IS NULL;
-- 削除済みレコードまで不要にスキャンする
```

**Correct (解決策の説明):**

```sql
-- なぜ良いのかを説明するコメント
CREATE INDEX users_active_email_idx ON users(email) WHERE deleted_at IS NULL;

SELECT * FROM users WHERE email = 'user@example.com' AND deleted_at IS NULL;
-- アクティブユーザーのみをインデックス化し、インデックスは 10x 小さく、クエリも高速
```

[任意: 追加の文脈、エッジケース、トレードオフ]

Reference: [Postgres Docs](https://www.postgresql.org/docs/current/)
