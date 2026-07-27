---
title: Project Initialization
impact: HIGH
impactDescription: 正しいプロジェクト構成の基盤
tags: setup, create-next-app, typescript, src-dir
---

## Project Initialization

Next.jsプロジェクトを作成する際は、`--src-dir`オプションを必ず有効にしてください。

**Incorrect（src-dirなし）:**

```bash
npx create-next-app@15.5.9 my-app --typescript --tailwind --app
# src/ディレクトリがなく、ファイル管理が煩雑になる
```

**Correct（推奨設定）:**

```bash
npx create-next-app@15.5.9 my-app --src-dir --typescript --tailwind --app --no-eslint
```

**重要なオプション：**

| オプション | 説明 |
|-----------|------|
| `--src-dir` | `src/`ディレクトリを使用する（**必須**） |
| `--typescript` | TypeScriptを使用 |
| `--tailwind` | Tailwind CSSを使用 |
| `--app` | App Routerを使用 |
| `--no-eslint` | ESLintを無効化（Biomeを使用するため） |

`--src-dir`を有効にすることで、アプリケーションコードと設定ファイルが明確に分離され、プロジェクトの見通しが良くなります。
