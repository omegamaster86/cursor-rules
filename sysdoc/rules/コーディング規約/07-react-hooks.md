## 7. React Hooks 規約

React Hooks を使用する際の規約を定義します。特に `useEffect` の使用については厳密なルールを設けます。

### 7.1 useEffect の使用ポリシー

#### 7.1.1 基本原則

`useEffect` は **外部世界との同期にのみ使用する** ことを原則とします。

**使用が許可される場合**：

- API 呼び出し
- WebSocket 接続
- ブラウザ API（例：`localStorage`、`addEventListener`）
- 外部ストアのサブスクリプション
- タイマー（`setTimeout`、`setInterval`）

**その他の場合には極力使用してはいけません。**

#### 7.1.2 アンチパターン（絶対に避けるべき使い方）

以下のような使い方は **禁止** です：

```typescript
// ❌ 悪い例1：propsや派生値をローカルステートにコピー
function Component({ userId }: { userId: string }) {
  const [id, setId] = useState(userId);

  useEffect(() => {
    setId(userId); // propsをstateにコピーするのは不要
  }, [userId]);

  // ...
}

// ❌ 悪い例2：フラグの変更に応じてロジックを実行
function Component() {
  const [shouldUpdate, setShouldUpdate] = useState(false);

  useEffect(() => {
    if (shouldUpdate) {
      // 何かの処理
      setShouldUpdate(false);
    }
  }, [shouldUpdate]);

  // ...
}

// ❌ 悪い例3：イベントハンドラの代わりにエフェクト内でユーザーアクションを処理
function Component() {
  const [clicked, setClicked] = useState(false);

  useEffect(() => {
    if (clicked) {
      // ユーザーアクションの処理
    }
  }, [clicked]);

  return <button onClick={() => setClicked(true)}>Click</button>;
}

// ❌ 悪い例4：エフェクト内で派生状態やバリデーション状態を更新
function Component({ email }: { email: string }) {
  const [isValid, setIsValid] = useState(false);

  useEffect(() => {
    setIsValid(email.includes("@")); // レンダリング中に計算すべき
  }, [email]);

  // ...
}

// ❌ 悪い例5：空の依存配列で一度だけの初期化を実行
function Component() {
  const [data, setData] = useState(null);

  useEffect(() => {
    setData(computeExpensiveValue()); // useMemoを使うべき
  }, []);

  // ...
}
```

#### 7.1.3 正しい使い方

```typescript
// ✅ 良い例1：propsから派生した値はレンダリング中に計算
function Component({ userId }: { userId: string }) {
  // useEffectを使わず、直接計算する
  const formattedId = `user-${userId}`;

  return <div>{formattedId}</div>;
}

// ✅ 良い例2：useMemoで計算結果をメモ化
function Component({ items }: { items: Item[] }) {
  // 一度だけ計算したい場合はuseMemoを使用
  const expensiveValue = useMemo(() => {
    return computeExpensiveValue(items);
  }, [items]);

  return <div>{expensiveValue}</div>;
}

// ✅ 良い例3：ユーザーアクションはイベントハンドラで処理
function Component() {
  function handleClick() {
    // ユーザーアクションの処理はイベントハンドラで行う
    console.log("Clicked!");
  }

  return <button onClick={handleClick}>Click</button>;
}

// ✅ 良い例4：バリデーションはレンダリング中に実行
function Component({ email }: { email: string }) {
  // useEffectを使わず、直接計算する
  const isValid = email.includes("@");

  return <div>{isValid ? "Valid" : "Invalid"}</div>;
}

// ✅ 良い例5：外部システムとの同期にuseEffectを使用
function Component() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // 外部API呼び出し（外部システムとの同期）
    async function fetchData() {
      const response = await fetch("/api/data");
      const result = await response.json();
      setData(result);
    }

    fetchData();
  }, []);

  return <div>{data}</div>;
}
```

#### 7.1.4 useEffect を使用する際の必須ルール

`useEffect` を記述する際は、**必ず短いコメントを追加**し、どの外部リソースと同期しているかを明記してください。

```typescript
// ✅ 良い例：コメントで外部リソースを明記
function Component() {
  const [data, setData] = useState(null);

  // 外部API（/api/users）からユーザーデータを取得
  useEffect(() => {
    async function fetchUsers() {
      const response = await fetch("/api/users");
      const users = await response.json();
      setData(users);
    }

    fetchUsers();
  }, []);

  // WebSocketサーバーに接続してリアルタイムデータを受信
  useEffect(() => {
    const ws = new WebSocket("wss://example.com/socket");

    ws.onmessage = (event) => {
      console.log("Received:", event.data);
    };

    // クリーンアップ関数
    return () => {
      ws.close();
    };
  }, []);

  return <div>{/* ... */}</div>;
}
```

#### 7.1.5 useEffect の3つの原則

1. **propsやstateから派生できる値は、レンダリング中に計算する**

   - `useEffect` で state を更新するのではなく、直接計算する

2. **ユーザーアクションはイベントハンドラで処理し、エフェクトでは処理しない**

   - ボタンのクリック、フォームの送信などは `onClick` や `onSubmit` で処理する

3. **エフェクトは、外部システムと接触する実際の副作用のためだけに使用する**
   - API、WebSocket、ブラウザ API、タイマーなど、外部との同期にのみ使用する

### 7.2 その他の Hooks の使用ガイドライン

#### 7.2.1 useState

- ユーザー入力やUI状態の管理に使用する
- 派生可能な値は state にしない（計算して求める）

```typescript
// ❌ 悪い例：派生可能な値をstateにする
const [firstName, setFirstName] = useState("");
const [lastName, setLastName] = useState("");
const [fullName, setFullName] = useState(""); // 不要

// ✅ 良い例：派生値は計算する
const [firstName, setFirstName] = useState("");
const [lastName, setLastName] = useState("");
const fullName = `${firstName} ${lastName}`; // 計算で求める
```

#### 7.2.2 useMemo

- 高コストな計算結果をメモ化する
- 空の依存配列での初期化に使用する

```typescript
// ✅ 良い例：高コストな計算をメモ化
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.price - b.price);
}, [items]);

// ✅ 良い例：一度だけの初期化
const initialValue = useMemo(() => {
  return computeExpensiveValue();
}, []);
```

#### 7.2.3 useCallback

- 子コンポーネントに渡す関数をメモ化する
- 依存配列を正しく指定する

```typescript
// ✅ 良い例：子コンポーネントに渡す関数をメモ化
const handleClick = useCallback(() => {
  console.log("Clicked!");
}, []);

return <ChildComponent onClick={handleClick} />;
```

---
