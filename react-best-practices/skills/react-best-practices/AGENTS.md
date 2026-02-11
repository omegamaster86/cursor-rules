# React ベストプラクティス

**バージョン 1.0.0**  
Vercel Engineering  
2026年1月

> **注記:**
> このドキュメントは主に、React / Next.js コードベースを保守・生成・
> リファクタリングするエージェントと LLM 向けです。
> 人間の開発者にも有用ですが、AI 支援ワークフローでの
> 自動化と一貫性を重視しています。

---

## 要約

React と Next.js アプリケーション向けの包括的なパフォーマンス最適化ガイド。AI エージェントと LLM の利用を前提に、8カテゴリ・40以上のルールを収録。ウォーターフォール排除やバンドル削減のような高インパクト項目から、高度なパターンまでを影響度順に整理し、自動リファクタリングとコード生成を支援します。

---

## 目次

1. [ウォーターフォール排除](#1-ウォーターフォール排除) — **CRITICAL**
   - 1.1 [API ルートのウォーターフォール連鎖を防ぐ](#11-API ルートのウォーターフォール連鎖を防ぐ)
   - 1.2 [必要になるまで Await を遅延する](#12-必要になるまで Await を遅延する)
   - 1.3 [依存関係ベースで並列化する](#13-依存関係ベースで並列化する)
   - 1.4 [独立処理は Promise.all() で並列実行する](#14-独立処理は Promise.all() で並列実行する)
   - 1.5 [戦略的に Suspense 境界を配置する](#15-戦略的に Suspense 境界を配置する)
2. [バンドルサイズ最適化](#2-バンドルサイズ最適化) — **CRITICAL**
   - 2.1 [バレルファイル経由の Import を避ける](#21-バレルファイル経由の Import を避ける)
   - 2.2 [モジュールを条件付きで読み込む](#22-モジュールを条件付きで読み込む)
   - 2.3 [非クリティカルなサードパーティライブラリを遅延する](#23-非クリティカルなサードパーティライブラリを遅延する)
   - 2.4 [重いコンポーネントは Dynamic Import する](#24-重いコンポーネントは Dynamic Import する)
   - 2.5 [ユーザー意図に基づいて Preload する](#25-ユーザー意図に基づいて Preload する)
3. [サーバーサイド性能](#3-サーバーサイド性能) — **HIGH**
   - 3.1 [非ブロッキング処理に after() を使う](#31-非ブロッキング処理に after() を使う)
   - 3.2 [Server Actions も API ルート同様に認証する](#32-Server Actions も API ルート同様に認証する)
   - 3.3 [リクエスト間は LRU キャッシュを使う](#33-リクエスト間は LRU キャッシュを使う)
   - 3.4 [React.cache() でリクエスト内重複を排除する](#34-React.cache() でリクエスト内重複を排除する)
   - 3.5 [RSC Props の重複シリアライズを避ける](#35-RSC Props の重複シリアライズを避ける)
   - 3.6 [コンポーネント合成でデータ取得を並列化する](#36-コンポーネント合成でデータ取得を並列化する)
   - 3.7 [RSC 境界のシリアライズを最小化する](#37-RSC 境界のシリアライズを最小化する)
4. [クライアント側データ取得](#4-クライアント側データ取得) — **MEDIUM-HIGH**
   - 4.1 [グローバルイベントリスナーを重複させない](#41-グローバルイベントリスナーを重複させない)
   - 4.2 [localStorage のデータをバージョン管理し最小化する](#42-localStorage のデータをバージョン管理し最小化する)
   - 4.3 [スクロール性能のため Passive Event Listener を使う](#43-スクロール性能のため Passive Event Listener を使う)
   - 4.4 [SWR で自動重複排除を行う](#44-SWR で自動重複排除を行う)
5. [再レンダー最適化](#5-再レンダー最適化) — **MEDIUM**
   - 5.1 [State の読み取りを使用時点まで遅らせる](#51-State の読み取りを使用時点まで遅らせる)
   - 5.2 [Effect 依存を狭める](#52-Effect 依存を狭める)
   - 5.3 [導出 State は Render 中に計算する](#53-導出 State は Render 中に計算する)
   - 5.4 [導出 State を購読する](#54-導出 State を購読する)
   - 5.5 [関数型 setState 更新を使う](#55-関数型 setState 更新を使う)
   - 5.6 [State 初期化を遅延する](#56-State 初期化を遅延する)
   - 5.7 [Memo コンポーネントの非プリミティブ既定値を定数に切り出す](#57-Memo コンポーネントの非プリミティブ既定値を定数に切り出す)
   - 5.8 [Memo 化コンポーネントへ分離する](#58-Memo 化コンポーネントへ分離する)
   - 5.9 [操作ロジックをイベントハンドラへ移す](#59-操作ロジックをイベントハンドラへ移す)
   - 5.10 [単純なプリミティブ式を useMemo で包まない](#510-単純なプリミティブ式を useMemo で包まない)
   - 5.11 [非緊急更新には Transition を使う](#511-非緊急更新には Transition を使う)
   - 5.12 [一時値には useRef を使う](#512-一時値には useRef を使う)
6. [描画性能](#6-描画性能) — **MEDIUM**
   - 6.1 [表示切替には Activity コンポーネントを使う](#61-表示切替には Activity コンポーネントを使う)
   - 6.2 [SVG 要素ではなくラッパーをアニメーションする](#62-SVG 要素ではなくラッパーをアニメーションする)
   - 6.3 [条件レンダリングは明示的に書く](#63-条件レンダリングは明示的に書く)
   - 6.4 [長いリストに CSS content-visibility を使う](#64-長いリストに CSS content-visibility を使う)
   - 6.5 [静的 JSX をホイストする](#65-静的 JSX をホイストする)
   - 6.6 [チラつきなしで Hydration 不一致を防ぐ](#66-チラつきなしで Hydration 不一致を防ぐ)
   - 6.7 [想定内の Hydration 不一致警告を抑制する](#67-想定内の Hydration 不一致警告を抑制する)
   - 6.8 [SVG 精度を最適化する](#68-SVG 精度を最適化する)
   - 6.9 [手動ローディング状態より useTransition を使う](#69-手動ローディング状態より useTransition を使う)
7. [JavaScript 性能](#7-JavaScript 性能) — **LOW-MEDIUM**
   - 7.1 [レイアウトスラッシングを避ける](#71-レイアウトスラッシングを避ける)
   - 7.2 [関数呼び出し結果をキャッシュする](#72-関数呼び出し結果をキャッシュする)
   - 7.3 [ループ内のプロパティ参照をキャッシュする](#73-ループ内のプロパティ参照をキャッシュする)
   - 7.4 [Storage API の読み取りをキャッシュする](#74-Storage API の読み取りをキャッシュする)
   - 7.5 [配列反復をまとめる](#75-配列反復をまとめる)
   - 7.6 [関数は早期 Return を使う](#76-関数は早期 Return を使う)
   - 7.7 [RegExp 生成をホイストする](#77-RegExp 生成をホイストする)
   - 7.8 [繰り返し検索にはインデックス Map を作る](#78-繰り返し検索にはインデックス Map を作る)
   - 7.9 [配列比較は先に Length を確認する](#79-配列比較は先に Length を確認する)
   - 7.10 [Min/Max 探索に Sort ではなくループを使う](#710-Min/Max 探索に Sort ではなくループを使う)
   - 7.11 [O(1) 検索に Set/Map を使う](#711-O(1) 検索に Set/Map を使う)
   - 7.12 [不変性のため sort() ではなく toSorted() を使う](#712-不変性のため sort() ではなく toSorted() を使う)
8. [高度なパターン](#8-高度なパターン) — **LOW**
   - 8.1 [イベントハンドラを Ref に保持する](#81-イベントハンドラを Ref に保持する)
   - 8.2 [アプリ初期化はマウントごとではなく一度だけ実行する](#82-アプリ初期化はマウントごとではなく一度だけ実行する)
   - 8.3 [安定したコールバック Ref に useEffectEvent を使う](#83-安定したコールバック Ref に useEffectEvent を使う)

---

## 1. ウォーターフォール排除

**影響: CRITICAL**

ウォーターフォールは最大の性能劣化要因です。逐次 await による待機を排除し、最も大きな改善を狙います。


## API ルートのウォーターフォール連鎖を防ぐ

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

API ルートや Server Actions では、まだ await しない処理でも、独立しているものはすぐ開始してください。

**Incorrect（config waits for auth, data waits for both):**

```typescript
export async function GET(request: Request) {
  const session = await auth()
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return Response.json({ data, config })
}
```

**Correct（auth and config start immediately):**

```typescript
export async function GET(request: Request) {
  const sessionPromise = auth()
  const configPromise = fetchConfig()
  const session = await sessionPromise
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id)
  ])
  return Response.json({ data, config })
}
```

依存関係がより複雑な処理では、`better-all` を使うと並列性を自動で最大化できます（依存関係ベース並列化を参照）。


## 必要になるまで Await を遅延する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

必要な分岐でのみ `await` するように移動し、不要なコードパスをブロックしないようにします。

**Incorrect（blocks both branches):**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  const userData = await fetchUserData(userId)
  
  if (skipProcessing) {
    // Returns immediately but still waited for userData
    return { skipped: true }
  }
  
  // Only this branch uses userData
  return processUserData(userData)
}
```

**Correct（only blocks when needed):**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  if (skipProcessing) {
    // Returns immediately without waiting
    return { skipped: true }
  }
  
  // Fetch only when needed
  const userData = await fetchUserData(userId)
  return processUserData(userData)
}
```

**別の例（早期 return 最適化）:**

```typescript
// Incorrect: always fetches permissions
async function updateResource(resourceId: string, userId: string) {
  const permissions = await fetchPermissions(userId)
  const resource = await getResource(resourceId)
  
  if (!resource) {
    return { error: 'Not found' }
  }
  
  if (!permissions.canEdit) {
    return { error: 'Forbidden' }
  }
  
  return await updateResourceData(resource, permissions)
}

// Correct: fetches only when needed
async function updateResource(resourceId: string, userId: string) {
  const resource = await getResource(resourceId)
  
  if (!resource) {
    return { error: 'Not found' }
  }
  
  const permissions = await fetchPermissions(userId)
  
  if (!permissions.canEdit) {
    return { error: 'Forbidden' }
  }
  
  return await updateResourceData(resource, permissions)
}
```

この最適化は、スキップされる分岐が頻繁に選ばれる場合や、遅延させる処理が高コストな場合に特に有効です。


## 依存関係ベースで並列化する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

部分的な依存関係がある処理では、`better-all` を使って並列性を最大化します。各タスクを可能な最速タイミングで自動開始します。

**Incorrect（profile waits for config unnecessarily):**

```typescript
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig()
])
const profile = await fetchProfile(user.id)
```

**Correct（config and profile run in parallel):**

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  }
})
```

**追加依存なしの代替案:**

先にすべての Promise を作成し、最後に `Promise.all()` でまとめて待つ方法もあります。

```typescript
const userPromise = fetchUser()
const profilePromise = userPromise.then(user => fetchProfile(user.id))

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(),
  profilePromise
])
```

参考: [https://github.com/shuding/better-all](https://github.com/shuding/better-all)


## 独立処理は Promise.all() で並列実行する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

非同期処理に依存関係がない場合は、`Promise.all()` で同時実行します。

**Incorrect（sequential execution, 3 round trips):**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**Correct（parallel execution, 1 round trip):**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```


## 戦略的に Suspense 境界を配置する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

async コンポーネントで JSX を返す前に await するのではなく、Suspense 境界を使ってデータ読み込み中でもラッパー UI を先に表示します。

**Incorrect（wrapper blocked by data fetching):**

```tsx
async function Page() {
  const data = await fetchData() // Blocks entire page
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <DataDisplay data={data} />
      </div>
      <div>Footer</div>
    </div>
  )
}
```

実際にデータが必要なのは中央セクションだけなのに、レイアウト全体が待たされます。

**Correct（wrapper shows immediately, data streams in):**

```tsx
function Page() {
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <Suspense fallback={<Skeleton />}>
          <DataDisplay />
        </Suspense>
      </div>
      <div>Footer</div>
    </div>
  )
}

async function DataDisplay() {
  const data = await fetchData() // Only blocks this component
  return <div>{data.content}</div>
}
```

Sidebar / Header / Footer は即時描画され、データ待ちになるのは DataDisplay のみです。

**代替案（share promise across components):**

```tsx
function Page() {
  // Start fetch immediately, but don't await
  const dataPromise = fetchData()
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay dataPromise={dataPromise} />
        <DataSummary dataPromise={dataPromise} />
      </Suspense>
      <div>Footer</div>
    </div>
  )
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // Unwraps the promise
  return <div>{data.content}</div>
}

function DataSummary({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // Reuses the same promise
  return <div>{data.summary}</div>
}
```

2つのコンポーネントで同じ Promise を共有するため fetch は 1 回で済みます。レイアウトは先に描画され、2 コンポーネントは同時に待機します。

**このパターンを使わない方がよいケース:**

- レイアウト判断に必須の重要データ（配置に影響する）
- ファーストビューの SEO 重要コンテンツ
- Suspense のオーバーヘッドに見合わない小規模・高速クエリ
- レイアウトシフト（loading から content へのジャンプ）を避けたい場合

**トレードオフ:** 初期描画の速さとレイアウトシフトの可能性のバランスです。UX 優先度に応じて選んでください。

---

## 2. バンドルサイズ最適化

**影響: CRITICAL**

初期バンドルを削減し、TTI と LCP を改善します。


## バレルファイル経由の Import を避ける

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

未使用モジュールを大量に読み込まないため、barrel file ではなくソースファイルから直接 import します。**Barrel file** は複数モジュールを再エクスポートするエントリポイントです（例: `index.js` で `export * from './module'` を行う）。

人気のアイコン/コンポーネントライブラリでは、エントリファイルに **最大 10,000 件**の再エクスポートが含まれることがあります。多くの React パッケージでは import だけで **200-800ms** かかり、開発速度と本番コールドスタートの両方に影響します。

**tree-shaking が効きにくい理由:** ライブラリを external（非バンドル）にすると、バンドラは最適化できません。tree-shaking のためにバンドルすると、モジュールグラフ全体の解析でビルドが大きく遅くなります。

**Incorrect（imports entire library):**

```tsx
import { Check, X, Menu } from 'lucide-react'
// Loads 1,583 modules, takes ~2.8s extra in dev
// Runtime cost: 200-800ms on every cold start

import { Button, TextField } from '@mui/material'
// Loads 2,225 modules, takes ~4.2s extra in dev
```

**Correct（imports only what you need):**

```tsx
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'
import Menu from 'lucide-react/dist/esm/icons/menu'
// Loads only 3 modules (~2KB vs ~1MB)

import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
// Loads only what you use
```

**代替案（Next.js 13.5+):**

```js
// next.config.js - use optimizePackageImports
module.exports = {
  experimental: {
    optimizePackageImports: ['lucide-react', '@mui/material']
  }
}

// Then you can keep the ergonomic barrel imports:
import { Check, X, Menu } from 'lucide-react'
// Automatically transformed to direct imports at build time
```

直接 import により、dev 起動 15-70% 高速化、ビルド 28% 高速化、コールドスタート 40% 高速化、HMR も大幅に改善します。

影響を受けやすいライブラリ: `lucide-react`, `@mui/material`, `@mui/icons-material`, `@tabler/icons-react`, `react-icons`, `@headlessui/react`, `@radix-ui/react-*`, `lodash`, `ramda`, `date-fns`, `rxjs`, `react-use`.

参考: [How we optimized package imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)


## モジュールを条件付きで読み込む

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

大きなデータやモジュールは、機能が有効化されたときだけ読み込みます。

**例（アニメーションフレームを遅延読み込み）:**

```tsx
function AnimationPlayer({ enabled, setEnabled }: { enabled: boolean; setEnabled: React.Dispatch<React.SetStateAction<boolean>> }) {
  const [frames, setFrames] = useState<Frame[] | null>(null)

  useEffect(() => {
    if (enabled && !frames && typeof window !== 'undefined') {
      import('./animation-frames.js')
        .then(mod => setFrames(mod.frames))
        .catch(() => setEnabled(false))
    }
  }, [enabled, frames, setEnabled])

  if (!frames) return <Skeleton />
  return <Canvas frames={frames} />
}
```

`typeof window !== 'undefined'` の判定により、このモジュールが SSR 用にバンドルされるのを防ぎ、サーバーバンドルサイズとビルド速度を最適化できます。


## 非クリティカルなサードパーティライブラリを遅延する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

分析・ログ・エラートラッキングはユーザー操作をブロックしないため、hydration 後に読み込みます。

**Incorrect（blocks initial bundle):**

```tsx
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

**Correct（loads after hydration):**

```tsx
import dynamic from 'next/dynamic'

const Analytics = dynamic(
  () => import('@vercel/analytics/react').then(m => m.Analytics),
  { ssr: false }
)

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```


## 重いコンポーネントは Dynamic Import する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

初期描画で不要な大きいコンポーネントは `next/dynamic` で遅延読み込みします。

**Incorrect（Monaco bundles with main chunk ~300KB):**

```tsx
import { MonacoEditor } from './monaco-editor'

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

**Correct（Monaco loads on demand):**

```tsx
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(
  () => import('./monaco-editor').then(m => m.MonacoEditor),
  { ssr: false }
)

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```


## ユーザー意図に基づいて Preload する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

重いバンドルは必要になる前に preload して体感遅延を下げます。

**例（hover/focus で preload）:**

```tsx
function EditorButton({ onClick }: { onClick: () => void }) {
  const preload = () => {
    if (typeof window !== 'undefined') {
      void import('./monaco-editor')
    }
  }

  return (
    <button
      onMouseEnter={preload}
      onFocus={preload}
      onClick={onClick}
    >
      Open Editor
    </button>
  )
}
```

**例（feature flag 有効時に preload）:**

```tsx
function FlagsProvider({ children, flags }: Props) {
  useEffect(() => {
    if (flags.editorEnabled && typeof window !== 'undefined') {
      void import('./monaco-editor').then(mod => mod.init())
    }
  }, [flags.editorEnabled])

  return <FlagsContext.Provider value={flags}>
    {children}
  </FlagsContext.Provider>
}
```

`typeof window !== 'undefined'` の判定により、preload 対象モジュールが SSR 用にバンドルされるのを防ぎ、サーバーバンドルサイズとビルド速度を最適化できます。

---

## 3. サーバーサイド性能

**影響: HIGH**

サーバー側レンダリングとデータ取得を最適化し、応答時間を短縮します。


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


## Server Actions も API ルート同様に認証する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

**影響: CRITICAL（サーバー更新処理への不正アクセスを防ぐ）**

Server Actions（`"use server"` を持つ関数）は API ルートと同様に公開エンドポイントです。各 Server Action **内部**で必ず認証・認可を検証してください。middleware / layout ガード / ページレベル検査だけに依存すると、直接呼び出しを防げません。

Next.js 公式にも、Server Actions は公開 API エンドポイントと同等のセキュリティ前提で扱い、ユーザーがその更新を実行可能か検証すべきだと明記されています。

**Incorrect（no authentication check):**

```typescript
'use server'

export async function deleteUser(userId: string) {
  // Anyone can call this! No auth check
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**Correct（authentication inside the action):**

```typescript
'use server'

import { verifySession } from '@/lib/auth'
import { unauthorized } from '@/lib/errors'

export async function deleteUser(userId: string) {
  // Always check auth inside the action
  const session = await verifySession()
  
  if (!session) {
    throw unauthorized('Must be logged in')
  }
  
  // Check authorization too
  if (session.user.role !== 'admin' && session.user.id !== userId) {
    throw unauthorized('Cannot delete other users')
  }
  
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**入力検証を組み合わせる場合:**

```typescript
'use server'

import { verifySession } from '@/lib/auth'
import { z } from 'zod'

const updateProfileSchema = z.object({
  userId: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email()
})

export async function updateProfile(data: unknown) {
  // Validate input first
  const validated = updateProfileSchema.parse(data)
  
  // Then authenticate
  const session = await verifySession()
  if (!session) {
    throw new Error('Unauthorized')
  }
  
  // Then authorize
  if (session.user.id !== validated.userId) {
    throw new Error('Can only update own profile')
  }
  
  // Finally perform the mutation
  await db.user.update({
    where: { id: validated.userId },
    data: {
      name: validated.name,
      email: validated.email
    }
  })
  
  return { success: true }
}
```

参考: [https://nextjs.org/docs/app/guides/authentication](https://nextjs.org/docs/app/guides/authentication)


## リクエスト間は LRU キャッシュを使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

`React.cache()` は 1 リクエスト内でのみ有効です。連続する複数リクエスト（例: ユーザーが A ボタンの後に B ボタンを押す）で共有したいデータには LRU キャッシュを使います。

**実装例:**

```typescript
import { LRUCache } from 'lru-cache'

const cache = new LRUCache<string, any>({
  max: 1000,
  ttl: 5 * 60 * 1000  // 5 minutes
})

export async function getUser(id: string) {
  const cached = cache.get(id)
  if (cached) return cached

  const user = await db.user.findUnique({ where: { id } })
  cache.set(id, user)
  return user
}

// Request 1: DB query, result cached
// Request 2: cache hit, no DB query
```

ユーザーの連続操作が短時間に同じデータを必要とする複数エンドポイントへ到達する場合に有効です。

**Vercel の [Fluid Compute](https://vercel.com/docs/fluid-compute) 利用時:** 複数の同時リクエストが同じ関数インスタンスとキャッシュを共有できるため、LRU キャッシュは特に効果的です。Redis などの外部ストレージを使わなくても、リクエストをまたいでキャッシュを維持できます。

**従来型 serverless の場合:** 各呼び出しは分離されるため、プロセス間キャッシュには Redis などを検討してください。

参考: [https://github.com/isaacs/node-lru-cache](https://github.com/isaacs/node-lru-cache)


## React.cache() でリクエスト内重複を排除する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

サーバー側のリクエスト内重複排除には `React.cache()` を使います。特に認証処理や DB クエリで効果が高いです。

**使用例：**

```typescript
import { cache } from 'react'

export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({
    where: { id: session.user.id }
  })
})
```

単一リクエスト内では `getCurrentUser()` を複数回呼んでもクエリ実行は 1 回だけです。

**引数にインラインオブジェクトを使わない:**

`React.cache()` は浅い等価比較（`Object.is`）でキャッシュヒットを判定します。インラインオブジェクトは毎回新しい参照になるためヒットしません。

**Incorrect（always cache miss):**

```typescript
const getUser = cache(async (params: { uid: number }) => {
  return await db.user.findUnique({ where: { id: params.uid } })
})

// Each call creates new object, never hits cache
getUser({ uid: 1 })
getUser({ uid: 1 })  // Cache miss, runs query again
```

**Correct（cache hit):**

```typescript
const getUser = cache(async (uid: number) => {
  return await db.user.findUnique({ where: { id: uid } })
})

// Primitive args use value equality
getUser(1)
getUser(1)  // Cache hit, returns cached result
```

オブジェクトを渡す必要がある場合は、同じ参照を渡してください:

```typescript
const params = { uid: 1 }
getUser(params)  // Query runs
getUser(params)  // Cache hit (same reference)
```

**Next.js 固有の注記：**

Next.js では `fetch` API にリクエストメモ化が組み込まれており、同じ URL とオプションのリクエストは単一リクエスト内で自動的に重複排除されます。そのため `fetch` に `React.cache()` は不要です。ただし、次のような他の非同期処理では `React.cache()` が依然重要です:

- データベースクエリ（Prisma, Drizzle など）
- 重い計算処理
- 認証チェック
- ファイルシステム操作
- fetch 以外の非同期処理全般

これらの処理をコンポーネントツリー全体で重複排除するために `React.cache()` を使います。

参考: [React.cache documentation](https://react.dev/reference/react/cache)


## RSC Props の重複シリアライズを避ける

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

**影響: LOW（重複シリアライズ回避によりネットワーク転送量を削減）**

RSC→client のシリアライズは値ではなくオブジェクト参照で重複排除されます。同じ参照は 1 回だけ、新しい参照は再シリアライズされます。変換（`.toSorted()` / `.filter()` / `.map()`）は server ではなく client 側で行ってください。

**Incorrect（duplicates array):**

```tsx
// RSC: sends 6 strings (2 arrays × 3 items)
<ClientList usernames={usernames} usernamesOrdered={usernames.toSorted()} />
```

**Correct（sends 3 strings):**

```tsx
// RSC: send once
<ClientList usernames={usernames} />

// Client: transform there
'use client'
const sorted = useMemo(() => [...usernames].sort(), [usernames])
```

**ネスト時の重複排除挙動:**

重複排除は再帰的に働きます。効果はデータ型で変わります:

- `string[]` / `number[]` / `boolean[]`: **影響 HIGH** - 配列とすべてのプリミティブが完全重複
- `object[]`: **影響 LOW** - 配列は重複するが、ネストオブジェクトは参照で重複排除される

```tsx
// string[] - duplicates everything
usernames={['a','b']} sorted={usernames.toSorted()} // sends 4 strings

// object[] - duplicates array structure only
users={[{id:1},{id:2}]} sorted={users.toSorted()} // sends 2 arrays + 2 unique objects (not 4)
```

**重複排除を壊す操作（新しい参照を作る）:**

- 配列: `.toSorted()` / `.filter()` / `.map()` / `.slice()` / `[...arr]`
- オブジェクト: `{...obj}` / `Object.assign()` / `structuredClone()` / `JSON.parse(JSON.stringify())`

**追加例:**

```tsx
// ❌ Bad
<C users={users} active={users.filter(u => u.active)} />
<C product={product} productName={product.name} />

// ✅ Good
<C users={users} />
<C product={product} />
// Do filtering/destructuring in client
```

**例外:** 変換が高コストな場合や client 側で元データが不要な場合は、導出データを渡して構いません。


## コンポーネント合成でデータ取得を並列化する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

React Server Components はツリー内で逐次実行されます。コンポジションで構造を組み替えてデータ取得を並列化します。

**Incorrect（Sidebar waits for Page's fetch to complete):**

```tsx
export default async function Page() {
  const header = await fetchHeader()
  return (
    <div>
      <div>{header}</div>
      <Sidebar />
    </div>
  )
}

async function Sidebar() {
  const items = await fetchSidebarItems()
  return <nav>{items.map(renderItem)}</nav>
}
```

**Correct（both fetch simultaneously):**

```tsx
async function Header() {
  const data = await fetchHeader()
  return <div>{data}</div>
}

async function Sidebar() {
  const items = await fetchSidebarItems()
  return <nav>{items.map(renderItem)}</nav>
}

export default function Page() {
  return (
    <div>
      <Header />
      <Sidebar />
    </div>
  )
}
```

**children prop を使う代替案:**

```tsx
async function Header() {
  const data = await fetchHeader()
  return <div>{data}</div>
}

async function Sidebar() {
  const items = await fetchSidebarItems()
  return <nav>{items.map(renderItem)}</nav>
}

function Layout({ children }: { children: ReactNode }) {
  return (
    <div>
      <Header />
      {children}
    </div>
  )
}

export default function Page() {
  return (
    <Layout>
      <Sidebar />
    </Layout>
  )
}
```


## RSC 境界のシリアライズを最小化する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

React の Server/Client 境界では、オブジェクトの全プロパティが文字列としてシリアライズされ、HTML レスポンスや後続 RSC リクエストに埋め込まれます。このデータ量はページ重量と読み込み時間へ直結するため、**サイズは非常に重要**です。client が実際に使うフィールドだけを渡してください。

**Incorrect（serializes all 50 fields):**

```tsx
async function Page() {
  const user = await fetchUser()  // 50 fields
  return <Profile user={user} />
}

'use client'
function Profile({ user }: { user: User }) {
  return <div>{user.name}</div>  // uses 1 field
}
```

**Correct（serializes only 1 field):**

```tsx
async function Page() {
  const user = await fetchUser()
  return <Profile name={user.name} />
}

'use client'
function Profile({ name }: { name: string }) {
  return <div>{name}</div>
}
```

---

## 4. クライアント側データ取得

**影響: MEDIUM-HIGH**

重複リクエストを減らし、効率的なデータ取得を実現します。


## グローバルイベントリスナーを重複させない

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

`useSWRSubscription()` を使い、コンポーネントインスタンス間でグローバルイベントリスナーを共有します。

**Incorrect（N instances = N listeners):**

```tsx
function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === key) {
        callback()
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [key, callback])
}
```

`useKeyboardShortcut` フックを複数回使うと、各インスタンスが新しいリスナーを登録してしまいます。

**Correct（N instances = 1 listener):**

```tsx
import useSWRSubscription from 'swr/subscription'

// Module-level Map to track callbacks per key
const keyCallbacks = new Map<string, Set<() => void>>()

function useKeyboardShortcut(key: string, callback: () => void) {
  // Register this callback in the Map
  useEffect(() => {
    if (!keyCallbacks.has(key)) {
      keyCallbacks.set(key, new Set())
    }
    keyCallbacks.get(key)!.add(callback)

    return () => {
      const set = keyCallbacks.get(key)
      if (set) {
        set.delete(callback)
        if (set.size === 0) {
          keyCallbacks.delete(key)
        }
      }
    }
  }, [key, callback])

  useSWRSubscription('global-keydown', () => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && keyCallbacks.has(e.key)) {
        keyCallbacks.get(e.key)!.forEach(cb => cb())
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  })
}

function Profile() {
  // Multiple shortcuts will share the same listener
  useKeyboardShortcut('p', () => { /* ... */ }) 
  useKeyboardShortcut('k', () => { /* ... */ })
  // ...
}
```


## localStorage のデータをバージョン管理し最小化する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

キーにバージョンプレフィックスを付け、必要なフィールドだけ保存します。スキーマ衝突や機微データの誤保存を防げます。

**Incorrect：**

```typescript
// No version, stores everything, no error handling
localStorage.setItem('userConfig', JSON.stringify(fullUserObject))
const data = localStorage.getItem('userConfig')
```

**Correct：**

```typescript
const VERSION = 'v2'

function saveConfig(config: { theme: string; language: string }) {
  try {
    localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify(config))
  } catch {
    // Throws in incognito/private browsing, quota exceeded, or disabled
  }
}

function loadConfig() {
  try {
    const data = localStorage.getItem(`userConfig:${VERSION}`)
    return data ? JSON.parse(data) : null
  } catch {
    return null
  }
}

// Migration from v1 to v2
function migrate() {
  try {
    const v1 = localStorage.getItem('userConfig:v1')
    if (v1) {
      const old = JSON.parse(v1)
      saveConfig({ theme: old.darkMode ? 'dark' : 'light', language: old.lang })
      localStorage.removeItem('userConfig:v1')
    }
  } catch {}
}
```

**サーバーレスポンスからは最小限のフィールドのみ保存:**

```typescript
// User object has 20+ fields, only store what UI needs
function cachePrefs(user: FullUser) {
  try {
    localStorage.setItem('prefs:v1', JSON.stringify({
      theme: user.preferences.theme,
      notifications: user.preferences.notifications
    }))
  } catch {}
}
```

**必ず try-catch で囲む:** `getItem()` / `setItem()` は、シークレット/プライベートブラウズ（Safari/Firefox）、容量超過、無効化時に例外を投げます。

**利点:** バージョニングによるスキーマ進化、保存サイズ削減、トークン/PII/内部フラグの保存防止。


## スクロール性能のため Passive Event Listener を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

touch / wheel イベントリスナーに `{ passive: true }` を付けるとスクロールを即時化できます。通常ブラウザは `preventDefault()` の有無確認のためリスナー完了まで待機するため、遅延が発生します。

**Incorrect：**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  
  document.addEventListener('touchstart', handleTouch)
  document.addEventListener('wheel', handleWheel)
  
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**Correct：**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  
  document.addEventListener('touchstart', handleTouch, { passive: true })
  document.addEventListener('wheel', handleWheel, { passive: true })
  
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**passive を使う場面:** トラッキング/分析、ログ、`preventDefault()` を呼ばないリスナー。

**passive を使わない場面:** カスタムスワイプ、カスタムズーム制御、`preventDefault()` が必要なリスナー。


## SWR で自動重複排除を行う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

SWR はコンポーネントインスタンス間で、リクエスト重複排除・キャッシュ・再検証を提供します。

**Incorrect（no deduplication, each instance fetches):**

```tsx
function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => {
    fetch('/api/users')
      .then(r => r.json())
      .then(setUsers)
  }, [])
}
```

**Correct（multiple instances share one request):**

```tsx
import useSWR from 'swr'

function UserList() {
  const { data: users } = useSWR('/api/users', fetcher)
}
```

**不変データの場合:**

```tsx
import { useImmutableSWR } from '@/lib/swr'

function StaticContent() {
  const { data } = useImmutableSWR('/api/config', fetcher)
}
```

**ミューテーションの場合:**

```tsx
import { useSWRMutation } from 'swr/mutation'

function UpdateButton() {
  const { trigger } = useSWRMutation('/api/user', updateUser)
  return <button onClick={() => trigger()}>Update</button>
}
```

参考: [https://swr.vercel.app](https://swr.vercel.app)

---

## 5. 再レンダー最適化

**影響: MEDIUM**

不要な再レンダーを減らし、UI 応答性を向上させます。


## State の読み取りを使用時点まで遅らせる

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

動的 state（searchParams / localStorage）をコールバック内でしか読まないなら、購読しないでください。

**Incorrect（subscribes to all searchParams changes):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const searchParams = useSearchParams()

  const handleShare = () => {
    const ref = searchParams.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>Share</button>
}
```

**Correct（reads on demand, no subscription):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const params = new URLSearchParams(window.location.search)
    const ref = params.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>Share</button>
}
```


## Effect 依存を狭める

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

Effect の再実行を減らすため、オブジェクトではなくプリミティブを依存に指定します。

**Incorrect（re-runs on any user field change):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**Correct（re-runs only when id changes):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**導出 state は Effect 外で計算:**

```tsx
// Incorrect: runs on width=767, 766, 765...
useEffect(() => {
  if (width < 768) {
    enableMobileMode()
  }
}, [width])

// Correct: runs only on boolean transition
const isMobile = width < 768
useEffect(() => {
  if (isMobile) {
    enableMobileMode()
  }
}, [isMobile])
```


## 導出 State は Render 中に計算する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

現在の props/state から計算できる値は、state に保持したり Effect で更新したりしないでください。render 中に導出することで余分な再レンダーと state ドリフトを防げます。prop 変更への追従だけのために Effect で state 設定するのは避け、導出値または key によるリセットを優先します。

**Incorrect（redundant state and effect):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const [fullName, setFullName] = useState('')

  useEffect(() => {
    setFullName(firstName + ' ' + lastName)
  }, [firstName, lastName])

  return <p>{fullName}</p>
}
```

**Correct（derive during render):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const fullName = firstName + ' ' + lastName

  return <p>{fullName}</p>
}
```

参考: [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)


## 導出 State を購読する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

連続値ではなく導出した boolean state を購読して、再レンダー頻度を下げます。

**Incorrect（re-renders on every pixel change):**

```tsx
function Sidebar() {
  const width = useWindowWidth()  // updates continuously
  const isMobile = width < 768
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

**Correct（re-renders only when boolean changes):**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)')
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```


## 関数型 setState 更新を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

現在の state 値に基づいて更新する場合は、state 変数を直接参照せず関数型の setState を使います。これにより stale closure を防ぎ、不要な依存を減らし、安定したコールバック参照を作れます。

**Incorrect（requires state as dependency):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // Callback must depend on items, recreated on every items change
  const addItems = useCallback((newItems: Item[]) => {
    setItems([...items, ...newItems])
  }, [items])  // ❌ items dependency causes recreations
  
  // Risk of stale closure if dependency is forgotten
  const removeItem = useCallback((id: string) => {
    setItems(items.filter(item => item.id !== id))
  }, [])  // ❌ Missing items dependency - will use stale items!
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

1つ目のコールバックは `items` 変更ごとに再生成され、子コンポーネントの不要再レンダーを招く可能性があります。2つ目のコールバックには stale closure バグがあり、常に初期 `items` を参照してしまいます。

**Correct（stable callbacks, no stale closures):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // Stable callback, never recreated
  const addItems = useCallback((newItems: Item[]) => {
    setItems(curr => [...curr, ...newItems])
  }, [])  // ✅ No dependencies needed
  
  // Always uses latest state, no stale closure risk
  const removeItem = useCallback((id: string) => {
    setItems(curr => curr.filter(item => item.id !== id))
  }, [])  // ✅ Safe and stable
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

**利点:**

1. **安定したコールバック参照** - state 変更時にコールバックを再生成する必要がない
2. **stale closure を防止** - 常に最新 state を基準に動作する
3. **依存を削減** - 依存配列を簡潔にでき、メモリリークのリスクも減らせる
4. **バグ予防** - React における代表的なクロージャバグ要因を排除できる

**関数型更新を使う場面:**

- 現在の state 値に依存するすべての setState
- state が必要な useCallback/useMemo 内
- state を参照する event handler
- state を更新する非同期処理

**直接更新で問題ない場面:**

- 静的値の設定: `setCount(0)`
- props/引数のみからの設定: `setName(newName)`
- 以前の値に依存しない state 更新

**注記:** [React Compiler](https://react.dev/learn/react-compiler) を有効化している場合、一部ケースは自動最適化されますが、正しさの確保と stale closure バグ防止のため、関数型更新は引き続き推奨されます。


## State 初期化を遅延する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

高コストな初期値には `useState` に関数を渡します。関数形式でない場合、値は一度しか使わなくても初期化式が毎レンダーで実行されます。

**Incorrect（runs on every render):**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() runs on EVERY render, even after initialization
  const [searchIndex, setSearchIndex] = useState(buildSearchIndex(items))
  const [query, setQuery] = useState('')
  
  // When query changes, buildSearchIndex runs again unnecessarily
  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse runs on every render
  const [settings, setSettings] = useState(
    JSON.parse(localStorage.getItem('settings') || '{}')
  )
  
  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

**Correct（runs only once):**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() runs ONLY on initial render
  const [searchIndex, setSearchIndex] = useState(() => buildSearchIndex(items))
  const [query, setQuery] = useState('')
  
  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse runs only on initial render
  const [settings, setSettings] = useState(() => {
    const stored = localStorage.getItem('settings')
    return stored ? JSON.parse(stored) : {}
  })
  
  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

localStorage/sessionStorage 由来の初期値計算、データ構造（index/map）構築、DOM 読み取り、重い変換処理では遅延初期化を使います。

単純なプリミティブ（`useState(0)`）、直接参照（`useState(props.value)`）、軽いリテラル（`useState({})`）では関数形式は不要です。


## Memo コンポーネントの非プリミティブ既定値を定数に切り出す

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

memo 化コンポーネントで、配列・関数・オブジェクトなど非プリミティブな任意引数にデフォルト値を直接書くと、その引数を省略した呼び出しで memo 化が破綻します。毎レンダー新しいインスタンスが作られ、`memo()` の厳密等価比較を通らないためです。

この問題を避けるには、デフォルト値を定数へ切り出します。

**Incorrect（`onClick` has different values on every rerender):**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```

**Correct（stable default value):**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```


## Memo 化コンポーネントへ分離する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

高コスト処理を memo 化コンポーネントへ分離し、計算前の早期 return を可能にします。

**Incorrect（computes avatar even when loading):**

```tsx
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user)
    return <Avatar id={id} />
  }, [user])

  if (loading) return <Skeleton />
  return <div>{avatar}</div>
}
```

**Correct（skips computation when loading):**

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user])
  return <Avatar id={id} />
})

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  )
}
```

**注記:** プロジェクトで [React Compiler](https://react.dev/learn/react-compiler) を有効化している場合、`memo()` や `useMemo()` による手動メモ化は不要です。再レンダー最適化はコンパイラが自動で行います。


## 操作ロジックをイベントハンドラへ移す

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

副作用が特定のユーザー操作（submit/click/drag）で発火するなら、その event handler 内で実行します。操作を state + effect で表現すると、無関係な変更で effect が再実行され、処理が重複する可能性があります。

**Incorrect（event modeled as state + effect):**

```tsx
function Form() {
  const [submitted, setSubmitted] = useState(false)
  const theme = useContext(ThemeContext)

  useEffect(() => {
    if (submitted) {
      post('/api/register')
      showToast('Registered', theme)
    }
  }, [submitted, theme])

  return <button onClick={() => setSubmitted(true)}>Submit</button>
}
```

**Correct（do it in the handler):**

```tsx
function Form() {
  const theme = useContext(ThemeContext)

  function handleSubmit() {
    post('/api/register')
    showToast('Registered', theme)
  }

  return <button onClick={handleSubmit}>Submit</button>
}
```

参考: [Should this code move to an event handler?](https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler)


## 単純なプリミティブ式を useMemo で包まない

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

式が単純（論理/算術演算子が少ない）で結果がプリミティブ（boolean/number/string）の場合、`useMemo` で包まないでください。
`useMemo` 呼び出しと依存比較のコストが、式そのものより高くなる場合があります。

**Incorrect：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading
  }, [user.isLoading, notifications.isLoading])

  if (isLoading) return <Skeleton />
  // return some markup
}
```

**Correct：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = user.isLoading || notifications.isLoading

  if (isLoading) return <Skeleton />
  // return some markup
}
```


## 非緊急更新には Transition を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

高頻度かつ非緊急な state 更新は transition として扱い、UI 応答性を維持します。

**Incorrect（blocks UI on every scroll):**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```

**Correct（non-blocking updates):**

```tsx
import { startTransition } from 'react'

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY))
    }
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```


## 一時値には useRef を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

値が頻繁に変わり、更新ごとの再レンダーが不要な場合（マウストラッカー、interval、一時フラグなど）は `useState` ではなく `useRef` に保存します。UI 用の値は state、一時的な DOM 近傍値は ref に分離します。ref 更新では再レンダーは発生しません。

**Incorrect（renders every update):**

```tsx
function Tracker() {
  const [lastX, setLastX] = useState(0)

  useEffect(() => {
    const onMove = (e: MouseEvent) => setLastX(e.clientX)
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: lastX,
        width: 8,
        height: 8,
        background: 'black',
      }}
    />
  )
}
```

**Correct（no re-render for tracking):**

```tsx
function Tracker() {
  const lastXRef = useRef(0)
  const dotRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      lastXRef.current = e.clientX
      const node = dotRef.current
      if (node) {
        node.style.transform = `translateX(${e.clientX}px)`
      }
    }
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      ref={dotRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: 8,
        height: 8,
        background: 'black',
        transform: 'translateX(0px)',
      }}
    />
  )
}
```

---

## 6. 描画性能

**影響: MEDIUM**

ブラウザの描画コストを下げ、表示性能を改善します。


## 表示切替には Activity コンポーネントを使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

表示/非表示を頻繁に切り替える高コストコンポーネントでは、React の `<Activity>` を使って state/DOM を保持します。

**使用例：**

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

高コストな再レンダーと state の消失を防げます。


## SVG 要素ではなくラッパーをアニメーションする

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

多くのブラウザでは SVG 要素上の CSS3 アニメーションがハードウェア加速されません。SVG を `<div>` で包み、ラッパー側をアニメーションさせます。

**Incorrect（animating SVG directly - no hardware acceleration):**

```tsx
function LoadingSpinner() {
  return (
    <svg 
      className="animate-spin"
      width="24" 
      height="24" 
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  )
}
```

**Correct（animating wrapper div - hardware accelerated):**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg 
        width="24" 
        height="24" 
        viewBox="0 0 24 24"
      >
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  )
}
```

これは `transform` / `opacity` / `translate` / `scale` / `rotate` などの CSS 変形・遷移全般に当てはまります。ラッパー div を使うことで GPU 加速が効き、より滑らかなアニメーションになります。


## 条件レンダリングは明示的に書く

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

条件が `0` / `NaN` など描画されうる falsy 値を取り得る場合、条件レンダリングは `&&` ではなく明示的な三項演算子（`? :`）を使います。

**Incorrect（renders "0" when count is 0):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  )
}

// When count = 0, renders: <div>0</div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```

**Correct（renders nothing when count is 0):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  )
}

// When count = 0, renders: <div></div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```


## 長いリストに CSS content-visibility を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

`content-visibility: auto` を適用して、画面外要素の描画を遅延します。

**CSS 例:**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**例:**

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map(msg => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  )
}
```

1000 件のメッセージでは、約 990 件の画面外要素の layout/paint をスキップでき、初期描画が約 10 倍高速化します。


## 静的 JSX をホイストする

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

静的 JSX はコンポーネント外へ切り出し、再生成を避けます。

**Incorrect（recreates element every render):**

```tsx
function LoadingSkeleton() {
  return <div className="animate-pulse h-20 bg-gray-200" />
}

function Container() {
  return (
    <div>
      {loading && <LoadingSkeleton />}
    </div>
  )
}
```

**Correct（reuses same element):**

```tsx
const loadingSkeleton = (
  <div className="animate-pulse h-20 bg-gray-200" />
)

function Container() {
  return (
    <div>
      {loading && loadingSkeleton}
    </div>
  )
}
```

これは大きく静的な SVG ノードで特に有効です。毎レンダー再生成すると高コストになります。

**注記:** プロジェクトで [React Compiler](https://react.dev/learn/react-compiler) を有効化している場合、静的 JSX 要素の hoist と再レンダー最適化は自動で行われるため、手動 hoist は不要です。


## チラつきなしで Hydration 不一致を防ぐ

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

client-side storage（localStorage / cookies）に依存する内容を描画する場合は、React が hydration する前に DOM を更新する同期スクリプトを注入し、SSR 破綻と hydration 後のチラつきを同時に防ぎます。

**Incorrect（breaks SSR):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  // localStorage is not available on server - throws error
  const theme = localStorage.getItem('theme') || 'light'
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

`localStorage` はサーバーでは未定義のため、SSR は失敗します。

**Incorrect（visual flickering):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState('light')
  
  useEffect(() => {
    // Runs after hydration - causes visible flash
    const stored = localStorage.getItem('theme')
    if (stored) {
      setTheme(stored)
    }
  }, [])
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

コンポーネントは先にデフォルト値（`light`）で描画され、hydration 後に更新されるため、誤った内容のフラッシュが発生します。

**Correct（no flicker, no hydration mismatch):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <>
      <div id="theme-wrapper">
        {children}
      </div>
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                var theme = localStorage.getItem('theme') || 'light';
                var el = document.getElementById('theme-wrapper');
                if (el) el.className = theme;
              } catch (e) {}
            })();
          `,
        }}
      />
    </>
  )
}
```

inline script が要素表示前に同期実行されるため、DOM は最初から正しい値を持ちます。チラつきも hydration mismatch も発生しません。

このパターンは、テーマ切替・ユーザー設定・認証状態など、デフォルト値のフラッシュなしに即時表示したい client-only データで特に有効です。


## 想定内の Hydration 不一致警告を抑制する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

SSR フレームワーク（例: Next.js）では、サーバーとクライアントで意図的に値が異なる場合があります（ランダム ID、日付、ロケール/タイムゾーン整形など）。このような**想定内**の不一致には、動的テキストを `suppressHydrationWarning` 付き要素で包み、不要な警告を抑制します。実バグの隠蔽には使わず、過剰利用もしないでください。

**Incorrect（known mismatch warnings):**

```tsx
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>
}
```

**Correct（suppress expected mismatch only):**

```tsx
function Timestamp() {
  return (
    <span suppressHydrationWarning>
      {new Date().toLocaleString()}
    </span>
  )
}
```


## SVG 精度を最適化する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

SVG 座標の精度を下げてファイルサイズを削減します。最適精度は viewBox サイズに依存しますが、一般に精度削減は検討すべきです。

**Incorrect（excessive precision):**

```svg
<path d="M 10.293847 20.847362 L 30.938472 40.192837" />
```

**Correct（1 decimal place):**

```svg
<path d="M 10.3 20.8 L 30.9 40.2" />
```

**SVGO で自動化:**

```bash
npx svgo --precision=1 --multipass icon.svg
```


## 手動ローディング状態より useTransition を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

ローディング state は手動の `useState` ではなく `useTransition` を使います。組み込みの `isPending` を得られ、遷移管理も自動化できます。

**Incorrect（manual loading state):**

```tsx
function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async (value: string) => {
    setIsLoading(true)
    setQuery(value)
    const data = await fetchResults(value)
    setResults(data)
    setIsLoading(false)
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isLoading && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**Correct（useTransition with built-in pending state):**

```tsx
import { useTransition, useState } from 'react'

function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  const handleSearch = (value: string) => {
    setQuery(value) // Update input immediately
    
    startTransition(async () => {
      // Fetch and update results
      const data = await fetchResults(value)
      setResults(data)
    })
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**利点:**

- **pending state の自動管理**: `setIsLoading(true/false)` を手動管理する必要がない
- **エラー耐性**: 遷移中に例外が出ても pending state が適切にリセットされる
- **応答性向上**: 更新中も UI の応答性を保てる
- **割り込み処理**: 新しい遷移で保留中の遷移を自動的に打ち切れる

参考: [useTransition](https://react.dev/reference/react/useTransition)

---

## 7. JavaScript 性能

**影響: LOW-MEDIUM**

ホットパスの最適化を積み上げ、全体性能を改善します。


## レイアウトスラッシングを避ける

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

style 書き込みと layout 読み取りを交互に行わないでください。style 変更の間に `offsetWidth` / `getBoundingClientRect()` / `getComputedStyle()` などを読むと、ブラウザに同期 reflow が強制されます。

**これは問題ありません（ブラウザが style 変更をバッチ化する）:**
```typescript
function updateElementStyles(element: HTMLElement) {
  // Each line invalidates style, but browser batches the recalculation
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
}
```

**Incorrect（interleaved reads and writes force reflows):**
```typescript
function layoutThrashing(element: HTMLElement) {
  element.style.width = '100px'
  const width = element.offsetWidth  // Forces reflow
  element.style.height = '200px'
  const height = element.offsetHeight  // Forces another reflow
}
```

**Correct（batch writes, then read once):**
```typescript
function updateElementStyles(element: HTMLElement) {
  // Batch all writes together
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
  
  // Read after all writes are done (single reflow)
  const { width, height } = element.getBoundingClientRect()
}
```

**Correct（batch reads, then writes):**
```typescript
function avoidThrashing(element: HTMLElement) {
  // Read phase - all layout queries first
  const rect1 = element.getBoundingClientRect()
  const offsetWidth = element.offsetWidth
  const offsetHeight = element.offsetHeight
  
  // Write phase - all style changes after
  element.style.width = '100px'
  element.style.height = '200px'
}
```

**より良い方法: CSS クラスを使う**
```css
.highlighted-box {
  width: 100px;
  height: 200px;
  background-color: blue;
  border: 1px solid black;
}
```
```typescript
function updateElementStyles(element: HTMLElement) {
  element.classList.add('highlighted-box')
  
  const { width, height } = element.getBoundingClientRect()
}
```

**React の例:**
```tsx
// Incorrect: interleaving style changes with layout queries
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  const ref = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (ref.current && isHighlighted) {
      ref.current.style.width = '100px'
      const width = ref.current.offsetWidth // Forces layout
      ref.current.style.height = '200px'
    }
  }, [isHighlighted])
  
  return <div ref={ref}>Content</div>
}

// Correct: toggle class
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  return (
    <div className={isHighlighted ? 'highlighted-box' : ''}>
      Content
    </div>
  )
}
```

可能な限り inline style より CSS クラスを優先してください。CSS ファイルはブラウザにキャッシュされ、関心の分離と保守性の面でも有利です。

レイアウト強制を引き起こす操作の詳細は、[this gist](https://gist.github.com/paulirish/5d52fb081b3570c81e3a) と [CSS Triggers](https://csstriggers.com/) を参照してください。


## 関数呼び出し結果をキャッシュする

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

render 中に同じ入力で同じ関数を繰り返し呼ぶ場合は、モジュールスコープの Map で結果をキャッシュします。

**Incorrect（redundant computation):**

```typescript
function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // slugify() called 100+ times for same project names
        const slug = slugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**Correct（cached results):**

