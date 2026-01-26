## 1. TypeScript 型定義規約

TypeScript を使用する際の型定義に関する規約を定義します。

### 1.1 型定義の基本方針

#### 1.1.1 `type` の優先使用

- 型を定義するときは基本的に `type` を使用する
- `type` で実現できない場合（例：宣言のマージが必要な場合）に限り `interface` を使用する

#### 1.1.2 型定義の配置場所

- 基本的に `src/types/index.ts` に集約する
- そのページでしか使用しない型に限り、`page.tsx` やその他のファイルに個別定義することを許容する
- `src/types/index.ts` に定義する型情報は、なるべく `src/types/database.types.ts` を使って再定義すること
  - データベースから取得したデータを扱う型は、`database.types.ts` の型定義をベースに作成する
  - これにより、データベーススキーマの変更が型定義に自動的に反映される
  - 例：`type User = Tables<"m_user">` のように再定義する

#### 1.1.3 DB管理データの型情報

- データベースの型定義は、Supabase CLI を使用して自動生成された `src/types/database.types.ts` を参照する
- 型定義ファイルは以下のコマンドで生成・更新する：

```bash
npx --yes supabase gen types typescript --schema public --local > src/types/database.types.ts
```

- データベーススキーマを変更した場合は、必ず型定義ファイルを再生成すること

### 1.2 型定義の記載例

```typescript
// src/types/index.ts（共通型定義）
import { Tables, TablesInsert, TablesUpdate } from '@/types/database.types';

// database.types.tsから再定義した型（推奨）
export type User = Tables<"m_user">;
export type UserInsert = TablesInsert<"m_user">;
export type UserUpdate = TablesUpdate<"m_user">;

// database.types.tsに基づかない型（データベースに関係ない型の場合）
export type ApiResponse<T> = {
  data: T;
  message: string;
};
```

```typescript
// app/dashboard/page.tsx（そのページでのみ使用する型）
type DashboardStats = {
  totalUsers: number;
  activeUsers: number;
};
```

```typescript
// src/types/database.types.ts（Supabase CLIで自動生成されたDB型定義）
// このファイルは自動生成されるため、直接編集しない
```

---
