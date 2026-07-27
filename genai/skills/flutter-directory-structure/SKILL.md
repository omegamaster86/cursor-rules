---
name: flutter-directory-structure
description: Defines Flutter mobile app directory structure (simplified Feature-First with Riverpod). Use when creating Flutter projects, adding features/widgets, placing Riverpod providers, or checking layer roles and naming.
---

# Flutter Directory Structure

Flutter モバイルアプリのディレクトリ構成ガイド。**簡略 Feature-First**（domain / UseCase なし）+ Riverpod を第一級とする。

## When to Apply

- Flutter プロジェクトの新規作成時
- 機能・ウィジェットの追加時
- Riverpod プロバイダーの配置を決める時
- レイヤー役割・命名を確認する時

## Rule Categories by Priority

| Priority | Category         | Impact | Prefix           |
|----------|------------------|--------|------------------|
| 1        | Structure Rules  | HIGH   | `structure-`     |
| 2        | Architecture     | HIGH   | `architecture-`  |
| 3        | Widget Placement | MEDIUM | `widget-`      |
| 4        | Naming Conventions | MEDIUM | `naming-`    |
| 5        | State Management | HIGH   | `state-`         |

## Quick Reference

### 1. Structure Rules (HIGH)

- [structure-overall](rules/structure-overall.md) - 全体構成
- [structure-core](rules/structure-core.md) - core/ の役割
- [structure-features](rules/structure-features.md) - features/ の役割

### 2. Architecture (HIGH)

- [architecture-layers](rules/architecture-layers.md) - data / presentation / providers
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

### 簡略 Feature-First（標準）

```
lib/features/auth/
├── data/                 # repository + Freezed models（@riverpod 同居可）
├── providers/            # 機能横断プロバイダー（auth_provider 等）
└── presentation/
    └── login/
        ├── login_screen.dart
        ├── login_controller.dart
        └── widgets/
```

`domain/` / UseCase / DataSource は **必須ではない**（大規模化時のオプション）。

### 依存方向

```
presentation → providers/controllers → data/repository → Supabase Edge
```

### Riverpod 配置

- 機能: `features/[feature]/providers/`
- 画面: `presentation/<flow>/*_controller.dart`
- Repository provider: `data/` 内に同居可
- ルーティング: `config/routes/router.dart`

## 詳細

各ルールの説明とコード例は Quick Reference のリンク先（`rules/` 内の .md）を参照。
