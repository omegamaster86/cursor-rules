---
title: Type Generation
impact: HIGH
impactDescription: database.types.ts の生成方法
tags: supabase, typescript, types
---

## Type Generation

**第一手段（モノレポルート）：**

```bash
npm run sb:types:gen
```

Web（`frontend/web/src/types/database.types.ts`）と Edge（`backend/supabase/functions/_shared/database.types.ts`）を同期する。

**手動相当（参考）：**

```bash
cd backend
supabase gen types typescript --schema public --local > ...
```

**実行タイミング：**

| タイミング | 必須 |
|-----------|------|
| `schemas/` 変更 + migration 適用後 | ✅ |
| テーブル / DB Function 変更後 | ✅ |
| RLS のみ | ❌ |

**パス注意：** ルートは `backend/supabase/`（`supabase/` 直下想定の古いパスは使わない）。

**チェックリスト：**

- [ ] `npm run sb:types:gen` を実行した
- [ ] Web / Edge 双方の `database.types.ts` が更新されている
