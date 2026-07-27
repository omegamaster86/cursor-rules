---
title: Import Path Aliases
impact: HIGH
impactDescription: インポートパスの可読性と保守性
tags: imports, aliases, tsconfig, paths
---

## Import Path Aliases

パスエイリアスは最小構成でよい。

**tsconfig.json（dev-starter 準拠）：**

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

細分化した `@/components/*` 等の追加 paths は不要（`@/*` で足りる）。

**Correct：**

```typescript
import { Button } from "@/components/ui/button";
import { cn } from "@/utils/class-name";
import { createClient } from "@/services/supabase/server";
import { callEdgeFunction } from "@/services/supabase/edge-function";
import { TodoSchema } from "@/types/schemas/todo";
import { env } from "@/env";
```

**使い分け：**

| インポート対象 | パス形式 |
|--------------|---------|
| 共通 UI | `@/components/ui/button` |
| ユーティリティ | `@/utils/class-name` |
| Supabase | `@/services/supabase/server` |
| Zod 境界型 | `@/types/schemas/todo` |
| ページ固有 | 相対パス（`./_components/...`, `../_actions/todo`） |

**注意**: `_actions/` / `_apis/` / `_components/` / `_utils/` は相対パス。