```typescript
// Module-level cache
const slugifyCache = new Map<string, string>()

function cachedSlugify(text: string): string {
  if (slugifyCache.has(text)) {
    return slugifyCache.get(text)!
  }
  const result = slugify(text)
  slugifyCache.set(text, result)
  return result
}

function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // Computed only once per unique project name
        const slug = cachedSlugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**単一値関数向けのよりシンプルなパターン:**

```typescript
let isLoggedInCache: boolean | null = null

function isLoggedIn(): boolean {
  if (isLoggedInCache !== null) {
    return isLoggedInCache
  }
  
  isLoggedInCache = document.cookie.includes('auth=')
  return isLoggedInCache
}

// Clear cache when auth changes
function onAuthChange() {
  isLoggedInCache = null
}
```

Map（hook ではなく）を使うことで、React コンポーネントだけでなく utility や event handler でも使えます。

参考: [How we made the Vercel Dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)


## ループ内のプロパティ参照をキャッシュする

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

ホットパスではオブジェクトのプロパティ参照をキャッシュします。

**Incorrect（3 lookups × N iterations):**

```typescript
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value)
}
```

**Correct（1 lookup total):**

```typescript
const value = obj.config.settings.value
const len = arr.length
for (let i = 0; i < len; i++) {
  process(value)
}
```


## Storage API の読み取りをキャッシュする

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

`localStorage` / `sessionStorage` / `document.cookie` は同期かつ高コストです。読み取り結果をメモリキャッシュします。

**Incorrect（reads storage on every call):**

```typescript
function getTheme() {
  return localStorage.getItem('theme') ?? 'light'
}
// Called 10 times = 10 storage reads
```

**Correct（Map cache):**

```typescript
const storageCache = new Map<string, string | null>()

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key))
  }
  return storageCache.get(key)
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value)
  storageCache.set(key, value)  // keep cache in sync
}
```

Map（hook ではなく）を使うことで、React コンポーネントだけでなく utility や event handler でも使えます。

**Cookie キャッシュ:**

```typescript
let cookieCache: Record<string, string> | null = null

