---
title: Component Split Guidelines
impact: MEDIUM
impactDescription: コンポーネント分割の判断基準
tags: react, components, architecture, best-practices
---

## Component Split Guidelines

コンポーネントを分割する際の判断基準です。

### 分割の判断基準

| 条件 | 分割推奨度 |
|-----|----------|
| 複数箇所で再利用される | ✅ 分割する |
| 100行を超える | ✅ 分割を検討 |
| 独立した責務を持つ | ✅ 分割する |
| テストを個別に書きたい | ✅ 分割する |
| 1箇所でのみ使用、50行未満 | ❌ 分割不要 |

### コンポーネント分割の例

**分割前（大きすぎるコンポーネント）：**

```typescript
// ❌ 悪い例：1つのファイルに複数の責務
export default function TodoPage() {
  return (
    <div>
      <header>
        <h1>ToDo一覧</h1>
        <nav>{/* ナビゲーション */}</nav>
      </header>
      <main>
        <form>{/* フォーム */}</form>
        <ul>{/* ToDo一覧 */}</ul>
      </main>
      <footer>{/* フッター */}</footer>
    </div>
  );
}
```

**分割後（責務ごとに分離）：**

```typescript
// ✅ 良い例：責務ごとにコンポーネントを分割
// app/todos/page.tsx
import { TodoList } from "./_components/TodoList";
import { NewTodoForm } from "./_components/NewTodoForm";

export default function TodoPage() {
  return (
    <div>
      <h1>ToDo一覧</h1>
      <NewTodoForm />
      <TodoList />
    </div>
  );
}

// _components/TodoList/index.tsx
export function TodoList() {
  // ToDo一覧の表示ロジック
}

// _components/NewTodoForm/index.tsx
export function NewTodoForm() {
  // フォームのロジック
}
```

### ファイル配置ルール

```
app/
  (app)/
    todos/
      _components/           ← ページ固有のコンポーネント
        TodoList/
          index.tsx
        NewTodoForm/
          index.tsx
      page.tsx

components/                  ← 共通コンポーネント
  ui/
    Button.tsx
    Input.tsx
  Header.tsx
```

### コンポーネントの命名規則

```typescript
// ✅ 良い例：PascalCase、役割が明確
export function UserProfile() { /* ... */ }
export function LoginForm() { /* ... */ }
export function HeaderNavigation() { /* ... */ }
export function ProductCard() { /* ... */ }

// ❌ 悪い例
export function userProfile() { /* ... */ } // camelCase
export function User() { /* ... */ } // 役割が不明確
export function Component1() { /* ... */ } // 意味のない名前
```

### Props型の命名

```typescript
// ✅ 良い例：コンポーネント名 + Props
type UserProfileProps = {
  userId: string;
  showAvatar?: boolean;
};

export function UserProfile({ userId, showAvatar }: UserProfileProps) {
  // ...
}

// ❌ 悪い例
type Props = { /* ... */ }; // 汎用的すぎる
```

**チェックリスト：**

- [ ] 再利用されるコンポーネントは分割
- [ ] 100行を超えたら分割を検討
- [ ] ページ固有コンポーネントは `_components/` に配置
- [ ] 共通コンポーネントは `components/` に配置
