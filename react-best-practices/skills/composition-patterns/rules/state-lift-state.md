---
title: State を Provider コンポーネントへリフトアップする
impact: HIGH
impactDescription: コンポーネント境界の外でも state 共有を可能にする
tags: composition, state, context, providers
---

## State を Provider コンポーネントへリフトアップする

state 管理は専用の Provider コンポーネントへ移してください。
これにより、メイン UI の外側にある兄弟コンポーネントでも、prop drilling や不自然な ref なしで
state の参照と更新が可能になります。

**Incorrect（state がコンポーネント内に閉じる）:**

```tsx
function ForwardMessageComposer() {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()

  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer />
    </Composer.Frame>
  )
}

// 問題: このボタンはどうやって composer state にアクセスするのか？
function ForwardMessageDialog() {
  return (
    <Dialog>
      <ForwardMessageComposer />
      <MessagePreview /> {/* composer state が必要 */}
      <DialogActions>
        <CancelButton />
        <ForwardButton /> {/* submit 呼び出しが必要 */}
      </DialogActions>
    </Dialog>
  )
}
```

**Incorrect（useEffect で state を上に同期）:**

```tsx
function ForwardMessageDialog() {
  const [input, setInput] = useState('')
  return (
    <Dialog>
      <ForwardMessageComposer onInputChange={setInput} />
      <MessagePreview input={input} />
    </Dialog>
  )
}

function ForwardMessageComposer({ onInputChange }) {
  const [state, setState] = useState(initialState)
  useEffect(() => {
    onInputChange(state.input) // 変更ごとに同期 😬
  }, [state.input])
}
```

**Incorrect（submit 時に ref から state を読む）:**

```tsx
function ForwardMessageDialog() {
  const stateRef = useRef(null)
  return (
    <Dialog>
      <ForwardMessageComposer stateRef={stateRef} />
      <ForwardButton onPress={() => submit(stateRef.current)} />
    </Dialog>
  )
}
```

**Correct（state を Provider にリフトアップ）:**

```tsx
function ForwardMessageProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()
  const inputRef = useRef(null)

  return (
    <Composer.Provider
      state={state}
      actions={{ update: setState, submit: forwardMessage }}
      meta={{ inputRef }}
    >
      {children}
    </Composer.Provider>
  )
}

function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        <ForwardMessageComposer />
        <MessagePreview /> {/* カスタムコンポーネントも state/actions にアクセス可能 */}
        <DialogActions>
          <CancelButton />
          <ForwardButton /> {/* カスタムコンポーネントも state/actions にアクセス可能 */}
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  )
}

function ForwardButton() {
  const { actions } = use(Composer.Context)
  return <Button onPress={actions.submit}>Forward</Button>
}
```

`ForwardButton` は `Composer.Frame` の外にあっても、同じ Provider の内側にあるため
submit アクションへアクセスできます。単発利用のコンポーネントでも、UI の外側から
composer の state/actions を利用可能です。

**重要な洞察:** 共有 state が必要なコンポーネント同士は、見た目として入れ子である必要はありません。
同じ Provider 境界の内側にあれば十分です。
