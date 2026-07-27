---
title: TypeScript Type Location
impact: HIGH
impactDescription: 型定義の配置場所と database.types.ts の活用
tags: typescript, types, organization
---

## TypeScript Type Location

型定義の配置場所に関するルールです。

**基本方針：**

1. **共通型**: `src/types/index.ts` に集約
2. **ページ固有型**: 各 `page.tsx` ファイル内に定義
3. **DB型**: `src/types/database.types.ts` をベースに再定義

**database.types.ts の活用：**

```typescript
// src/types/index.ts
import type { Tables, TablesInsert, TablesUpdate } from "@/types/database.types";

// database.types.ts から再定義（推奨）
export type User = Tables<"m_user">;
export type UserInsert = TablesInsert<"m_user">;
export type UserUpdate = TablesUpdate<"m_user">;

// データベースに関係ない型
export type ApiResponse<T> = {
  success: boolean;
  data?: T;
  error?: string;
};
```

**ページ固有の型：**

```typescript
// app/dashboard/page.tsx
// そのページでのみ使用する型は、ページファイル内に定義

type DashboardStats = {
  totalUsers: number;
  activeUsers: number;
};

export default function DashboardPage() {
  const stats: DashboardStats = {
    totalUsers: 100,
    activeUsers: 50,
  };
  // ...
}
```

**型定義ファイルの生成：**

```bash
# Supabase CLI で型を生成
npx --yes supabase gen types typescript --schema public --local > src/types/database.types.ts && npx @biomejs/biome check --write src/types/database.types.ts
```

**type vs interface：**

```typescript
// ✅ 良い例：type を優先使用
type User = {
  id: string;
  name: string;
};

// interface は宣言のマージが必要な場合のみ
interface Window {
  customProperty: string;
}
```

**チェックリスト：**

- [ ] 共通型は `src/types/index.ts` に配置
- [ ] DB から取得するデータは `database.types.ts` から再定義
- [ ] ページ固有の型は各ページファイル内に定義
- [ ] `type` を優先使用（`interface` は必要な場合のみ）