function getCookie(name: string) {
  if (!cookieCache) {
    cookieCache = Object.fromEntries(
      document.cookie.split('; ').map(c => c.split('='))
    )
  }
  return cookieCache[name]
}
```

**重要（外部変更時に無効化）:**

ストレージが外部で変更される可能性がある場合（別タブ、サーバー設定 Cookie など）はキャッシュを無効化します:

```typescript
window.addEventListener('storage', (e) => {
  if (e.key) storageCache.delete(e.key)
})

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    storageCache.clear()
  }
})
```


## 配列反復をまとめる

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

`.filter()` や `.map()` を複数回呼ぶと配列を何度も走査します。1 回のループに統合してください。

**Incorrect（3 iterations):**

```typescript
const admins = users.filter(u => u.isAdmin)
const testers = users.filter(u => u.isTester)
const inactive = users.filter(u => !u.isActive)
```

**Correct（1 iteration):**

```typescript
const admins: User[] = []
const testers: User[] = []
const inactive: User[] = []

for (const user of users) {
  if (user.isAdmin) admins.push(user)
  if (user.isTester) testers.push(user)
  if (!user.isActive) inactive.push(user)
}
```


## 関数は早期 Return を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

結果が確定した時点で早期 return し、不要な処理を省きます。

**Incorrect（processes all items even after finding answer):**

```typescript
function validateUsers(users: User[]) {
  let hasError = false
  let errorMessage = ''
  
  for (const user of users) {
    if (!user.email) {
      hasError = true
      errorMessage = 'Email required'
    }
    if (!user.name) {
      hasError = true
      errorMessage = 'Name required'
    }
    // Continues checking all users even after error found
  }
  
  return hasError ? { valid: false, error: errorMessage } : { valid: true }
}
```

**Correct（returns immediately on first error):**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) {
      return { valid: false, error: 'Email required' }
    }
    if (!user.name) {
      return { valid: false, error: 'Name required' }
    }
  }

  return { valid: true }
}
```


