---
name: nextjs-library-guide
description: Defines recommended libraries and packages for Next.js web apps (UI, forms, validation, testing, dev tools). Use when adding UI components, implementing forms/validation, writing tests, setting up tooling, or evaluating libraries for Next.js projects.
---

# Next.js Library Guide

Next.js Web アプリで推奨するライブラリ・パッケージのガイド。UI・フォーム・テスト・開発ツールの選定と使い方を定義する。

## When to Apply

- 新しい UI コンポーネントを追加する時
- フォーム・バリデーションを実装する時
- テストを書く時
- 開発環境のセットアップ時
- ライブラリの導入検討・使用方法の確認時

## Rule Categories by Priority

| Priority | Category        | Impact | Prefix     |
|----------|-----------------|--------|------------|
| 1        | UI Libraries    | HIGH   | `ui-`      |
| 2        | Backend/API     | HIGH   | `backend-` |
| 3        | Development Tools | MEDIUM | `dev-`   |
| 4        | Testing         | HIGH   | `test-`    |
| 5        | Utilities       | MEDIUM | `util-`    |

## Quick Reference

### 1. UI Libraries (HIGH)

- [ui-components](rules/ui-components.md) - shadcn/ui と Radix UI
- [ui-styling](rules/ui-styling.md) - Tailwind CSS のスタイリング
- [ui-tables](rules/ui-tables.md) - TanStack Table（任意・未導入）

### 2. Backend/API (HIGH)

- [backend-supabase](rules/backend-supabase.md) - Supabase SDK

### 3. Development Tools (MEDIUM)

- [dev-linting](rules/dev-linting.md) - Biome によるリント・フォーマット
- [dev-typescript](rules/dev-typescript.md) - TypeScript 設定と型安全性
- [dev-env](rules/dev-env.md) - `@t3-oss/env-nextjs` による環境変数検証

### 4. Testing (HIGH)

- [test-unit](rules/test-unit.md) - Vitest 単体テスト（任意・未導入）
- [test-component](rules/test-component.md) - React Testing Library（任意・未導入）
- [test-e2e](rules/test-e2e.md) - Playwright E2E（標準）

### 5. Utilities (MEDIUM)

- [util-classnames](rules/util-classnames.md) - tailwind-merge と clsx
- [util-dates](rules/util-dates.md) - date-fns による日付処理

## Core Principles

### 依存関係

- 必要なライブラリのみ追加。バンドルサイズを意識し、ツリーシェイキング対応を優先。

### TypeScript ファースト

- 型定義が充実したライブラリを選定。型推論を活かした実装。

### パフォーマンス

- 軽量ライブラリを優先。遅延読み込みの活用。Server/Client コンポーネントの使い分け。

### 一貫性

- shadcn/ui + Radix UI で UI を統一。Biome でコードスタイルを統一。

### 参考スタック版（dev-starter）

- Next `^15.5.12` / React `19.2.1` / Tailwind `^4` / Zod `^4.3.6`
- `@t3-oss/env-nextjs` `^0.13.11` / Playwright `^1.57.0` / Biome schema `2.5.4`

## 詳細

各ルールの説明とコード例は Quick Reference のリンク先（`rules/` 内の .md）を参照。
