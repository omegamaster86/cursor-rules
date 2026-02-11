# React コンポジションパターン

**バージョン 1.0.0**  
エンジニアリング  
2026年1月

> **注記:**  
> このドキュメントは主に、コンポジションを使う React コードベースを保守・生成・
> リファクタリングするエージェント / LLM 向けです。人間の開発者にも有用ですが、
> AI 支援ワークフローでの自動化と一貫性を重視して最適化されています。

---

## 要約

柔軟で保守しやすい React コンポーネントを構築するためのコンポジションパターン。
複合コンポーネントの活用、state のリフトアップ、内部要素の合成によって boolean props の増殖を防ぎます。
これらのパターンは、規模拡大時にも人間と AI エージェント双方の開発効率を維持します。

---

## 目次

1. [コンポーネント設計](#1-コンポーネント設計) — **HIGH**
   - 1.1 [Boolean Prop の増殖を避ける](#11-boolean-prop-の増殖を避ける)
   - 1.2 [複合コンポーネントを使う](#12-複合コンポーネントを使う)
2. [状態管理](#2-状態管理) — **MEDIUM**
   - 2.1 [状態管理実装を UI から分離する](#21-状態管理実装を-ui-から分離する)
   - 2.2 [依存性注入のための汎用 Context インターフェースを定義する](#22-依存性注入のための汎用-context-インターフェースを定義する)
   - 2.3 [State を Provider コンポーネントへリフトアップする](#23-state-を-provider-コンポーネントへリフトアップする)
3. [実装パターン](#3-実装パターン) — **MEDIUM**
   - 3.1 [明示的なコンポーネントバリアントを作る](#31-明示的なコンポーネントバリアントを作る)
   - 3.2 [Render Props より Children 合成を優先する](#32-render-props-より-children-合成を優先する)
4. [React 19 API](#4-react-19-api) — **MEDIUM**
   - 4.1 [React 19 API 変更](#41-react-19-api-変更)

---

## 1. コンポーネント設計

**Impact: HIGH**

props の増殖を防ぎ、柔軟なコンポジションを可能にするための基本設計です。

### 1.1 Boolean Prop の増殖を避ける

**Impact: CRITICAL（保守不能なバリアント化を防ぐ）**

`isThread`、`isEditing`、`isDMThread` のような boolean prop を増やして挙動を切り替えないでください。
boolean が増えるたびに状態の組み合わせは倍増し、条件分岐は急速に複雑化します。
代わりにコンポジションで表現します。

**Incorrect: boolean props により複雑性が指数的に増える**

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

**Correct: コンポジションで条件分岐を排除する**

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

各バリアントが描画内容を明示するため、巨大な親コンポーネントにロジックを集中させる必要がありません。

### 1.2 複合コンポーネントを使う

**Impact: HIGH（prop drilling なしで柔軟な合成を実現）**

複雑な UI は、共有 context を持つ複合コンポーネントとして分解します。
各サブコンポーネントは props ではなく context から必要な state/action を取得します。

**Incorrect: render props で肥大化した単一コンポーネント**

```tsx
function Composer({
  renderHeader,
  renderFooter,
  renderActions,
  showAttachments,
  showFormatting,
  showEmojis,
}: Props) {
  return (
    <form>
      {renderHeader?.()}
      <Input />
      {showAttachments && <Attachments />}
      {renderFooter ? (
        renderFooter()
      ) : (
        <Footer>
          {showFormatting && <Formatting />}
          {showEmojis && <Emojis />}
          {renderActions?.()}
        </Footer>
      )}
    </form>
  )
}
```

**Correct: 共有 context を持つ複合コンポーネント**

```tsx
const ComposerContext = createContext<ComposerContextValue | null>(null)

function ComposerProvider({ children, state, actions, meta }: ProviderProps) {
  return (
    <ComposerContext value={{ state, actions, meta }}>
      {children}
    </ComposerContext>
  )
}

function ComposerFrame({ children }: { children: React.ReactNode }) {
  return <form>{children}</form>
}

function ComposerInput() {
  const {
    state,
    actions: { update },
    meta: { inputRef },
  } = use(ComposerContext)
  return (
    <TextInput
      ref={inputRef}
      value={state.input}
      onChangeText={(text) => update((s) => ({ ...s, input: text }))}
    />
  )
}

function ComposerSubmit() {
  const {
    actions: { submit },
  } = use(ComposerContext)
  return <Button onPress={submit}>Send</Button>
}

const Composer = {
  Provider: ComposerProvider,
  Frame: ComposerFrame,
  Input: ComposerInput,
  Submit: ComposerSubmit,
  Header: ComposerHeader,
  Footer: ComposerFooter,
  Attachments: ComposerAttachments,
  Formatting: ComposerFormatting,
  Emojis: ComposerEmojis,
}
```

**Usage:**

```tsx
<Composer.Provider state={state} actions={actions} meta={meta}>
  <Composer.Frame>
    <Composer.Header />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Submit />
    </Composer.Footer>
  </Composer.Frame>
</Composer.Provider>
```

利用側が必要な要素のみを明示的に合成でき、隠れた条件分岐を減らせます。

---

## 2. 状態管理

**Impact: MEDIUM**

合成コンポーネント間で state と context を扱うためのパターンです。

### 2.1 状態管理実装を UI から分離する

**Impact: MEDIUM（UI を変えずに state 実装を差し替え可能）**

state 管理の詳細を知るのは Provider のみとし、UI は context インターフェースのみを参照します。

**Incorrect: UI が state 実装に結合している**

```tsx
function ChannelComposer({ channelId }: { channelId: string }) {
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

**Correct: Provider に状態管理を隔離する**

```tsx
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
```

同じ UI を複数の Provider 実装で再利用できます。

### 2.2 依存性注入のための汎用 Context インターフェースを定義する

**Impact: HIGH（ユースケース横断で state 注入を可能にする）**

context 契約を `state` / `actions` / `meta` の 3 層に統一し、
UI を実装詳細から切り離します。

```tsx
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

この契約を満たす Provider であれば、UI を変えずに差し替えられます。

### 2.3 State を Provider コンポーネントへリフトアップする

**Impact: HIGH（コンポーネント境界の外でも state 共有できる）**

state を UI コンポーネント内部に閉じ込めず Provider へ移し、
見た目上は離れた兄弟コンポーネントからも state/actions を扱えるようにします。

**Correct: state を Provider へリフトアップ**

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

function ForwardButton() {
  const { actions } = use(Composer.Context)
  return <Button onPress={actions.submit}>Forward</Button>
}
```

重要なのは見た目の入れ子ではなく Provider 境界です。

---

## 3. 実装パターン

**Impact: MEDIUM**

複合コンポーネントを実装するときの具体的指針です。

### 3.1 明示的なコンポーネントバリアントを作る

**Impact: MEDIUM（自己説明的で隠れた分岐がない）**

1 つのコンポーネントに多数の boolean モードを持たせるのではなく、
`ThreadComposer` / `EditMessageComposer` のような明示的バリアントを作ります。

- どの provider/state を使うか
- どの UI 要素を含むか
- どのアクションを提供するか

を実装ごとに明確化できます。

### 3.2 Render Props より Children 合成を優先する

**Impact: MEDIUM（読みやすく自然な合成）**

構造の合成には `children` を使い、親が子へデータを渡して描画制御する必要がある場合のみ render props を使います。

```tsx
// render props が適切な例
<List
  data={items}
  renderItem={({ item, index }) => <Item item={item} index={index} />}
/>
```

---

## 4. React 19 API

**Impact: MEDIUM**

React 19+ では `forwardRef` を避け、`useContext()` ではなく `use()` を使います。

### 4.1 React 19 API 変更

**Impact: MEDIUM（定義と context 利用が簡潔になる）**

> **⚠️ React 19+ 専用。** React 18 以下では適用しません。

- `ref` は通常の props として扱える（`forwardRef` 不要）
- `useContext(MyContext)` は `use(MyContext)` に置き換える
- `use()` は `useContext()` と異なり条件分岐内でも呼び出し可能

```tsx
function ComposerInput({ ref, ...props }: Props & { ref?: React.Ref<TextInput> }) {
  return <TextInput ref={ref} {...props} />
}

const value = use(MyContext)
```

---

## 参照

1. [https://react.dev](https://react.dev)
2. [https://react.dev/learn/passing-data-deeply-with-context](https://react.dev/learn/passing-data-deeply-with-context)
3. [https://react.dev/reference/react/use](https://react.dev/reference/react/use)
