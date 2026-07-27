---
title: Components Directory Structure
impact: MEDIUM
impactDescription: コンポーネントの再利用性と保守性
tags: components, ui, layouts, organization
---

## Components Directory Structure

`components/` は複数ページで共有するコンポーネントを配置します。

**推奨構成（shadcn/ui 準拠）：**

```
components/
├── ui/                      # shadcn — フラット kebab-case.tsx
│   ├── button.tsx
│   ├── input.tsx
│   ├── alert-dialog.tsx
│   └── table.tsx
├── layout/                  # アプリレイアウト
├── brand/
└── input/                   # 複合入力（_apis を同居させる例あり）
```

**ページ固有はコロケーション：**

```
app/(dashboard)/todos/_components/
└── TodoList/
    └── index.tsx
```

**ポイント：**

1. `components/ui/` は **フラットな kebab-case.tsx**（`Button/index.tsx` 構成ではない）
2. Storybook / `__tests__/` は必須ではない（現状 starter 未整備）
3. ページ固有 UI は `_components/` に置く
4. インポート例: `import { Button } from "@/components/ui/button"`