## RegExp 生成をホイストする

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

RegExp を render 内で毎回生成しないでください。モジュールスコープへ hoist するか `useMemo()` でメモ化します。

**Incorrect（new RegExp every render):**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${query})`, 'gi')
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**Correct（memoize or hoist):**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Highlighter({ text, query }: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, 'gi'),
    [query]
  )
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**注意（グローバル regex は可変 state を持つ）:**

グローバル regex（`/g`）は `lastIndex` という可変 state を持ちます:

```typescript
const regex = /foo/g
regex.test('foo')  // true, lastIndex = 3
regex.test('foo')  // false, lastIndex = 0
```


## 繰り返し検索にはインデックス Map を作る

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

同じキーで `.find()` を繰り返す場合は Map を使います。

**Incorrect（O(n) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map(order => ({
    ...order,
    user: users.find(u => u.id === order.userId)
  }))
}
```

**Correct（O(1) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map(u => [u.id, u]))

  return orders.map(order => ({
    ...order,
    user: userById.get(order.userId)
  }))
}
```

Map を 1 回だけ構築（O(n)）すれば、その後の検索はすべて O(1) です。
1000 件の注文 × 1000 人のユーザーでは、100 万操作が約 2000 操作まで減ります。


## 配列比較は先に Length を確認する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

配列を高コスト処理（ソート・深い比較・シリアライズ）で比較する場合は、先に length を確認します。length が異なれば等価ではありません。

実運用では、比較処理がホットパス（event handler / render ループ）で実行される場合に特に有効です。

**Incorrect（always runs expensive comparison):**

```typescript
function hasChanges(current: string[], original: string[]) {
  // Always sorts and joins, even when lengths differ
  return current.sort().join() !== original.sort().join()
}
```

`current.length` が 5、`original.length` が 100 のように明らかに違う場合でも、O(n log n) のソートが 2 回走ってしまいます。さらに join と文字列比較のオーバーヘッドも発生します。

**Correct（O(1) length check first):**

```typescript
function hasChanges(current: string[], original: string[]) {
  // Early return if lengths differ
  if (current.length !== original.length) {
    return true
  }
  // Only sort when lengths match
  const currentSorted = current.toSorted()
  const originalSorted = original.toSorted()
  for (let i = 0; i < currentSorted.length; i++) {
    if (currentSorted[i] !== originalSorted[i]) {
      return true
    }
  }
  return false
}
```

この方法が効率的な理由:
- 長さが異なる時点で、ソートや join のオーバーヘッドを回避できる
- join した文字列のメモリ消費を避けられる（大きな配列で特に重要）
- 元の配列を破壊しない
- 差分を見つけた時点で早期 return できる


## Min/Max 探索に Sort ではなくループを使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

最小値・最大値の探索は配列を 1 回走査すれば十分です。ソートは無駄で遅くなります。

**Incorrect（O(n log n) - sort to find latest):**

```typescript
interface Project {
  id: string
  name: string
  updatedAt: number
}

