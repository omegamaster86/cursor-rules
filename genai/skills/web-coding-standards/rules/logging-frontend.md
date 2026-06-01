---
title: Frontend Logging Rules
impact: HIGH
impactDescription: Next.js Server Actions/Route Handlers でのログ出力規約
tags: logging, next.js, server-actions, observability
---

## Frontend Logging Rules

Next.js（Server Actions、Route Handlers）でのログ出力に関する規約です。

### 基本方針

- **共通の logger を使用する**: `src/services/logger.ts` に定義した共通ロガーを使用
- **構造化ログを出力する**: JSON形式で出力し、ログ解析ツールで検索しやすくする
- **センシティブデータをマスキングする**: パスワード、トークン、個人情報は自動的にマスキング
- **requestId でリクエストを追跡する**: 1つのリクエスト内のログを関連付ける

### logger.ts の配置

```
src/
└── services/
    └── logger.ts    # 共通ロガー
```

### 使用例

#### Server Actions での使用

```typescript
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

### ログ出力のタイミング

| タイミング | メソッド | 必須 | 備考 |
|------------|----------|------|------|
| 処理開始時 | `logger.start()` | ✅ | アクション名、パラメータを記録 |
| 処理終了時 | `logger.end()` | ✅ | 成否、処理時間を記録 |
| DB操作後 | `logger.info()` | 推奨 | 影響件数を記録 |
| 外部API呼び出し前後 | `logger.info()` | 推奨 | 成否、レスポンス時間を記録 |
| バリデーションエラー | `logger.warn()` | 推奨 | 不正な入力を記録 |
| 業務エラー | `logger.warn()` | 推奨 | 想定済みのエラーを記録 |
| 例外発生時 | `logger.error()` | ✅ | スタックトレースを含めて記録 |

### 出力例

```json
{"level":"info","ts":"2025-12-04T10:00:00.000Z","requestId":"abc123-...","action":"updateUserProfile","userId":"123","message":"action_start"}
{"level":"info","ts":"2025-12-04T10:00:00.050Z","requestId":"abc123-...","action":"updateUserProfile","table":"users","message":"db_update_start"}
{"level":"info","ts":"2025-12-04T10:00:00.100Z","requestId":"abc123-...","action":"updateUserProfile","affectedCount":1,"message":"db_update_completed"}
{"level":"info","ts":"2025-12-04T10:00:00.150Z","requestId":"abc123-...","action":"updateUserProfile","success":true,"durationMs":150,"message":"action_end"}
```

**チェックリスト：**

- [ ] `createLogger` で共通ロガーを使用
- [ ] 処理開始時に `start()` を呼び出し
- [ ] 処理終了時に `end()` を呼び出し
- [ ] 例外発生時は `error()` でスタックトレースを記録
