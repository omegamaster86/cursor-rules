---
title: Dio HTTP Client
impact: HIGH
impactDescription: Dio による HTTP 通信
tags: flutter, http, dio, api
---

## Dio HTTP Client

Dio を使用した HTTP 通信のパターンです。

**インストール：**

```yaml
dependencies:
  dio: ^5.4.0
```

**Riverpod プロバイダー：**

```dart
// core/providers/dio_provider.dart
import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'dio_provider.g.dart';

@Riverpod(keepAlive: true)
Dio dio(DioRef ref) {
  final dio = Dio(
    BaseOptions(
      baseUrl: const String.fromEnvironment('API_BASE_URL'),
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
      },
    ),
  );

  // インターセプターを追加
  dio.interceptors.addAll([
    LogInterceptor(requestBody: true, responseBody: true),
    _AuthInterceptor(ref),
  ]);

  return dio;
}

class _AuthInterceptor extends Interceptor {
  final DioRef ref;
  
  _AuthInterceptor(this.ref);
  
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    // 認証トークンを追加
    final token = ref.read(authTokenProvider);
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }
}
```

**データソースでの使用：**

```dart
// features/product/data/datasources/product_remote_data_source.dart
class ProductRemoteDataSource {
  final Dio _dio;

  ProductRemoteDataSource(this._dio);

  Future<List<ProductModel>> getProducts() async {
    try {
      final response = await _dio.get('/products');
      return (response.data as List)
          .map((json) => ProductModel.fromJson(json))
          .toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<ProductModel> createProduct(ProductModel product) async {
    try {
      final response = await _dio.post(
        '/products',
        data: product.toJson(),
      );
      return ProductModel.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Exception _handleError(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.receiveTimeout:
        return NetworkException('接続タイムアウト');
      case DioExceptionType.badResponse:
        return ServerException(e.response?.statusCode ?? 500);
      default:
        return NetworkException('ネットワークエラー');
    }
  }
}
```

**チェックリスト：**

- [ ] `Dio` は Riverpod プロバイダーで管理
- [ ] `BaseOptions` でタイムアウトとヘッダーを設定
- [ ] インターセプターで認証トークンを自動付与
- [ ] `DioException` をキャッチしてカスタム例外に変換
