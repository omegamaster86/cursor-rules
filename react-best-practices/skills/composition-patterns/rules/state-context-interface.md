---
title: 依存性注入のための汎用 Context インターフェースを定義する
impact: HIGH
impactDescription: ユースケース横断で依存性注入可能な state を実現する
tags: composition, context, state, typescript, dependency-injection
---

## 依存性注入のための汎用 Context インターフェースを定義する

コンポーネント context には、`state`、`actions`、`meta` の 3 要素を持つ
**汎用インターフェース**を定義してください。
このインターフェースは任意の Provider が実装できる契約であり、
同じ UI コンポーネントを異なる state 実装で動作させられます。

**コア原則:** state をリフトアップし、内部を合成し、state を依存性注入可能にする。

**Incorrect（UI が特定の state 実装に密結合）:**

```tsx
function ComposerInput() {
  // 特定の hook に強く依存
  const { input, setInput } = useChannelComposerState()
  return <TextInput value={input} onChangeText={setInput} />
}
```

**Correct（汎用インターフェースで依存性注入を可能にする）:**

```tsx
// 任意の Provider が実装できる汎用インターフェースを定義
interface ComposerState {
  input: string
  attachments: Attachment[]
  isSubmitting: boolean
}

interface ComposerActions {
  update: (updater: (state: ComposerState) => ComposerState) => void
  submit: () => void
}

interface ComposerMeta {
  inputRef: React.RefObject<TextInput>
}

interface ComposerContextValue {
  state: ComposerState
  actions: ComposerActions
  meta: ComposerMeta
}

const ComposerContext = createContext<ComposerContextValue | null>(null)
```

**UI コンポーネントは実装ではなくインターフェースに依存する:**

```tsx
function ComposerInput() {
  const {
    state,
    actions: { update },
    meta,
  } = use(ComposerContext)

  // このコンポーネントは、インターフェースを満たす任意の Provider で動作する
  return (
    <TextInput
      ref={meta.inputRef}
      value={state.input}
      onChangeText={(text) => update((s) => ({ ...s, input: text }))}
    />
  )
}
```

**異なる Provider が同じインターフェースを実装できる:**

```tsx
// Provider A: 一時フォーム向けのローカル state
function ForwardMessageProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState(initialState)
  const inputRef = useRef(null)
  const submit = useForwardMessage()

  return (
    <ComposerContext
      value={{
        state,
        actions: { update: setState, submit },
        meta: { inputRef },
      }}
    >
      {children}
    </ComposerContext>
  )
}

// Provider B: チャンネル向けのグローバル同期 state
function ChannelProvider({ channelId, children }: Props) {
  const { state, update, submit } = useGlobalChannel(channelId)
  const inputRef = useRef(null)

  return (
    <ComposerContext
      value={{
        state,
        actions: { update, submit },
        meta: { inputRef },
      }}
    >
      {children}
    </ComposerContext>
  )
}
```

**同じ合成 UI が両方で動作する:**

```tsx
// ForwardMessageProvider（ローカル state）で動作
<ForwardMessageProvider>
  <Composer.Frame>
    <Composer.Input />
    <Composer.Submit />
  </Composer.Frame>
</ForwardMessageProvider>

// ChannelProvider（グローバル同期 state）で動作
<ChannelProvider channelId="abc">
  <Composer.Frame>
    <Composer.Input />
    <Composer.Submit />
  </Composer.Frame>
</ChannelProvider>
```

**コンポーネント外のカスタム UI からも state/actions にアクセスできる:**

Provider 境界が重要で、見た目の入れ子構造は本質ではありません。
共有 state が必要なコンポーネントは `Composer.Frame` の内側にある必要はなく、
同じ Provider 配下にあればアクセスできます。

```tsx
function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        {/* composer UI */}
        <Composer.Frame>
          <Composer.Input placeholder="必要ならメッセージを追加" />
          <Composer.Footer>
            <Composer.Formatting />
            <Composer.Emojis />
          </Composer.Footer>
        </Composer.Frame>

        {/* composer の外側だが Provider の内側にあるカスタム UI */}
        <MessagePreview />

        {/* ダイアログ下部のアクション */}
        <DialogActions>
          <CancelButton />
          <ForwardButton />
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  )
}

// Composer.Frame の外側でも context に基づいて submit できる
function ForwardButton() {
  const {
    actions: { submit },
  } = use(ComposerContext)
  return <Button onPress={submit}>Forward</Button>
}

// Composer.Frame の外側でも composer state を参照できる
function MessagePreview() {
  const { state } = use(ComposerContext)
  return <Preview message={state.input} attachments={state.attachments} />
}
```

`ForwardButton` と `MessagePreview` は composer の見た目の枠外にあっても、
同じ Provider 配下にあるため state/actions を利用できます。これが state リフトアップの力です。

UI は再利用可能な部品として合成し、state は Provider から依存性注入します。
Provider を差し替えても UI は維持できます。
