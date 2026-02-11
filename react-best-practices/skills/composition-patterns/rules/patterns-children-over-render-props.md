---
title: Render Props より Children 合成を優先する
impact: MEDIUM
impactDescription: よりクリーンで読みやすいコンポジションを実現する
tags: composition, children, render-props
---

## Render Props より Children 合成を優先する

`renderX` props より `children` を使って合成してください。`children` は可読性が高く、
自然に合成でき、コールバックのシグネチャ理解を要求しません。

**Incorrect（render props）:**

```tsx
function Composer({
  renderHeader,
  renderFooter,
  renderActions,
}: {
  renderHeader?: () => React.ReactNode
  renderFooter?: () => React.ReactNode
  renderActions?: () => React.ReactNode
}) {
  return (
    <form>
      {renderHeader?.()}
      <Input />
      {renderFooter ? renderFooter() : <DefaultFooter />}
      {renderActions?.()}
    </form>
  )
}

// 利用側が扱いにくく柔軟性も低い
return (
  <Composer
    renderHeader={() => <CustomHeader />}
    renderFooter={() => (
      <>
        <Formatting />
        <Emojis />
      </>
    )}
    renderActions={() => <SubmitButton />}
  />
)
```

**Correct（children を使った複合コンポーネント）:**

```tsx
function ComposerFrame({ children }: { children: React.ReactNode }) {
  return <form>{children}</form>
}

function ComposerFooter({ children }: { children: React.ReactNode }) {
  return <footer className='flex'>{children}</footer>
}

// 利用側は柔軟に合成できる
return (
  <Composer.Frame>
    <CustomHeader />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Emojis />
      <SubmitButton />
    </Composer.Footer>
  </Composer.Frame>
)
```

**render props が適しているケース:**

```tsx
// 親から子にデータを渡して描画させる場面では有効
<List
  data={items}
  renderItem={({ item, index }) => <Item item={item} index={index} />}
/>
```

親が子へデータや state を供給する必要がある場合は render props を使います。
静的な構造を合成する場合は children を使います。
