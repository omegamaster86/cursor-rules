---
name: flutter-coding-standards
description: Defines Flutter mobile app coding standards for Dart types, Freezed, theme/UI, Supabase auth and data access, Riverpod, and naming. Use when implementing or reviewing Dart types, Freezed classes, UI styling, Supabase integration, Riverpod providers, or naming conventions in Flutter projects.
---

# Flutter Coding Standards

Flutter モバイルアプリのコーディング規約。型定義・UI・Supabase・Riverpod・命名のルールを定義する。

## When to Apply

- Dart の型定義を作成・確認する時
- Freezed でイミュータブルクラスを作る時
- テーマ・スタイル・共通ウィジェットを定義する時
- Supabase の認証・データアクセスを実装する時
- Riverpod プロバイダーを実装する時
- 命名規則を確認する時

## Rule Categories by Priority

| Priority | Category   | Impact  | Prefix        |
|----------|------------|---------|---------------|
| 1        | Dart Types | HIGH    | `dart-`       |
| 2        | UI/Styling | MEDIUM  | `ui-`         |
| 3        | Supabase   | CRITICAL| `supabase-`   |
| 4        | Riverpod   | HIGH    | `riverpod-`   |
| 5        | Naming     | MEDIUM  | `naming-`     |
| 6        | Validation | HIGH    | `validation-` |

## Quick Reference

### 1. Dart Types (HIGH)

- [dart-type-declaration](rules/dart-type-declaration.md) - 明示的な型宣言
- [dart-freezed](rules/dart-freezed.md) - Freezed によるイミュータブルクラス
- [dart-json-serializable](rules/dart-json-serializable.md) - JSON シリアライゼーション

### 2. UI/Styling (MEDIUM)

- [ui-theme](rules/ui-theme.md) - テーマ設定
- [ui-widgets](rules/ui-widgets.md) - 共通ウィジェット
- [ui-spacing](rules/ui-spacing.md) - 間隔の定義

### 3. Supabase (CRITICAL)

- [supabase-auth](rules/supabase-auth.md) - 認証状態の管理
- [supabase-data-access](rules/supabase-data-access.md) - データアクセス階層
- [supabase-edge-function](rules/supabase-edge-function.md) - Edge Function 呼び出し

### 4. Riverpod (HIGH)

- [riverpod-providers](rules/riverpod-providers.md) - プロバイダーの種類と用途
- [riverpod-generator](rules/riverpod-generator.md) - riverpod_generator の使用
- [riverpod-best-practices](rules/riverpod-best-practices.md) - ベストプラクティス

### 5. Naming (MEDIUM)

- [naming-variables](rules/naming-variables.md) - 変数・関数の命名
- [naming-classes](rules/naming-classes.md) - クラスの命名
- [naming-files](rules/naming-files.md) - ファイルの命名

### 6. Validation (HIGH)

- [validation-response](rules/validation-response.md) - API レスポンスのバリデーション

## Core Principles

### 型定義

- 明示的な型宣言。Freezed でイミュータブル。`dynamic` は極力避ける。
- モデルは `data/models/` の Freezed（Entity 分離はオプション）

### レイヤー構成（標準）

```
Widget → Controller/Provider → Repository → Supabase Edge Function
```

Either / dartz / UseCase は必須ではない。エラーは `AppException` 等を throw。

### Riverpod

- `ref.watch`: build 内 / `ref.read`: イベントハンドラ内
- 画面状態は `*Controller`（AsyncNotifier）

## 詳細

各ルールの説明とコード例は Quick Reference のリンク先（`rules/` 内の .md）を参照。
