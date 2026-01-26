# Supabase 実装ガイド（分割）: ディレクトリ構成/型定義

## 3. ディレクトリ構成

### 3.1 標準構成

```
supabase/
├── config.toml              # Supabaseプロジェクト設定
├── migrations/              # データベースマイグレーション（スキーマ、関数、RLS）
│   ├── 20250101000000_initial_schema.sql
│   ├── 20250102000000_create_function_sel_users.sql
│   ├── 20250103000000_create_function_ins_order.sql
│   └── 20250104000000_add_rls_policies.sql
├── db-functions/            # Database Functions開発用（オプション）
│   ├── sel_users.sql
│   ├── ins_order.sql
│   └── upd_user_profile.sql
└── functions/               # Edge Functions
    ├── _shared/             # 共通モジュール・型定義
    │   ├── database.types.ts   # Supabase型定義（自動生成）
    │   ├── cors.ts            # CORS対応ヘルパー
    │   ├── auth.ts            # 認証ヘルパー
    │   ├── logger.ts          # ログ出力ヘルパー
    │   ├── response.ts        # レスポンスヘルパー
    │   ├── supabase.ts        # Supabaseクライアント
    │   └── validation.ts      # バリデーションヘルパー
    ├── get-user-data/
    │   └── index.ts
    ├── create-order/
    │   └── index.ts
    └── webhook-handler/
        └── index.ts
```

### 3.2 _shared フォルダと型定義

#### _shared フォルダの役割

`_shared` フォルダは、複数の Edge Functions で共有するモジュールや型定義を配置します。

**主な共通モジュール**:
- `database.types.ts`: Supabase から自動生成される型定義
- `cors.ts`: CORS ヘッダーの設定
- `auth.ts`: 認証処理のヘルパー関数
- `logger.ts`: ログ出力のヘルパー関数
- `response.ts`: レスポンス生成のヘルパー関数
- `supabase.ts`: Supabase クライアントの初期化
- `validation.ts`: リクエストのバリデーション

#### database.types.ts の生成方法

`database.types.ts` は、Supabase の型定義を自動生成します。データベーススキーマを変更した際は、必ずこのファイルを再生成してください。

**生成コマンド**:

```bash
npx --yes supabase gen types typescript --schema public --local > supabase/functions/_shared/database.types.ts
```

**実行タイミング**:
- データベースマイグレーション後
- テーブル定義を変更した後
- Database Functions を追加・変更した後

**生成される型**:
- `Database`: 全体のデータベース型定義
- `Tables`: テーブルの型（`Tables["table_name"]` で参照）
- Database Functions の型（`Database["public"]["Functions"]["function_name"]["Returns"]` で参照）
- `Enums`: Enum 型の定義
- `CompositeTypes`: 複合型の定義

> 💡 **重要**: データベーススキーマを変更したら、必ず型定義を再生成してください。型定義が古いままだと、Edge Functions で型エラーが発生する可能性があります。

**ワークフロー例**:

```bash
# 1. マイグレーションを適用
supabase db push

# 2. 型定義を再生成
npx --yes supabase gen types typescript --schema public --local > supabase/functions/_shared/database.types.ts

# 3. Edge Functions をデプロイ
supabase functions deploy function-name --project-ref your-project-id
```

#### logger.ts（構造化ロガー）

`logger.ts` は、Supabase Edge Functions（Deno）向けの軽量な構造化ロガーです。requestId によるリクエスト相関と簡便な出力メソッドを提供します。

**主な機能**:
- リクエストごとの一意な `requestId` 生成
- 構造化 JSON ログ出力
- センシティブデータの自動マスキング
- JWT からのユーザー ID 抽出

**サンプルコード**:

