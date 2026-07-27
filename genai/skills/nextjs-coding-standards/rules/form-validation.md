---
title: Form Validation with Zod
impact: HIGH
impactDescription: Zod を使用したフォームバリデーション規約
tags: forms, validation, zod, server-actions
---

## Form Validation with Zod

フォームバリデーションは Zod（**v4**）を使用して実装します。

### バリデーション戦略

```
1. Server Action での Zod バリデーション（形式チェック）— validate() 優先
   ↓
2. DB Function / Edge での DB バリデーション（DB 参照が必要なチェック）
```

### 標準: `validate()` ヘルパー

本番の Server Action ではインライン `safeParse` より `services/handler.ts` の `validate()` を使う。

```typescript
import { validate } from "@/services/handler";
import { CreateTodoFormSchema } from "./schema";

const data = validate(
  CreateTodoFormSchema,
  {
    title: formData.get("title"),
    description: formData.get("description") || null,
    priority: formData.get("priority"),
  },
  logger,
);
// 失敗時は FormValidationError（fieldErrors 付き）を throw → actionError が受け取る
```

### スキーマ定義（Zod 4）

```typescript
// _actions/schema.ts
import { z } from "zod";
import { TodoPrioritySchema } from "@/types/schemas/common";

export const CreateTodoFormSchema = z.object({
  title: z
    .string()
    .min(1, "※タイトルは必須です")
    .max(100, "※タイトルは100文字以内で入力してください"),
  description: z
    .string()
    .max(1000, "※説明は1000文字以内で入力してください")
    .optional()
    .nullable(),
  priority: TodoPrioritySchema,
});
```

Zod 3 の `errorMap` は使わず、Zod 4 のメッセージ引数 / スキーマ API に合わせる。

API 境界の UUID 例（`types/schemas`）:

```typescript
id: z.uuidv7(),
```

### クライアントサイドバリデーション

**基本方針：** HTML5 ネイティブバリデーション属性は使わない

リアルタイムが必要な場合は `react-hook-form` + `@hookform/resolvers/zod`。

### safeParse() vs parse()

`validate()` 内部は `safeParse()`。自前で書く場合も **`safeParse()` を使う**（`parse()` 禁止）。

**チェックリスト：**

- [ ] サーバーサイドで必ず Zod バリデーション
- [ ] 本番アクションは `validate()` を優先
- [ ] Zod 4 記法（`errorMap` など Zod 3 専用 API を避ける）
- [ ] HTML5 バリデーション属性は使わない
- [ ] スキーマは `_actions/schema.ts` または `types/schemas/` に配置
