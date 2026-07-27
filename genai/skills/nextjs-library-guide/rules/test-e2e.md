---
title: E2E Testing with Playwright
impact: HIGH
impactDescription: ブラウザ自動化によるエンドツーエンドテスト
tags: playwright, e2e-test, browser-automation
---

## E2E Testing with Playwright

Playwright を使用した E2E テストのベストプラクティスです。

**インストール（参考版）:**

```bash
npm install --save-dev @playwright/test dotenv
# 例: @playwright/test ^1.57.0
npx playwright install
```

**配置:** `frontend/web/test/e2e/`（`tests/e2e` ではない）

**設定の要点（dev-starter 準拠）:**

```typescript
// frontend/web/test/e2e/playwright.config.ts
export default defineConfig({
  testDir: ".",
  testMatch: /.*\.spec\.ts/,
  globalSetup: "./global-setup.ts",
  fullyParallel: false,
  workers: 1, // DB 競合回避
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
  },
});
```

- ローカルは `.env.test` を dotenv で読み込み可
- CI はワークフローの環境変数に依存

**実行:**

```bash
npm run web:test:e2e
# または frontend/web で npm run test:e2e
```

**チェックリスト:**

- [ ] 配置は `frontend/web/test/e2e/`
- [ ] DB を触る E2E は `workers: 1` / 並列オフを検討
- [ ] `globalSetup` でリセット等が必要な場合は明示
