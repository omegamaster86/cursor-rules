---
title: Tables with TanStack Table
impact: MEDIUM
impactDescription: 高機能なテーブル実装（ソート、フィルター、ページネーション）
tags: tanstack-table, table, sorting, filtering, pagination
---

## Tables with TanStack Table

TanStack Table を使用したテーブル実装のベストプラクティスです。

**インストール：**

```bash
npm install @tanstack/react-table
```

**基本的なテーブル実装：**

```tsx
'use client'

import {
  useReactTable,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  flexRender,
  type ColumnDef,
  type SortingState,
} from '@tanstack/react-table'
import { useState } from 'react'
import { ArrowUpDown } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

// 1. データ型を定義
type User = {
  id: string
  name: string
  email: string
  role: string
}

// 2. カラム定義
const columns: ColumnDef<User>[] = [
  {
    accessorKey: 'name',
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
      >
        名前
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
  },
  {
    accessorKey: 'email',
    header: 'メールアドレス',
  },
  {
    accessorKey: 'role',
    header: 'ロール',
    cell: ({ row }) => (
      <span className="rounded-full bg-primary/10 px-2 py-1 text-sm">
        {row.getValue('role')}
      </span>
    ),
  },
]

// 3. テーブルコンポーネント
export function UsersTable({ data }: { data: User[] }) {
  const [sorting, setSorting] = useState<SortingState>([])
  const [globalFilter, setGlobalFilter] = useState('')

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    state: {
      sorting,
      globalFilter,
    },
  })

  return (
    <div className="space-y-4">
      {/* 検索フィールド */}
      <Input
        placeholder="検索..."
        value={globalFilter}
        onChange={(e) => setGlobalFilter(e.target.value)}
        className="max-w-sm"
      />

      {/* テーブル */}
      <div className="rounded-md border">
        <table className="w-full">
          <thead className="border-b bg-muted/50">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th key={header.id} className="px-4 py-3 text-left">
                    {flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id} className="border-b">
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id} className="px-4 py-3">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ページネーション */}
      <div className="flex items-center justify-end gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          前へ
        </Button>
        <span className="text-sm text-muted-foreground">
          {table.getState().pagination.pageIndex + 1} / {table.getPageCount()}
        </span>
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          次へ
        </Button>
      </div>
    </div>
  )
}
```

**チェックリスト：**

- [ ] カラム定義は外部で定義（再レンダリング防止）
- [ ] ソート・フィルター状態は useState で管理
- [ ] `flexRender` でカスタムセルを描画
- [ ] ページネーションは `getPaginationRowModel` を使用
- [ ] アクセシビリティを考慮したマークアップ
