---
title: Styling with Tailwind CSS
impact: HIGH
impactDescription: 一貫したスタイリングとレスポンシブデザイン
tags: tailwind, css, styling, responsive
---

## Styling with Tailwind CSS

Tailwind CSS **v4** を使用したスタイリングのベストプラクティスです。

**セットアップ（CSS-first）:**

- `globals.css` で `@import "tailwindcss"`
- テーマは CSS 変数（多くは `oklch(...)`）+ `@theme`
- 旧来の `tailwind.config.js` 中心の色定義は必須ではない

**セマンティックカラーを優先:**

```tsx
// ✅ DESIGN / テーマトークン
<div className="rounded-lg border bg-card p-4 text-foreground">
<button className="bg-primary text-primary-foreground hover:bg-primary/90">

// ❌ 汎用 gray / blue-600 の多用（DESIGN.md がある場合は避ける）
<header className="bg-white dark:bg-gray-900">
```

**cn ユーティリティ:**

```tsx
import { cn } from "@/utils/class-name";

<button
  className={cn(
    "rounded-md bg-primary px-4 py-2 text-primary-foreground",
    disabled && "cursor-not-allowed opacity-50",
    className,
  )}
/>
```

**ポイント:**

1. rem ベースのスペーシングを優先（`tailwind-rem-units` 参照）
2. shadcn 由来の任意値（`min-h-[80px]` 等）は UI プリミティブ内では許容
3. アプリ固有画面ではセマンティックトークンを優先
