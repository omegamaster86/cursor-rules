---
title: JSON Serializable
impact: HIGH
impactDescription: JSON シリアライゼーション対応
tags: dart, json, serializable, freezed
---

## JSON Serializable

API レスポンスの JSON をパースするモデルには **Freezed + json_serializable** を使用します。

**Model の定義：**

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
```

**Entity への変換：**

```dart
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

**共通のレスポンス型：**

```dart
// lib/core/types/api_response.dart
@freezed
class ApiResponse<T> with _$ApiResponse<T> {
  const factory ApiResponse({
    required bool success,
    T? data,
    String? error,
  }) = _ApiResponse<T>;

  factory ApiResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Object? json) fromJsonT,
  ) =>
      _$ApiResponseFromJson(json, fromJsonT);
}
```

**コード生成：**

```bash
# 一度だけ生成
flutter pub run build_runner build --delete-conflicting-outputs

# ウォッチモード（開発中に自動生成）
flutter pub run build_runner watch --delete-conflicting-outputs
```

**@JsonKey の使い方：**

| 用途 | 例 |
|------|-----|
| スネークケース変換 | `@JsonKey(name: 'display_name')` |
| デフォルト値 | `@JsonKey(defaultValue: 0)` |
| null時の変換 | `@JsonKey(fromJson: _parseDate)` |

**チェックリスト：**

- [ ] `part 'xxx.freezed.dart'` と `part 'xxx.g.dart'` を追加
- [ ] `fromJson` ファクトリメソッドを追加
- [ ] API のスネークケースは `@JsonKey` で変換
- [ ] Entity への変換メソッド（`toEntity()`）を追加
- [ ] コード生成を実行
