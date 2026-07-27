---
name: flutter-library-guide
description: Defines recommended packages for Flutter mobile apps (state management, routing, HTTP, testing, dev tools). Use when adding packages, using Riverpod, implementing routing/Supabase, or configuring code generation (build_runner) in Flutter projects.
---

# Flutter Library Guide

Flutter モバイルアプリで推奨するパッケージのガイド。

## When to Apply

- 新しいパッケージを追加する時
- Riverpod / go_router / Supabase の使い方を確認する時
- コード生成（build_runner）の設定時

## Rule Categories by Priority

| Priority | Category        | Impact | Prefix   |
|----------|-----------------|--------|----------|
| 1        | Core Packages   | HIGH   | `pkg-`   |
| 2        | State Management| HIGH   | `state-` |
| 3        | Development Tools | MEDIUM | `dev-` |
| 4        | Testing         | HIGH   | `test-`  |
| 5        | Utilities       | MEDIUM | `util-`  |

## Quick Reference

### 1. Core Packages (HIGH)

- [pkg-supabase](rules/pkg-supabase.md) - supabase_flutter
- [pkg-routing](rules/pkg-routing.md) - go_router
- [pkg-http](rules/pkg-http.md) - HTTP（既定は Supabase SDK。Dio は任意）
- [pkg-storage](rules/pkg-storage.md) - ローカルストレージ（任意・starter 未採用）

### 2. State Management (HIGH)

- [state-riverpod](rules/state-riverpod.md) - flutter_riverpod
- [state-generator](rules/state-generator.md) - riverpod_generator

### 3. Development Tools (MEDIUM)

- [dev-code-gen](rules/dev-code-gen.md) - build_runner
- [dev-freezed](rules/dev-freezed.md) - Freezed
- [dev-linting](rules/dev-linting.md) - flutter_lints

### 4. Testing (HIGH)

- [test-unit](rules/test-unit.md) - flutter_test
- [test-mock](rules/test-mock.md) - mocktail（任意・未導入）

### 5. Utilities (MEDIUM)

- [util-intl](rules/util-intl.md) - intl
- [util-image](rules/util-image.md) - 画像（任意）

## Core Principles

### 主要パッケージ（dev-starter 参考版）

| 用途 | パッケージ | 参考版 |
|------|------------|--------|
| バックエンド | supabase_flutter | ^2.8.2 |
| 状態管理 | flutter_riverpod / riverpod_annotation / riverpod_generator | ^2.6.x |
| ルーティング | go_router | ^14.6.2 |
| イミュータブル | freezed / freezed_annotation | ^2.5.7 / ^2.4.4 |
| Lint | flutter_lints | ^6.0.0 |
| SDK | Dart | ^3.10.3 |
| プッシュ / Deep Link | firebase_messaging, flutter_local_notifications, app_links | 採用 |
| HTTP | （既定）Supabase functions.invoke。dio は pubspec にあっても lib 未使用可 | 任意 |
| ローカル DB | isar | **未採用** |
| Either | dartz | pubspec のみ・lib 未使用 |

### FVM

`.fvmrc` と `npm run mobile:run` で Flutter 版を固定。

### コード生成

```bash
dart run build_runner build --delete-conflicting-outputs
```

## 詳細

各ルールの説明とコード例は Quick Reference のリンク先（`rules/` 内の .md）を参照。
