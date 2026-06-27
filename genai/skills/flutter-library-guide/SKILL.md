---
name: flutter-library-guide
description: Defines recommended packages for Flutter mobile apps (state management, routing, HTTP, testing, dev tools). Use when adding packages, using Riverpod/Dio, implementing local storage, or configuring code generation (build_runner) in Flutter projects.
---

# Flutter Library Guide

Flutter モバイルアプリで推奨するパッケージのガイド。状態管理・ルーティング・HTTP・テスト・開発ツールの選定と使い方を定義する。

## When to Apply

- 新しいパッケージを追加する時
- Riverpod の使い方を確認する時
- HTTP（Dio）を実装する時
- ローカルストレージを実装する時
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
- [pkg-http](rules/pkg-http.md) - Dio
- [pkg-storage](rules/pkg-storage.md) - ローカルストレージ（isar, shared_preferences）

### 2. State Management (HIGH)

- [state-riverpod](rules/state-riverpod.md) - flutter_riverpod
- [state-generator](rules/state-generator.md) - riverpod_generator

### 3. Development Tools (MEDIUM)

- [dev-code-gen](rules/dev-code-gen.md) - build_runner
- [dev-freezed](rules/dev-freezed.md) - Freezed
- [dev-linting](rules/dev-linting.md) - flutter_lints

### 4. Testing (HIGH)

- [test-unit](rules/test-unit.md) - flutter_test
- [test-mock](rules/test-mock.md) - mockito / mocktail

### 5. Utilities (MEDIUM)

- [util-intl](rules/util-intl.md) - intl（国際化）
- [util-image](rules/util-image.md) - cached_network_image

## Core Principles

### 主要パッケージ

| 用途       | パッケージ                          |
|------------|-------------------------------------|
| バックエンド | supabase_flutter                    |
| 状態管理   | flutter_riverpod + riverpod_annotation |
| ルーティング | go_router                           |
| HTTP       | dio                                 |
| ローカル DB | isar                                |

### コード生成

```bash
flutter pub run build_runner build --delete-conflicting-outputs
flutter pub run build_runner watch --delete-conflicting-outputs
```

## 詳細

各ルールの説明とコード例は Quick Reference のリンク先（`rules/` 内の .md）を参照。
