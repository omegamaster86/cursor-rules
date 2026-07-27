---
title: Services Directory Structure
impact: MEDIUM
impactDescription: 外部サービス連携の一元管理
tags: services, supabase, external-services, configuration
---

## Services Directory Structure

`services/` は外部サービス設定と共通ハンドラーを配置します。

**推奨構成：**

```
services/
├── handler.ts                 # Server Action 共通 handler / validate / success
├── logger.ts                  # 構造化ログ
├── supabase/
│   ├── client.ts              # ブラウザ用
│   ├── server.ts              # Server Component / Action 用
│   ├── edge-function.ts       # callEdgeFunction
│   ├── middleware.ts          # セッション更新
│   └── admin.ts               # service role（必要なときのみ）
└── (stripe|line|...)/         # その他外部サービス（任意）
```

**Correct：**

```typescript
// services/supabase/server.ts
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import { env } from "@/env";
import type { Database } from "@/types/database.types";

export async function createClient() {
  const cookieStore = await cookies();
  return createServerClient<Database>(
    env.NEXT_PUBLIC_SUPABASE_URL,
    env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          // ...
        },
      },
    },
  );
}
```

```typescript
import { callEdgeFunction } from "@/services/supabase/edge-function";
import { handler } from "@/services/handler";
```

**ポイント：**

1. パスは `@/services/supabase/*`（旧 `supabase-service` は使わない）
2. Edge 呼び出しは `edge-function.ts` に集約
3. URL / キーは `import { env } from "@/env"` のみ
