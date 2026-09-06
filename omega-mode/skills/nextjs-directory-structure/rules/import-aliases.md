---
title: Import Path Aliases
impact: HIGH
impactDescription: インポートパスの可読性と保守性
tags: imports, aliases, tsconfig, paths
---

## Import Path Aliases

パスエイリアスを設定してインポートを簡潔にします。

**tsconfig.jsonの設定：**

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/apis/*": ["./src/apis/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/utils/*": ["./src/utils/*"],
      "@/services/*": ["./src/services/*"],
      "@/types/*": ["./src/types/*"]
    }
  }
}
```

**Incorrect（相対パスの深いネスト）:**

```typescript
// app/todos/new/_components/NewTodoForm/index.tsx
import { Button } from '../../../../../components/ui/Button'
import { formatDate } from '../../../../../utils/format'
import type { Todo } from '../../../../../types'
```

**Correct（エイリアス使用）:**

```typescript
// app/todos/new/_components/NewTodoForm/index.tsx
import { Button } from '@/components/ui/Button'
import { formatDate } from '@/utils/format'
import type { Todo } from '@/types'
```

**使い分け：**

| インポート対象 | パス形式 |
|--------------|---------|
| 共通コンポーネント | `@/components/ui/Button` |
| 共通APIクライアント | `@/apis/users.server` |
| 共通フック | `@/hooks/useAuth` |
| ユーティリティ | `@/utils/format` |
| サービス | `@/services/supabase-service/client` |
| 型定義 | `@/types` |
| ページ固有（同階層） | `./Component` |
| ページ固有（親階層） | `../_actions/todo` |

**ページ固有リソースのインポート：**

```typescript
// app/todos/new/page.tsx
import { NewTodoForm } from './_components/NewTodoForm'

// app/todos/new/_components/NewTodoForm/index.tsx
import { createTodo, type CreateTodoState } from '../../_actions/todo'
```

**注意**: ページ固有リソース（`_actions/`, `_apis/`, `_components/`）は相対パスを使用。エイリアスは共通リソースのみに適用。
