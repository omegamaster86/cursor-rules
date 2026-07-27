---
title: TypeScript type vs interface
impact: HIGH
impactDescription: 型定義の基本方針
tags: typescript, types, best-practices
---

## TypeScript type vs interface

型を定義するときの `type` と `interface` の使い分けルールです。

**基本方針：`type` を優先使用**

- 型を定義するときは基本的に `type` を使用する
- `type` で実現できない場合（例：宣言のマージが必要な場合）に限り `interface` を使用する

**`type` を使用する場合（推奨）：**

```typescript
// ✅ 良い例：type を使用
type User = {
  id: string;
  name: string;
};

type ApiResponse<T> = {
  data: T;
  message: string;
};

// Union型
type Status = "pending" | "active" | "inactive";

// Intersection型
type AdminUser = User & {
  permissions: string[];
};
```

**`interface` を使用する場合（限定的）：**

```typescript
// interface が必要なケース：宣言のマージ（Declaration Merging）
// 例：グローバルオブジェクトの拡張
declare global {
  interface Window {
    customProperty: string;
  }
}

// 例：ライブラリの型拡張
interface Request {
  userId?: string;
}
```

**チェックリスト：**

- [ ] 新しい型を定義する際は `type` を使用
- [ ] `interface` は宣言のマージが必要な場合のみ使用
- [ ] チーム内で一貫した方針を維持
