---
title: App Router Directory Structure
impact: HIGH
impactDescription: ルーティングとレイアウト管理の基盤
tags: app-router, routing, layout, pages
---

## App Router Directory Structure

`app/`ディレクトリはNext.js App Routerのルーティング構造を定義します。

**概念的な構成：**

```
Next.js App Router
├── Server Components（サーバーサイドレンダリング）
│   ├── データフェッチ（UI表示用。BFF/Edge Functions経由）
│   ├── 初期HTML生成
│   └── SEO最適化
├── Client Components（クライアントサイド）
│   ├── インタラクティブUI
│   ├── 状態管理
│   └── ユーザー入力
├── BFF（Route Handlers）
│   ├── 入力検証・セッション連携・レート制限・キャッシュ制御
│   └── Edge Functionsの呼び出し
└── Server Actions（サーバー関数）
    ├── UI補助のサーバ処理
    └── 軽微なデータ変更のトリガー
```

**ディレクトリ構造例：**

```
app/
├── globals.css           # グローバルスタイル
├── layout.tsx            # ルートレイアウト
├── page.tsx              # トップページ
├── (auth)/               # 認証関連ページグループ
│   ├── login/
│   │   ├── _actions/
│   │   ├── _apis/
│   │   ├── _components/
│   │   └── page.tsx
│   └── register/
├── (dashboard)/          # ダッシュボードグループ
│   ├── layout.tsx        # 共有レイアウト
│   └── page.tsx
└── api/                  # BFF（Route Handlers）
    └── users/
        └── route.ts
```

**重要なポイント：**

1. **デフォルトはServer Components** - 可能な限りServer Componentsを使用
2. **ページグループ化** - `(group)`でレイアウトを共有
3. **BFFは薄いゲートウェイ** - ビジネスロジックはEdge Functionsに一元化
