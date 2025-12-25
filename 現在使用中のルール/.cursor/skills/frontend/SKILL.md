---
name: nextjs-frontend
description: Next.js (App Router) と React 19 を使用したフロントエンド開発タスクに適用。コンポーネント作成、ルーティング、データ取得、状態管理などのフロントエンド実装時に使用。
---

# Next.js フロントエンド開発

## 基本方針

### Server Components 優先
- デフォルトは Server Components を使用
- `'use client'` はインタラクションが必要な場合のみ付与
- データ取得はサーバー側で行う

### 命名規則
- **ディレクトリ**: 機能名で明確に（例: `Header`, `UserProfile`）
- **ファイル**: ケバブケース（例: `user-table.tsx`, `use-selected-ids.ts`）
- **コンポーネント**: パスカルケース（例: `UserTable`, `HeaderBreadcrumb`）

## ルーティング

- Next.js App Router を使用（React Router は不可）
- 動的セグメント: `[id]`, `[...slug]`
- SSG が必要な場合: `generateStaticParams` を実装
- ナビゲーション: `Link` を優先、制御が必要な場合のみ `useRouter()`
- メタデータ: `generateMetadata`（動的）または `export const metadata`（静的）

## データ取得・キャッシュ

```typescript
// リアルタイム/常に最新
fetch(url, { cache: 'no-store' })

// ISR（増分静的再生成）
fetch(url, { next: { revalidate: 60 } })
```

## クライアントコンポーネント

以下の場合のみ `'use client'` を使用:
- フォーム操作
- イベントハンドリング
- アニメーション
- ブラウザ API の使用

## 状態管理

- ローカル: `useState`, `useReducer`
- グローバル: Context で十分な場合は Context を使用

## エラーハンドリング

- `error.tsx`: エラー境界
- `not-found.tsx`: 404 ページ
- `loading.tsx`: ローディング状態

## TypeScript

- すべて型定義必須、`any` は禁止
- 共通型は `types/index.ts` に集約

## CSS

- Tailwind CSS を使用
- `className` の合成は `clsx` を使用

詳細は [references/REFERENCE.md](references/REFERENCE.md) を参照。
