---
name: mock-store-guide
description: Defines mock store patterns for Next.js demo apps without a database (HMR, type-safe store, CRUD). Use when building demos, prototypes, or pre-DB UI, or when preparing E2E mock data.
---

# Mock Store Guide

データベースなしでデモアプリを実装するためのモックストアガイド。HMR 対応・型安全・CRUD パターンを定義する。

## When to Apply

- デモアプリを作成する時
- プレゼン用プロトタイプを作る時
- DB 設定前に画面開発を進める時（**principle-foundational-thinking** のフロントトラック）
- E2E テスト用モックデータを準備する時

## Rule Categories by Priority

| Priority | Category          | Impact | Prefix      |
|----------|-------------------|--------|-------------|
| 1        | Store Implementation | HIGH | `store-`    |
| 2        | Server Actions    | HIGH   | `action-`   |
| 3        | API Implementation | MEDIUM | `api-`    |
| 4        | Best Practices    | MEDIUM | `practice-` |

## Quick Reference

### 1. Store Implementation (HIGH)

- [store-basic](rules/store-basic.md) - 基本ストア実装
- [store-crud](rules/store-crud.md) - CRUD 操作
- [store-advanced](rules/store-advanced.md) - 検索・フィルタ・ページネーション

### 2. Server Actions (HIGH)

- [action-create](rules/action-create.md) - 作成処理
- [action-update](rules/action-update.md) - 更新処理
- [action-delete](rules/action-delete.md) - 削除処理

### 3. API Implementation (MEDIUM)

- [api-server](rules/api-server.md) - サーバーサイド API

### 4. Best Practices (MEDIUM)

- [practice-naming](rules/practice-naming.md) - ストアキー命名
- [practice-typing](rules/practice-typing.md) - 型定義の明示
- [practice-revalidate](rules/practice-revalidate.md) - revalidatePath の使用

## Core Principles

### Mock Store の特徴

- HMR 対応でデータがホットリロードで保持。TypeScript で型安全。少ないコードで CRUD を実現。

### ストアの仕組み

```typescript
globalThis.__mockStoreContainer = {
  "demo:todos": { todos: [...], nextId: 4 },
  "demo:users": { users: [...], nextId: 3 },
}
```

### 実装フロー

```
型定義 → ストア → Server Actions → API → UI
```

### 配置

| 種別         | 配置場所                        |
|--------------|---------------------------------|
| 型定義       | `types/demo-types.ts`           |
| ストア       | `services/mock-store/stores/`   |
| Server Actions | `app/demo/{entity}/_actions/` |
| API          | `app/demo/{entity}/_apis/`      |

## ⚠️ 注意

**本番では使用しないこと**

- データ永続性なし（再起動で消失）
- スケーリング不可・メモリリークの可能性・セキュリティ機能なし

## 詳細

各ルールの説明とコード例は Quick Reference のリンク先（`rules/` 内の .md）を参照。
