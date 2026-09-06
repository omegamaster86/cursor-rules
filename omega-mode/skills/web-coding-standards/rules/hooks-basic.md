---
title: React Hooks Basic Rules
impact: HIGH
impactDescription: useState と useEffect の基本ルール
tags: react, hooks, usestate, useeffect
---

## React Hooks Basic Rules

useState と useEffect の正しい使い方に関するルールです。

### useEffect の使用ポリシー

**基本原則：useEffect は外部世界との同期にのみ使用する**

**使用が許可される場合：**

- API 呼び出し
- WebSocket 接続
- ブラウザ API（`localStorage`、`addEventListener`）
- 外部ストアのサブスクリプション
- タイマー（`setTimeout`、`setInterval`）

**❌ アンチパターン（禁止）：**

```typescript
// ❌ 悪い例1：propsや派生値をローカルステートにコピー
function Component({ userId }: { userId: string }) {
  const [id, setId] = useState(userId);
  useEffect(() => {
    setId(userId); // propsをstateにコピーするのは不要
  }, [userId]);
}

// ❌ 悪い例2：派生状態をエフェクト内で更新
function Component({ email }: { email: string }) {
  const [isValid, setIsValid] = useState(false);
  useEffect(() => {
    setIsValid(email.includes("@")); // レンダリング中に計算すべき
  }, [email]);
}
```

**✅ 正しい使い方：**

```typescript
// ✅ 良い例1：派生した値はレンダリング中に計算
function Component({ userId }: { userId: string }) {
  const formattedId = `user-${userId}`; // 直接計算
  return <div>{formattedId}</div>;
}

// ✅ 良い例2：バリデーションはレンダリング中に実行
function Component({ email }: { email: string }) {
  const isValid = email.includes("@"); // 直接計算
  return <div>{isValid ? "Valid" : "Invalid"}</div>;
}

// ✅ 良い例3：外部システムとの同期にuseEffectを使用
function Component() {
  const [data, setData] = useState(null);

  // 外部API（/api/users）からユーザーデータを取得
  useEffect(() => {
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

**useEffect 記述時の必須ルール：**

`useEffect` を記述する際は、必ず短いコメントを追加し、どの外部リソースと同期しているかを明記してください。

```typescript
// ✅ 良い例：コメントで外部リソースを明記
// 外部API（/api/users）からユーザーデータを取得
useEffect(() => {
  // ...
}, []);

// WebSocketサーバーに接続してリアルタイムデータを受信
useEffect(() => {
  // ...
}, []);
```

### useState のルール

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

**チェックリスト：**

- [ ] useEffect は外部システムとの同期にのみ使用
- [ ] 派生可能な値は state にせず計算
- [ ] useEffect には外部リソースを明記するコメントを追加
