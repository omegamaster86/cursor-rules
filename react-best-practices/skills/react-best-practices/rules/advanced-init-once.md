---
title: アプリ初期化はマウントごとではなく一度だけ実行する
impact: LOW-MEDIUM
impactDescription: avoids duplicate init in development
tags: initialization, useEffect, app-startup, side-effects
---

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
