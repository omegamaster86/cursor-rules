---
title: Hooks Dependencies Rules
impact: HIGH
impactDescription: useMemo と useCallback の依存配列設定
tags: react, hooks, usememo, usecallback, dependencies
---

## Hooks Dependencies Rules

useMemo と useCallback の正しい使い方と依存配列の設定ルールです。

### useMemo

高コストな計算結果をメモ化する際に使用します。

```typescript
// ✅ 良い例：高コストな計算をメモ化
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.price - b.price);
}, [items]);

// ✅ 良い例：一度だけの初期化
const initialValue = useMemo(() => {
  return computeExpensiveValue();
}, []);

// ✅ 良い例：複数の依存関係
const filteredAndSorted = useMemo(() => {
  return items
    .filter(item => item.category === selectedCategory)
    .sort((a, b) => a.name.localeCompare(b.name));
}, [items, selectedCategory]);
```

**useMemo を使うべき場合：**

| ケース | 説明 |
|-------|------|
| 高コストな計算 | ソート、フィルタリング、複雑な変換処理 |
| 参照の安定化 | オブジェクトや配列を子コンポーネントに渡す場合 |
| 不要な再計算の防止 | 計算結果が頻繁に変わらない場合 |

### useCallback

子コンポーネントに渡す関数をメモ化する際に使用します。

```typescript
// ✅ 良い例：子コンポーネントに渡す関数をメモ化
const handleClick = useCallback(() => {
  console.log("Clicked!");
}, []);

// ✅ 良い例：依存関係のある関数
const handleSubmit = useCallback((data: FormData) => {
  submitForm(data, userId);
}, [userId]);

// 使用例
return <ChildComponent onClick={handleClick} />;
```

**useCallback を使うべき場合：**

| ケース | 説明 |
|-------|------|
| React.memo でラップした子コンポーネントに渡す関数 | 不要な再レンダリングを防ぐ |
| useEffect の依存配列に含める関数 | 無限ループを防ぐ |
| 他のフックの依存配列に含める関数 | 安定した参照を保つ |

### 依存配列の設定ルール

```typescript
// ✅ 良い例：すべての依存関係を含める
const memoizedValue = useMemo(() => {
  return computeValue(a, b, c);
}, [a, b, c]); // すべての変数を含める

// ❌ 悪い例：依存関係の欠落
const memoizedValue = useMemo(() => {
  return computeValue(a, b, c);
}, [a, b]); // c が欠落している

// ❌ 悪い例：空の依存配列で変数を参照
const memoizedValue = useMemo(() => {
  return items.filter(item => item.active);
}, []); // items が欠落している
```

**ESLint ルール：**

`react-hooks/exhaustive-deps` ルールを有効にして、依存配列の問題を検出してください。

### 使用を避けるべき場合

```typescript
// ❌ 不要：単純な計算
const doubled = useMemo(() => value * 2, [value]);
// ✅ 良い例：直接計算
const doubled = value * 2;

// ❌ 不要：単純な関数
const handleClick = useCallback(() => {
  setCount(c => c + 1);
}, []);
// ✅ 良い例：React.memo を使用していないなら不要
const handleClick = () => setCount(c => c + 1);
```

**チェックリスト：**

- [ ] すべての依存関係を依存配列に含める
- [ ] ESLint の `exhaustive-deps` ルールを有効化
- [ ] 単純な計算にはメモ化を使わない
- [ ] React.memo と組み合わせて使用
