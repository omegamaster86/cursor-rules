---
title: revalidatePath Usage
impact: HIGH
impactDescription: revalidatePath の使用パターン
tags: mock-store, nextjs, cache, revalidate
---

## revalidatePath Usage

Server Action でデータ変更後にキャッシュを更新するパターンです。

**基本ルール：**

データ変更後は必ず `revalidatePath` を呼び出します。

**基本パターン：**

```typescript
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

export async function createTodoMock(
  _prevState: ActionResponse,
  formData: FormData
): Promise<ActionResponse> {
  // データ作成処理
  addMockTodo(newTodo);
  
  // キャッシュ無効化（必須）
  revalidatePath("/demo/todos");
  
  // リダイレクト
  redirect("/demo/todos");
}
```

**リダイレクトなしの場合：**

```typescript
export async function deleteTodoMock(id: number): Promise<ActionResponse> {
  const deleted = removeMockTodo(id);
  
  if (!deleted) {
    return { success: false, message: "見つかりません" };
  }

  // キャッシュ無効化（リダイレクトしない場合も必須）
  revalidatePath("/demo/todos");
  
  return { success: true, message: "削除しました" };
}
```

**複数パスの無効化：**

```typescript
export async function updateTodoMock(
  id: number,
  _prevState: ActionResponse,
  formData: FormData
): Promise<ActionResponse> {
  // 更新処理
  updateMockTodo(id, updates);
  
  // 一覧ページと詳細ページの両方を無効化
  revalidatePath("/demo/todos");
  revalidatePath(`/demo/todos/${id}`);
  
  redirect("/demo/todos");
}
```

**layout を含む無効化：**

```typescript
// type を指定して layout も含めて無効化
revalidatePath("/demo/todos", "layout");

// page のみを無効化（デフォルト）
revalidatePath("/demo/todos", "page");
```

**よくある間違い：**

```typescript
// ❌ Bad: revalidatePath を忘れている
export async function createTodoMock(...) {
  addMockTodo(newTodo);
  redirect("/demo/todos");  // データが更新されない！
}

// ❌ Bad: redirect の後に revalidatePath
export async function createTodoMock(...) {
  addMockTodo(newTodo);
  redirect("/demo/todos");  // ここで処理が終了
  revalidatePath("/demo/todos");  // 実行されない！
}

// ✅ Good: revalidatePath → redirect の順序
export async function createTodoMock(...) {
  addMockTodo(newTodo);
  revalidatePath("/demo/todos");
  redirect("/demo/todos");
}
```

**redirect との併用時の注意：**

```typescript
export async function createTodoMock(
  _prevState: ActionResponse,
  formData: FormData
): Promise<ActionResponse> {
  try {
    // 処理
    addMockTodo(newTodo);
    
    // キャッシュ無効化 → リダイレクト
    revalidatePath("/demo/todos");
    redirect("/demo/todos");
  } catch (error) {
    // redirect は Error をスローするため、再スロー
    if ((error as Error).message === "NEXT_REDIRECT") {
      throw error;
    }
    
    return { success: false, message: "エラーが発生しました" };
  }
}
```

**パス指定のパターン：**

```typescript
// 特定のパス
revalidatePath("/demo/todos");

// 動的セグメントを含むパス
revalidatePath("/demo/todos/[id]", "page");

// すべてのサブパス（layout を含む）
revalidatePath("/demo", "layout");
```

**チェックリスト：**

- [ ] データ変更後は必ず `revalidatePath` を呼び出す
- [ ] `revalidatePath` は `redirect` より前に実行
- [ ] 関連する複数のパスを無効化
- [ ] `redirect` のエラーは再スロー
