---
title: 導出 State は Render 中に計算する
impact: MEDIUM
impactDescription: avoids redundant renders and state drift
tags: rerender, derived-state, useEffect, state
---

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
