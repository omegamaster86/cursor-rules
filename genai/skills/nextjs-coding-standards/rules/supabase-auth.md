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
| Edge Function 呼び出し | `callEdgeFunction()` | 内部で `getSession` + `getClaims` を実施 |
| JWT 検証（トークンから user id） | `getClaims(accessToken)` | ネットワーク不要でクレーム検証 |
| セッション / アクセストークン取得 | `getSession()` | Cookie からセッションを読む |
| ユーザー表示・ミドルウェア更新 | `getSession()` | 表示用・セッションリフレッシュ用途 |
| Auth SDK（signIn / signOut 等） | `supabase.auth.*` | Server Action から直接呼んでよい |

**標準パターン（Edge Function 呼び出し）：**

本番コードでは認証と Edge 呼び出しを自分で組み立てず、`callEdgeFunction` を使う。

```typescript
import { callEdgeFunction } from "@/services/supabase/edge-function";
import { TodoSchema } from "@/types/schemas/todo";

// callEdgeFunction 内部の流れ:
// 1. getSession() で access_token 取得
// 2. getClaims(session.access_token) で JWT 検証・user id 取得
// 3. Authorization ヘッダー付きで Edge Function を fetch
// 4. レスポンスを Zod で検証
await callEdgeFunction("get-todos", z.array(TodoSchema), {
  method: "GET",
  logger,
});
```

`callEdgeFunction` の認証ロジック（要約）：

```typescript
const {
  data: { session },
} = await supabase.auth.getSession();
if (!session) throw new ActionError("セッションが見つかりません");

const { data: claimsData, error: claimsError } =
  await supabase.auth.getClaims(session.access_token);
const authUserId = claimsData?.claims?.sub as string | undefined;
if (claimsError || !authUserId) {
  throw new ActionError("認証に失敗しました");
}
```

**例外：Supabase Auth SDK 直接呼び出し**

ログイン・サインアップ・パスワードリセット等は Edge Function 経由ではなく、Server Action から `supabase.auth.signInWithPassword` 等を直接呼ぶ。

**`getUser()` について**

- 旧ルールの「常に `getUser()`」は現行の Edge 呼び出し経路では使わない
- Auth サーバーへのネットワーク往復が必要なケースでは `getUser()` を使ってもよいが、標準の Edge 経路は `getClaims` を正とする

**チェックリスト：**

- [ ] Edge Function 呼び出しは `callEdgeFunction` 経由
- [ ] 自前で組み立てる場合は `getSession` + `getClaims` で JWT を検証
- [ ] Auth SDK（signIn 等）は Server Action から直接呼んでよい
- [ ] 認証エラー時は `ActionError` / 適切なエラーレスポンスを返す