function getLatestProject(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => b.updatedAt - a.updatedAt)
  return sorted[0]
}
```

最大値を求めるためだけに配列全体をソートしています。

**Incorrect（O(n log n) - sort for oldest and newest):**

```typescript
function getOldestAndNewest(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => a.updatedAt - b.updatedAt)
  return { oldest: sorted[0], newest: sorted[sorted.length - 1] }
}
```

min/max だけが必要なのに不要なソートを行っています。

**Correct（O(n) - single loop):**

```typescript
function getLatestProject(projects: Project[]) {
  if (projects.length === 0) return null
  
  let latest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt > latest.updatedAt) {
      latest = projects[i]
    }
  }
  
  return latest
}

function getOldestAndNewest(projects: Project[]) {
  if (projects.length === 0) return { oldest: null, newest: null }
  
  let oldest = projects[0]
  let newest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt < oldest.updatedAt) oldest = projects[i]
    if (projects[i].updatedAt > newest.updatedAt) newest = projects[i]
  }
  
  return { oldest, newest }
}
```

配列を 1 回走査するだけで、コピーもソートも不要です。

**代替案（Math.min/Math.max for small arrays):**

```typescript
const numbers = [5, 2, 8, 1, 9]
const min = Math.min(...numbers)
const max = Math.max(...numbers)
```

この方法は小さな配列には有効ですが、スプレッド演算子の制限により、非常に大きい配列では遅くなったりエラーになったりします。最大配列長は Chrome 143 で約 124000、Safari 18 で約 638000 程度です（環境により変動。詳細は [the fiddle](https://jsfiddle.net/qw1jabsx/4/) 参照）。信頼性を重視するならループ方式を使ってください。


## O(1) 検索に Set/Map を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

包含判定を繰り返す場合は配列を Set/Map に変換します。

**Incorrect（O(n) per check):**

```typescript
const allowedIds = ['a', 'b', 'c', ...]
items.filter(item => allowedIds.includes(item.id))
```

**Correct（O(1) per check):**

```typescript
const allowedIds = new Set(['a', 'b', 'c', ...])
items.filter(item => allowedIds.has(item.id))
```


## 不変性のため sort() ではなく toSorted() を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

`.sort()` は配列を破壊的に変更するため、React の state/props で不具合の原因になります。非破壊で新しい配列を返す `.toSorted()` を使ってください。

**Incorrect（mutates original array):**

```typescript
function UserList({ users }: { users: User[] }) {
  // Mutates the users prop array!
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**Correct（creates new array):**

