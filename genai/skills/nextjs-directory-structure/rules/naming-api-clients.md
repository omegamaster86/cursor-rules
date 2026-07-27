---
title: API Client Naming Convention
impact: HIGH
impactDescription: サーバー/クライアント分離の明確化
tags: naming, api-clients, server, client, convention
---

## API Client Naming Convention

API クライアントファイルの命名規則です。

**命名パターン：**

```
[resource].server.ts    # サーバー用（読み取り）— 標準
[resource].client.ts    # クライアント用 GET — 任意・現状ほぼ未使用
```

**Correct：**

```
_apis/
└── todo.server.ts    # ✅ サーバー用読み取り
```

`src/apis/` と `*.client.ts` は複数ページ共有やクライアント GET が必要になったときのオプション。

**サーバー用の中身：**

```typescript
"use server";

import { handler } from "@/services/handler";
import { callEdgeFunction } from "@/services/supabase/edge-function";

export async function getTodos() {
  return handler("getTodos", async (logger) =>
    callEdgeFunction("get-todos", /* schema */, { method: "GET", logger }),
  {
    onError: () => {
      throw new Error("取得に失敗しました");
    },
  });
}
```

**書き込みは `_actions/`**（`_apis` に置かない）。

| リソース | 読み取り | 書き込み |
|---------|----------|----------|
| Todo | `_apis/todo.server.ts` | `_actions/todo.ts` |
