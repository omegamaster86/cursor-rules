---
title: Unit Testing
impact: HIGH
impactDescription: flutter_test による単体テスト
tags: flutter, testing, unit-test
---

## Unit Testing

flutter_test を使用した単体テストのパターンです。

**ディレクトリ構成：**

```
test/
├── features/
│   └── auth/
│       ├── data/
│       │   └── repositories/
│       │       └── auth_repository_impl_test.dart
│       ├── domain/
│       │   └── usecases/
│       │       └── login_test.dart
│       └── presentation/
│           └── providers/
│               └── auth_provider_test.dart
└── core/
    └── utils/
        └── validators_test.dart
```

**基本的なテスト：**

```dart
// test/core/utils/validators_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:your_app/core/utils/validators.dart';

void main() {
  group('EmailValidator', () {
    test('有効なメールアドレスを検証できる', () {
      expect(Validators.isValidEmail('test@example.com'), isTrue);
    });

    test('無効なメールアドレスを検出できる', () {
      expect(Validators.isValidEmail('invalid-email'), isFalse);
      expect(Validators.isValidEmail(''), isFalse);
      expect(Validators.isValidEmail('test@'), isFalse);
    });
  });
}
```

**非同期テスト：**

```dart
void main() {
  group('AuthRepository', () {
    late AuthRepositoryImpl repository;
    late MockAuthRemoteDataSource mockRemoteDataSource;

    setUp(() {
      mockRemoteDataSource = MockAuthRemoteDataSource();
      repository = AuthRepositoryImpl(
        remoteDataSource: mockRemoteDataSource,
      );
    });

    test('ログイン成功時にユーザーを返す', () async {
      // Arrange
      when(() => mockRemoteDataSource.login(any(), any()))
          .thenAnswer((_) async => testUserModel);

      // Act
      final result = await repository.login('test@example.com', 'password');

      // Assert
      expect(result.isRight(), isTrue);
      result.fold(
        (failure) => fail('Should not return failure'),
        (user) => expect(user.email, 'test@example.com'),
      );
    });
  });
}
```

**Riverpod プロバイダーのテスト：**

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  test('authNotifierProvider のテスト', () async {
    final container = ProviderContainer(
      overrides: [
        authRepositoryProvider.overrideWithValue(MockAuthRepository()),
      ],
    );

    addTearDown(container.dispose);

    final notifier = container.read(authNotifierProvider.notifier);
    await notifier.login('test@example.com', 'password');

    final state = container.read(authNotifierProvider);
    expect(state.value?.email, 'test@example.com');
  });
}
```

**コマンド：**

```bash
# 全テスト実行
flutter test

# 特定のファイルを実行
flutter test test/core/utils/validators_test.dart

# カバレッジ付き
flutter test --coverage
```

**チェックリスト：**

- [ ] テストファイルは `_test.dart` 接尾辞
- [ ] テストディレクトリは `lib/` と同じ構造
- [ ] `group()` と `test()` で構造化
- [ ] AAA パターン（Arrange, Act, Assert）を使用
