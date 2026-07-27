---
title: Freezed for Immutable Classes
impact: HIGH
impactDescription: Freezed によるイミュータブルクラスの生成
tags: flutter, freezed, immutable, code-generation
---

## Freezed for Immutable Classes

Freezed を使用したイミュータブルクラスの生成パターンです。

**インストール：**

```yaml
dependencies:
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0

dev_dependencies:
  freezed: ^2.4.0
  json_serializable: ^6.7.0
  build_runner: ^2.4.0
```

**基本的なエンティティ（Freezed）：**

```dart
// features/auth/domain/entities/user.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String email,
    required String displayName,
    String? avatarUrl,
    required DateTime createdAt,
  }) = _User;
}
```

**JSON シリアライゼーション対応モデル：**

```dart
// features/auth/data/models/user_model.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_model.freezed.dart';
part 'user_model.g.dart';

@freezed
class UserModel with _$UserModel {
  const factory UserModel({
    required String id,
    required String email,
    @JsonKey(name: 'display_name') required String displayName,
    @JsonKey(name: 'avatar_url') String? avatarUrl,
    @JsonKey(name: 'created_at') required DateTime createdAt,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);
}

// Entity への変換
extension UserModelX on UserModel {
  User toEntity() {
    return User(
      id: id,
      email: email,
      displayName: displayName,
      avatarUrl: avatarUrl,
      createdAt: createdAt,
    );
  }
}
```

**コード生成コマンド：**

```bash
# 一度だけ生成
flutter pub run build_runner build --delete-conflicting-outputs

# ウォッチモード（開発中に自動生成）
flutter pub run build_runner watch --delete-conflicting-outputs
```

**チェックリスト：**

- [ ] `part` 宣言を忘れずに追加
- [ ] Entity は `freezed` のみ、Model は `freezed` + `json_serializable`
- [ ] `@JsonKey` で API のスネークケースをキャメルケースに変換
- [ ] コード生成後に `.freezed.dart` と `.g.dart` を確認
