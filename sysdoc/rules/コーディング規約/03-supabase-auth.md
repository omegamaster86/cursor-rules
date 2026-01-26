## 3. Supabase 認証規約

Supabase の認証機能を使用する際のセキュリティに関する規約を定義します。

### 3.1 サーバーサイドでの認証処理

#### 3.1.1 `getUser()` の使用（必須）

- **Server Components、Server Actions、API Routes** では、認証確認に **必ず `getUser()` を使用する**
- `getSession()` は **使用禁止**（セキュリティリスクあり）

**理由**:
- `getUser()`: JWT を Supabase Auth サーバーで検証するため、改ざんされたトークンを検出できる（セキュア）
- `getSession()`: Cookie から直接セッション情報を読み取るだけで、JWT の検証を行わない（非セキュア）

#### 3.1.2 Access Token が必要な場合の処理

Edge Function 呼び出しなど、`access_token` が必要な場合は以下の手順で実装します：

1. **認証検証**: `getUser()` で認証を検証
2. **トークン取得**: `getSession()` で `access_token` を取得

```typescript
// ✅ 良い例：Server Actionsでの認証処理
"use server";

import { createClient } from "@/lib/supabase/server";

export async function secureServerAction() {
  const supabase = await createClient();

  // 1. 認証検証（必須）: getUser() で JWT を検証
  const {
    data: { user },
    error: userError,
  } = await supabase.auth.getUser();

  if (userError || !user) {
    throw new Error("認証が必要です");
  }

  // 2. トークン取得（必要な場合のみ）: access_token が必要な場合
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    throw new Error("セッションが見つかりません");
  }

  // access_token を使用して処理を実行
  const token = session.access_token;
  // ...
}
```

```typescript
// ❌ 悪い例：getSession() のみを使用（セキュリティリスク）
export async function insecureServerAction() {
  const supabase = await createClient();

  // ❌ サーバーサイドで getSession() のみを使用するのは危険
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    return null;
  }

  // JWT が検証されていないため、改ざんされたトークンでも通過する可能性がある
  // ...
}
```

### 3.2 クライアントサイドでの認証処理

#### 3.2.1 `getSession()` の使用（許可）

- **Client Components** では `getSession()` の使用が許可される
- クライアントサイドでは、ブラウザの Cookie から直接セッション情報を取得するため、改ざんのリスクは限定的

```typescript
// ✅ 良い例：Client Componentでの認証処理
"use client";

import { createClient } from "@/lib/supabase/client";

export function ClientComponent() {
  const supabase = createClient();

  async function handleAction() {
    // クライアントサイドでは getSession() を使用可能
    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (!session) {
      console.error("ログインが必要です");
      return;
    }

    // ...
  }
}
```

### 3.3 Edge Function 呼び出し時の規約

Edge Function を呼び出す際は、`fetch` メソッドを使用し、適切に認証トークンを渡します。

#### 3.3.1 Server Actions からの呼び出し

```typescript
"use server";

import { createClient } from "@/lib/supabase/server";

export async function callEdgeFunction() {
  const supabase = await createClient();

  // 1. 認証検証
  const {
    data: { user },
    error: userError,
  } = await supabase.auth.getUser();

  if (userError || !user) {
    return null;
  }

  // 2. トークン取得
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    return null;
  }

  // 3. fetchメソッドでEdge Functionを呼び出し
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const response = await fetch(`${supabaseUrl}/functions/v1/function-name`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${session.access_token}`,
    },
    body: JSON.stringify({ data: "..." }),
  });

  if (!response.ok) {
    console.error("Edge Function呼び出しエラー:", response.statusText);
    return null;
  }

  return await response.json();
}
```

#### 3.3.2 Client Components からの呼び出し

```typescript
"use client";

import { createClient } from "@/lib/supabase/client";

export function ClientComponent() {
  const supabase = createClient();

  async function callEdgeFunction() {
    // クライアントサイドでは getSession() を使用
    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (!session) {
      return null;
    }

    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const response = await fetch(`${supabaseUrl}/functions/v1/function-name`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${session.access_token}`,
      },
      body: JSON.stringify({ data: "..." }),
    });

    return await response.json();
  }
}
```

### 3.4 認証規約まとめ

| 実行環境                     | 認証確認     | トークン取得   | 備考                                         |
| ---------------------------- | ------------ | -------------- | -------------------------------------------- |
| Server Components            | `getUser()`  | `getSession()` | 認証検証は必ず `getUser()` を使用           |
| Server Actions               | `getUser()`  | `getSession()` | 認証検証は必ず `getUser()` を使用           |
| Route Handlers                   | `getUser()`  | `getSession()` | 認証検証は必ず `getUser()` を使用           |
| Client Components            | `getSession()` または `getUser()` | `getSession()` | どちらも使用可能、通常は `getSession()` で十分 |

---
