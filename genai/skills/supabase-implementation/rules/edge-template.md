---
title: Edge Function Template
impact: HIGH
impactDescription: handler() を使った Edge Function の標準ひな形
tags: supabase, edge-functions, handler, zod
---

## Edge Function Template

標準の Edge Function は `_shared/handler.ts` の `handler()` を使う。

**最小例（create-todo）：**

```typescript
// functions/create-todo/index.ts
import { handler } from "../_shared/handler.ts";
import { createTodoSchema } from "../_shared/schemas/create-todo-schema.ts";

Deno.serve(
  handler(async (_req, ctx) => {
    const body = await ctx.validate(createTodoSchema);

    const data = await ctx.callRpc("ins_todo", {
      p_auth_user_id: ctx.authUserId,
      p_title: body.title,
      p_description: body.description ?? null,
      p_priority: body.priority,
      p_due_date: body.dueDate ?? null,
      p_created_program: "create-todo",
    });

    return ctx.success(data?.[0] ?? null, 201);
  }),
);
```

**GET 例：**

```typescript
Deno.serve(
  handler(
    async (_req, ctx) => {
      const data = await ctx.callRpc("sel_todos_by_user", {
        target_auth_user_id: ctx.authUserId,
      });
      return ctx.success(data ?? []);
    },
    { methods: ["GET"] }, // 既定は ["POST"]
  ),
);
```

**HandlerContext：**

| メソッド | 役割 |
|----------|------|
| `ctx.authUserId` | JWT から得たユーザー ID |
| `ctx.validate(schema)` | ボディを Zod 検証（失敗は ValidationError） |
| `ctx.callRpc(name, args, { serviceRole? })` | DB Function 呼び出し |
| `ctx.callExternalApi(...)` | 外部 HTTP（Stripe 等） |
| `ctx.log(message, meta?)` | 情報ログ |
| `ctx.success(data, status?)` | `{ success: true, data }` |
| `ctx.error(status, code, message)` | `{ success: false, error: { code, message } }` |

**オプション：**

```typescript
handler(fn, {
  methods: ["POST"],      // 既定
  requireAdmin: true,     // app_metadata.admin === true 必須
});
```

**Zod スキーマ配置：** `functions/_shared/schemas/*.ts`

**RPC 引数プレフィックス：** 新規は `p_` 優先。レガシーに `target_` が残る場合は共存を許容。

**やってはいけないこと：**

- 手書きの長い `Deno.serve` 内に認証・ログ・レスポンスを直書き（標準 CRUD では）
- `createLogger` / `createSuccessResponse` など旧 API 名（現行に存在しない）

例外パターンは [edge-exceptions](edge-exceptions.md) を参照。
