---
title: ユーザー意図に基づいて Preload する
impact: MEDIUM
impactDescription: reduces perceived latency
tags: bundle, preload, user-intent, hover
---

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
