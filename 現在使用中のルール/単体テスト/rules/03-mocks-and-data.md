## 03. モック/スタブとテストデータ

### モック/スタブの原則
- 実ネットワーク/FS/DBは禁止。Jest/Vitestのモックで代替。
- 呼び出し検証（引数/回数）を行い、副作用を明示的に検証。

### 実装指針
- リポジトリ/クライアント層をモックし、サービス層のビジネスロジックを検証。
- タイマー/日付/乱数は固定（`useFakeTimers`/固定日時/seed）。

### データファクトリ
- ファクトリ関数/クラスで意味のある初期値を提供し、`overrides`で差分指定。
- 重複データはfixturesへ分離。大規模テストでは`test/fixtures`配下に配置。

### 例（良い/悪い）

#### 良い例：ファクトリ+モック呼び出し検証
```ts
const createUser = (overrides: Partial<User> = {}) => ({
  name: '田中太郎', email: 'tanaka@example.com', age: 25, ...overrides,
});

test('UserService.register 保存呼び出し', async () => {
  const repo = { save: vi.fn().mockResolvedValue({ id: 1 }) };
  const service = new UserService(repo as any);
  const user = createUser();
  await service.register(user);
  expect(repo.save).toHaveBeenCalledWith(expect.objectContaining({ email: user.email }));
});
```

#### 悪い例：実DB/実ネットワークへの依存
```ts
test('登録', async () => {
  // 実DBへ接続/実API呼び出し → 禁止
  await realDb.connect();
  await fetch('https://api.example.com/users', { method: 'POST' });
});
```


