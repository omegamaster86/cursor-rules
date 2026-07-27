---
title: Build Runner Code Generation
impact: HIGH
impactDescription: build_runner によるコード生成
tags: flutter, build-runner, code-generation
---

## Build Runner Code Generation

build_runner を使用したコード生成のワークフローです。

**インストール：**

```yaml
dev_dependencies:
  build_runner: ^2.4.0
```

**コード生成が必要なパッケージ：**

| パッケージ | 生成ファイル | 用途 |
|-----------|-------------|------|
| `riverpod_generator` | `.g.dart` | プロバイダー生成 |
| `freezed` | `.freezed.dart` | イミュータブルクラス |
| `json_serializable` | `.g.dart` | JSON シリアライゼーション |
| `isar_generator` | `.g.dart` | Isar スキーマ |

**コマンド：**

```bash
# 一度だけ生成（CI/CD 用）
flutter pub run build_runner build --delete-conflicting-outputs

# ウォッチモード（開発中に自動生成）
flutter pub run build_runner watch --delete-conflicting-outputs

# キャッシュをクリアして再生成
flutter pub run build_runner clean
flutter pub run build_runner build --delete-conflicting-outputs
```

**part 宣言の書き方：**

```dart
// Riverpod Generator
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'my_provider.g.dart';

// Freezed + JSON Serializable
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_model.freezed.dart';
part 'user_model.g.dart';

// Isar
import 'package:isar/isar.dart';

part 'product_cache.g.dart';
```

**build.yaml の設定（オプション）：**

```yaml
# build.yaml
targets:
  $default:
    builders:
      json_serializable:
        options:
          explicit_to_json: true
          field_rename: snake
```

**トラブルシューティング：**

```bash
# 生成ファイルが古い場合
flutter pub run build_runner clean
flutter packages get
flutter pub run build_runner build --delete-conflicting-outputs

# 依存関係の問題がある場合
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

**チェックリスト：**

- [ ] `part` 宣言をファイル上部に追加
- [ ] 開発中は `watch` モードを使用
- [ ] 生成ファイルはバージョン管理に含める（推奨）
- [ ] CI/CD では `build` コマンドを使用