```typescript
function UserList({ users }: { users: User[] }) {
  // Creates new sorted array, original unchanged
  const sorted = useMemo(
    () => users.toSorted((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**React で重要な理由:**

1. Props/state の破壊的変更は React の不変性モデルを壊す - React は props と state を読み取り専用として扱う前提
2. stale closure バグを誘発する - クロージャ（callback/effect）内で配列を破壊的変更すると予期しない挙動につながる

**ブラウザサポート（古い環境向け代替）:**

`.toSorted()` は主要モダン環境（Chrome 110+ / Safari 16+ / Firefox 115+ / Node.js 20+）で利用できます。古い環境ではスプレッド演算子を使ってください:

```typescript
// Fallback for older browsers
const sorted = [...items].sort((a, b) => a.value - b.value)
```

**その他の非破壊配列メソッド:**

- `.toSorted()` - 非破壊ソート
- `.toReversed()` - 非破壊 reverse
- `.toSpliced()` - 非破壊 splice
- `.with()` - 非破壊要素置換

---

## 8. 高度なパターン

**影響: LOW**

適用条件が限定される高度な実装パターンです。


## イベントハンドラを Ref に保持する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

コールバック変更のたびに再購読させたくない Effect では、コールバックを `ref` に保持します。

**Incorrect（毎レンダーで再購読される）:**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}
```

