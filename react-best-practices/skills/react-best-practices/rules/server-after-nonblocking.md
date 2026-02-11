---
title: 非ブロッキング処理に after() を使う
impact: MEDIUM
impactDescription: faster response times
tags: server, async, logging, analytics, side-effects
---

## 非ブロッキング処理に after() を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

Next.js の `after()` を使って、レスポンス送信後に実行すべき処理をスケジュールします。これによりログ・分析などの副作用がレスポンスをブロックしなくなります。

**Incorrect（blocks response):**

```tsx
import { logUserAction } from '@/app/utils'

export async function POST(request: Request) {
  // Perform mutation
  await updateDatabase(request)
  
  // Logging blocks the response
  const userAgent = request.headers.get('user-agent') || 'unknown'
  await logUserAction({ userAgent })
  
  return new Response(JSON.stringify({ status: 'success' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  })
}
```

**Correct（non-blocking):**

```tsx
import { after } from 'next/server'
import { headers, cookies } from 'next/headers'
import { logUserAction } from '@/app/utils'

export async function POST(request: Request) {
  // Perform mutation
  await updateDatabase(request)
  
  // Log after response is sent
  after(async () => {
    const userAgent = (await headers()).get('user-agent') || 'unknown'
    const sessionCookie = (await cookies()).get('session-id')?.value || 'anonymous'
    
    logUserAction({ sessionCookie, userAgent })
  })
  
  return new Response(JSON.stringify({ status: 'success' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  })
}
```

レスポンスは即時返却され、ログ処理はバックグラウンドで実行されます。

**よくあるユースケース：**

- 分析トラッキング
- 監査ログ
- 通知送信
- キャッシュ無効化
- クリーンアップ処理

**重要な注意点：**

- `after()` はレスポンス失敗時やリダイレクト時でも実行される
- Server Actions / Route Handlers / Server Components で利用可能

参考: [https://nextjs.org/docs/app/api-reference/functions/after](https://nextjs.org/docs/app/api-reference/functions/after)
