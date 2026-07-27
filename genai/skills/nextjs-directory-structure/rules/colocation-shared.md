---
title: Shared Resources Guidelines
impact: MEDIUM
impactDescription: 適切な共通化による保守性向上
tags: shared, common, refactoring, organization
---

## Shared Resources Guidelines

共通化のタイミングと判断基準を明確にします。

**段階的な共通化：**

```
段階1: まずページ固有のディレクトリに配置
       app/[page]/_components/
       app/[page]/_apis/
       app/[page]/_actions/
       app/[page]/_utils/
           ↓
段階2: 再利用が必要になったら共通ディレクトリに移動
       components/
       apis/
       utils/
```

**Incorrect（早すぎる共通化）:**

```typescript
// components/TodoForm.tsx
// 1ページでしか使わないのに最初から共通化
export function TodoForm({ mode }: { mode: 'create' | 'edit' }) {
  // modeによる分岐が複雑になる
}
```

**Correct（必要になってから共通化）:**

```typescript
// app/todos/new/_components/NewTodoForm/index.tsx
// まずはページ固有として実装
export function NewTodoForm() {
  // 新規作成専用の実装
}

// app/todos/[id]/edit/_components/EditTodoForm/index.tsx
// 編集も別に実装
export function EditTodoForm() {
  // 編集専用の実装
}

// 共通化が必要になったら
// components/TodoForm/index.tsx に移動
```

**共通化の判断チェックリスト：**

| チェック項目 | 共通化する？ |
|-------------|-------------|
| 2つ以上のページで使用する | ✅ 検討 |
| 特定のページに依存しない | ✅ 検討 |
| 汎用的なUIパターン | ✅ 検討 |
| 1つのページでのみ使用 | ❌ ページ固有 |
| ページ固有のロジックを含む | ❌ ページ固有 |
| 将来使うかもしれない | ❌ まずページ固有 |

**YAGNI原則（You Ain't Gonna Need It）：**
- 「将来使うかもしれない」という理由だけで共通化しない
- 実際に再利用が必要になった時点で共通化する
- 早すぎる抽象化は複雑性を増加させる
