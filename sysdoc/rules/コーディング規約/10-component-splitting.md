## 10. コンポーネント分割規約

### 10.1 基本原則

- **単一責任の原則**：1つのコンポーネントは1つの明確な責務のみを持つ
- **DRY原則**：同じUIパターンが3回以上登場したらコンポーネント化する
- **抽象化レベル**：コンポーネント内は同じ抽象化レベルに統一する

```typescript
// ❌ 悪い例：複数の責務を1つのコンポーネントに詰め込む
export function UserDashboard() {
  // ユーザー情報、統計、通知、設定... すべてを1つで処理
  return <div>{/* 500行以上のJSX */}</div>;
}

// ✅ 良い例：責務ごとに分割
export function UserDashboard() {
  return (
    <div>
      <UserProfile />
      <UserStatistics />
      <NotificationList />
      <UserSettings />
    </div>
  );
}
```

### 10.2 分割判断基準

以下の **いずれか1つでも該当** する場合は分割を検討：

| 基準 | 目安 | 理由 |
|------|------|------|
| コード行数 | 200行超 | 可読性・保守性の低下 |
| JSX行数 | 100行超 | UI構造の複雑化 |
| useState | 5個以上 | 状態管理の複雑化 |
| useEffect | 3個以上 | 副作用の追跡困難 |
| Props | 10個超 | 使いづらさ |
| 再利用性 | 同じパターンが3回以上 | DRY原則違反 |

**分割しない方が良い場合**：
- 再利用されない単純なUI（10行以下）
- 分割でかえって複雑になる場合

### 10.3 分割パターン

#### 10.3.1 プレゼンテーショナル/コンテナパターン

UIとロジックを分離してテストしやすく再利用しやすくする。

```typescript
// プレゼンテーショナル（UI表示のみ）
type UserCardProps = {
  name: string;
  email: string;
  avatarUrl: string;
  isOnline: boolean;
  onSendMessage: () => void;
};

export function UserCard({ name, email, avatarUrl, isOnline, onSendMessage }: UserCardProps) {
  return (
    <div className="border rounded-lg p-4">
      {/* UI表示のみ */}
    </div>
  );
}

// コンテナ（ロジックとデータ取得）
export function UserCardContainer({ userId }: { userId: string }) {
  const { data: user } = useUser(userId);
  const [isOnline, setIsOnline] = useState(false);

  // ビジネスロジック
  const handleSendMessage = () => {/* ... */};

  if (!user) return null;

  return <UserCard {...user} isOnline={isOnline} onSendMessage={handleSendMessage} />;
}
```

#### 10.3.2 Compound Component Pattern

関連コンポーネントをグループ化して柔軟性を保つ。

```typescript
// 親コンポーネント
export function Card({ children }: { children: React.ReactNode }) {
  const [isExpanded, setIsExpanded] = useState(false);
  return (
    <CardContext.Provider value={{ isExpanded, toggle: () => setIsExpanded(!isExpanded) }}>
      <div className="border rounded-lg">{children}</div>
    </CardContext.Provider>
  );
}

// 子コンポーネント群
Card.Header = function CardHeader({ children }) {
  const { toggle } = useCardContext();
  return <div className="p-4 border-b cursor-pointer" onClick={toggle}>{children}</div>;
};

Card.Body = function CardBody({ children }) {
  const { isExpanded } = useCardContext();
  return isExpanded ? <div className="p-4">{children}</div> : null;
};

// 使用例
<Card>
  <Card.Header><h3>ユーザー情報</h3></Card.Header>
  <Card.Body><p>名前: 山田太郎</p></Card.Body>
</Card>
```

### 10.4 ファイル構成

```
# 小規模（単一ファイル）
components/
└── Button.tsx

# 中規模（ディレクトリ）
components/
└── UserCard/
    ├── index.tsx
    ├── UserAvatar.tsx
    ├── UserInfo.tsx
    └── types.ts

# 大規模（機能ごと）
_components/
└── DataTable/
    ├── index.tsx
    ├── DataTable.tsx
    ├── _components/
    ├── _hooks/
    ├── _utils/
    └── types.ts
```

### 10.5 ベストプラクティス

```typescript
// ✅ 明確な命名
function UserProfileCard() { /* ... */ }  // 役割が明確

// ✅ Propsのデフォルト値
export function Button({ variant = "primary", size = "md" }) { /* ... */ }

// ✅ 外部非公開のサブコンポーネントはファイル内に定義
export function UserList() {
  return <div>{users.map(user => <UserListItem key={user.id} user={user} />)}</div>;
}
function UserListItem({ user }) { /* ... */ }  // 外部非公開

// ✅ 不要なdivラッパーを避ける
export function UserActions() {
  return (
    <>
      <button>編集</button>
      <button>削除</button>
    </>
  );
}
```

### 10.6 アンチパターン

```typescript
// ❌ God Component：すべてを1つに詰め込む
export function Dashboard() {
  // 1000行、20個のuseState、10個のuseEffect...
}

// ❌ 過度な分割：1行のためだけにコンポーネント化
function H1({ children }) { return <h1>{children}</h1>; }

// ❌ Props Drilling：深いprops渡し
function A() {
  const data = useData();
  return <B data={data} />;
}
function B({ data }) { return <C data={data} />; }
// ... E まで繰り返し

// ✅ 改善策：Context APIまたはデータフェッチコロケーション
const DataContext = createContext(null);
function A() {
  const data = useData();
  return <DataContext.Provider value={data}><E /></DataContext.Provider>;
}
function E() {
  const data = useContext(DataContext);  // または useData()で直接取得
  return <div>{data.value}</div>;
}
```

---
