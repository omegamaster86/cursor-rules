---
title: 戦略的に Suspense 境界を配置する
impact: HIGH
impactDescription: faster initial paint
tags: async, suspense, streaming, layout-shift
---

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
