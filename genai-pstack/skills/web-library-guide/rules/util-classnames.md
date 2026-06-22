---
title: Class Name Utilities (tailwind-merge + clsx)
impact: MEDIUM
impactDescription: 動的なクラス名の結合と競合解決
tags: tailwind-merge, clsx, classnames, styling
---

## Class Name Utilities (tailwind-merge + clsx)

tailwind-merge と clsx を使用したクラス名管理のベストプラクティスです。

**インストール：**

```bash
npm install tailwind-merge clsx
```

**cn ユーティリティ関数：**

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**基本的な使用方法：**

```tsx
import { cn } from '@/lib/utils'

// 1. 複数のクラス名を結合
<div className={cn('p-4', 'bg-white', 'rounded-lg')}>
  Content
</div>

// 2. 条件付きクラス名
<button className={cn(
  'px-4 py-2 rounded-md',
  isActive && 'bg-primary text-white',
  isDisabled && 'opacity-50 cursor-not-allowed'
)}>
  Button
</button>

// 3. 外部から渡されたクラス名をマージ
type CardProps = {
  className?: string
  children: React.ReactNode
}

function Card({ className, children }: CardProps) {
  return (
    <div className={cn('p-4 bg-card rounded-lg shadow', className)}>
      {children}
    </div>
  )
}

// 使用時に上書き可能
<Card className="p-8 bg-blue-100">
  Content
</Card>
```

**tailwind-merge の競合解決：**

```tsx
// tailwind-merge なしの場合（競合が発生）
<div className="p-4 p-8">  // 両方適用される（予測不能）

// tailwind-merge ありの場合（後の値が優先）
cn('p-4', 'p-8')  // → "p-8"
cn('bg-red-500', 'bg-blue-500')  // → "bg-blue-500"
cn('text-sm', 'text-lg')  // → "text-lg"
```

**clsx のパターン：**

```tsx
import { clsx } from 'clsx'

// オブジェクト構文
clsx({
  'bg-primary': isPrimary,
  'bg-secondary': isSecondary,
  'opacity-50': isDisabled,
})

// 配列構文
clsx([
  'base-class',
  condition && 'conditional-class',
  anotherCondition ? 'true-class' : 'false-class',
])

// 混合構文
clsx(
  'always-applied',
  condition && 'conditional',
  { 'object-style': anotherCondition }
)
```

**バリアントパターン（cva との組み合わせ）：**

```tsx
// class-variance-authority (cva) と組み合わせる場合
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 px-3',
        lg: 'h-11 px-8',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> &
  VariantProps<typeof buttonVariants>

function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  )
}
```

**チェックリスト：**

- [ ] `cn()` 関数を `lib/utils.ts` に定義
- [ ] 外部から className を受け取るコンポーネントは `cn()` でマージ
- [ ] 条件付きクラスは clsx の構文を活用
- [ ] Tailwind クラスの競合は tailwind-merge が解決
