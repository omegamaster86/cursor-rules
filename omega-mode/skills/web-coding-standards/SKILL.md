---
name: web-coding-standards
description: Defines Next.js web app coding standards for TypeScript types, Tailwind CSS, Supabase auth/data, React Hooks, forms, and component structure. Use when implementing or reviewing types, styling, Supabase, hooks, forms, or naming in Next.js projects.
---

# Web Coding Standards

Next.js Web アプリのコーディング規約。型定義・Tailwind・Supabase・Hooks・フォーム・コンポーネント・命名のルールを定義する。

## When to Apply

- 新機能・画面・API を着手する前（`forge-mode/principles/foundational-thinking.md` を参照）
- TypeScript の型定義を作成・確認する時
- Tailwind CSS でスタイリングする時
- Supabase の認証・データアクセスを実装する時
- React Hooks を使用する時
- フォームを実装する時
- コンポーネントを分割する時
- 命名規則を確認する時

## Rule Categories by Priority

| Priority | Category   | Impact  | Prefix       |
|----------|------------|---------|--------------|
| 1        | TypeScript | HIGH    | `ts-`        |
| 2        | Tailwind CSS | MEDIUM | `tailwind-`  |
| 3        | Supabase   | CRITICAL| `supabase-`  |
| 4        | React Hooks | HIGH   | `hooks-`     |
| 5        | Forms      | HIGH    | `form-`      |
| 6        | Components | MEDIUM  | `component-` |
| 7        | Naming     | MEDIUM  | `naming-`    |
| 8        | Logging    | HIGH    | `logging-`   |

## Quick Reference

### 1. TypeScript (HIGH)

- [ts-type-vs-interface](rules/ts-type-vs-interface.md) - type と interface の使い分け
- [ts-type-location](rules/ts-type-location.md) - 型定義の配置場所
- [ts-database-types](rules/ts-database-types.md) - database.types.ts の活用

### 2. Tailwind CSS (MEDIUM)

- [tailwind-cn-function](rules/tailwind-cn-function.md) - cn() ユーティリティ

### 3. Supabase (CRITICAL)

- [supabase-auth](rules/supabase-auth.md) - 認証規約（getUser vs getSession）
- [supabase-data-access](rules/supabase-data-access.md) - データアクセス（3層）
- [supabase-server-action](rules/supabase-server-action.md) - Server Action パターン

### 4. React Hooks (HIGH)

- [hooks-basic](rules/hooks-basic.md) - useState, useEffect の基本
- [hooks-custom](rules/hooks-custom.md) - カスタムフック
- [hooks-dependencies](rules/hooks-dependencies.md) - 依存配列

### 5. Forms (HIGH)

- [form-action-state](rules/form-action-state.md) - useActionState パターン
- [form-validation](rules/form-validation.md) - Zod バリデーション

### 6. Components (MEDIUM)

- [component-split](rules/component-split.md) - コンポーネント分割の判断
- [component-server-client](rules/component-server-client.md) - Server/Client 分離

### 7. Naming (MEDIUM)

- [naming-variables](rules/naming-variables.md) - 変数・関数の命名
- [naming-files](rules/naming-files.md) - ファイル・ディレクトリの命名

### 8. Logging (HIGH)

- [logging-frontend](rules/logging-frontend.md) - フロントエンドログ

## Core Principles

### 型定義

- `type` を優先。`src/types/index.ts` に集約。database.types.ts をベースに再定義。

### Supabase 認証

- サーバーでは `getUser()` を必須。`getSession()` は使用禁止（セキュリティリスク）。

### データアクセス

```
Page Component → Server Action → Edge Function → DB
```

## 詳細

各ルールの説明とコード例は Quick Reference のリンク先（`rules/` 内の .md）を参照。
