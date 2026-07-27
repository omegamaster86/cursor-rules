---
title: Services Directory Structure
impact: MEDIUM
impactDescription: 外部サービス連携の一元管理
tags: services, supabase, external-services, configuration
---

## Services Directory Structure

`services/`ディレクトリは外部サービスの設定とクライアントを配置します。

**推奨構成：**

```
services/
├── logger.ts              # ロギングサービス
└── supabase-service/      # Supabase設定
    ├── client.ts          # クライアントサイド用
    ├── server.ts          # サーバーサイド用
    └── proxy.ts           # プロキシ設定（オプション）
```

**Incorrect（lib/に混在）:**

```
lib/
├── supabase.ts
├── utils.ts
├── format.ts
└── auth.ts
# 外部サービス設定とユーティリティが混在
```

**Correct（services/で分離）:**

```typescript
// services/supabase-service/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// services/supabase-service/server.ts
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()
  
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          // ...cookie設定
        },
      },
    }
  )
}
```

**ポイント：**

1. 外部サービスごとにサブディレクトリを作成
2. クライアントサイド用とサーバーサイド用を分離
3. ヘルパー関数は`utils/`に、サービス設定は`services/`に配置