```typescript
// Supabase Edge Functions（Deno）向けの軽量な構造化ロガー
// requestId によるリクエスト相関と簡便な出力メソッドを提供します

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

type JsonValue = string | number | boolean | null | JsonValue[] | { [k: string]: JsonValue };

type StartMeta = {
  function?: string;
};

type EndMeta = {
  errorMessage?: string;
};

function loadMaskTargetsFromEnv(): Set<string> {
  const fallback = [
    "password",
    "pass",
    "pwd",
    "email",
    "lastName",
    "firstName",
    "postalCode1",
    "postalCode2",
    "prefecture",
    "city",
    "address",
    "building",
    "phone",
    "tel",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "auth",
    "jwt",
  ];
  try {
    const raw = Deno.env.get("MASK_TARGETS");
    if (!raw) return new Set(fallback);
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      const keys = parsed.filter((v) => typeof v === "string");
      return new Set(keys.length > 0 ? keys : fallback);
    }
    return new Set(fallback);
  } catch {
    return new Set(fallback);
  }
}

const SENSITIVE_KEYS = loadMaskTargetsFromEnv();

function maskSensitiveData<T extends Record<string, unknown>>(obj: T): Record<string, JsonValue> {
  const result: Record<string, JsonValue> = {};
  for (const [k, v] of Object.entries(obj ?? {})) {
    if (SENSITIVE_KEYS.has(k)) {
      result[k] = "***";
      continue;
    }
    if (v && typeof v === "object" && !Array.isArray(v)) {
      result[k] = maskSensitiveData(v as Record<string, unknown>);
    } else if (Array.isArray(v)) {
      result[k] = v.map((item) =>
        typeof item === "object" && item !== null
          ? maskSensitiveData(item as Record<string, unknown>)
          : (item as JsonValue)
      ) as JsonValue;
    } else {
      result[k] = (v as JsonValue) ?? null;
    }
  }
  return result;
}

function pickRequestInfo(req: Request) {
  const urlObj = new URL(req.url);
  const method = req.method;
  const path = urlObj.pathname;
  const searchParams: Record<string, string> = {};
  for (const [k, v] of urlObj.searchParams.entries()) {
    searchParams[k] = v;
  }
  const userAgent = req.headers.get("user-agent") || req.headers.get("User-Agent") || "";
  const contentType = req.headers.get("content-type") || req.headers.get("Content-Type") || "";
  const hasAuthorization = !!(req.headers.get("authorization") || req.headers.get("Authorization"));
  const acceptLanguage =
    req.headers.get("accept-language") || req.headers.get("Accept-Language") || "";
  return {
    method,
    path,
    query: searchParams,
    headers: { userAgent, contentType, authorizationPresent: hasAuthorization, acceptLanguage },
  };
}

function safeSerializeError(err: unknown) {
  if (err instanceof Error) {
    return { name: err.name, message: err.message, stack: err.stack };
  }
  try {
    return typeof err === "object"
      ? maskSensitiveData((err as Record<string, unknown>) ?? {})
      : { message: String(err) };
  } catch {
    return { message: "Unknown error" };
  }
}

async function extractUserIdFromRequest(req: Request): Promise<string | null> {
  const supabaseUrl = Deno.env.get("SUPABASE_URL");
  const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  // 認証ヘッダから JWT を受け取って検証し、sub を user_id として扱う
  const authHeader = req.headers.get("authorization") ?? req.headers.get("Authorization");
  if (!authHeader || !/^Bearer\s+/.test(authHeader)) {
    return null;
  }
  const jwt = authHeader.replace(/^Bearer\s+/i, "");
  const supabase = createClient(supabaseUrl, serviceRoleKey, { auth: { persistSession: false } });
  try {
    // jwt を検証してユーザー情報取得（Edge では getUser で検証可能）
    const { data: userResult, error: userError } = await supabase.auth.getUser(jwt);
    if (userError || !userResult?.user) {
      return null;
    }
    const authUserId = userResult.user.id; // JWT の sub（auth_user_id）
    return authUserId;
  } catch {
    return null;
  }
}

export async function createRequestLogger(req: Request) {
  // 各 HTTP リクエストごとに新しい requestId を生成します
  const requestId = globalThis.crypto?.randomUUID?.() ?? Math.random().toString(36).slice(2);
  const startedAt = globalThis.performance?.now ? globalThis.performance.now() : Date.now();
  const base = pickRequestInfo(req);
  const userId = await extractUserIdFromRequest(req);

  function log(
    level: "info" | "warn" | "error" | "log",
    message: string,
    extra?: Record<string, unknown>
  ) {
    const maskedExtra =
      extra && typeof extra === "object"
        ? maskSensitiveData(extra as Record<string, unknown>)
        : undefined;
    const payload = {
      level,
      ts: new Date().toISOString(),
      requestId,
      method: base.method,
      path: base.path,
      ...(userId ? { userId } : {}),
      ...(maskedExtra ?? {}),
      message,
    } as Record<string, unknown>;
    try {
      const out = JSON.stringify(payload);
      switch (level) {
        case "error":
          console.error(out);
          break;
        case "warn":
          console.warn(out);
          break;
        case "info":
          console.info(out);
          break;
        default:
          console.log(out);
      }
    } catch {
      // 失敗時はプレーン文字列でフォールバック
      const fallback = `[${level}] ${message} requestId=${requestId}`;
      switch (level) {
        case "error":
          console.error(fallback);
          break;
        case "warn":
          console.warn(fallback);
          break;
        case "info":
          console.info(fallback);
          break;
        default:
          console.log(fallback);
      }
    }
  }

  function LoggingStart(
    meta?: StartMeta,
    bodyOrQuery?: { body?: unknown; query?: Record<string, unknown> }
  ) {
    const query = (bodyOrQuery?.query as Record<string, unknown>) || base.query || {};
    const body =
      bodyOrQuery?.body && typeof bodyOrQuery.body === "object"
        ? (bodyOrQuery.body as Record<string, unknown>)
        : undefined;
    log("info", "request_start", {
      ...meta,
      request: {
        method: base.method,
        path: base.path,
        headers: base.headers,
        query,
        body,
      },
    });
  }

  function LoggingEnd(status: number, meta?: EndMeta) {
    const endedAt = globalThis.performance?.now ? globalThis.performance.now() : Date.now();
    const durationMs = Math.max(0, Math.round(endedAt - startedAt));
    log("info", "request_end", {
      status,
      durationMs,
      ...(meta?.errorMessage ? { errorMessage: meta.errorMessage } : {}),
    });
  }

  function LoggingError(error: unknown, meta?: Record<string, unknown>) {
    const serialized = safeSerializeError(error);
    log("error", "error", { ...meta, error: serialized });
  }

  function LoggingInfo(message: string, meta?: Record<string, unknown>) {
    log("info", message, meta);
  }

  function LoggingWarn(message: string, meta?: Record<string, unknown>) {
    log("warn", message, meta);
  }

  return {
    LoggingStart,
    LoggingEnd,
    LoggingError,
    LoggingInfo,
    LoggingWarn,
  };
}
```

