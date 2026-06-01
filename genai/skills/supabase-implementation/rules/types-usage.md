---
title: Type Usage
impact: HIGH
impactDescription: database.types.ts の型定義の使用方法
tags: supabase, typescript, types
---

## Type Usage

`database.types.ts` から型をインポートして型安全なコードを実現します。

**基本原則：**

- Database Functions の戻り値は `database.types.ts` から型を参照する
- 型安全性を確保し、スキーマ変更時に自動的に型エラーを検知できる

**Database Functions の型参照：**

```typescript
import type { Database } from "../_shared/database.types.ts";

// Database Function の戻り値の型を定義
type UserData = Database["public"]["Functions"]["sel_user_by_auth_id"]["Returns"][0];

Deno.serve(async (req) => {
  const { data, error } = await supabase.rpc("sel_user_by_auth_id", {
    target_auth_user_id: "xxx",
  });

  // database.types.ts で定義された型を使用
  const userData: UserData = data[0];
});
```

**Tables 型を使用する場合（簡潔な書き方）：**

```typescript
import type { Database, Tables } from "../_shared/database.types.ts";

// Database Function の戻り値の型
type UserData = Database["public"]["Functions"]["sel_user_by_auth_id"]["Returns"][0];

// テーブルの型を直接参照する場合（簡潔な書き方）
type Customer = Tables["m_customer"];

// 複数のテーブル型を使用する例
type Office = Tables["m_office"];
type Department = Tables["m_department"];
```

**Database 型を使用する場合（詳細な型定義）：**

```typescript
import type { Database } from "../_shared/database.types.ts";

// フルパスで指定する場合
type Customer = Database["public"]["Tables"]["m_customer"]["Row"];
type CustomerInsert = Database["public"]["Tables"]["m_customer"]["Insert"];
type CustomerUpdate = Database["public"]["Tables"]["m_customer"]["Update"];
```

**型の種類：**

| 型 | 用途 |
|----|------|
| `["Row"]` | SELECT で取得する行の型 |
| `["Insert"]` | INSERT 時の型（オプショナルなカラムは optional） |
| `["Update"]` | UPDATE 時の型（すべてのカラムが optional） |
| `["Returns"]` | Database Functions の戻り値の型 |
| `["Args"]` | Database Functions の引数の型 |

**型定義のメリット：**

| メリット | 説明 |
|----------|------|
| ✅ 型安全性の向上 | データベースの型定義と完全に同期 |
| ✅ 補完機能 | IDE でプロパティが正確に補完される |
| ✅ メンテナンス性 | スキーマ変更時に自動的に型エラーで検知できる |
| ✅ 可読性 | 型定義で意図が明確 |

> 💡 **推奨**: 通常は `Tables` 型とともに `Database["public"]["Functions"]` を使用します。

**チェックリスト：**

- [ ] `database.types.ts` から型をインポートしている
- [ ] Database Functions の戻り値に型を適用している
- [ ] `any` 型を使用していない
- [ ] テーブルの型は `Tables` または `Database["public"]["Tables"]` から参照
