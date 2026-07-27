---
title: BFF (Backend for Frontend) Design
impact: HIGH
impactDescription: セキュリティとアーキテクチャの一貫性
tags: bff, route-handlers, api, edge-functions
---

## BFF (Backend for Frontend) Design

BFF（Route Handlers）は薄いゲートウェイとして機能させ、ビジネスロジックは Edge Functions に一元化します。

**標準の Web データ経路：**

多くの画面は Route Handler ではなく **Server Action / `_apis` → `callEdgeFunction`** を使う。Route Handler は Webhook 受信・特殊な BFF が必要なときに限定する。

**BFF の責務（使う場合）：**

1. 入力検証
2. セッション連携
3. レート制限 / キャッシュ制御
4. Edge Functions の呼び出し（ビジネスロジックは載せない）

**Incorrect（BFF / Action から直接テーブル操作）：**

```typescript
const { data } = await supabase.from("todos").insert(body).select().single();
```

**Correct（薄いゲートウェイ or Server Action）：**

```typescript
import { callEdgeFunction } from "@/services/supabase/edge-function";
import { createLogger } from "@/services/logger";

const logger = createLogger("POST /api/todos");
logger.start();

const data = await callEdgeFunction("create-todo", TodoSchema, {
  method: "POST",
  body: validatedData,
  logger,
});
```

**認証：**

- Edge 呼び出し経路では `callEdgeFunction` 内の `getSession` + `getClaims` が正
- Route Handler を自前で書く場合も同じ検証方針に合わせる

**ポイント：**

1. クライアントから直接 DB アクセス禁止
2. ビジネスルールは Edge / DB Function 側
3. Web の通常 CRUD は Server Action 優先（BFF 必須ではない）
