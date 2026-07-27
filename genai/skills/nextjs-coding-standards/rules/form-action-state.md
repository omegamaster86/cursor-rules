---
title: useActionState Pattern
impact: HIGH
impactDescription: useActionState を使用したフォーム実装パターン
tags: react, forms, server-actions, useactionstate
---

## useActionState Pattern

Next.js の `useActionState` を使用したフォーム実装パターンです。

### 基本パターン

1. `_actions/` に Server Action（`handler` + `validate` + `callEdgeFunction`）を作成
2. `schema.ts` / `types.ts` を分割
3. Client Component で `useActionState` を使用
4. `<form action={formAction}>` に渡す

### Server Action の実装

```typescript
// _actions/types.ts
export type CreateTodoState = {
  success: boolean;
  message: string;
  payload?: FormData;
  fieldErrors?: {
    title?: string[];
    description?: string[];
    priority?: string[];
  };
};
```

```typescript
// _actions/todo.ts
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
      const data = validate(
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
        body: { ...data, dueDate: null },
        logger,
      });

      return success("ToDoを作成しました");
    },
    {
      onError: (error): CreateTodoState => actionError(error, formData),
    },
  );
}
```

### Client Component の実装

```typescript
"use client";

import { useRouter } from "next/navigation";
import { useActionState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { createTodo, type CreateTodoState } from "../../_actions/todo";

const initialState: CreateTodoState = {
  success: false,
  message: "",
};

export function NewTodoForm() {
  const router = useRouter();
  const [state, formAction, pending] = useActionState(createTodo, initialState);

  useEffect(() => {
    if (state.success) {
      router.push("/todos");
    }
  }, [state.success, router]);

  return (
    <form action={formAction} className="space-y-6">
      {state.message && !state.success && (
        <div className="rounded-md bg-destructive/10 p-4" role="alert">
          <p className="text-sm text-destructive">{state.message}</p>
        </div>
      )}

      <Input
        id="title"
        name="title"
        type="text"
        disabled={pending}
        defaultValue={
          state.payload?.get("title")?.toString() ?? undefined
        }
        aria-invalid={state.fieldErrors?.title ? "true" : "false"}
      />
      {state.fieldErrors?.title && (
        <p className="text-sm text-destructive">{state.fieldErrors.title[0]}</p>
      )}

      <Button type="submit" disabled={pending}>
        {pending ? "作成中..." : "ToDoを作成"}
      </Button>
    </form>
  );
}
```

### Uncontrolled Component の優先使用

```typescript
// ✅ Uncontrolled
<form action={formAction}>
  <input name="title" type="text" />
</form>

// ❌ 不要な Controlled
const [title, setTitle] = useState("");
```

### 非入力値の渡し方（bind 優先、hidden は限定許容）

`id` / `lock_no` などユーザーが編集しない値は **`bind` を優先**する。

```typescript
export async function updateTodo(
  id: string,
  lock_no: number,
  _prevState: UpdateTodoState,
  formData: FormData,
): Promise<UpdateTodoState> {
  // ...
}
```

```tsx
const boundAction = useMemo(
  () => updateTodo.bind(null, todo.id, todo.lock_no),
  [todo.id, todo.lock_no],
);
const [state, formAction, pending] = useActionState(boundAction, initialState);
```

**hidden の許容例（実装で使用されているパターン）：**

- 削除確認など単一 ID を送る簡易フォーム
- Stripe / 外部 SDK 連携でフィールド名が固定されている場合
- enum トグルなど UI 上の制約で bind より hidden が簡潔な場合

**チェックリスト：**

- [ ] Server Action は `_actions/` に配置
- [ ] `handler` + `validate` + `callEdgeFunction` を使う
- [ ] 状態型に `payload?: FormData` を含め、エラー時に入力を復元できる
- [ ] Uncontrolled を優先
- [ ] `id` / `lock_no` は原則 `bind`
- [ ] `pending` で UI を無効化
