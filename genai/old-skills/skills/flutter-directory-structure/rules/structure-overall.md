---
title: Overall Directory Structure
impact: HIGH
impactDescription: プロジェクト全体の構成と各ディレクトリの役割
tags: flutter, directory, structure
---

## Overall Directory Structure

Flutter プロジェクトの全体ディレクトリ構成です。

**基本構成：**

```
your_flutter_app/
├── lib/                              # Flutter アプリケーションコード
│   ├── core/                         # コア機能（全体で共有）
│   │   ├── constants/               # 定数
│   │   ├── errors/                  # エラーハンドリング
│   │   ├── network/                 # ネットワーク関連
│   │   ├── providers/               # グローバルプロバイダー（Riverpod）
│   │   ├── theme/                   # テーマ設定
│   │   ├── utils/                   # ユーティリティ
│   │   └── widgets/                 # 共通ウィジェット
│   ├── features/                    # 機能別ディレクトリ（Feature-First）
│   │   ├── auth/                   # 認証機能
│   │   ├── home/                   # ホーム画面
│   │   └── profile/                # プロフィール機能
│   ├── config/                     # アプリ設定
│   │   ├── routes/                # ルーティング
│   │   └── env/                   # 環境変数
│   └── main.dart                  # エントリーポイント
│
├── supabase/                        # Supabase関連
│   ├── config.toml
│   ├── migrations/
│   └── functions/
│
├── android/                         # Android プラットフォーム
├── ios/                             # iOS プラットフォーム
└── pubspec.yaml                     # パッケージ設定
```

**各ディレクトリの役割：**

| ディレクトリ | 役割 |
|-------------|------|
| `core/` | アプリ全体で共有される機能・コンポーネント |
| `features/` | 機能単位で分割されたコード |
| `config/` | ルーティング・環境変数などの設定 |
| `supabase/` | バックエンド関連（migrations, functions） |

**チェックリスト：**

- [ ] `lib/` 直下に機能コードを置かない
- [ ] 共通機能は `core/` に配置
- [ ] 機能ごとに `features/` 内にディレクトリを作成
- [ ] ルーティングは `config/routes/` で管理
