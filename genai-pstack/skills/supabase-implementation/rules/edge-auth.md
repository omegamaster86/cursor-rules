---
title: Edge Functions Authentication
impact: HIGH
impactDescription: Edge Functions での認証処理
tags: supabase, edge-functions, authentication
---

## Edge Functions Authentication

Edge Functions で認証済みユーザーの情報を取得する方法です。

**基本原則：**

- Authorization ヘッダーから JWT トークンを取得
- `getUser()` で認証状態を検証（サーバーサイドで必須）
- 認証トークンを Supabase クライアントに設定してリクエストを実行

**認証フロー：**

```typescript
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

Deno.serve(async (req) => {
  // 1. 認証トークンを取得
  const authHeader = req.headers.get("Authorization");
  if (!authHeader) {
    return new Response(
      JSON.stringify({ success: false, error: "認証トークンがありません" }),
      {
        headers: { "Content-Type": "application/json" },
        status: 401,
      }
    );
  }

  // 2. Supabaseクライアントに認証トークンを設定
  const supabaseWithAuth = createClient(
    Deno.env.get("SUPABASE_URL") ?? "",
    Deno.env.get("SUPABASE_ANON_KEY") ?? "",
    {
      global: {
        headers: { Authorization: authHeader },
      },
    }
  );

  // 3. 認証ユーザー情報を取得（サーバーサイドでは必ず getUser() を使用）
  const {
    data: { user },
    error: authError,
  } = await supabaseWithAuth.auth.getUser();

  if (authError || !user) {
    console.error("[ERROR] Authentication failed", {
      error: authError?.message,
    });
    return new Response(
      JSON.stringify({ success: false, error: "ユーザー認証に失敗しました" }),
      {
        headers: { "Content-Type": "application/json" },
        status: 401,
      }
    );
  }

  // 4. 認証ユーザーのUUIDを使用して処理を続行
  const authUserId = user.id;

  // Database Function 呼び出し等...
});
```

**getUser() vs getSession() の使い分け：**

| メソッド | 用途 | 検証 |
|----------|------|------|
| `getUser()` | サーバーサイド（Edge Functions、Server Actions） | JWT をサーバーで検証 |
| `getSession()` | クライアントサイドのみ | JWT を検証しない |

> ⚠️ **重要**: サーバーサイドでは必ず `getUser()` を使用してください。`getSession()` は JWT の検証を行わないため、改ざんされたトークンを検知できません。

**クライアント（Next.js）からの呼び出し：**

```typescript
// Server Action から Edge Function を呼び出す
const { data: { session } } = await supabase.auth.getSession();

const response = await fetch(
  `${process.env.NEXT_PUBLIC_SUPABASE_URL}/functions/v1/function-name`,
  {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${session?.access_token}`,
    },
  }
);
```

**チェックリスト：**

- [ ] Authorization ヘッダーの存在を確認している
- [ ] `getUser()` で認証状態を検証している（`getSession()` ではない）
- [ ] 認証エラー時に 401 を返している
- [ ] エラーログを出力している
