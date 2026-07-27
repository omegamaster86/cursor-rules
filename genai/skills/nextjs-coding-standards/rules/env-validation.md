---
title: Environment Variable Validation
impact: CRITICAL
impactDescription: 環境変数は src/env.ts で一元検証し、利用箇所は env 経由で参照する
tags: env, environment-variables, t3-env, zod, security, next.js
---

## Environment Variable Validation

アプリコードから `process.env.XXX` を直接読まず、`@t3-oss/env-nextjs` + Zod で定義した `env` を参照する。

**配置：**

```
frontend/web/
├── src/env.ts          # スキーマ定義・検証（唯一の定義場所）
├── next.config.ts      # import "./src/env" でビルド時検証
└── .env.example        # ドキュメント用サンプル（必須値はコメントアウトしない）
```

**定義（`src/env.ts`）：**

```typescript
import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    // サーバー専用（クライアントからアクセスするとエラー）
    SUPABASE_SECRET_KEY: z.string().min(1),
  },
  client: {
    // ブラウザ公開。必ず NEXT_PUBLIC_ プレフィックス
    NEXT_PUBLIC_SUPABASE_URL: z.url(),
    NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY: z.string().min(1),
    NEXT_PUBLIC_SITE_URL: z.url(),
  },
  runtimeEnv: {
    // Next.js (Edge/Client) 向けにキーごとに明示 destructure
    SUPABASE_SECRET_KEY: process.env.SUPABASE_SECRET_KEY,
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY:
      process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY,
    NEXT_PUBLIC_SITE_URL: process.env.NEXT_PUBLIC_SITE_URL,
  },
  emptyStringAsUndefined: true,
});
```

| キー | 役割 |
|------|------|
| `server` | サーバー専用変数の Zod スキーマ |
| `client` | `NEXT_PUBLIC_*` の Zod スキーマ |
| `runtimeEnv` | 各キーへの `process.env` 配線（ここ以外で `process.env` を書かない） |

**参照（利用箇所）：**

```typescript
import { env } from "@/env";

// ✅ 良い例
const url = env.NEXT_PUBLIC_SUPABASE_URL;

// ❌ 禁止：直接参照・非 null 断言・fallback
const url1 = process.env.NEXT_PUBLIC_SUPABASE_URL;
const url2 = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const url3 = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "http://localhost:3000";
```

**ビルド時検証：**

```typescript
// next.config.ts
import "./src/env";
```

欠落・不正な値があると `next build` / 起動時に失敗する。利用箇所での `if (!x) throw` は不要。

**例外（`process.env` 直接参照を許可）：**

- `src/env.ts` の `runtimeEnv` 内
- `process.env.NODE_ENV` / `process.env.CI` などフレームワーク・テストランナー固有の値
- Playwright などアプリ外（`test/e2e/`）の設定

**機能フラグで prune するテンプレートの場合：**

機能固有の変数は `// feature:<id>:start` 〜 `// feature:<id>:end` で囲み、機能削除時にスキーマごと除去する。残存する機能の変数は必須とする。

**チェックリスト：**

- [ ] 新規環境変数は `src/env.ts` の `server` / `client` / `runtimeEnv` に追加した
- [ ] アプリコードは `import { env } from "@/env"` 経由でのみ参照している
- [ ] `??` / `||` / `!` による fallback・非 null 断言をしていない
- [ ] 秘匿値は `server` に置き、`NEXT_PUBLIC_` を付けていない
- [ ] `.env.example` を更新した
