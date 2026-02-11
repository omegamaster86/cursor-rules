---
title: 状態管理実装を UI から分離する
impact: MEDIUM
impactDescription: UI を変更せずに state 実装を差し替え可能にする
tags: composition, state, architecture
---

## 状態管理実装を UI から分離する

state をどう管理するかを知るべきなのは Provider コンポーネントだけです。
UI コンポーネントは context インターフェースを消費し、
state が `useState`、Zustand、サーバー同期のどれかを知る必要はありません。

**Incorrect（UI が state 実装に結合）:**

```tsx
function ChannelComposer({ channelId }: { channelId: string }) {
  // UI コンポーネントがグローバル state 実装を知っている
  const state = useGlobalChannelState(channelId)
  const { submit, updateInput } = useChannelSync(channelId)

  return (
    <Composer.Frame>
      <Composer.Input
        value={state.input}
        onChange={(text) => sync.updateInput(text)}
      />
      <Composer.Submit onPress={() => sync.submit()} />
    </Composer.Frame>
  )
}
```

**Correct（Provider に状態管理を隔離）:**

```tsx
// Provider が state 管理の詳細をすべて扱う
function ChannelProvider({
  channelId,
  children,
}: {
  channelId: string
  children: React.ReactNode
}) {
  const { state, update, submit } = useGlobalChannel(channelId)
  const inputRef = useRef(null)

  return (
    <Composer.Provider
      state={state}
      actions={{ update, submit }}
      meta={{ inputRef }}
    >
      {children}
    </Composer.Provider>
  )
}

// UI コンポーネントは context インターフェースだけを知っていればよい
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <Composer.Footer>
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// 利用例
function Channel({ channelId }: { channelId: string }) {
  return (
    <ChannelProvider channelId={channelId}>
      <ChannelComposer />
    </ChannelProvider>
  )
}
```

**異なる Provider でも同じ UI を使える:**

```tsx
// 一時フォーム向けローカル state
function ForwardMessageProvider({ children }) {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()

  return (
    <Composer.Provider
      state={state}
      actions={{ update: setState, submit: forwardMessage }}
    >
      {children}
    </Composer.Provider>
  )
}

// チャンネル向けグローバル同期 state
function ChannelProvider({ channelId, children }) {
  const { state, update, submit } = useGlobalChannel(channelId)

  return (
    <Composer.Provider state={state} actions={{ update, submit }}>
      {children}
    </Composer.Provider>
  )
}
```

同じ `Composer.Input` が両方の Provider で動作するのは、実装ではなく context インターフェースに依存しているからです。
