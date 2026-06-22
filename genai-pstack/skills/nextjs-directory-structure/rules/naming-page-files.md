---
title: Page File Naming Convention
impact: HIGH
impactDescription: App Routerの正しい動作
tags: naming, pages, app-router, convention
---

## Page File Naming Convention

Next.js App Routerの特殊なファイル名規則に従います。

**ページファイル一覧：**

| ファイル名 | 役割 |
|-----------|------|
| `page.tsx` | ページコンポーネント |
| `layout.tsx` | レイアウトコンポーネント |
| `loading.tsx` | ローディングUI |
| `error.tsx` | エラーUI |
| `not-found.tsx` | 404ページ |
| `template.tsx` | テンプレート（状態がリセットされる） |
| `default.tsx` | Parallel Routesのデフォルト |

**ディレクトリ構造例：**

```
app/
├── layout.tsx          # ルートレイアウト（必須）
├── page.tsx            # トップページ
├── loading.tsx         # グローバルローディング
├── error.tsx           # グローバルエラー
├── not-found.tsx       # 404ページ
└── todos/
    ├── layout.tsx      # todosセクションのレイアウト
    ├── page.tsx        # /todos ページ
    ├── loading.tsx     # todosのローディング
    ├── error.tsx       # todosのエラー
    └── [id]/
        ├── page.tsx    # /todos/[id] ページ
        └── edit/
            └── page.tsx # /todos/[id]/edit ページ
```

**Incorrect（カスタムファイル名）:**

```
app/
└── todos/
    ├── TodosPage.tsx     # ❌ 認識されない
    └── todos-layout.tsx  # ❌ 認識されない
```

**Correct（規則に従う）:**

```
app/
└── todos/
    ├── page.tsx          # ✅ /todos ルートとして認識
    └── layout.tsx        # ✅ レイアウトとして認識
```

**Route Groups（ルーティングに影響しない）：**

```
app/
├── (auth)/               # /auth は URL に含まれない
│   ├── login/
│   │   └── page.tsx     # /login
│   └── register/
│       └── page.tsx     # /register
└── (dashboard)/
    ├── layout.tsx       # 共有レイアウト
    └── page.tsx         # /
```
