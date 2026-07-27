---
title: Class Name Utilities (tailwind-merge + clsx)
impact: MEDIUM
impactDescription: 動的なクラス名の結合と競合解決
tags: tailwind-merge, clsx, classnames, styling
---

## Class Name Utilities (tailwind-merge + clsx)

**インストール:**

```bash
npm install tailwind-merge clsx
```

**配置（dev-starter 準拠）:**

```typescript
// src/utils/class-name.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

```tsx
import { cn } from "@/utils/class-name";
```

`@/lib/utils` は使わない（現行パスは `@/utils/class-name`）。

**チェックリスト:**

- [ ] `cn` は `utils/class-name.ts` に定義
- [ ] 外部 `className` は `cn()` でマージ
- [ ] Tailwind クラス競合は tailwind-merge に任せる
