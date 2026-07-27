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

**アイコンの使用（Lucide React）：**

```tsx
import { Plus, Trash2, Edit } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function ActionButtons() {
  return (
    <div className="flex gap-2">
      <Button>
        <Plus className="mr-2 h-4 w-4" />
        追加
      </Button>
      <Button variant="outline" size="icon">
        <Edit className="h-4 w-4" />
      </Button>
      <Button variant="destructive" size="icon">
        <Trash2 className="h-4 w-4" />
      </Button>
    </div>
  )
}
```

**チェックリスト：**

- [ ] shadcn/ui コンポーネントを優先的に使用
- [ ] カスタマイズが必要な場合のみ Radix UI を直接使用
- [ ] アイコンは Lucide React から選択
- [ ] `asChild` prop でカスタムトリガーを実装
- [ ] アクセシビリティ属性（aria-*）を適切に設定
