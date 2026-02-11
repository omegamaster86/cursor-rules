---
title: 手動ローディング状態より useTransition を使う
impact: LOW
impactDescription: reduces re-renders and improves code clarity
tags: rendering, transitions, useTransition, loading, state
---

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
