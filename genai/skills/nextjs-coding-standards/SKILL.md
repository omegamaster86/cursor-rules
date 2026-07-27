---
name: nextjs-coding-standards
description: Defines Next.js web app coding standards for TypeScript types, Tailwind CSS, Supabase auth/data, React Hooks, forms, environment variables, and component structure. Use when implementing or reviewing types, styling, Supabase, hooks, forms, env, or naming in Next.js projects.
---

# Next.js Coding Standards

Next.js Web アプリのコーディング規約。型定義・Tailwind・Supabase・Hooks・フォーム・環境変数・コンポーネント・命名のルールを定義する。

## When to Apply

- TypeScript の型定義を作成・確認する時
- Tailwind CSS でスタイリングする時
- Supabase の認証・データアクセスを実装する時
- React Hooks を使用する時
- フォームを実装する時
- 環境変数を追加・参照する時
- コンポーネントを分割する時
- 命名規則を確認する時

## Rule Categories by Priority

| Priority | Category   | Impact  | Prefix       |
|----------|------------|---------|--------------|
| 1        | TypeScript | HIGH    | `ts-`        |
| 2        | Tailwind CSS | MEDIUM | `tailwind-`  |
| 3        | Supabase   | CRITICAL| `supabase-`  |
| 4        | Environment | CRITICAL | `env-`     |
| 5        | React Hooks | HIGH   | `hooks-`     |
| 6        | Forms      | HIGH    | `form-`      |
| 7        | Components | MEDIUM  | `component-` |
| 8        | Naming     | MEDIUM  | `naming-`    |
| 9        | Logging    | HIGH    | `logging-`   |

## Quick Reference

### 1. TypeScript (HIGH)

- [ts-type-vs-interface](rules/ts-type-vs-interface.md) - type と interface の使い分け
- [ts-type-location](rules/ts-type-location.md) - 型定義の配置場所（`types/schemas/` + コロケーション）
- [ts-database-types](rules/ts-database-types.md) - database.types.ts と Zod 境界型

### 2. Tailwind CSS (MEDIUM)

- [tailwind-cn-function](rules/tailwind-cn-function.md) - cn() ユーティリティ
- [tailwind-rem-units](rules/tailwind-rem-units.md) - スペーシング・サイジング系は rem 単位を使用

### 3. Supabase (CRITICAL)

- [supabase-auth](rules/supabase-auth.md) - 認証規約（`getSession` + `getClaims`）
- [supabase-data-access](rules/supabase-data-access.md) - データアクセス（3層 + handler/callEdgeFunction）
- [supabase-server-action](rules/supabase-server-action.md) - Server Action パターン

### 4. Environment (CRITICAL)

- [env-validation](rules/env-validation.md) - `@/env` 一元検証・参照規約

### 5. React Hooks (HIGH)

- [hooks-basic](rules/hooks-basic.md) - useState, useEffect の基本
- [hooks-custom](rules/hooks-custom.md) - カスタムフック
- [hooks-dependencies](rules/hooks-dependencies.md) - 依存配列

### 6. Forms (HIGH)

- [form-action-state](rules/form-action-state.md) - useActionState + handler パターン
- [form-validation](rules/form-validation.md) - Zod バリデーション（`validate()` 優先）

### 7. Components (MEDIUM)

- [component-split](rules/component-split.md) - コンポーネント分割の判断
- [component-server-client](rules/component-server-client.md) - Server/Client 分離

### 8. Naming (MEDIUM)

- [naming-variables](rules/naming-variables.md) - 変数・関数の命名
- [naming-files](rules/naming-files.md) - ファイル・ディレクトリの命名

### 9. Logging (HIGH)

- [logging-frontend](rules/logging-frontend.md) - フロントエンドログ（`handler()` 内包）

## Core Principles

### 型定義

- `type` を優先。API 境界型は `src/types/schemas/*.ts`（Zod）。アクション状態は `_actions/types.ts`。

### Supabase 認証

- Edge Function 呼び出しは `callEdgeFunction`（内部で `getSession` + `getClaims`）。認証 SDK（signIn 等）は Server Action から直接呼んでよい。

### 環境変数

- `src/env.ts`（`@t3-oss/env-nextjs`）で一元定義。利用箇所は `import { env } from "@/env"` のみ。`process.env` 直接参照・fallback 禁止。

### データアクセス

```
Page Component → Server Action / _apis → callEdgeFunction → Edge Function → DB
```

本番の Server Action は `handler()` + `validate()` + `callEdgeFunction()` を標準とする。

## 詳細

各ルールの説明とコード例は Quick Reference のリンク先（`rules/` 内の .md）を参照。
