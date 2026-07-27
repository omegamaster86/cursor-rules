---
title: API Clients Colocation
impact: HIGH
impactDescription: API呼び出しの一貫性とセキュリティ
tags: api-clients, colocation, server, client
---

## API Clients Colocation

API モジュールはコロケーション原則に従い、**ページ／機能固有は `_apis/`** に置く。

**dev-starter の標準：**

- `src/apis/` は **任意（現状未使用）**
- `*.client.ts` は **任意（現状未使用）** — データ取得も Server 側 `_apis/*.server.ts` が中心
- 書き込みは `_actions/`（`_apis` に置かない）

```
app/(dashboard)/todos/
├── _apis/
│   └── todo.server.ts      # 読み取り（"use server"）
├── new/
│   └── _actions/
│       └── todo.ts         # 書き込み
└── page.tsx
```

**読み取り API の例：**

```typescript
// _apis/todo.server.ts
"use server";

import { z } from "zod";
import { handler } from "@/services/handler";
import { callEdgeFunction } from "@/services/supabase/edge-function";
import { TodoSchema } from "@/types/schemas/todo";

export async function getTodos() {
  return handler(
    "getTodos",
    async (logger) =>
      callEdgeFunction("get-todos", z.array(TodoSchema), {
        method: "GET",
        logger,
      }),
    {
      onError: () => {
        throw new Error("取得に失敗しました");
      },
    },
  );
}
```

**命名：**

| ファイル名 | 用途 |
|-----------|------|
| `[resource].server.ts` | サーバー用読み取り |
| `[resource].client.ts` | クライアント用 GET（必要なときのみ・任意） |

**セキュリティ：**

- クライアントから直接テーブルアクセス禁止
- データ変更は Server Actions（`_actions/`）
