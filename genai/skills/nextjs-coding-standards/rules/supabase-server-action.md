---
title: Supabase Server Action Pattern
impact: HIGH
impactDescription: Server Action の実装パターンと Edge Function 呼び出し
tags: supabase, server-action, next.js, api
---

## Supabase Server Action Pattern

Server Action の実装パターンとファイル配置のルールです。

**ファイル配置（コロケーション）：**

Server Action は、使用する Page Component と同じディレクトリ配下の `_apis/` または `_actions/` ディレクトリに配置します。

```
app/
  (app)/
    dashboard/
      _apis/
        schedule.server.ts  ← データ取得用 Server Action
      _actions/
        todo.ts             ← データ変更用 Server Action
      page.tsx              ← Page Component
```

**命名規則：**

- ファイル名: `<機能名>.server.ts`（例: `schedule.server.ts`）
- 関数名: `get` + 機能名（camelCase）（例: `getTodaySchedules`）
- ファイルの先頭に `"use server";` ディレクティブを記載

**データ取得 Server Action の実装例：**

```typescript
// _apis/schedule.server.ts
"use server";

import { createClient } from "@/services/supabase/server";

export async function getTodaySchedules(
  userId: number,
  todayStart: string,
  tomorrowStart: string
) {
  const supabase = await createClient();

  try {
    // 1. 認証検証（必須）
    const {
      data: { user },
      error: userError,
    } = await supabase.auth.getUser();

    if (userError || !user) {
      return null;
    }

    // 2. トークン取得（Edge Function呼び出し用）
    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (!session) {
      return null;
    }

    // 3. Edge Function呼び出し（GETメソッド）
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const queryParams = new URLSearchParams({
      userId: userId.toString(),
      todayStart,
      tomorrowStart,
    });

    const response = await fetch(
      `${supabaseUrl}/functions/v1/get-today-schedules?${queryParams.toString()}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      }
    );

    if (!response.ok) {
      console.error("Edge Function呼び出しエラー:", response.status);
      return null;
    }

    const data = await response.json();
    if (!data?.success) {
      console.error("スケジュール取得エラー:", data?.error);
      return null;
    }

    return data.data;
  } catch (error) {
    console.error("スケジュール取得エラー:", error);
    return null;
  }
}
```

**データ変更 Server Action の実装例：**

```typescript
// _actions/todo.ts
"use server";

import { createClient } from "@/services/supabase/server";
import { revalidatePath } from "next/cache";

export async function createTodo(formData: FormData) {
  const supabase = await createClient();

  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return { success: false, error: "認証が必要です" };

  const { data: { session } } = await supabase.auth.getSession();
  if (!session) return { success: false, error: "セッションが必要です" };

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_SUPABASE_URL}/functions/v1/create-todo`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${session.access_token}`,
      },
      body: JSON.stringify({ title: formData.get("title") }),
    }
  );

  if (!response.ok) return { success: false, error: "作成に失敗しました" };

  revalidatePath("/todos");
  return { success: true };
}
```

**チェックリスト：**

- [ ] `"use server";` ディレクティブを記載
- [ ] `getUser()` で認証検証を実施
- [ ] Edge Function は fetch で呼び出し
- [ ] データ変更後は `revalidatePath` でキャッシュ更新
