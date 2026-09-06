---
title: TypeScript Configuration
impact: HIGH
impactDescription: 型安全性の最大化と開発体験の向上
tags: typescript, types, configuration
---

## TypeScript Configuration

TypeScript の設定と型安全性のベストプラクティスです。

**推奨 tsconfig.json（Next.js）：**

```json
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**strict モードのルール：**

```typescript
// strict: true は以下を有効化
// - noImplicitAny: 暗黙の any を禁止
// - strictNullChecks: null/undefined の厳密なチェック
// - strictFunctionTypes: 関数型の厳密なチェック
// - strictBindCallApply: bind/call/apply の型チェック
// - strictPropertyInitialization: プロパティ初期化の強制
// - noImplicitThis: 暗黙の this を禁止
// - alwaysStrict: 常に "use strict" を出力
```

**型定義のベストプラクティス：**

```typescript
// 1. 型のインポートは type キーワードを使用
import type { User } from '@/types'
import { createUser } from '@/services/user'

// 2. コンポーネントの Props 型
type ButtonProps = {
  variant?: 'primary' | 'secondary'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
}

// 3. API レスポンス型
type ApiResponse<T> = {
  data: T | null
  error: string | null
  status: number
}

// 4. 型ガード
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value
  )
}

// 5. ユーティリティ型の活用
type PartialUser = Partial<User>
type RequiredUser = Required<User>
type ReadonlyUser = Readonly<User>
type UserKeys = keyof User
type PickedUser = Pick<User, 'id' | 'name'>
type OmittedUser = Omit<User, 'password'>
```

**Supabase 型の自動生成：**

```bash
# Supabase CLI で型を生成
npx supabase gen types typescript --project-id <project-id> > database.types.ts
```

```typescript
// database.types.ts から型をインポート
import type { Database } from '@/types/database.types'

type Todo = Database['public']['Tables']['todos']['Row']
type InsertTodo = Database['public']['Tables']['todos']['Insert']
type UpdateTodo = Database['public']['Tables']['todos']['Update']
```

**チェックリスト：**

- [ ] `strict: true` を有効化
- [ ] 型のインポートは `import type` を使用
- [ ] `any` の使用を最小限に
- [ ] API レスポンスに適切な型を定義
- [ ] Supabase の型は自動生成を活用
- [ ] 型ガードで unknown 型を安全に変換
