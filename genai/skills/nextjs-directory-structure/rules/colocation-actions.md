---
title: Server Actions Colocation
impact: HIGH
impactDescription: フォーム処理の保守性と見通し
tags: server-actions, colocation, forms, data-mutation
---

## Server Actions Colocation

Server Actionsはページ固有の`_actions/`ディレクトリに配置します。

**Incorrect（共通ディレクトリに配置）:**

```
src/
├── actions/              # すべてのServer Actionsを集約
│   ├── todo.ts
│   ├── user.ts
│   └── auth.ts
└── app/
    └── todos/
        └── new/
            └── page.tsx  # actionsから遠い
```

**Correct（ページ近くに配置）:**

```
app/
└── todos/
    ├── new/
    │   ├── _actions/
    │   │   └── todo.ts        # createTodo Server Action
    │   ├── _components/
    │   │   └── NewTodoForm/
    │   └── page.tsx
    └── [id]/
        └── edit/
            ├── _actions/
            │   └── todo.ts    # updateTodo Server Action
            └── page.tsx
```

**Server Action実装例：**

```typescript
// app/todos/new/_actions/todo.ts
"use server";

import { z } from 'zod'
import { revalidatePath } from 'next/cache'

// 状態型をエクスポート
export type CreateTodoState = {
  success: boolean;
  message: string;
  errors?: {
    title?: string[];
    description?: string[];
  };
};

const TodoSchema = z.object({
  title: z.string().min(1, '必須項目です').max(100),
  description: z.string().max(500).optional(),
});

// useActionStateと統合できる形式
export async function createTodo(
  prevState: CreateTodoState,
  formData: FormData,
): Promise<CreateTodoState> {
  // Zodでバリデーション
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

  // Edge Functionの呼び出し
  // ...

  revalidatePath('/todos')
  return { success: true, message: '作成しました' };
}
```

**ポイント：**

1. `_actions`ディレクトリはルーティングに影響しない
2. ファイル名はリソース名（例: `todo.ts`, `user.ts`）
3. 状態型をエクスポートしてClient Componentで型安全に使用
4. FormDataのバリデーションは必ずZodで実行
