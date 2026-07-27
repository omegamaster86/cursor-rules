---
title: Server Actions Colocation
impact: HIGH
impactDescription: フォーム処理の保守性と見通し
tags: server-actions, colocation, forms, data-mutation
---

## Server Actions Colocation

Server Actions はページ固有の `_actions/` に配置します。

**Correct：**

```
app/(dashboard)/todos/
├── new/
│   ├── _actions/
│   │   ├── todo.ts
│   │   ├── schema.ts
│   │   └── types.ts
│   ├── _components/
│   │   └── NewTodoForm/
│   └── page.tsx
└── [id]/
    └── edit/
        ├── _actions/
        │   ├── todo.ts
        │   ├── schema.ts
        │   └── types.ts
        └── page.tsx
```

**実装の要点：**

```typescript
"use server";

import { actionError, handler, success, validate } from "@/services/handler";
import { callEdgeFunction } from "@/services/supabase/edge-function";
import type { CreateTodoState } from "./types";

export async function createTodo(
  _prevState: CreateTodoState,
  formData: FormData,
): Promise<CreateTodoState> {
  return handler(
    "createTodo",
    async (logger) => {
      const data = validate(CreateTodoFormSchema, { /* FormData */ }, logger);
      await callEdgeFunction("create-todo", TodoSchema, {
        method: "POST",
        body: data,
        logger,
      });
      return success("作成しました");
    },
    { onError: (error) => actionError(error, formData) },
  );
}
```

状態フィールドは `fieldErrors`（`errors` ではない）。任意で `payload?: FormData`。

読み取り専用ロジックは `_apis/*.server.ts` に置く（`_actions` と混在させない）。
