---
title: BFF (Backend for Frontend) Design
impact: HIGH
impactDescription: セキュリティとアーキテクチャの一貫性
tags: bff, route-handlers, api, edge-functions
---

## BFF (Backend for Frontend) Design

BFF（Route Handlers）は薄いゲートウェイとして機能させ、ビジネスロジックはEdge Functionsに一元化します。

**BFFの責務：**

1. 入力検証
2. セッション連携
3. レート制限
4. キャッシュ制御
5. Edge Functionsの呼び出し

**Incorrect（BFFにビジネスロジック）:**

```typescript
// app/api/todos/route.ts
export async function POST(request: Request) {
  const supabase = await createClient()
  const body = await request.json()
  
  // ❌ ビジネスロジックがBFFに
  const { data: user } = await supabase.auth.getUser()
  const today = new Date()
  const { count } = await supabase
    .from('todos')
    .select('*', { count: 'exact' })
    .eq('user_id', user.id)
    .gte('created_at', today.toISOString())
  
  if (count >= 10) {
    return NextResponse.json({ error: '1日10件まで' }, { status: 400 })
  }
  
  const { data, error } = await supabase
    .from('todos')
    .insert({ ...body, user_id: user.id })
    .select()
    .single()
  
  return NextResponse.json(data)
}
```

**Correct（BFFは薄いゲートウェイ）:**

```typescript
// app/api/todos/route.ts
import { NextResponse } from 'next/server'
import { createClient } from '@/services/supabase-service/server'
import { z } from 'zod'

const CreateTodoSchema = z.object({
  title: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
})

export async function POST(request: Request) {
  try {
    // 1. 入力検証
    const body = await request.json()
    const validatedData = CreateTodoSchema.parse(body)
    
    // 2. セッション確認
    const supabase = await createClient()
    const { data: { session } } = await supabase.auth.getSession()
    
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    // 3. Edge Functionの呼び出し（ビジネスロジックは全てここ）
    const { data, error } = await supabase.functions.invoke('todos-create', {
      body: validatedData
    })
    
    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 })
    }
    
    return NextResponse.json(data)
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({ error: error.errors }, { status: 400 })
    }
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
  }
}
```

**Edge Function側（ビジネスロジック）：**

```typescript
// supabase/functions/todos-create/index.ts
serve(async (req) => {
  const supabase = createClient(/* ... */)
  const body = await req.json()
  
  // ビジネスロジック: 1日の作成制限チェック
  const { data: user } = await supabase.auth.getUser()
  const today = new Date().toISOString().split('T')[0]
  
  const { count } = await supabase
    .from('todos')
    .select('*', { count: 'exact' })
    .eq('user_id', user.id)
    .gte('created_at', today)
  
  if (count >= 10) {
    return new Response(
      JSON.stringify({ error: '1日の作成上限に達しました' }),
      { status: 400 }
    )
  }
  
  // データ作成
  const { data, error } = await supabase
    .from('todos')
    .insert({ ...body, user_id: user.id })
    .select()
    .single()
  
  return new Response(JSON.stringify(data))
})
```

**アーキテクチャ：**

```
Client → BFF (Route Handler) → Edge Function → Database
         ↓                     ↓
         入力検証              ビジネスロジック
         セッション確認         データ操作
```
