---
title: Unit Testing with Vitest
impact: HIGH
impactDescription: 高速な単体テストによるコード品質の保証
tags: vitest, unit-test, testing
---

## Unit Testing with Vitest

Vitest を使用した単体テストのガイドです。

**ステータス（dev-starter）:** `frontend/web` の `package.json` には **Vitest は未導入**。E2E（Playwright）が主。単体テストが必要になったときのオプションとして扱う。

**導入する場合:**

```bash
npm install --save-dev vitest @vitejs/plugin-react
```

モック例のパスは `@/services/supabase/server`（旧 `supabase-service` ではない）。

**チェックリスト（導入時）:**

- [ ] 設定・スクリプトを web パッケージに追加
- [ ] Supabase モックパスを現行に合わせる
