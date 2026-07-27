---
title: Utilities Colocation
impact: MEDIUM
impactDescription: ページ固有ヘルパーの配置と命名の一貫性
tags: utilities, helpers, colocation, utils
---

## Utilities Colocation

ページ／機能固有のヘルパー関数は`_utils/`に、アプリ全体で使うものは`src/utils/`に配置します。`_lib/`や`lib/`は使いません。

**Incorrect（`_lib/` / `lib/` を使う）:**

```
app/(dashboard)/todos/
├── _lib/                 # ❌ `_utils/` を使う
│   └── todo-labels.ts
└── page.tsx

src/
└── lib/                  # ❌ ヘルパーは `utils/` に置く
    └── format.ts
```

**Correct（`_utils/` と `utils/` を使い分ける）:**

```
src/
├── utils/                      # 複数機能で使う共通ヘルパー
│   ├── class-name.ts
│   └── redirect.ts
└── app/
    └── (dashboard)/
        └── todos/
            ├── _utils/         # todos 機能内で共有するヘルパー
            │   └── todo-labels.ts
            ├── _components/
            ├── [id]/
            └── page.tsx
```

**配置の判断：**

| 用途 | 配置先 |
|------|--------|
| 1つのルートグループ／機能でのみ使う | `app/[feature]/_utils/` |
| アプリ全体で使う汎用ヘルパー | `src/utils/` |

**命名の一貫性：**

| 種類 | ページ／機能固有 | 共通 |
|------|------------------|------|
| Server Actions | `_actions/` | - |
| API クライアント | `_apis/` | `apis/` |
| コンポーネント | `_components/` | `components/` |
| ヘルパー関数 | `_utils/` | `utils/` |

**例：**

```typescript
// app/(dashboard)/todos/_utils/todo-labels.ts
export function getStatusLabel(status: string): string {
  switch (status) {
    case "completed":
      return "完了";
    case "in_progress":
      return "進行中";
    case "pending":
      return "未着手";
    case "cancelled":
      return "キャンセル";
    default:
      return status;
  }
}
```

```typescript
// app/(dashboard)/todos/_components/TodoList/index.tsx
import { getStatusLabel } from "../../_utils/todo-labels";
```

**ポイント：**

1. `_utils`はルーティングに影響しない（`_`プレフィックス）
2. `_actions` / `_apis` / `_components` と同じコロケーション規約に揃える
3. ヘルパーに`_lib` / `lib`は使わない（`utils`に統一）
4. 複数機能で再利用が必要になったら`src/utils/`へ移動する
