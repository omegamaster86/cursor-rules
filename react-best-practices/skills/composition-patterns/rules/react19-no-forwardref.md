---
title: React 19 API 変更
impact: MEDIUM
impactDescription: コンポーネント定義と context 利用をより簡潔にする
tags: react19, refs, context, hooks
---

## React 19 API 変更

> **⚠️ React 19+ 専用。** React 18 以下ではこのルールを適用しません。

React 19 では `ref` が通常の props として扱えます（`forwardRef` ラッパーは不要）。
また `useContext()` は `use()` へ置き換わります。

**Incorrect（React 19 で `forwardRef` を使う）:**

```tsx
const ComposerInput = forwardRef<TextInput, Props>((props, ref) => {
  return <TextInput ref={ref} {...props} />
})
```

**Correct（`ref` を通常の props として扱う）:**

```tsx
function ComposerInput({ ref, ...props }: Props & { ref?: React.Ref<TextInput> }) {
  return <TextInput ref={ref} {...props} />
}
```

**Incorrect（React 19 で `useContext` を使う）:**

```tsx
const value = useContext(MyContext)
```

**Correct（`useContext` の代わりに `use` を使う）:**

```tsx
const value = use(MyContext)
```

`use()` は `useContext()` と異なり、条件分岐の中でも呼び出せます。
