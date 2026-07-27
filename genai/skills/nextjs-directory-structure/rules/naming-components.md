---
title: Component Naming Convention
impact: MEDIUM
impactDescription: コードの可読性と一貫性
tags: naming, components, convention, organization
---

## Component Naming Convention

コンポーネントファイルの命名規則です。

**2つのレイヤー：**

| 種類 | 配置 | 命名 |
|------|------|------|
| shadcn/ui | `components/ui/*.tsx` | **kebab-case.tsx**（`button.tsx`） |
| 機能コンポーネント | `_components/Name/` または `components/...` | ディレクトリ **PascalCase** + `index.tsx` |

**Correct：**

```
components/ui/
├── button.tsx
├── alert-dialog.tsx
└── table.tsx

app/(dashboard)/todos/_components/
└── TodoList/
    └── index.tsx
```

**命名パターン：**

| 種類 | 例 |
|------|-----|
| UI | `button`, `input`（ファイル） / `Button`（export） |
| カード | `TodoCard` |
| フォーム | `NewTodoForm`, `LoginForm` |
| リスト | `TodoList` |

**インポート：**

```typescript
import { Button } from "@/components/ui/button";
import { TodoList } from "./_components/TodoList";
```

Storybook / `__tests__/` は任意（現状 starter では必須ではない）。
