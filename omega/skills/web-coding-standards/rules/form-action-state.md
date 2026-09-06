---
title: useActionState Pattern
impact: HIGH
impactDescription: useActionState を使用したフォーム実装パターン
tags: react, forms, server-actions, useactionstate
---

## useActionState Pattern

Next.js の `useActionState` を使用したフォーム実装パターンです。

### 基本パターン

**実装手順：**

1. Server Action を作成（`_actions/` ディレクトリ）
2. Client Component で `useActionState` を使用
3. `<form>` の `action` プロップスに Server Action を渡す

### Server Action の実装

```typescript
// _actions/todo.ts
"use server";

import { z } from "zod";
import { createClient } from "@/services/supabase/server";

// バリデーションスキーマ
const CreateTodoFormSchema = z.object({
  title: z.string().min(1, "タイトルは必須です").max(100),
  description: z.string().max(1000).optional().nullable(),
  priority: z.enum(["low", "medium", "high"]),
});

// 状態型
export type CreateTodoState = {
  success: boolean;
  message: string;
  error?: string;
  fieldErrors?: {
    title?: string[];
    description?: string[];
    priority?: string[];
  };
};

// Server Action（useActionState対応）
export async function createTodo(
  _prevState: CreateTodoState,  // 第一引数は前回の状態
  formData: FormData,           // 第二引数はフォームデータ
): Promise<CreateTodoState> {
  try {
    // 1. FormDataから値を取得
    const rawFormData = {
      title: formData.get("title"),
      description: formData.get("description") || null,
      priority: formData.get("priority"),
    };

    // 2. Zodでバリデーション
    const validationResult = CreateTodoFormSchema.safeParse(rawFormData);

    if (!validationResult.success) {
      const fieldErrors = validationResult.error.flatten().fieldErrors;
      return {
        success: false,
        message: fieldErrors.title?.[0] || "入力内容が不正です",
        error: "VALIDATION_ERROR",
        fieldErrors,
      };
    }

    // 3. バリデーション済みデータを使用
    const validatedData = validationResult.data;

    // 4. 認証チェック & データベース操作
    // ...

    return {
      success: true,
      message: "ToDoを作成しました",
    };
  } catch (error) {
    console.error("[EXCEPTION] ToDo作成エラー:", error);
    return {
      success: false,
      message: "予期しないエラーが発生しました",
      error: "UNEXPECTED_ERROR",
    };
  }
}
```

### Client Component の実装

```typescript
// _components/NewTodoForm/index.tsx
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
  
  // useActionStateでServer Actionを統合
  const [state, formAction, pending] = useActionState(createTodo, initialState);

  // 成功時のリダイレクト
  useEffect(() => {
    if (state.success) {
      router.push("/todos");
    }
  }, [state.success, router]);

  return (
    <form action={formAction} className="space-y-6">
      {/* エラーメッセージ表示 */}
      {state.message && !state.success && (
        <div className="rounded-md bg-red-50 p-4" role="alert">
          <p className="text-sm text-red-800">{state.message}</p>
        </div>
      )}

      {/* タイトル入力 */}
      <div className="space-y-2">
        <Input
          id="title"
          name="title"
          type="text"
          placeholder="例：週報を作成する"
          disabled={pending}
          aria-invalid={state.fieldErrors?.title ? "true" : "false"}
        />
        {state.fieldErrors?.title && (
          <p className="text-sm text-red-600">{state.fieldErrors.title[0]}</p>
        )}
      </div>

      {/* 送信ボタン */}
      <Button type="submit" disabled={pending}>
        {pending ? "作成中..." : "ToDoを作成"}
      </Button>
    </form>
  );
}
```

### Uncontrolled Component の優先使用

```typescript
// ✅ 良い例：Uncontrolled Component
<form action={formAction}>
  <input name="title" type="text" />
  <button type="submit">送信</button>
</form>

// ❌ 悪い例：不要な Controlled Component
const [title, setTitle] = useState("");
<form>
  <input value={title} onChange={(e) => setTitle(e.target.value)} />
</form>
```

**チェックリスト：**

- [ ] Server Action は `_actions/` ディレクトリに配置
- [ ] `useActionState` で状態を管理
- [ ] Uncontrolled Component を優先使用
- [ ] `pending` 状態で UI を無効化
