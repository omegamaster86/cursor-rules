---
name: flutter-directory-structure
description: Defines Flutter mobile app directory structure (Feature-First, Clean Architecture, Riverpod). Use when creating Flutter projects, adding features/widgets, placing Riverpod providers, or checking layer roles and naming.
---

# Flutter Directory Structure

Flutter モバイルアプリのディレクトリ構成ガイド。Feature-First + Clean Architecture + Riverpod による保守しやすい構造を定義する。

## When to Apply

- Flutter プロジェクトの新規作成時
- 機能・ウィジェットの追加時
- Riverpod プロバイダーの配置を決める時
- Clean Architecture の各層の役割を確認する時
- ファイル・ディレクトリの命名を確認する時

## Rule Categories by Priority

| Priority | Category         | Impact | Prefix           |
|----------|------------------|--------|------------------|
| 1        | Structure Rules  | HIGH   | `structure-`     |
| 2        | Clean Architecture | HIGH | `architecture-`  |
| 3        | Widget Placement | MEDIUM | `widget-`      |
| 4        | Naming Conventions | MEDIUM | `naming-`    |
| 5        | State Management | HIGH   | `state-`         |

## Quick Reference

### 1. Structure Rules (HIGH)

- [structure-overall](rules/structure-overall.md) - 全体構成
- [structure-core](rules/structure-core.md) - core/ の役割
- [structure-features](rules/structure-features.md) - features/ の役割

### 2. Clean Architecture (HIGH)

- [architecture-layers](rules/architecture-layers.md) - data/domain/presentation の分離
- [architecture-dependencies](rules/architecture-dependencies.md) - 依存の方向

### 3. Widget Placement (MEDIUM)

- [widget-colocation](rules/widget-colocation.md) - ウィジェットのコロケーション
- [widget-shared](rules/widget-shared.md) - 共通ウィジェットの配置

### 4. Naming Conventions (MEDIUM)

- [naming-files](rules/naming-files.md) - ファイル（snake_case）
- [naming-classes](rules/naming-classes.md) - クラス（PascalCase）

### 5. State Management (HIGH)

- [state-riverpod](rules/state-riverpod.md) - Riverpod の配置と使い方

## Core Principles

### Feature-First

機能単位でディレクトリを分割：

```
lib/features/
├── auth/
├── home/
└── profile/
```

### Clean Architecture

各機能内で 3 層に分離：

```
features/auth/
├── data/
├── domain/
└── presentation/
```

### Riverpod

- グローバル: `core/providers/`
- 機能別: `features/[機能]/presentation/providers/`

## 詳細

各ルールの説明とコード例は Quick Reference のリンク先（`rules/` 内の .md）を参照。
