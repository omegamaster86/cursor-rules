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

---
