---
name: supabase-implementation
description: Defines backend implementation patterns for Supabase (Database Functions, Edge Functions, auth, RLS). Use when implementing SQL/Edge functions, auth, RLS, type generation, or logging in Web/Mobile projects using Supabase.
---

# Supabase Implementation

Supabase を使ったバックエンド実装ガイド。Database Functions・Edge Functions・認証・RLS の実装方法を定義する。Web/Mobile 共通。

## When to Apply

- Database Functions（SQL 関数）を実装する時
- Edge Functions を実装する時
- 認証・認可を実装する時
- RLS ポリシーを設定する時
- 型定義（database.types.ts）の生成時
- ログ出力を実装する時
- ディレクトリ構成を確認する時

## Rule Categories by Priority

| Priority | Category              | Impact  | Prefix       |
|----------|-----------------------|---------|--------------|
| 1        | Database Functions    | HIGH    | `db-`        |
| 2        | Edge Functions        | HIGH    | `edge-`      |
| 3        | Type Definitions      | HIGH    | `types-`     |
| 4        | Security              | CRITICAL| `security-`  |
| 5        | Logging               | HIGH    | `logging-`   |
| 6        | Directory & Practices | HIGH    | -            |

## Quick Reference

### 1. Database Functions (HIGH)

- [db-syntax](rules/db-syntax.md) - 基本構文・命名規則・レスポンス型

### 2. Edge Functions (HIGH)

- [edge-template](rules/edge-template.md) - ひな形
- [edge-auth](rules/edge-auth.md) - 認証処理
- [edge-deploy](rules/edge-deploy.md) - デプロイ手順

### 3. Type Definitions (HIGH)

- [types-generation](rules/types-generation.md) - database.types.ts の生成
- [types-usage](rules/types-usage.md) - 型定義の使用方法

### 4. Security (CRITICAL)

- [security-rls](rules/security-rls.md) - RLS ポリシー

### 5. Logging (HIGH)

- [logging-required](rules/logging-required.md) - 必須ログ
- [logging-structure](rules/logging-structure.md) - 構造化ログ（logger.ts）

### 6. Directory & Best Practices (HIGH)

- [directory-structure](rules/directory-structure.md) - ディレクトリ構成
- [best-practices](rules/best-practices.md) - ベストプラクティス

## Core Principles

### Database Functions 命名

| プレフィックス | 用途     |
|---------------|----------|
| `sel_`        | SELECT   |
| `ins_`        | INSERT   |
| `upd_`        | UPDATE   |
| `del_`        | DELETE   |
| `upsert_`     | UPSERT   |

### 型定義の生成

```bash
npx --yes supabase gen types typescript --schema public --local > supabase/functions/_shared/database.types.ts
```

### 3層アーキテクチャ

```
Page Component → Server Action → Edge Function → Database Function
```

## 詳細

各ルールの説明とコード例は Quick Reference のリンク先（`rules/` 内の .md）を参照。