**Correct（購読が安定する）:**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  const handlerRef = useRef(handler)
  useEffect(() => {
    handlerRef.current = handler
  }, [handler])

  useEffect(() => {
    const listener = (e) => handlerRef.current(e)
    window.addEventListener(event, listener)
    return () => window.removeEventListener(event, listener)
  }, [event])
}
```

**代替案（最新 React を使っている場合は `useEffectEvent` を使う）:**

```tsx
import { useEffectEvent } from 'react'

function useWindowEvent(event: string, handler: (e) => void) {
  const onEvent = useEffectEvent(handler)

  useEffect(() => {
    window.addEventListener(event, onEvent)
    return () => window.removeEventListener(event, onEvent)
  }, [event])
}
```

`useEffectEvent` は同じパターンをより簡潔に書ける API です。常に最新のハンドラを呼び出す、安定した関数参照を作成できます。


## アプリ初期化はマウントごとではなく一度だけ実行する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

アプリ読み込みごとに一度だけ実行すべき初期化処理を、コンポーネントの `useEffect([])` に置かないでください。コンポーネントは再マウントされ、Effect は再実行されます。代わりにモジュールスコープのガード、またはエントリーモジュールのトップレベル初期化を使います。

**Incorrect（runs twice in dev, re-runs on remount):**

```tsx
function Comp() {
  useEffect(() => {
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

**Correct（once per app load):**

```tsx
let didInit = false

function Comp() {
  useEffect(() => {
    if (didInit) return
    didInit = true
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

参考: [Initializing the application](https://react.dev/learn/you-might-not-need-an-effect#initializing-the-application)


## 安定したコールバック Ref に useEffectEvent を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

依存配列に追加せずに、コールバック内で最新値へアクセスします。古いクロージャを避けつつ Effect の再実行を防げます。

**Incorrect（effect re-runs on every callback change):**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')

  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300)
    return () => clearTimeout(timeout)
  }, [query, onSearch])
}
```

**Correct（using React's useEffectEvent):**

```tsx
import { useEffectEvent } from 'react';

function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')
  const onSearchEvent = useEffectEvent(onSearch)

  useEffect(() => {
    const timeout = setTimeout(() => onSearchEvent(query), 300)
    return () => clearTimeout(timeout)
  }, [query])
}
```

---

## 参考資料

1. https://react.dev
2. https://nextjs.org
3. https://swr.vercel.app
4. https://github.com/shuding/better-all
5. https://github.com/isaacs/node-lru-cache
6. https://vercel.com/blog/how-we-optimized-package-imports-in-next-js
7. https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast
