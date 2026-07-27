---
title: Supabase Authentication Rules
impact: CRITICAL
impactDescription: サーバーサイドでの認証処理における必須ルール
tags: supabase, authentication, security
---

## Supabase Authentication Rules

サーバーサイドでの認証処理に関する**必須ルール**です。

**基本原則：**

| 用途 | 使用する関数 | 備考 |
|------|------------|------|
| 認証検証 | `getUser()` | **必須** - JWT をサーバーで検証 |
| トークン取得 | `getSession()` | 認証検証後のみ使用可 |

**⚠️ `getSession()` は認証検証に使用禁止**

- `getSession()`: Cookie から直接読み取るだけで JWT 検証なし（非セキュア）
- `getUser()`: Supabase Auth サーバーで JWT を検証（セキュア）

**正しい実装パターン：**

```typescript
// ✅ 良い例：Server Actions での認証処理
"use server";

import { createClient } from "@/services/supabase-service/server";

export async function secureServerAction() {
  const supabase = await createClient();

  // 1. 認証検証（必須）
  const { data: { user }, error: authError } = await supabase.auth.getUser();

  if (authError || !user) {
    return { success: false, error: "認証が必要です" };
  }

  // 2. アクセストークンが必要な場合のみ getSession を使用
  const { data: { session } } = await supabase.auth.getSession();
  const accessToken = session?.access_token;

  // 3. Edge Function 呼び出し
  const { data, error } = await supabase.functions.invoke("function-name", {
    headers: { Authorization: `Bearer ${accessToken}` },
  });

  // ...
}
```

**❌ 悪い例：**

```typescript
// ❌ getSession のみで認証チェック（脆弱性あり）
export async function insecureAction() {
  const supabase = await createClient();
  
  // 改ざんされたトークンを検出できない！
  const { data: { session } } = await supabase.auth.getSession();
  
  if (!session) {
    return { error: "認証が必要です" };
  }
  
  // ...
}
```

**チェックリスト：**

- [ ] Server Components / Server Actions では `getUser()` で認証検証
- [ ] `getSession()` は認証検証後のトークン取得にのみ使用
- [ ] 認証エラー時は適切なエラーレスポンスを返す
