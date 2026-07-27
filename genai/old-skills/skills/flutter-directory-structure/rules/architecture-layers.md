---
title: Clean Architecture Layers
impact: HIGH
impactDescription: data/domain/presentation 層の分離と責務
tags: flutter, clean-architecture, layers
---

## Clean Architecture Layers

各機能（Feature）内での3層アーキテクチャ構成です。

**層の構成：**

```
features/auth/
├── data/                    # データ層
│   ├── datasources/        # API通信・ローカルDB
│   │   ├── auth_local_data_source.dart
│   │   └── auth_remote_data_source.dart
│   ├── models/             # JSONシリアライゼーション対応モデル
│   │   └── user_model.dart
│   └── repositories/       # リポジトリ実装
│       └── auth_repository_impl.dart
├── domain/                  # ドメイン層（ビジネスロジック）
│   ├── entities/           # エンティティ
│   │   └── user.dart
│   ├── repositories/       # リポジトリインターフェース
│   │   └── auth_repository.dart
│   └── usecases/           # ユースケース
│       ├── login.dart
│       └── logout.dart
└── presentation/            # プレゼンテーション層（UI）
    ├── providers/          # Riverpodプロバイダー
    ├── screens/            # 画面
    └── widgets/            # ウィジェット
```

**依存関係の方向：**

```
presentation → domain ← data
```

- `presentation` は `domain` に依存
- `data` は `domain` に依存
- `domain` は他の層に依存しない

**依存性逆転の実装例：**

```dart
// domain/repositories/auth_repository.dart（インターフェース）
abstract class AuthRepository {
  Future<Either<Failure, User>> login(String email, String password);
}

// data/repositories/auth_repository_impl.dart（実装）
class AuthRepositoryImpl implements AuthRepository {
  @override
  Future<Either<Failure, User>> login(String email, String password) {
    // 実装
  }
}
```

**チェックリスト：**

- [ ] `domain` 層は他の層に依存しない
- [ ] リポジトリは `domain` でインターフェース、`data` で実装
- [ ] ユースケースは単一責任（1ユースケース1機能）
- [ ] Model と Entity を分離（JSON変換はModelで）
