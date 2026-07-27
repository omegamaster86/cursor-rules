# レビューチェックリスト詳細

## A. セキュリティ

### 認証（CRITICAL）

- [ ] 標準 Edge は `handler()`（内部で `getClaims`）を使っている
- [ ] 管理者 API は `requireAdmin: true`（旧 `checkAdminUser` ではない）
- [ ] 認証エラー時に 401 相当を返している
- [ ] webhook / cron は代替認証（署名 / CRON_KEY）がある

### RLS（CRITICAL）

- [ ] 新規テーブルに RLS 有効化（`schemas/rls`）
- [ ] `04_grants.sql` 等で GRANT が明示されている
- [ ] `get_current_user_id()` / `is_admin()` 等のヘルパー利用が妥当
- [ ] `service_role` の使用はオーケストレーションに限定され、所有権チェックがある

### DB Function セキュリティ

- [ ] 機密・RLS バイパスが必要な関数は `SECURITY DEFINER` + `search_path`
- [ ] 「全関数に DEFINER / GRANT EXECUTE 必須」ではない — カテゴリに応じて判断
- [ ] 動的 SQL は `format()` / `quote_ident()` 等で安全化

### データ保護 / 環境変数

- [ ] センシティブデータをログ・レスポンスに出していない
- [ ] 環境変数未設定時の扱いが明確（空文字放置を避ける）

## B. schemas / DB Function

### 正本

- [ ] テーブル・関数変更は `schemas/` を編集している
- [ ] 関数は `schemas/functions/<name>.sql`（1ファイル1関数）

### 命名

| プレフィックス | 用途 |
|---------------|------|
| `sel_` / `ins_` / `upd_` / `del_` / `upsert_` | CRUD |

- [ ] 引数は新規 `p_` 優先（レガシー `target_` 共存可）

## C. Migration

### ファイル命名

```
YYYYMMDDHHMMSS_<snake_description>.sql
# 例: 20260721000000_add_todo_detail_crud.sql
```

- [ ] `db diff -f <name>` 由来の分かりやすい description
- [ ] 旧 `*_create_function_*` はレガシー例（必須ではない）

### 内容

- [ ] 生成 SQL をレビュー済み
- [ ] DML / cron 等 diff 不能なものは手書きまたは seed

## D. Edge Function

### 標準テンプレート

- [ ] `handler()` + Zod（`_shared/schemas`）
- [ ] レスポンスは `ctx.success` / `ctx.error`（`{ success, data | error }`）
- [ ] 既定 method は POST。GET は `{ methods: ["GET"] }`
- [ ] CRUD は `ctx.callRpc` 優先
- [ ] Stripe/FCM 等の `.from()` は認可・ログ付きで意図的か

### 例外

- [ ] webhook / cron / health は [edge-exceptions](../supabase-implementation/rules/edge-exceptions.md) に沿う
- [ ] `config.toml` の `verify_jwt` が意図どおり

## E. ログ

- [ ] 標準は handler 内包（`createRequestLogger`）
- [ ] 旧 `createLogger` / `createSuccessResponse` を使っていない

## F. 型定義

- [ ] スキーマ変更後に `npm run sb:types:gen`
- [ ] Web / Edge の `database.types.ts` が同期

## G. 命名・パス

- [ ] 配置は `backend/supabase/`
- [ ] Edge フォルダ名は kebab-case 機能名
