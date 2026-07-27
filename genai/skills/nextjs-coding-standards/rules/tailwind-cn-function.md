---
title: Tailwind CSS cn Function
impact: MEDIUM
impactDescription: Tailwind クラス名のマージに cn() を使用
tags: tailwind, css, styling, utility
---

## Tailwind CSS cn Function

Tailwind CSS クラスを記述する際は、`cn` ユーティリティ関数を使用します。

**cn 関数の定義：**

```typescript
// utils/class-name.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Tailwind CSS クラス名をマージするユーティリティ関数
 * clsx で条件付きクラスを生成し、tailwind-merge で競合を解決
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

**使用ルール：**

- 条件付きクラスや動的クラスが必要な場合は必ず `cn` 関数を使用
- 単純な文字列連結は使用しない

**使用例：**

```typescript
import { cn } from "@/utils/class-name";

type ButtonProps = {
  variant?: "primary" | "secondary";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  className?: string;
};

export function Button({
  variant = "primary",
  size = "md",
  disabled = false,
  className,
}: ButtonProps) {
  return (
    <button
      className={cn(
        // ベースクラス
        "rounded-md font-medium transition-colors",
        // バリアント別クラス
        variant === "primary" && "bg-blue-600 text-white hover:bg-blue-700",
        variant === "secondary" && "bg-gray-200 text-gray-900 hover:bg-gray-300",
        // サイズ別クラス
        size === "sm" && "px-3 py-1.5 text-sm",
        size === "md" && "px-4 py-2 text-base",
        size === "lg" && "px-6 py-3 text-lg",
        // 無効化時のクラス
        disabled && "cursor-not-allowed opacity-50",
        // 外部から渡されるクラス（競合が自動的に解決される）
        className
      )}
      disabled={disabled}
    >
      Click me
    </button>
  );
}
```

**良い例と悪い例：**

```typescript
// ❌ 悪い例：文字列連結（クラス競合が解決されない）
<button className={`px-4 py-2 ${variant === "primary" ? "bg-blue-600" : "bg-gray-200"} ${className}`}>
  Click me
</button>

// ✅ 良い例：cn 関数を使用（クラス競合が自動的に解決される）
<button className={cn("px-4 py-2", variant === "primary" ? "bg-blue-600" : "bg-gray-200", className)}>
  Click me
</button>
```

**チェックリスト：**

- [ ] 条件付きクラスは `cn` 関数を使用
- [ ] 外部から className を受け取る場合は `cn` でマージ
- [ ] 文字列連結やテンプレートリテラルは使用しない
