---
title: 関数型 setState 更新を使う
impact: MEDIUM
impactDescription: prevents stale closures and unnecessary callback recreations
tags: react, hooks, useState, useCallback, callbacks, closures
---

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
