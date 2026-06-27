---
title: Features Directory Structure
impact: HIGH
impactDescription: features/ ディレクトリの役割と構成
tags: flutter, directory, features, feature-first
---

## Features Directory Structure

`features/` ディレクトリは、Feature-First アプローチに基づいて機能単位でコードを整理します。

**構成：**

```
lib/features/
├── auth/                   # 認証機能
│   ├── data/
│   │   ├── datasources/
│   │   │   ├── auth_local_data_source.dart
│   │   │   └── auth_remote_data_source.dart
│   │   ├── models/
│   │   │   └── user_model.dart
│   │   └── repositories/
│   │       └── auth_repository_impl.dart
│   ├── domain/
│   │   ├── entities/
│   │   │   └── user.dart
│   │   ├── repositories/
│   │   │   └── auth_repository.dart
│   │   └── usecases/
│   │       ├── login.dart
│   │       ├── logout.dart
│   │       └── register.dart
│   └── presentation/
│       ├── providers/      # Riverpodプロバイダー
│       │   ├── auth_provider.dart
│       │   ├── auth_provider.g.dart
│       │   └── auth_notifier.dart
│       ├── screens/        # 画面
│       │   ├── login_screen.dart
│       │   │   └── widgets/  # login画面固有のウィジェット
│       │   │       ├── login_form.dart
│       │   │       └── social_login_buttons.dart
│       │   └── register_screen.dart
│       │       └── widgets/  # register画面固有のウィジェット
│       │           └── register_form.dart
│       └── widgets/        # auth機能全体で共有
│           └── auth_text_field.dart
├── home/                   # ホーム画面
└── profile/                # プロフィール機能
```

**各層の役割（Clean Architecture）：**

| 層 | ディレクトリ | 役割 |
|----|-------------|------|
| データ層 | `data/datasources/` | API通信・ローカルDB |
| データ層 | `data/models/` | JSONシリアライゼーション対応モデル |
| データ層 | `data/repositories/` | リポジトリ実装（domain の interface を実装） |
| ドメイン層 | `domain/entities/` | エンティティ（ビジネスオブジェクト） |
| ドメイン層 | `domain/repositories/` | リポジトリインターフェース |
| ドメイン層 | `domain/usecases/` | ユースケース（ビジネスロジック） |
| プレゼンテーション層 | `presentation/providers/` | Riverpod プロバイダー |
| プレゼンテーション層 | `presentation/screens/` | 画面ウィジェット |
| プレゼンテーション層 | `presentation/widgets/` | 機能内共有ウィジェット |

**Feature-First の利点：**

- 機能ごとに独立して開発・テスト可能
- 新しい機能の追加が容易
- 機能ごとにコードが凝集している

**チェックリスト：**

- [ ] 各機能は `features/[機能名]/` に配置
- [ ] 各機能内で `data/`, `domain/`, `presentation/` の3層に分離
- [ ] 画面固有のウィジェットは `screens/[画面]/widgets/` に配置
- [ ] 機能内共有ウィジェットは `presentation/widgets/` に配置