**使用例**:

```typescript
import { createRequestLogger } from "../_shared/logger.ts";

Deno.serve(async (req) => {
  const logger = await createRequestLogger(req);

  // リクエスト開始ログ
  logger.LoggingStart({ function: "get-user-data" });

  try {
    // 処理...
    logger.LoggingInfo("処理中", { step: "validation" });

    // 成功時
    logger.LoggingEnd(200);
    return new Response(JSON.stringify({ success: true }), { status: 200 });
  } catch (err) {
    // エラーログ
    logger.LoggingError(err, { context: "main process" });
    logger.LoggingEnd(500, { errorMessage: err.message });
    return new Response(JSON.stringify({ error: "Internal error" }), { status: 500 });
  }
});
```

### 3.3 Database Functions の管理方法

Database Functions（PostgreSQL関数）は**マイグレーションファイルとして管理**します。

#### パターン A: migrations のみで管理（推奨・シンプル）

すべて `migrations/` フォルダで管理します。

**メリット**:
- ✅ Supabase標準の構成
- ✅ バージョン管理が確実
- ✅ デプロイが自動化される

**デメリット**:
- ❌ ファイル名がタイムスタンプ付きで検索しづらい
- ❌ 開発中に何度も作り直すと番号が増える

#### パターン B: db-functions + migrations で管理（推奨・開発時）

開発用に `db-functions/` フォルダを作成し、完成したら `migrations/` に移します。

**メリット**:
- ✅ 関数ごとにファイル分割で管理しやすい
- ✅ 開発中は自由に編集できる
- ✅ 完成したらマイグレーションとして確定

**デメリット**:
- ❌ 二重管理になる可能性
- ❌ db-functions の内容が古くなるリスク

**運用方法**:
1. `db-functions/` で開発・SQL Editorでテスト
2. 完成したらマイグレーションファイル作成
   ```bash
   supabase migration new create_function_sel_users
   ```
3. `db-functions/sel_users.sql` の内容をマイグレーションファイルにコピー
4. マイグレーション適用
   ```bash
   supabase db push
   ```

> 💡 **推奨**: 小規模プロジェクトはパターンA、中〜大規模プロジェクトはパターンBを採用

### 3.4 db-functions フォルダの使い方（パターンBの場合）

`db-functions/` は開発・テスト用のワーキングディレクトリです。

```
db-functions/
├── README.md                # 使い方の説明
├── users/
│   ├── sel_user_by_id.sql
│   ├── sel_users_by_role.sql
│   └── upd_user_profile.sql
├── orders/
│   ├── sel_order_details.sql
│   ├── ins_order.sql
│   └── upd_order_status.sql
└── common/
    └── get_current_user.sql
```

**README.md の例**:
```markdown
# Database Functions

このフォルダは開発用です。完成した関数は migrations/ に移してください。

## 使い方

1. SQL Editorで動作確認
2. このフォルダに保存
3. 完成したらマイグレーション作成
   `supabase migration new create_function_xxx`
4. マイグレーションファイルにコピー
```

---
