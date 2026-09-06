---
title: Import Order Convention
impact: LOW
impactDescription: コードの可読性と一貫性
tags: imports, order, convention, organization, biome
---

## Import Order Convention

インポート文の順序は **Biome の organizeImports** に完全に準拠します。手動で整理する必要はなく、Biome が自動的に整列します。

**Biome のインポート整理順序：**

1. 副作用インポート（`import './styles.css'`）
2. Node.js ビルトイン（`node:` プレフィックス）
3. 外部ライブラリ（`react`, `react-hook-form` など）
4. 内部モジュール（エイリアス `@/` を使用）
5. 相対パスインポート（`./`, `../`）

各グループ内ではアルファベット順にソートされ、**グループ間に空行は入りません**。

**Incorrect（ランダムな順序）:**

```typescript
import { Button } from '@/components/ui/Button'
import React from 'react'
import { createTodo } from './_actions/todo'
import type { Todo } from '@/types'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import './styles.css'
```

**Correct（Biome による整理後）:**

```typescript
import './styles.css'
import React, { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import type { Todo, User } from '@/types'
import { Button } from '@/components/ui/Button'
import { useAuth } from '@/hooks/useAuth'
import { formatDate } from '@/utils/format'
import { createTodo } from './_actions/todo'
import { NewTodoForm } from './_components/NewTodoForm'
```

**Biome の設定（biome.json）:**

```json
{
  "assist": {
    "actions": {
      "source": {
        "organizeImports": "on"
      }
    }
  }
}
```

**自動整列の実行方法：**

```bash
# チェックのみ
biome check --organize-imports-enabled=true

# 自動修正
biome check --write --organize-imports-enabled=true
```

**Note:** VSCode/Cursor で Biome 拡張機能を使用している場合、保存時に自動的にインポートが整理されます。
