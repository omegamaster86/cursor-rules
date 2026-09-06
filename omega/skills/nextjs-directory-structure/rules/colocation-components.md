---
title: Page-Specific Components Colocation
impact: MEDIUM
impactDescription: コンポーネントの責務分離と見通し
tags: components, colocation, page-specific
---

## Page-Specific Components Colocation

ページ固有のコンポーネントは`_components/`ディレクトリに配置します。

**Incorrect（すべて共通コンポーネントに）:**

```
components/
├── ui/
│   └── Button/
├── LoginForm/           # loginページでしか使わない
├── RegisterForm/        # registerページでしか使わない
└── NewTodoForm/         # todos/newでしか使わない
# 共通コンポーネントが肥大化
```

**Correct（ページ近くに配置）:**

```
app/
├── login/
│   ├── _components/
│   │   ├── LoginForm/
│   │   │   ├── index.tsx
│   │   │   └── __tests__/
│   │   │       └── LoginForm.test.tsx
│   │   └── SocialLoginButtons/
│   │       └── index.tsx
│   └── page.tsx
└── todos/
    └── new/
        ├── _components/
        │   └── NewTodoForm/
        │       └── index.tsx
        └── page.tsx
```

**共通化の判断基準：**

| 条件 | 配置場所 |
|------|----------|
| 1つのページでのみ使用 | `app/[page]/_components/` |
| 2つ以上のページで使用 | `components/` |
| 汎用的なUIコンポーネント | `components/ui/` |

**コンポーネント構造：**

```
_components/
└── LoginForm/
    ├── index.tsx              # コンポーネント本体
    └── __tests__/             # テストファイル
        └── LoginForm.test.tsx
```

**ポイント：**

1. `_components`ディレクトリはルーティングに影響しない
2. 最初はページ固有として配置し、再利用が必要になったら`components/`に移動
3. 単一責任の原則を守り、大きなコンポーネントは分割する
