---
title: Supabase SDK Integration
impact: HIGH
impactDescription: Supabase クライアントの設定と認証・データアクセス
tags: supabase, backend, authentication, database
---

## Supabase SDK Integration

Supabase SDK を使用したバックエンド連携のベストプラクティスです。

**インストール（参考版）:**

```bash
npm install @supabase/supabase-js @supabase/ssr
# 例: @supabase/ssr ^0.7.0 / @supabase/supabase-js ^2.84.0
```

**クライアント配置:**

```
services/supabase/
├── client.ts
├── server.ts          # createClient<Database>()
├── edge-function.ts   # callEdgeFunction
├── middleware.ts
└── admin.ts           # service role（必要なときのみ）
```

**データ取得（正しい経路）:**

Page から直接 `.from('todos')` しない。`_apis` + `callEdgeFunction` を使う。

```typescript
import { callEdgeFunction } from "@/services/supabase/edge-function";
import { TodoSchema } from "@/types/schemas/todo";

const todos = await callEdgeFunction("get-todos", z.array(TodoSchema), {
  method: "GET",
  logger,
});
```

**認証:**

- Edge 呼び出し: `callEdgeFunction` 内の `getSession` + `getClaims`
- Auth SDK（signIn 等）: Server Action から直接可

**チェックリスト:**

- [ ] パスは `@/services/supabase/*`
- [ ] テーブル直アクセスを Page / Action からしていない
- [ ] Edge は `callEdgeFunction` + Zod schemas
- [ ] env は `@/env`
