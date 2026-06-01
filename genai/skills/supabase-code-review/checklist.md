# レビューチェックリスト詳細

SKILL.md の各観点に対応する詳細なチェック項目。

## A. セキュリティ

### 認証（CRITICAL）

- [ ] Edge Function で `getAuthUser()` を呼び出し、`getUser()` でJWTを検証している
- [ ] `getSession()` のみで認証判定していない
- [ ] 認証エラー時に 401 レスポンスを返している
- [ ] Authorization ヘッダーの存在チェックがある
- [ ] 管理者向けAPIでは `checkAdminUser()` による権限チェックがある

### RLS（CRITICAL）

- [ ] 新規テーブルには `enable row level security` が設定されている
- [ ] 必要な操作（SELECT/INSERT/UPDATE/DELETE）にポリシーが設定されている
- [ ] ポリシーの条件が最小権限の原則に従っている（`auth.uid()` の適切な使用）
- [ ] `service_role` キーの使用は必要最小限

### DB Function セキュリティ

- [ ] `SECURITY DEFINER` が適切に設定されている
- [ ] `SET search_path = public` が `SECURITY DEFINER` とセットで指定されている
- [ ] `GRANT EXECUTE ON FUNCTION ... TO authenticated` で実行権限を付与している
- [ ] SQL インジェクションの余地がない（動的SQLを使う場合は `format()` / `quote_ident()` を使用）

### データ保護

- [ ] パスワード、トークン、個人情報がログに出力されていない
- [ ] レスポンスに不要なセンシティブデータが含まれていない
- [ ] 環境変数を直接レスポンスに公開していない

## B. DB Function（PostgreSQL）

### 命名規則

| プレフィックス | 用途 | 例 |
|---------------|------|-----|
| `sel_` | SELECT（取得） | `sel_user_by_id` |
| `ins_` | INSERT（登録） | `ins_user` |
| `upd_` | UPDATE（更新） | `upd_user_profile` |
| `del_` | DELETE（削除） | `del_user` |
| `upsert_` | UPSERT（登録更新） | `upsert_user_settings` |
| `validate_` | 検証 | `validate_takkenshi_questions_by_exam_id` |

- [ ] 関数名がプレフィックス規則に従っている
- [ ] 関数名から用途が明確にわかる
- [ ] 引数名にプレフィックス（`target_`, `p_` など）が付いており、カラム名と衝突しない

### 基本構文

```sql
CREATE FUNCTION public.sel_xxx(target_id BIGINT)
RETURNS TABLE(...)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  RETURN QUERY
  SELECT ...
  FROM ...
  WHERE ... AND deleted_at IS NULL;
END;
$$;
```

- [ ] `create or replace function` または `DROP FUNCTION IF EXISTS` + `CREATE FUNCTION` を使用
- [ ] `LANGUAGE plpgsql` を指定
- [ ] レスポンス型（`RETURNS TABLE` / `RETURNS bigint` / `RETURNS void`）が適切に定義されている
- [ ] テーブルエイリアスを使用し、カラム名が明確
- [ ] 論理削除対象テーブルでは `deleted_at IS NULL` 条件がある

### GRANT / COMMENT

- [ ] `GRANT EXECUTE ON FUNCTION public.xxx(...) TO authenticated` が記述されている
- [ ] `COMMENT ON FUNCTION` で関数の目的が説明されている

## C. Migration ファイル

### ファイル命名

```
YYYYMMDDHHMMSS_create_function_<関数名>.sql
YYYYMMDDHHMMSS_create_<テーブル名>_tables.sql
YYYYMMDDHHMMSS_add_rls_policies.sql
```

- [ ] タイムスタンプ形式 `YYYYMMDDHHMMSS` で始まっている
- [ ] ファイル名から内容（テーブル作成/関数作成/RLS追加）がわかる
- [ ] DB Function の migration は `create_function_` プレフィックスがついている

### ファイル構成

- [ ] ファイル先頭にコメントブロックで目的・返却列・注意事項が記載されている
- [ ] 1ファイルに1つの関数/テーブル定義（原則）
- [ ] `DROP FUNCTION IF EXISTS` で既存関数を削除してから `CREATE FUNCTION` している（冪等性）

### テーブル定義

- [ ] 主キー（`id`）が適切に定義されている
- [ ] `created_at` / `updated_at` カラムがある
- [ ] 論理削除が必要なテーブルには `deleted_at` カラムがある
- [ ] 外部キー制約が適切に設定されている
- [ ] NOT NULL 制約が必要なカラムに設定されている

## D. Edge Function テンプレート

### 基本構造

```typescript
import { getAuthUser } from "@shared/auth.ts";
import { createLogger } from "@shared/logger.ts";
import { createSuccessResponse, createErrorResponse, ... } from "@shared/response.ts";
import { createAuthenticatedClient } from "@shared/supabase.ts";

Deno.serve(async (req) => {
  const logger = createLogger("function-name");
  logger.start({ method: req.method, url: req.url });
  // メソッド制限 → 認証 → ビジネスロジック → レスポンス
});
```

