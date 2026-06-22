---
title: Styling with Tailwind CSS
impact: HIGH
impactDescription: 一貫したスタイリングとレスポンシブデザイン
tags: tailwind, css, styling, responsive
---

## Styling with Tailwind CSS

Tailwind CSS を使用したスタイリングのベストプラクティスです。

**基本的なスタイリング：**

```tsx
// レスポンシブデザイン
export function Card({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-lg border bg-card p-4 shadow-sm md:p-6 lg:p-8">
      {children}
    </div>
  )
}

// ダークモード対応
export function Header() {
  return (
    <header className="bg-white dark:bg-gray-900">
      <h1 className="text-gray-900 dark:text-white">タイトル</h1>
    </header>
  )
}

// 状態に応じたスタイリング
export function InteractiveButton() {
  return (
    <button className="rounded-md bg-primary px-4 py-2 text-white transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50">
      クリック
    </button>
  )
}
```

**tailwind-merge と clsx の併用：**

```tsx
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

// cn ユーティリティ関数（shadcn/ui 標準）
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// 使用例
interface ButtonProps {
  variant?: 'primary' | 'secondary'
  disabled?: boolean
  className?: string
}

export function Button({ variant = 'primary', disabled, className }: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-md px-4 py-2 font-medium transition-colors',
        variant === 'primary' && 'bg-primary text-white hover:bg-primary/90',
        variant === 'secondary' && 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        disabled && 'cursor-not-allowed opacity-50',
        className
      )}
      disabled={disabled}
    >
      ボタン
    </button>
  )
}
```

**Tailwind CSS のカスタマイズ：**

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // shadcn/ui のカラーシステムを使用
        border: 'hsl(var(--border))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
      },
    },
  },
}
```

**チェックリスト：**

- [ ] `cn()` ユーティリティを使用してクラス名を結合
- [ ] レスポンシブプレフィックス（sm:, md:, lg:）を適切に使用
- [ ] ダークモード対応（dark: プレフィックス）
- [ ] CSS変数を使用したテーマカラー
- [ ] 重複するスタイルを tailwind-merge で解決
