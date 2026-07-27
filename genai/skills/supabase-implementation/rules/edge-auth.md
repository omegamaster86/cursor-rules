---
title: Edge Function Authentication
impact: CRITICAL
impactDescription: getClaims ベースの認証と requireAdmin
tags: supabase, edge-functions, auth, getClaims
---

## Edge Function Authentication

標準 Edge Function では `handler()` が認証を担う。自前実装が必要なときの正は `getClaims`。

**標準（推奨）：**

```typescript
Deno.serve(
  handler(async (_req, ctx) => {
    // ctx.authUserId が利用可能（認証済み）
    // ...
  }),
);

// 管理者専用
Deno.serve(
  handler(async (_req, ctx) => { /* ... */ }, { requireAdmin: true }),
);
```

**`getAuthUser`（`_shared/auth.ts`）：**

```typescript
const { data: claimsData, error } = await supabaseClient.auth.getClaims(token);
const authUserId = claimsData?.claims?.sub as string | undefined;
const isAdmin =
  (claimsData?.claims?.app_metadata as { admin?: boolean } | undefined)
    ?.admin === true;
```

**旧パターン（使わない）：**

- `getUser()` を標準認証経路にする
- `checkAdminUser()`（現行コードに存在しない）

**環境変数（API キー）：**

プラットフォームが Edge Functions に自動注入する複数形 JSON を使う:

- `SUPABASE_PUBLISHABLE_KEYS` → `JSON.parse(...)['default']`
- `SUPABASE_SECRET_KEYS` → `JSON.parse(...)['default']`

`_shared/supabase.ts` は上記のみを参照する。空文字のまま放置せず、起動時または初回利用時に明示チェックするのが理想。

**チェックリスト：**

- [ ] 通常 API は `handler()` 経由
- [ ] 管理者 API は `requireAdmin: true`
- [ ] JWT 検証は `getClaims`
