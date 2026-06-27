---
title: File Naming Convention
impact: MEDIUM
impactDescription: ファイル・ディレクトリの命名規則
tags: typescript, naming, conventions, files
---

## File Naming Convention

ファイルとディレクトリの命名規則です。

### コンポーネントファイル（PascalCase.tsx）

コンポーネント名と同じ `PascalCase` を使用します。

```
✅ 良い例
UserProfile.tsx
LoginForm.tsx
HeaderNavigation.tsx

❌ 悪い例
userProfile.tsx // camelCase
user-profile.tsx // kebab-case
user_profile.tsx // snake_case
```

### ユーティリティ・ヘルパーファイル（camelCase.ts）

```
✅ 良い例
formatDate.ts
validateEmail.ts
apiClient.ts
utils.ts

❌ 悪い例
FormatDate.ts // PascalCase
format-date.ts // kebab-case
format_date.ts // snake_case
```

### Next.js 特有のファイル

Next.js の規約に従います。

```
✅ Next.jsの規約に従ったファイル名
page.tsx          // ページコンポーネント
layout.tsx        // レイアウトコンポーネント
loading.tsx       // ローディング画面
error.tsx         // エラー画面
route.ts          // API Route
```

### 型・インターフェースの命名（PascalCase）

```typescript
// ✅ 良い例
type User = {
  id: string;
  name: string;
};

type ApiResponse<T> = {
  data: T;
  message: string;
};

// ❌ 悪い例
type user = { /* ... */ }; // camelCase
type user_type = { /* ... */ }; // snake_case
```

### Props 型の命名

コンポーネント名 + `Props` の形式を使用します。

```typescript
// ✅ 良い例
type UserProfileProps = {
  userId: string;
  showAvatar?: boolean;
};

export function UserProfile({ userId, showAvatar }: UserProfileProps) {
  // ...
}

// ❌ 悪い例
type Props = { /* ... */ }; // 汎用的すぎる
type UserProfileProperties = { /* ... */ }; // 冗長
```

### ディレクトリの命名（kebab-case）

Next.js App Router の規約に従い、`kebab-case` を使用します。

```
✅ 良い例
components/
hooks/
lib/
types/
app/user-profile/
app/admin-dashboard/

❌ 悪い例
Components/ // PascalCase
user_profile/ // snake_case
userProfile/ // camelCase
```

### 動的ルートのディレクトリ

```
✅ Next.jsの規約に従ったディレクトリ名
app/posts/[id]/
app/users/[userId]/
app/products/[slug]/
```

### Server Action のファイル名

```
✅ 良い例
_apis/schedule.server.ts    // データ取得用
_actions/todo.ts            // データ変更用

❌ 悪い例
scheduleServer.ts // サフィックスなし
```

**チェックリスト：**

- [ ] コンポーネントは PascalCase.tsx
- [ ] ユーティリティは camelCase.ts
- [ ] ディレクトリは kebab-case
- [ ] Next.js 規約ファイルは固定名を使用
- [ ] Props 型は ComponentNameProps 形式
