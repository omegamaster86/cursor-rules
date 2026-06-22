---
title: Server Actions Best Practices
impact: HIGH
impactDescription: フォーム処理のセキュリティと型安全性
tags: server-actions, forms, zod, validation, useActionState
---

## Server Actions Best Practices

Server Actionsの設計と実装のベストプラクティスです。

**基本パターン：**

```typescript
// app/todos/new/_actions/todo.ts
"use server";

import { z } from 'zod'
import { revalidatePath } from 'next/cache'
import { createClient } from '@/services/supabase-service/server'

// 1. 状態型をエクスポート
export type CreateTodoState = {
  success: boolean;
  message: string;
  errors?: {
    title?: string[];
    description?: string[];
  };
};

// 2. Zodスキーマを定義
const TodoSchema = z.object({
  title: z.string()
    .min(1, '必須項目です')
    .max(100, '100文字以内で入力してください'),
  description: z.string()
    .max(500, '500文字以内で入力してください')
    .optional(),
});

// 3. useActionStateと統合できる形式
export async function createTodo(
  prevState: CreateTodoState,
  formData: FormData,
): Promise<CreateTodoState> {
  // 4. Zodでバリデーション
  const validatedFields = TodoSchema.safeParse({
    title: formData.get('title'),
    description: formData.get('description'),
  });

  if (!validatedFields.success) {
    return {
      success: false,
      message: '入力内容に誤りがあります',
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  try {
    // 5. Edge Functionの呼び出し
    const supabase = await createClient()
    const { error } = await supabase.functions.invoke('todos-create', {
      body: validatedFields.data
    })

    if (error) throw error

    // 6. キャッシュを無効化
    revalidatePath('/todos')
    
    return { success: true, message: '作成しました' };
  } catch (error) {
    return { success: false, message: 'エラーが発生しました' };
  }
}
```

**Client Componentでの使用：**

```tsx
// _components/NewTodoForm/index.tsx
'use client'

import { useActionState } from 'react'
import { createTodo, type CreateTodoState } from '../../_actions/todo'

const initialState: CreateTodoState = {
  success: false,
  message: '',
}

export function NewTodoForm() {
  const [state, formAction, isPending] = useActionState(createTodo, initialState)

  return (
    <form action={formAction}>
      <input name="title" />
      {state.errors?.title && (
        <p className="text-red-500">{state.errors.title[0]}</p>
      )}
      
      <textarea name="description" />
      {state.errors?.description && (
        <p className="text-red-500">{state.errors.description[0]}</p>
      )}
      
      <button type="submit" disabled={isPending}>
        {isPending ? '送信中...' : '送信'}
      </button>
      
      {state.message && <p>{state.message}</p>}
    </form>
  )
}
```

**チェックリスト：**

- [ ] `"use server"`ディレクティブがある
- [ ] 状態型がエクスポートされている
- [ ] Zodでバリデーションしている
- [ ] 第一引数が`prevState`、第二引数が`FormData`
- [ ] ビジネスロジックはEdge Functionsに委譲