- [ ] `_shared/` の共有モジュールからインポートしている
- [ ] `Deno.serve(async (req) => { ... })` のパターンに従っている
- [ ] ファイル先頭にJSDocコメントで関数の目的を記述している
- [ ] 処理順序がテンプレート通り（メソッド制限 → 認証 → ロジック → レスポンス）
- [ ] CORS関連の処理が含まれていない（OPTIONSハンドリング、`handleOptionsRequest`、CORSヘッダー設定など。Server Componentから呼び出すためCORSは不要）

### レスポンス

- [ ] `createSuccessResponse()` / `createErrorResponse()` を使用している
- [ ] `createMethodNotAllowedResponse()` でメソッド制限している
- [ ] `createAuthErrorResponse()` で認証エラーを返している
- [ ] `createBadRequestResponse()` でバリデーションエラーを返している
- [ ] 直接 `new Response()` を使用していない（共有モジュール経由が必須）

### RPC 呼び出し

- [ ] `supabase.rpc("関数名", { ... })` で DB Function を呼び出している
- [ ] `error` チェック後に適切なエラーレスポンスを返している
- [ ] RPC の引数名が DB Function の引数名と一致している

## E. 認証

### 認証フロー

- [ ] `req.headers.get("Authorization")` でトークンを取得
- [ ] `createAuthenticatedClient(authHeader)` で認証付きクライアントを作成
- [ ] `getAuthUser(supabase)` でユーザー情報を取得
- [ ] `auth.user.id` で認証ユーザーID（UUID）を使用

### HTTPメソッド制限

- [ ] GET のみの API は `req.method !== "GET"` で制限
- [ ] POST/PUT/DELETE を含む API は許可メソッドを明示

### CORS不要の確認

> Edge FunctionはServer Componentから呼び出すため、CORS処理は不要。

- [ ] `@shared/cors.ts` をインポートしていない
- [ ] `handleOptionsRequest` を呼び出していない
- [ ] `req.method === "OPTIONS"` のハンドリングがない
- [ ] レスポンスヘッダーに `Access-Control-Allow-Origin` を設定していない

## F. ログ出力

### 基本

- [ ] `createLogger("function-name")` でロガーを初期化（関数名は Edge Function のディレクトリ名と一致）
- [ ] `console.log` / `console.error` を直接使用していない（_shared内は例外）

### タイミング

- [ ] `logger.start({ method, url })` でリクエスト開始を記録
- [ ] `logger.end({ success })` で処理終了を記録（全ての return パスで呼び出し）
- [ ] エラー発生時に `logger.error(err, { context })` で記録
- [ ] DB Function 呼び出し前後で `logger.info()` を出力
- [ ] 認証成功/失敗で `logger.info()` / `logger.warn()` を出力
- [ ] バリデーションエラーで `logger.warn()` を出力

### 注意事項

- [ ] センシティブデータ（パスワード、トークン等）をログに含めていない
- [ ] `logger.end()` が全ての return パス（正常系・エラー系・例外系）で呼ばれている

## G. 型定義

### database.types.ts

- [ ] DB Function 追加/変更後に `database.types.ts` が再生成されている
- [ ] Edge Function で `database.types.ts` から型をインポートしている
- [ ] `any` 型を使用していない
- [ ] 型アサーション (`as`) を最小限にしている

### 型の使用

```typescript
import type { Database } from "../_shared/database.types.ts";
type UserData = Database["public"]["Functions"]["sel_user_by_auth_id"]["Returns"][0];
```

- [ ] DB Function の戻り値は `Database["public"]["Functions"]` から型を参照
- [ ] テーブル型は `Tables["テーブル名"]` または `Database["public"]["Tables"]` から参照
- [ ] `type` を使用している（`interface` ではなく、外部ライブラリ型の拡張を除く）

## H. 命名規則

### Edge Function ディレクトリ名

| パターン | 例 |
|----------|-----|
| `get-<リソース>` | `get-exams`, `get-admin-user` |
| `create-<リソース>` | `create-exam` |
| `update-<リソース>` | `update-submission` |
| `<動詞>-<リソース>` | `process-ocr`, `admin-login` |

- [ ] ケバブケース（小文字 + ハイフン）
- [ ] 操作が明確にわかる命名

### Migration ファイル名

- [ ] `YYYYMMDDHHMMSS_create_function_<関数名>.sql`（DB Function）
- [ ] `YYYYMMDDHHMMSS_create_<説明>_tables.sql`（テーブル）
- [ ] スネークケース（小文字 + アンダースコア）

### SQL

- [ ] テーブル名: スネークケース（`m_exam`, `t_submission`）
- [ ] カラム名: スネークケース（`created_at`, `auth_user_id`）
- [ ] 関数名: スネークケース + プレフィックス（`sel_`, `ins_` 等）
- [ ] SQL キーワード: 大文字（`SELECT`, `FROM`, `WHERE`）

### ベストプラクティス

- [ ] Edge Function 内で `new Date()` を使用していない（日付はクライアントから受け取る）
- [ ] 3層アーキテクチャに従っている（Edge Function → DB Function → DB）
- [ ] 複雑なクエリは DB Function にまとめている
- [ ] トランザクションが必要な処理は DB Function で実装している
