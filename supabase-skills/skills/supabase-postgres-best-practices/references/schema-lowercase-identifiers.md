---
title: 互換性のために識別子は小文字で統一する
impact: MEDIUM
impactDescription: ツール/ORM/AI での大文字小文字問題を回避
tags: naming, identifiers, case-sensitivity, schema, conventions
---

## 互換性のために識別子は小文字で統一する

PostgreSQL は引用符なしの識別子を小文字に折りたたみます。引用符付きの混在ケースは常に引用が必要になり、ツール/ORM/AI が認識できず問題になります。

**Incorrect (混在ケースの識別子):**

```sql
-- 引用符付き識別子は大文字小文字を保持するが、常に引用が必要
CREATE TABLE "Users" (
  "userId" bigint PRIMARY KEY,
  "firstName" text,
  "lastName" text
);

-- 常に引用しないと失敗
SELECT "firstName" FROM "Users" WHERE "userId" = 1;

-- これは失敗する - Users が users に折りたたまれる
SELECT firstName FROM Users;
-- ERROR: relation "users" does not exist
```

**Correct (小文字の snake_case):**

```sql
-- 引用なしの小文字は移植性が高く、ツールに優しい
CREATE TABLE users (
  user_id bigint PRIMARY KEY,
  first_name text,
  last_name text
);

-- 引用なしで動作し、すべてのツールで認識
SELECT first_name FROM users WHERE user_id = 1;
```

混在ケースが生まれる典型例:

```sql
-- ORM が camelCase を引用して生成することがある -> snake_case に設定
-- 他 DB からの移行で元の大文字小文字が残る
-- GUI ツールがデフォルトで引用する場合がある -> 無効化

-- どうしても混在ケースの場合は互換ビューを作る
CREATE VIEW users AS SELECT "userId" AS user_id, "firstName" AS first_name FROM "Users";
```

Reference: [Identifiers and Key Words](https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS)
