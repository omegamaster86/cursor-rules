---
title: Components Directory Structure
impact: MEDIUM
impactDescription: コンポーネントの再利用性と保守性
tags: components, ui, layouts, organization
---

## Components Directory Structure

`components/`ディレクトリは複数ページで共有するコンポーネントを配置します。

**推奨構成：**

```
components/
├── ui/                  # 基本UIコンポーネント
│   ├── Button/
│   │   ├── index.tsx
│   │   ├── Button.stories.tsx
│   │   └── __tests__/
│   │       └── Button.test.tsx
│   ├── Input/
│   └── Modal/
└── layouts/             # レイアウトコンポーネント
    ├── Header/
    └── Footer/
```

**Incorrect（フラットな構造）:**

```
components/
├── Button.tsx
├── Button.test.tsx
├── Button.stories.tsx
├── Input.tsx
├── Header.tsx
└── ...
# ファイルが増えると管理が困難
```

**Correct（コンポーネントごとにディレクトリ）:**

```
components/
└── ui/
    └── Button/
        ├── index.tsx              # コンポーネント本体
        ├── Button.stories.tsx     # Storybookファイル
        └── __tests__/             # テストは__tests__に集約
            └── Button.test.tsx
```

**配置ルール：**

1. `components/ui/` - 基本的なUIコンポーネント（Button, Input, Modalなど）
2. `components/layouts/` - レイアウトコンポーネント（Header, Footerなど）
3. 各コンポーネントは独立したディレクトリに配置
4. テストファイルは`__tests__/`ディレクトリに集約
5. Storybookファイル（`.stories.tsx`）はコンポーネント直下に配置
