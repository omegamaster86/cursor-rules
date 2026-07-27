---
title: Overall Directory Structure
impact: HIGH
impactDescription: プロジェクト全体の見通しと保守性
tags: structure, directories, organization
---

## Overall Directory Structure

Next.js App Router プロジェクトの推奨ディレクトリ構成です（モノレポ）。

**推奨構成（dev-starter 準拠）：**

```
project-root/
├── backend/
│   └── supabase/            # Supabase（schemas / migrations / functions）
│       ├── config.toml
│       ├── schemas/         # 宣言的スキーマ（正本）
│       ├── migrations/
│       ├── seed.sql
│       ├── functions/
│       └── test/            # Edge 統合テスト（Deno）
├── frontend/
│   ├── web/                 # Next.js
│   │   ├── src/
│   │   │   ├── app/                   # App Router
│   │   │   │   ├── (auth)/
│   │   │   │   ├── (dashboard)/
│   │   │   │   │   └── todos/
│   │   │   │   │       ├── _actions/
│   │   │   │   │       ├── _apis/
│   │   │   │   │       ├── _components/
│   │   │   │   │       ├── _utils/
│   │   │   │   │       └── page.tsx
│   │   │   │   └── demo/              # mock-store デモ
│   │   │   ├── components/            # 共通 UI（shadcn 等）
│   │   │   │   ├── ui/                # フラット kebab-case.tsx
│   │   │   │   ├── layout/
│   │   │   │   ├── brand/
│   │   │   │   └── input/
│   │   │   ├── services/              # handler, logger, supabase, stripe...
│   │   │   ├── utils/
│   │   │   ├── types/
│   │   │   │   ├── database.types.ts
│   │   │   │   └── schemas/           # Zod 境界型
│   │   │   ├── constants/
│   │   │   ├── env.ts
│   │   │   └── middleware.ts
│   │   └── test/
│   │       └── e2e/                   # Playwright
│   └── mobile/                        # Flutter
```

**ポイント：**

1. Web は `frontend/web/`（`web/` 直下ではない）
2. E2E は `frontend/web/test/e2e/`
3. `src/apis/` / `src/hooks/` は **任意**（現状 starter はコロケーション中心で未使用）
4. `app/` 内の `_` プレフィックスはルーティングに影響しない
5. 読み取りは `_apis/`、書き込みは `_actions/`
