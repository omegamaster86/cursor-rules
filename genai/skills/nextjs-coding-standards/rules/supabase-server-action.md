---
title: Supabase Server Action Pattern
impact: HIGH
impactDescription: Server Action の実装パターンと Edge Function 呼び出し
tags: supabase, server-action, next.js, api
---

## Supabase Server Action Pattern

Server Action の実装パターンとファイル配置のルールです。

**ファイル配置（コロケーション）：**

```
app/
  (dashboard)/
    todos/
      _apis/
        todo.server.ts      ← データ取得
      new/
        _actions/
          todo.ts           ← データ変更
          schema.ts         ← Zod フォームスキーマ
          types.ts          ← Action State 型
        _components/
          NewTodoForm/
            index.tsx
        page.tsx
```

**命名・責務：**

| 種類 | 配置 | ファイル例 | 内容 |
|------|------|-----------|------|
| 読み取り | `_apis/` | `todo.server.ts` | `"use server"` + `handler` + `callEdgeFunction` |
| 書き込み | `_actions/` | `todo.ts` | `"use server"` + `handler` + `validate` + `callEdgeFunction` |
| フォームスキーマ | `_actions/schema.ts` | — | Zod |
| 状態型 | `_actions/types.ts` | — | `success` / `message` / `payload?` / `fieldErrors?` |

**標準実装（書き込み）：**

```typescript
"use server";

import { actionError, handler, success, validate } from "@/services/handler";
import { callEdgeFunction } from "@/services/supabase/edge-function";
import { TodoSchema } from "@/types/schemas/todo";
import { CreateTodoFormSchema } from "./schema";
import type { CreateTodoState } from "./types";

export async function createTodo(
  _prevState: CreateTodoState,
  formData: FormData,
): Promise<CreateTodoState> {
  return handler(
    "createTodo",
    async (logger): Promise<CreateTodoState> => {
      const { title, description, priority } = validate(
        CreateTodoFormSchema,
        {
          title: formData.get("title"),
          description: formData.get("description") || null,
          priority: formData.get("priority"),
        },
        logger,
      );

      await callEdgeFunction("create-todo", TodoSchema, {
        method: "POST",
        body: {
          title: title.trim(),
          description: description?.trim() ?? null,
          priority,
          dueDate: null,
        },
        logger,
      });

      return success("ToDoを作成しました");
    },
    {
      startMeta: {
        title: formData.get("title"),
        priority: formData.get("priority"),
      },
      onError: (error): CreateTodoState => actionError(error, formData),
    },
  );
}
```

**`handler` / `callEdgeFunction` の役割：**

- `handler`: `createLogger` / `start` / `end` / try-catch を内包。ビジネスロジックだけ書く
- `validate`: Zod `safeParse` + `FormValidationError`（fieldErrors 付き）
- `success` / `actionError`: 統一レスポンス形状
- `callEdgeFunction`: 認証・fetch・レスポンス Zod 検証を内包。失敗時は `ActionError`

**チェックリスト：**

- [ ] `"use server";` を先頭に記載
- [ ] 読み取りは `_apis/*.server.ts`、書き込みは `_actions/`
- [ ] `handler` + `validate` + `callEdgeFunction` を使う
- [ ] スキーマと状態型は `_actions/schema.ts` / `types.ts` に分割
- [ ] 手動の `getUser` + raw `fetch` + `console.error` は書かない
