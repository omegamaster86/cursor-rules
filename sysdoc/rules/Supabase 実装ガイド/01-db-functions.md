# Supabase 実装ガイド（分割）: Database Functions

## 1. Database Functions（SQL）

### 1.1 基本構文

Database Functions は PostgreSQL の関数として実装します。

```sql
create or replace function sel_XXX(YYY 型)  -- sel_XXX(YYY 型)はファンクション名と引数を定義する。引数はなければ未定義でよい
-- レスポンスを定義する。例は複数レコードの結果を返却する場合
returns TABLE(
  id bigint,
  title text,
  row_number bigint,
  column_number bigint
)
language plpgsql
as $$
begin
  return query
  -- SQLを記載する
  select
    *
  from
    m_bingo_sheet mbs
  inner join
    m_bingo_cell mbc
  on
    mbc.bingo_sheet_id = mbs.id
  where
    mbs.id = target_id
  ;
  -- SQLを記載する
end;
$$;
```

### 1.2 命名規則

| プレフィックス | 用途               | 例                     |
| -------------- | ------------------ | ---------------------- |
| `sel_`         | SELECT（取得）     | `sel_user_by_id`       |
| `ins_`         | INSERT（登録）     | `ins_user`             |
| `upd_`         | UPDATE（更新）     | `upd_user_profile`     |
| `del_`         | DELETE（削除）     | `del_user`             |
| `upsert_`      | UPSERT（登録更新） | `upsert_user_settings` |

### 1.3 実装手順

SQLの強み（1回のクエリで完結、集合処理）を活かせるように設計・記述する。

1. **SQL Editor で開発**
   - Supabase Dashboard の SQL Editor を使用
   - 動作確認を行いながら実装

2. **期待通りに動作確認**
   - テストデータで実行
   - レスポンス形式が正しいか確認

3. **マイグレーションファイルとして保存**
   ```bash
   supabase migration new create_function_sel_xxx
   ```

> 💡 **重要**: SQLはSQL Editor上で動作確認をして、期待通りに動くものを記載するようにしてください。

### 1.4 レスポンス型の定義

**レコードを返す場合**:
```sql
returns TABLE(
  id bigint,
  name text
)
```

**単一の値を返す場合**:
```sql
returns bigint
```

**VOID（戻り値なし）**:
```sql
returns void
```

### 1.5 SQL パターン

#### UPSERT（INSERT ... ON CONFLICT）

SELECT → INSERT/UPDATE を別々に行うと競合が発生します。`ON CONFLICT` で原子的に処理してください。

```sql
-- ❌ 悪い例: チェック→挿入で競合が起きる
-- 2つのリクエストが同時に SELECT → 両方 INSERT を試行 → 片方がエラー

-- ✅ 良い例: 原子的な UPSERT
create or replace function upsert_user_settings(
  p_user_id bigint,
  p_key text,
  p_value text
)
returns void
language plpgsql
as $$
begin
  insert into user_settings (user_id, key, value)
  values (p_user_id, p_key, p_value)
  on conflict (user_id, key)
  do update set value = excluded.value, updated_at = now();
end;
$$;
```

> 💡 `on conflict ... do nothing` で「既存なら挿入しない」パターンも可能です。

#### カーソルベースのページネーション

OFFSET ベースはページが深くなるほど遅くなります（スキップした行をすべて走査）。カーソルベースは常に O(1) です。

```sql
-- ❌ 悪い例: OFFSET（10000ページ目 = 200,000行を走査）
select * from products order by id limit 20 offset 199980;

-- ✅ 良い例: カーソルベース（常にインデックススキャンで高速）
create or replace function sel_products_paged(
  p_last_id bigint default 0,
  p_limit int default 20
)
returns TABLE(id bigint, name text, price numeric, created_at timestamptz)
language plpgsql
as $$
begin
  return query
  select p.id, p.name, p.price, p.created_at
  from products p
  where p.id > p_last_id
  order by p.id
  limit p_limit;
end;
$$;
```

---
