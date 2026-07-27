---
title: Frontend Logging Rules
impact: HIGH
impactDescription: Next.js Server Actions/Route Handlers でのログ出力規約
tags: logging, next.js, server-actions, observability
---

## Frontend Logging Rules

Next.js（Server Actions、Route Handlers）でのログ出力に関する規約です。

### 基本方針

- **共通の logger を使用する**: `src/services/logger.ts` の `createLogger`
- **本番 Server Action は `handler()` を使う**: `start` / `end` / 例外時の `error` を内包する
- **構造化ログ**: JSON で出力し、`requestId` で追跡する
- **センシティブデータをマスキング**: パスワード・トークン・個人情報

### logger.ts の配置

```
src/
└── services/
    ├── logger.ts
    └── handler.ts    # createLogger / start / end を内包
```

### 標準: `handler()` 経由

```typescript
"use server";

import { actionError, handler, success, validate } from "@/services/handler";

export async function createTodo(
  _prevState: CreateTodoState,
  formData: FormData,
): Promise<CreateTodoState> {
  return handler(
    "createTodo",
    async (logger): Promise<CreateTodoState> => {
      // logger.start / end は handler が担う
      // ビジネス固有の info / warn だけここで書く
      const data = validate(CreateTodoFormSchema, { /* ... */ }, logger);
      // ...
      return success("作成しました");
    },
    {
      startMeta: { title: formData.get("title") },
      onError: (error) => actionError(error, formData),
    },
  );
}
```

**ログ責務の分担：**

| イベント | 担当 |
|----------|------|
| `start` / 成功時 `end` / catch 時 `end` | `handler()` |
| 既知の `ActionError` | `handler` は `error()` を呼ばない（呼び出し元で記録済み） |
| 未知例外 | `handler` が `logger.error` |
| Edge 認証・HTTP・レスポンス検証失敗 | `callEdgeFunction` 内で記録して `ActionError` |
| ビジネス固有の info / warn | `fn` 内 |

### Route Handlers（`handler` を使わない場合）

```typescript
import { createLogger } from "@/services/logger";

export async function GET(request: NextRequest) {
  const logger = createLogger("GET /api/users");
  logger.start({ path: request.nextUrl.pathname });
  try {
    // ...
    logger.end({ success: true });
    return NextResponse.json({ success: true, data });
  } catch (err) {
    logger.error(err);
    logger.end({ success: false, errorMessage: "失敗" });
    return NextResponse.json({ success: false }, { status: 500 });
  }
}
```

### 例外

- **mock-store デモ**: `console.log` を使う例がある。本番アクションでは使わない

**チェックリスト：**

- [ ] 本番 Server Action は `handler()` を使い、手動の start/end 定型を書かない
- [ ] Edge 呼び出しは `callEdgeFunction`（ログ内包）
- [ ] 例外時はスタックトレース付きで記録される
- [ ] パスワード・トークンをログに出さない
