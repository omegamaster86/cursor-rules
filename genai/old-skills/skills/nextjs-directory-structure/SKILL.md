---
name: nextjs-directory-structure
description: Defines Next.js App Router directory structure and file placement (Server/Client Components, Server Actions, API clients, colocation). Use when creating or refactoring Next.js projects, placing pages/actions/APIs, or checking naming and Supabase Edge Functions integration.
---

# Next.js Directory Structure

Next.js App Router のディレクトリ構成とファイル配置のガイド。コロケーションに基づく保守しやすい構造を定義する。

## When to Apply

- Next.js プロジェクトの新規作成時
- ページ・コンポーネントの追加時
- Server Actions・API クライアントの配置を決める時
- ファイル・ディレクトリの命名を確認する時
- 構成のリファクタリング時
- Supabase Edge Functions 連携の実装時

## Rule Categories by Priority

| Priority | Category         | Impact | Prefix         |
|----------|------------------|--------|----------------|
| 1        | Structure Rules  | HIGH   | `structure-`   |
| 2        | Colocation Rules | HIGH   | `colocation-`  |
| 3        | Naming Conventions | MEDIUM | `naming-`    |
| 4        | Import Rules     | MEDIUM | `import-`      |
| 5        | Best Practices   | HIGH   | `practice-`    |

## Quick Reference

### 1. Structure Rules (HIGH)

- [structure-project-init](rules/structure-project-init.md) - create-next-app の推奨設定
- [structure-overall](rules/structure-overall.md) - 全体構成
- [structure-app-router](rules/structure-app-router.md) - App Router の役割
- [structure-components](rules/structure-components.md) - components 構成
- [structure-services](rules/structure-services.md) - services 構成
- [structure-supabase](rules/structure-supabase.md) - supabase 構成

### 2. Colocation Rules (HIGH)

- [colocation-actions](rules/colocation-actions.md) - Server Actions（_actions/）
- [colocation-components](rules/colocation-components.md) - ページ固有（_components/）
- [colocation-apis](rules/colocation-apis.md) - API クライアント（_apis/）
- [colocation-shared](rules/colocation-shared.md) - 共通化の判断

### 3. Naming Conventions (MEDIUM)

- [naming-page-files](rules/naming-page-files.md) - ページファイル（page.tsx 等）
- [naming-components](rules/naming-components.md) - コンポーネント（PascalCase）
- [naming-utilities](rules/naming-utilities.md) - ユーティリティファイル
- [naming-api-clients](rules/naming-api-clients.md) - API クライアント（.server.ts, .client.ts）

### 4. Import Rules (MEDIUM)

- [import-aliases](rules/import-aliases.md) - パスエイリアス（@/*）
- [import-order](rules/import-order.md) - インポート順序

### 5. Best Practices (HIGH)

- [practice-component-design](rules/practice-component-design.md) - コンポーネント設計
- [practice-server-actions](rules/practice-server-actions.md) - Server Actions パターン
- [practice-server-client](rules/practice-server-client.md) - Server/Client 分離
- [practice-bff](rules/practice-bff.md) - BFF と Edge Functions 連携

## Core Principles

### コロケーション

コンポーネント・ロジック・API を使う場所の近くに配置：

```
app/[page]/
├── _actions/
├── _apis/
├── _components/
└── page.tsx
```

### Server/Client 分離

- Server Components（デフォルト）でデータフェッチと UI。Client はインタラクティブ部分のみ。Server Actions でフォーム・データ変更。

### ファイル命名

| 用途           | 単一ページ              | 複数ページ        |
|----------------|-------------------------|-------------------|
| Server Actions | `_actions/[resource].ts` | -                 |
| API クライアント| `_apis/[resource].server.ts` | `apis/[resource].server.ts` |
| コンポーネント | `_components/Name/`     | `components/Name/` |

## 詳細

各ルールの説明とコード例は Quick Reference のリンク先（`rules/` 内の .md）を参照。
