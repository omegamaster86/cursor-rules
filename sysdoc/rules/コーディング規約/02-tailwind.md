## 2. Tailwind CSS クラス記述規約

Tailwind CSS クラスを記述する際は、`tailwind-merge` と `clsx` を組み合わせた `cn` ユーティリティ関数を使用します。

### 2.1 `cn` 関数の定義

`utils/class-name.ts` に以下の関数を定義します。この関数は `clsx` で条件付きクラス名を生成し、`tailwind-merge` で Tailwind クラスの競合を解決します。

```typescript
// utils/class-name.ts（cn 関数の定義）
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

### 2.2 使用ルール

- Tailwind CSS クラスを記述する際に、条件付きクラスや動的クラスが必要な場合は必ず `cn` 関数で記述する
- 単純な文字列連結は使用しない

### 2.3 使用例

```typescript
// components/Button.tsx（使用例）
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

### 2.4 良い例と悪い例

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

---
