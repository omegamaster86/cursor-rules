---
title: UI Components (shadcn/ui + Radix UI)
impact: HIGH
impactDescription: 統一されたUIコンポーネントとアクセシビリティ対応
tags: shadcn, radix-ui, components, accessibility
---

## UI Components (shadcn/ui + Radix UI)

shadcn/uiとRadix UIを使用したUIコンポーネント実装のベストプラクティスです。

**インストール：**

```bash
# shadcn/ui の初期化
npx shadcn@latest init

# コンポーネントの追加
npx shadcn@latest add button
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
```

**基本的な使用：**

```tsx
// shadcn/ui コンポーネントのインポート
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'

export function ConfirmDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">削除</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>本当に削除しますか？</DialogTitle>
          <DialogDescription>
            この操作は取り消せません。
          </DialogDescription>
        </DialogHeader>
        <div className="flex justify-end gap-2">
          <Button variant="outline">キャンセル</Button>
          <Button variant="destructive">削除</Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
```

**Radix UI の直接使用（カスタマイズが必要な場合）：**

```tsx
import * as DropdownMenu from '@radix-ui/react-dropdown-menu'

export function CustomDropdown() {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button className="rounded-md p-2">メニュー</button>
      </DropdownMenu.Trigger>
      <DropdownMenu.Portal>
        <DropdownMenu.Content className="rounded-md bg-white shadow-lg">
          <DropdownMenu.Item className="cursor-pointer p-2 hover:bg-gray-100">
            編集
          </DropdownMenu.Item>
          <DropdownMenu.Item className="cursor-pointer p-2 hover:bg-gray-100">
            削除
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  )
}
```

**アイコンの使用（Material Symbols）：**

```tsx
import { Add } from '@material-symbols-svg/react/icons/add'
import { Delete } from '@material-symbols-svg/react/icons/delete'
import { Edit } from '@material-symbols-svg/react/icons/edit'
import { Button } from '@/components/ui/button'

export function ActionButtons() {
  return (
    <div className="flex gap-2">
      <Button>
        <Add size={16} className="mr-2" />
        追加
      </Button>
      <Button variant="outline" size="icon">
        <Edit size={16} />
      </Button>
      <Button variant="destructive" size="icon">
        <Delete size={16} />
      </Button>
    </div>
  )
}
```

**Suspense フォールバック（Skeleton）：**

ローディング UI は空の `div` や独自の pulse 実装ではなく、shadcn/ui の `Skeleton` を使う。

```bash
npx shadcn@latest add skeleton
```

```tsx
import { Skeleton } from "@/components/ui/skeleton";

/**
 * 一覧の Suspense フォールバック
 * 実コンポーネントのレイアウト（見出し・カード・行）に合わせる
 */
export function TodoListSkeleton() {
  return (
    <output aria-busy="true" className="flex flex-col gap-4">
      <span className="sr-only">ToDoを読み込み中</span>
      <div className="section-heading">
        <Skeleton className="h-7 w-40" />
      </div>
      <div className="flex flex-col gap-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="rounded border border-border bg-card p-5">
            <div className="flex flex-wrap items-center gap-2">
              <Skeleton className="h-5 w-48" />
              <Skeleton className="h-5 w-16" />
            </div>
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
          </div>
        ))}
      </div>
    </output>
  );
}
```

**配置：**

```
_components/
└── TodoList/
    ├── index.tsx              # 本体
    └── TodoListSkeleton.tsx   # Suspense fallback
```

**ルール：**

1. `@/components/ui/skeleton` の `Skeleton` を使う（独自の `animate-pulse` div は作らない）
2. 実コンポーネントと同じ余白・カード構造に揃える
3. アクセシブル名は `aria-label` を素の `div` に付けない。`<output aria-busy>` + `sr-only` テキスト、または `ul` など名前を持てる要素を使う
4. ファイル名は `{ComponentName}Skeleton.tsx` とし、本体と同ディレクトリにコロケーションする

**チェックリスト：**

- [ ] shadcn/ui コンポーネントを優先的に使用
- [ ] カスタマイズが必要な場合のみ Radix UI を直接使用
- [ ] アイコンは `@material-symbols-svg/react`（deep import）から選択
- [ ] `asChild` prop でカスタムトリガーを実装
- [ ] アクセシビリティ属性（aria-*）を適切に設定
- [ ] Suspense フォールバックは shadcn/ui の `Skeleton` を使用
