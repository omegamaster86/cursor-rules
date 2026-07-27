---
title: Response Validation
impact: HIGH
impactDescription: API レスポンスバリデーション
tags: flutter, validation, api, response
---

## Response Validation

API からのレスポンスを安全に処理するためのバリデーション規約です。

**基本原則：Freezed + json_serializable による型安全なパース**

```
外部API → [JSON] → Model.fromJson() → Entity → Widget
```

**レスポンスモデルの定義：**

```dart
// features/user/data/models/get_user_response.dart
@freezed
class GetUserResponse with _$GetUserResponse {
  const factory GetUserResponse({
    required bool success,
    UserModel? data,
    String? error,
  }) = _GetUserResponse;

  factory GetUserResponse.fromJson(Map<String, dynamic> json) =>
      _$GetUserResponseFromJson(json);
}
```

**DataSource でのバリデーション：**

```dart
Future<UserModel> getUserById(String userId) async {
  final response = await _supabase.functions.invoke(
    'get-user-data',
    queryParameters: {'userId': userId},
  );

  // HTTP ステータスチェック
  if (response.status != 200) {
    throw ServerException(
      'HTTP Error: ${response.status}',
      statusCode: response.status,
    );
  }

  // JSON パースとバリデーション（型安全）
  try {
    final jsonData = response.data as Map<String, dynamic>;
    final apiResponse = GetUserResponse.fromJson(jsonData);

    if (!apiResponse.success) {
      throw ServerException(apiResponse.error ?? 'Unknown error');
    }

    if (apiResponse.data == null) {
      throw ServerException('ユーザーが見つかりません');
    }

    return apiResponse.data!;
  } on FormatException catch (e) {
    throw ServerException('レスポンスの形式が不正です: ${e.message}');
  } on TypeError catch (e) {
    throw ServerException('型変換エラー: ${e.toString()}');
  }
}
```

**例外クラスの定義：**

```dart
// lib/core/errors/exceptions.dart
class ServerException implements Exception {
  final String message;
  final int? statusCode;

  ServerException(this.message, {this.statusCode});

  @override
  String toString() => 'ServerException: $message';
}

class NetworkException implements Exception {
  final String message;

  NetworkException(this.message);
}
```

**Failure クラスの定義：**

```dart
// lib/core/errors/failures.dart
abstract class Failure {
  final String message;

  const Failure(this.message);
}

class ServerFailure extends Failure {
  const ServerFailure(super.message);
}

class NetworkFailure extends Failure {
  const NetworkFailure(super.message);
}

class ValidationFailure extends Failure {
  const ValidationFailure(super.message);
}
```

**リストレスポンスのバリデーション：**

```dart
@freezed
class GetProductsResponse with _$GetProductsResponse {
  const factory GetProductsResponse({
    required bool success,
    GetProductsData? data,
    String? error,
  }) = _GetProductsResponse;

  factory GetProductsResponse.fromJson(Map<String, dynamic> json) =>
      _$GetProductsResponseFromJson(json);
}

@freezed
class GetProductsData with _$GetProductsData {
  const factory GetProductsData({
    required List<ProductModel> products,
    required int total,
    required int page,
    @JsonKey(name: 'per_page') required int perPage,
  }) = _GetProductsData;

  factory GetProductsData.fromJson(Map<String, dynamic> json) =>
      _$GetProductsDataFromJson(json);
}
```

**バリデーションの階層：**

| レイヤー | バリデーション方法 |
|---------|-------------------|
| DataSource | `Model.fromJson()` + try-catch |
| Repository | Exception → `Either<Failure, T>` |
| UseCase | ビジネスルールのバリデーション |
| Provider | AsyncValue でエラー状態を管理 |
| Widget | `.when()` でエラー表示 |

**チェックリスト：**

- [ ] レスポンスモデルを Freezed で定義
- [ ] HTTP ステータスコードをチェック
- [ ] `success` フラグをチェック
- [ ] `try-catch` で JSON パースエラーをハンドリング
- [ ] 適切な Exception を throw
- [ ] Repository で Either 型に変換
