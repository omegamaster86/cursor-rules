---
title: Environment Validation Library
impact: HIGH
impactDescription: @t3-oss/env-nextjs による環境変数の型安全な一元検証
tags: env, t3-env, zod, configuration, next.js
---

## Environment Validation Library

環境変数の定義・検証には `@t3-oss/env-nextjs` を使う（Zod は既存依存を利用）。

**インストール：**

```bash
npm install @t3-oss/env-nextjs
```

**役割：**

| パッケージ | 用途 |
|-----------|------|
| `@t3-oss/env-nextjs` | client/server 境界付きの env スキーマ・ビルド時検証 |
| `zod` | 各変数の型・制約（必須 / URL 等） |

詳細な配置・参照規約は `nextjs-coding-standards` の [env-validation](../../nextjs-coding-standards/rules/env-validation.md) を参照。

**チェックリスト：**

- [ ] `@t3-oss/env-nextjs` を導入済み
- [ ] `src/env.ts` と `next.config.ts` の `import "./src/env"` がある
- [ ] アプリコードは `import { env } from "@/env"` のみで参照している
