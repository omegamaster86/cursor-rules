## 8. ログ出力規約

Next.js（Server Actions、Route Handlers）でのログ出力に関する規約を定義します。

### 8.1 基本方針

- **共通の logger を使用する**: `src/services/logger.ts` に定義した共通ロガーを使用する
- **構造化ログを出力する**: JSON形式で出力し、ログ解析ツールで検索しやすくする
- **センシティブデータをマスキングする**: パスワード、トークン、個人情報は自動的にマスキングする
- **requestId でリクエストを追跡する**: 1つのリクエスト内のログを関連付ける

### 8.2 logger.ts の配置

```
src/
└── services/
    └── logger.ts    # 共通ロガー
```

### 8.3 logger.ts のサンプルコード

```typescript
// src/services/logger.ts
// Next.js（Server Actions / Route Handlers）向けの軽量な構造化ロガー

type JsonValue = string | number | boolean | null | JsonValue[] | { [k: string]: JsonValue };

type LogMeta = {
  action?: string;
  [key: string]: unknown;
};

// マスキング対象のキー（環境変数で上書き可能）
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
    const raw = process.env.MASK_TARGETS;
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

export function createLogger(actionName?: string) {
  const requestId = crypto.randomUUID();
  const startedAt = performance.now();

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
      ...(actionName ? { action: actionName } : {}),
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

  function start(meta?: LogMeta) {
    log("info", "action_start", meta);
  }

  function end(meta?: { success: boolean; errorMessage?: string }) {
    const endedAt = performance.now();
    const durationMs = Math.max(0, Math.round(endedAt - startedAt));
    log("info", "action_end", {
      success: meta?.success ?? true,
      durationMs,
      ...(meta?.errorMessage ? { errorMessage: meta.errorMessage } : {}),
    });
  }

  function error(err: unknown, meta?: Record<string, unknown>) {
    const serialized = safeSerializeError(err);
    log("error", "error", { ...meta, error: serialized });
  }

  function info(message: string, meta?: Record<string, unknown>) {
    log("info", message, meta);
  }

  function warn(message: string, meta?: Record<string, unknown>) {
    log("warn", message, meta);
  }

  return {
    start,
    end,
    error,
    info,
    warn,
    requestId,
  };
}
```

### 8.4 使用例

#### Server Actions での使用

```typescript
// src/actions/userActions.ts
"use server";

import { createLogger } from "@/services/logger";

export async function updateUserProfile(formData: FormData) {
  const logger = createLogger("updateUserProfile");
  logger.start({ userId: formData.get("userId") });

  try {
    // バリデーション
    const name = formData.get("name");
    if (!name) {
      logger.warn("validation_failed", { field: "name" });
      logger.end({ success: false, errorMessage: "名前は必須です" });
      return { success: false, error: "名前は必須です" };
    }

    // DB更新処理
    logger.info("db_update_start", { table: "users" });
    // ... 更新処理 ...
    logger.info("db_update_completed", { affectedCount: 1 });

    logger.end({ success: true });
    return { success: true };
  } catch (err) {
    logger.error(err, { context: "updateUserProfile" });
    logger.end({ success: false, errorMessage: "予期せぬエラーが発生しました" });
    return { success: false, error: "予期せぬエラーが発生しました" };
  }
}
```

#### Route Handlers での使用

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from "next/server";
import { createLogger } from "@/services/logger";

export async function GET(request: NextRequest) {
  const logger = createLogger("GET /api/users");
  logger.start({
    method: "GET",
    path: request.nextUrl.pathname,
    query: Object.fromEntries(request.nextUrl.searchParams),
  });

  try {
    // ... データ取得処理 ...
    const users = []; // 取得結果

    logger.info("data_fetched", { recordCount: users.length });
    logger.end({ success: true });

    return NextResponse.json({ success: true, data: users });
  } catch (err) {
    logger.error(err);
    logger.end({ success: false, errorMessage: "データ取得に失敗しました" });

    return NextResponse.json(
      { success: false, error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
```

### 8.5 ログ出力のタイミング

| タイミング | メソッド | 必須 | 備考 |
|------------|----------|------|------|
| 処理開始時 | `logger.start()` | ✅ | アクション名、パラメータを記録 |
| 処理終了時 | `logger.end()` | ✅ | 成否、処理時間を記録 |
| DB操作後 | `logger.info()` | 推奨 | 影響件数を記録 |
| 外部API呼び出し前後 | `logger.info()` | 推奨 | 成否、レスポンス時間を記録 |
| バリデーションエラー | `logger.warn()` | 推奨 | 不正な入力を記録 |
| 業務エラー | `logger.warn()` | 推奨 | 想定済みのエラーを記録 |
| 例外発生時 | `logger.error()` | ✅ | スタックトレースを含めて記録 |

### 8.6 出力例

```json
{"level":"info","ts":"2025-12-04T10:00:00.000Z","requestId":"abc123-...","action":"updateUserProfile","userId":"123","message":"action_start"}
{"level":"info","ts":"2025-12-04T10:00:00.050Z","requestId":"abc123-...","action":"updateUserProfile","table":"users","message":"db_update_start"}
{"level":"info","ts":"2025-12-04T10:00:00.100Z","requestId":"abc123-...","action":"updateUserProfile","affectedCount":1,"message":"db_update_completed"}
{"level":"info","ts":"2025-12-04T10:00:00.150Z","requestId":"abc123-...","action":"updateUserProfile","success":true,"durationMs":150,"message":"action_end"}
```

---
