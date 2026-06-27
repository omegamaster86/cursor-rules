---
title: Form Validation with Zod
impact: HIGH
impactDescription: Zod を使用したフォームバリデーション規約
tags: forms, validation, zod, server-actions
---

## Form Validation with Zod

フォームバリデーションは Zod を使用して実装します。

### バリデーション戦略

```
1. Server Action でのZodバリデーション（形式チェック）
   ↓
2. DB Function でのDBバリデーション（DB参照が必要なチェック）
```

### Server Action での Zod バリデーション

**実施タイミング：** Server Action で、DBアクセスの前に実施

**対象：**
- 入力値の形式チェック（メールアドレス、URL、日付など）
- 必須項目チェック
- 文字数制限
- 数値範囲チェック
- 列挙型（enum）の値チェック

```typescript
"use server";

import { z } from "zod";

// Zodスキーマ定義
const CreateUserFormSchema = z.object({
  email: z.string().email("有効なメールアドレスを入力してください"),
  username: z.string()
    .min(3, "ユーザー名は3文字以上必要です")
    .max(20, "ユーザー名は20文字以内で入力してください"),
  age: z.number()
    .int()
    .min(18, "18歳以上である必要があります")
    .max(120),
  role: z.enum(["admin", "user", "guest"], {
    errorMap: () => ({ message: "無効な役割です" }),
  }),
});

export async function createUser(
  _prevState: CreateUserState,
  formData: FormData,
): Promise<CreateUserState> {
  // 1. FormDataから値を取得
  const rawFormData = {
    email: formData.get("email"),
    username: formData.get("username"),
    age: parseInt(formData.get("age") as string, 10),
    role: formData.get("role"),
  };

  // 2. ✅ Zodでバリデーション（DBアクセス前）
  const validationResult = CreateUserFormSchema.safeParse(rawFormData);

  if (!validationResult.success) {
    const fieldErrors = validationResult.error.flatten().fieldErrors;
    return {
      success: false,
      message: fieldErrors.email?.[0] || "入力内容が不正です",
      error: "VALIDATION_ERROR",
      fieldErrors,
    };
  }

  // 3. バリデーション済みデータを使用
  const validatedData = validationResult.data;
  // ...
}
```

### クライアントサイドバリデーション

**基本方針：** HTML5 ネイティブバリデーションは使用しない

**リアルタイムバリデーションが必要な場合：** `react-hook-form` + `zod` を使用

```typescript
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

// サーバーサイドと同じZodスキーマを使用
const CreateUserFormSchema = z.object({
  email: z.string().email("有効なメールアドレスを入力してください"),
  username: z.string().min(3, "ユーザー名は3文字以上必要です"),
});

type FormData = z.infer<typeof CreateUserFormSchema>;

export function CreateUserForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(CreateUserFormSchema),
    mode: "onBlur", // フォーカスを外したときにバリデーション
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="text" {...register("email")} />
      {errors.email && <p>{errors.email.message}</p>}
      <button type="submit" disabled={isSubmitting}>送信</button>
    </form>
  );
}
```

### safeParse() vs parse()

**必ず `safeParse()` を使用してください。**

```typescript
// ✅ 良い例：safeParse()を使用
const result = Schema.safeParse(jsonData);
if (!result.success) {
  return { success: false, error: result.error.message };
}
const data = result.data;

// ❌ 悪い例：parse()を使用（例外が投げられる）
try {
  const data = Schema.parse(jsonData);
} catch (error) {
  // エラーハンドリングが複雑
}
```

**チェックリスト：**

- [ ] サーバーサイドで必ず Zod バリデーションを実施
- [ ] HTML5 バリデーション属性は使用しない
- [ ] `safeParse()` を使用
- [ ] クライアント/サーバーで Zod スキーマを共有
