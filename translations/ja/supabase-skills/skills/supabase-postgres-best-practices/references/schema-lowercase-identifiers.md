---
title: 互換性のため識別子は小文字を使う
impact: MEDIUM
impactDescription: ツール・ORM・AI アシスタントでの大文字小文字バグを回避
tags: naming, identifiers, case-sensitivity, schema, conventions
---

## 互換性のため識別子は小文字を使う

PostgreSQL は引用符なし識別子を小文字に正規化します。引用符付き mixed-case は永続的に引用が必要になり、各種ツールで問題を生みます。

**誤り（mixed-case 識別子）:**

```sql
-- Quoted identifiers preserve case but require quotes everywhere
CREATE TABLE "Users" (
  "userId" bigint PRIMARY KEY,
  "firstName" text,
  "lastName" text
);

-- Must always quote or queries fail
SELECT "firstName" FROM "Users" WHERE "userId" = 1;

-- This fails - Users becomes users without quotes
SELECT firstName FROM Users;
-- ERROR: relation "users" does not exist
```

**正しい例（小文字 snake_case）:**

```sql
-- Unquoted lowercase identifiers are portable and tool-friendly
CREATE TABLE users (
  user_id bigint PRIMARY KEY,
  first_name text,
  last_name text
);

-- Works without quotes, recognized by all tools
SELECT first_name FROM users WHERE user_id = 1;
```

mixed-case が生まれる典型例:

```sql
-- ORMs often generate quoted camelCase - configure them to use snake_case
-- Migrations from other databases may preserve original casing
-- Some GUI tools quote identifiers by default - disable this

-- If stuck with mixed-case, create views as a compatibility layer
CREATE VIEW users AS SELECT "userId" AS user_id, "firstName" AS first_name FROM "Users";
```

Reference: [Identifiers and Key Words](https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS)
