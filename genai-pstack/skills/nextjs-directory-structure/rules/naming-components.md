---
title: Component Naming Convention
impact: MEDIUM
impactDescription: コードの可読性と一貫性
tags: naming, components, convention, organization
---

## Component Naming Convention

コンポーネントファイルの命名規則です。

**コンポーネントディレクトリ構成：**

```
ComponentName/
├── index.tsx                    # コンポーネント本体
├── ComponentName.stories.tsx    # Storybookファイル
└── __tests__/                   # テストディレクトリ
    └── ComponentName.test.tsx   # テストファイル
```

**Incorrect（一貫性のない命名）:**

```
components/
├── button.tsx              # ❌ 小文字
├── UserCard/
│   └── user-card.tsx      # ❌ ケバブケース
├── login_form.tsx         # ❌ スネークケース
└── myComponent.tsx        # ❌ キャメルケース
```

**Correct（PascalCase統一）:**

```
components/
├── Button/
│   └── index.tsx          # ✅ PascalCase
├── UserCard/
│   └── index.tsx          # ✅ PascalCase
└── LoginForm/
    └── index.tsx          # ✅ PascalCase
```

**命名のベストプラクティス：**

| 種類 | 命名パターン | 例 |
|------|-------------|-----|
| UIコンポーネント | 名詞 | `Button`, `Input`, `Modal` |
| カード系 | `[名詞]Card` | `UserCard`, `TodoCard` |
| リスト系 | `[名詞]List` | `TodoList`, `UserList` |
| フォーム系 | `[名詞]Form` | `LoginForm`, `NewTodoForm` |
| ボタン系 | `[動詞]Button` | `SubmitButton`, `DeleteButton` |
| セクション | `[名詞]Section` | `HeaderSection`, `HeroSection` |

**テストファイル配置：**

```
Button/
├── index.tsx
└── __tests__/              # テストは __tests__/ に集約
    └── Button.test.tsx
```

**Storybookファイル配置：**

```
Button/
├── index.tsx
├── Button.stories.tsx      # Storybookはコンポーネント直下
└── __tests__/
    └── Button.test.tsx
```
