---
title: File Naming Convention
impact: MEDIUM
impactDescription: ファイル・ディレクトリの命名規則
tags: typescript, naming, conventions, files
---

## File Naming Convention

ファイルとディレクトリの命名規則です。

### コンポーネントファイル

- **機能コンポーネント（コロケーション）**: ディレクトリ + `index.tsx`（例: `NewTodoForm/index.tsx`）または `PascalCase.tsx`
- **shadcn/ui**: フラットな `kebab-case.tsx`（例: `components/ui/button.tsx`）

```
✅
_components/NewTodoForm/index.tsx
components/ui/button.tsx
components/ui/alert-dialog.tsx

❌
components/ui/Button/index.tsx  // shadcn 標準と異なる
```

### ユーティリティ・ヘルパーファイル（kebab-case.ts）

複数語の util は **kebab-case**（実装どおり）。

```
✅
utils/class-name.ts
app/.../_utils/todo-labels.ts

❌
formatDate.ts          // camelCase（複数語 util）
utils/className.ts
```

単一語（`utils.ts`）や既存の単一モジュール名はそのままでよい。

### Next.js 特有のファイル

```
page.tsx / layout.tsx / loading.tsx / error.tsx / route.ts
```

### 型・Props

```typescript
type User = { id: string; name: string };
type UserProfileProps = { userId: string };
```

### ディレクトリ（kebab-case）

```
app/user-profile/
app/(dashboard)/todos/
```

### Server Action / API

```
✅
_apis/todo.server.ts
_actions/todo.ts
_actions/schema.ts
_actions/types.ts

❌
scheduleServer.ts
```

**チェックリスト：**

- [ ] shadcn/ui は `kebab-case.tsx`
- [ ] 複数語 util は kebab-case
- [ ] ディレクトリは kebab-case
- [ ] 読み取りは `_apis/*.server.ts`、書き込みは `_actions/`
