---
title: Flutter Lints
impact: MEDIUM
impactDescription: flutter_lints の設定
tags: flutter, linting, code-quality
---

## Flutter Lints

flutter_lints を使用したコード品質の維持です。

**インストール：**

```yaml
dev_dependencies:
  flutter_lints: ^3.0.0
```

**analysis_options.yaml：**

```yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
  errors:
    invalid_annotation_target: ignore

linter:
  rules:
    # 推奨ルール
    prefer_const_constructors: true
    prefer_const_declarations: true
    prefer_final_locals: true
    avoid_print: true
    prefer_single_quotes: true
    sort_constructors_first: true
    sort_unnamed_constructors_first: true
    
    # 無効化するルール（必要に応じて）
    # prefer_relative_imports: false
```

**生成ファイルの除外：**

```yaml
analyzer:
  exclude:
    - "**/*.g.dart"           # json_serializable, riverpod_generator
    - "**/*.freezed.dart"     # freezed
    - "lib/generated/**"      # その他の生成ファイル
```

**よく使うリントルール：**

| ルール | 説明 |
|--------|------|
| `prefer_const_constructors` | const コンストラクタを推奨 |
| `prefer_final_locals` | ローカル変数は final 推奨 |
| `avoid_print` | print() の使用を警告 |
| `prefer_single_quotes` | シングルクォートを推奨 |
| `always_use_package_imports` | package: インポートを強制 |

**IDE での設定：**

VS Code / Cursor で自動フォーマット：

```json
// settings.json
{
  "editor.formatOnSave": true,
  "[dart]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "Dart-Code.dart-code"
  }
}
```

**コマンドライン：**

```bash
# 静的解析を実行
flutter analyze

# フォーマット
dart format .

# フォーマットチェック（CI 用）
dart format --set-exit-if-changed .
```

**チェックリスト：**

- [ ] `flutter_lints` を `dev_dependencies` に追加
- [ ] `analysis_options.yaml` で生成ファイルを除外
- [ ] IDE で保存時自動フォーマットを有効化
- [ ] CI で `flutter analyze` を実行
