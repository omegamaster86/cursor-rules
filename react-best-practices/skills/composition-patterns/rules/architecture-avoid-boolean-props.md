---
title: Boolean Prop の増殖を避ける
impact: CRITICAL
impactDescription: 保守不能なコンポーネントバリアント化を防ぐ
tags: composition, props, architecture
---

## Boolean Prop の増殖を避ける

`isThread`、`isEditing`、`isDMThread` のような boolean prop を追加して
コンポーネント挙動を切り替えないでください。boolean が 1 つ増えるたびに状態空間は倍増し、
条件分岐は保守不能になります。代わりにコンポジションを使ってください。

**Incorrect（boolean props により複雑性が指数的に増える）:**

```tsx
function Composer({
  onSubmit,
  isThread,
  channelId,
  isDMThread,
  dmId,
  isEditing,
  isForwarding,
}: Props) {
  return (
    <form>
      <Header />
      <Input />
      {isDMThread ? (
        <AlsoSendToDMField id={dmId} />
      ) : isThread ? (
        <AlsoSendToChannelField id={channelId} />
      ) : null}
      {isEditing ? (
        <EditActions />
      ) : isForwarding ? (
        <ForwardActions />
      ) : (
        <DefaultActions />
      )}
      <Footer onSubmit={onSubmit} />
    </form>
  )
}
```

**Correct（コンポジションで条件分岐を排除）:**

```tsx
// チャンネル用 composer
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <Composer.Footer>
        <Composer.Attachments />
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// スレッド用 composer - 「チャンネルにも送信」フィールドを追加
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <AlsoSendToChannelField id={channelId} />
      <Composer.Footer>
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// 編集用 composer - フッターアクションが異なる
function EditComposer() {
  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer>
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.CancelEdit />
        <Composer.SaveEdit />
      </Composer.Footer>
    </Composer.Frame>
  )
}
```

各バリアントは何を描画するかを明示します。巨大な親コンポーネントを共有しなくても、内部パーツは共有できます。
