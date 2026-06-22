---
title: Database Functions Syntax
impact: HIGH
impactDescription: PostgreSQL 関数の基本構文と命名規則
tags: supabase, database-functions, postgresql
---

## Database Functions Syntax

Database Functions（PostgreSQL関数）の基本構文と命名規則です。

**基本構文：**

```sql
create or replace function sel_user_by_id(target_user_id bigint)
returns TABLE(
  id bigint,
  email text,
  display_name text,
  created_at timestamptz
)
language plpgsql
as $$
begin
  return query
  select
    u.id,
    u.email,
    u.display_name,
    u.created_at
  from
    users u
  where
    u.id = target_user_id
    and u.deleted_at is null
  ;
end;
$$;
```

**命名規則：**

| プレフィックス | 用途 | 例 |
|---------------|------|-----|
| `sel_` | SELECT（取得） | `sel_user_by_id` |
| `ins_` | INSERT（登録） | `ins_user` |
| `upd_` | UPDATE（更新） | `upd_user_profile` |
| `del_` | DELETE（削除） | `del_user` |
| `upsert_` | UPSERT（登録更新） | `upsert_user_settings` |

**レスポンス型の定義：**

```sql
-- レコードを返す場合
returns TABLE(
  id bigint,
  name text
)

-- 単一の値を返す場合
returns bigint

-- VOID（戻り値なし）
returns void
```

**実装手順：**

1. SQL Editor で開発・動作確認
2. 期待通りに動作することを確認
3. マイグレーションファイルとして保存

```bash
supabase migration new create_function_sel_xxx
```

**チェックリスト：**

- [ ] 命名規則に従っている
- [ ] SQL Editor で動作確認済み
- [ ] マイグレーションファイルに保存
- [ ] レスポンス型が適切に定義されている
