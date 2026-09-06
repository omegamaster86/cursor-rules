---
title: Linting with Biome
impact: HIGH
impactDescription: 高速なリント・フォーマットによるコード品質の維持
tags: biome, linting, formatting, code-quality
---

## Linting with Biome

Biome を使用したリントとフォーマットのベストプラクティスです。

**インストール：**

```bash
npm install --save-dev @biomejs/biome
npx @biomejs/biome init
```

**基本設定（biome.json）：**

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": {
        "noExcessiveCognitiveComplexity": "warn"
      },
      "style": {
        "useImportType": "error",
        "noNonNullAssertion": "warn"
      },
      "suspicious": {
        "noExplicitAny": "warn"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "asNeeded",
      "trailingCommas": "es5"
    }
  }
}
```

**package.json スクリプト：**

```json
{
  "scripts": {
    "lint": "biome lint .",
    "lint:fix": "biome lint --write .",
    "format": "biome format --write .",
    "check": "biome check .",
    "check:fix": "biome check --write ."
  }
}
```

**VS Code 設定（.vscode/settings.json）：**

```json
{
  "editor.defaultFormatter": "biomejs.biome",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports.biome": "explicit",
    "quickfix.biome": "explicit"
  }
}
```

**CI での使用（GitHub Actions）：**

```yaml
# .github/workflows/lint.yml
name: Lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run check
```

**よく使うコマンド：**

```bash
# リントのみ実行
npx biome lint .

# フォーマットのみ実行
npx biome format .

# リント + フォーマット + インポート整理（自動修正）
npx biome check --write .

# 特定のファイルのみチェック
npx biome check src/components/Button.tsx

# CI用（修正なし、エラー時に終了コード1）
npx biome ci .
```

**チェックリスト：**

- [ ] `biome.json` をプロジェクトルートに配置
- [ ] VS Code 拡張機能をインストール
- [ ] 保存時の自動フォーマットを有効化
- [ ] CI でリントチェックを実行
- [ ] pre-commit フックで `biome check` を実行
