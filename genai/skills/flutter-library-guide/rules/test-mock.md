---
title: Mocking with Mocktail
impact: HIGH
impactDescription: mocktail によるモック
tags: flutter, testing, mock, mocktail
---

## Mocking with Mocktail

mocktail を使用したモックオブジェクト生成のパターンです。

**インストール：**

```yaml
dev_dependencies:
  mocktail: ^1.0.0
```

**モッククラスの作成：**

```dart
// test/mocks.dart
import 'package:mocktail/mocktail.dart';
import 'package:your_app/features/auth/domain/repositories/auth_repository.dart';
import 'package:your_app/features/auth/data/datasources/auth_remote_data_source.dart';

class MockAuthRepository extends Mock implements AuthRepository {}

class MockAuthRemoteDataSource extends Mock implements AuthRemoteDataSource {}

// Fake クラス（引数のマッチングに必要）
class FakeUser extends Fake implements User {}
```

**setUpAll での登録：**

```dart
void main() {
  setUpAll(() {
    // Fake クラスを登録（any() でマッチングするため）
    registerFallbackValue(FakeUser());
  });

  // テスト...
}
```

**基本的なモック：**

```dart
void main() {
  late MockAuthRepository mockRepository;

  setUp(() {
    mockRepository = MockAuthRepository();
  });

  test('ログイン成功', () async {
    // Arrange: モックの振る舞いを定義
    when(() => mockRepository.login(any(), any()))
        .thenAnswer((_) async => Right(testUser));

    // Act
    final result = await mockRepository.login('test@example.com', 'password');

    // Assert
    expect(result.isRight(), isTrue);
    
    // 呼び出しを検証
    verify(() => mockRepository.login('test@example.com', 'password')).called(1);
  });

  test('ログイン失敗', () async {
    // Arrange: 例外をスロー
    when(() => mockRepository.login(any(), any()))
        .thenAnswer((_) async => Left(ServerFailure()));

    // Act
    final result = await mockRepository.login('test@example.com', 'wrong');

    // Assert
    expect(result.isLeft(), isTrue);
  });
}
```

**Stream のモック：**

```dart
test('認証状態の変更を監視', () async {
  when(() => mockSupabase.auth.onAuthStateChange)
      .thenAnswer((_) => Stream.fromIterable([
        AuthState(AuthChangeEvent.signedIn, testSession),
      ]));

  final stream = mockSupabase.auth.onAuthStateChange;
  
  await expectLater(
    stream,
    emits(predicate<AuthState>((state) => state.event == AuthChangeEvent.signedIn)),
  );
});
```

**呼び出し検証：**

```dart
// 呼び出し回数を検証
verify(() => mockRepository.login(any(), any())).called(1);

// 呼び出されていないことを検証
verifyNever(() => mockRepository.logout());

// 特定の引数で呼び出されたことを検証
verify(() => mockRepository.login('test@example.com', 'password'));
```

**チェックリスト：**

- [ ] モッククラスは `Mock` を継承して `implements`
- [ ] Fake クラスは `registerFallbackValue()` で登録
- [ ] `when()` でモックの振る舞いを定義
- [ ] `verify()` で呼び出しを検証
