---
title: 操作ロジックをイベントハンドラへ移す
impact: MEDIUM
impactDescription: avoids effect re-runs and duplicate side effects
tags: rerender, useEffect, events, side-effects, dependencies
---

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
