---
title: 明示的なコンポーネントバリアントを作る
impact: MEDIUM
impactDescription: 自己説明的で隠れた条件分岐のないコードにする
tags: composition, variants, architecture
---

## 明示的なコンポーネントバリアントを作る

boolean props を多数持つ 1 つのコンポーネントに集約せず、明示的なバリアントコンポーネントを作ります。
各バリアントは必要なパーツだけを合成するため、コード自体が仕様書になります。

**Incorrect（1 コンポーネントに多数のモード）:**

```tsx
// 実際に何が描画されるのか読み取りにくい
<Composer
  isThread
  isEditing={false}
  channelId='abc'
  showAttachments
  showFormatting={false}
/>
```

**Correct（明示的なバリアント）:**

```tsx
// 何が描画されるか一目で分かる
<ThreadComposer channelId="abc" />

// または
<EditMessageComposer messageId="xyz" />

// または
<ForwardMessageComposer messageId="123" />
```

各実装は固有で明示的、かつ自己完結です。同時に共有パーツは再利用できます。

**実装例:**

```tsx
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <ThreadProvider channelId={channelId}>
      <Composer.Frame>
        <Composer.Input />
        <AlsoSendToChannelField channelId={channelId} />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.Submit />
        </Composer.Footer>
      </Composer.Frame>
    </ThreadProvider>
  )
}

function EditMessageComposer({ messageId }: { messageId: string }) {
  return (
    <EditMessageProvider messageId={messageId}>
      <Composer.Frame>
        <Composer.Input />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.CancelEdit />
          <Composer.SaveEdit />
        </Composer.Footer>
      </Composer.Frame>
    </EditMessageProvider>
  )
}

function ForwardMessageComposer({ messageId }: { messageId: string }) {
  return (
    <ForwardMessageProvider messageId={messageId}>
      <Composer.Frame>
        <Composer.Input placeholder="必要ならメッセージを追加" />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.Mentions />
        </Composer.Footer>
      </Composer.Frame>
    </ForwardMessageProvider>
  )
}
```

各バリアントでは次を明示できます。

- どの provider/state を使うか
- どの UI 要素を含むか
- どのアクションが利用できるか

boolean props の組み合わせを推論する必要はありません。実現不能な状態も避けられます。
