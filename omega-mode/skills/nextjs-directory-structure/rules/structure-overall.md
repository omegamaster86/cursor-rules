---
title: Overall Directory Structure
impact: HIGH
impactDescription: プロジェクト全体の見通しと保守性
tags: structure, directories, organization
---

## Overall Directory Structure

Next.js App Routerプロジェクトの推奨ディレクトリ構成です。

**推奨構成：**

```
project-root/
├── backend/
│   └── supabase/            # Supabase関連
│       ├── config.toml
│       ├── migrations/
│       ├── seed.sql
│       └── functions/       # Edge Functions
│           ├── _shared/     # 共通モジュール
│           └── [function]/  # 各Edge Function
├── web/                     # Next.js Webアプリケーション
│   └── src/
│       ├── apis/                  # 共通APIクライアント（複数ページで使用）
│       ├── app/                   # App Router（ページ・レイアウト）
│       │   ├── (group)/          # ページグループ
│       │   │   ├── [page]/
│       │   │   │   ├── _actions/    # ページ固有のServer Actions
│       │   │   │   ├── _apis/       # ページ固有のAPIクライアント
│       │   │   │   ├── _components/ # ページ固有のコンポーネント
│       │   │   │   └── page.tsx
│       │   └── api/              # BFF（Route Handlers）
│       ├── components/           # 共通コンポーネント
│       │   ├── ui/              # 基本UIコンポーネント
│       │   └── layouts/         # レイアウトコンポーネント
│       ├── hooks/               # カスタムフック（共通）
│       ├── services/            # 外部サービス設定
│       ├── utils/               # ヘルパー関数（共通）
│       └── types/               # 型定義
├── mobile/                  # モバイルアプリケーション（将来拡張用）
└── tests/                   # テスト
    ├── e2e/                 # E2Eテスト（Playwright）
    └── functions/           # Edge Functionsテスト（Deno）
```

**ポイント：**

1. `app/`内の`_`プレフィックスディレクトリはルーティングに影響しない
2. `backend/supabase/`にSupabase関連ファイルを配置
3. `web/src/`にNext.jsアプリケーションを配置
4. 共通リソースは`web/src/`直下、ページ固有リソースは`app/[page]/_*`に配置
5. モノレポ構成で`backend/`、`web/`、`mobile/`を分離
