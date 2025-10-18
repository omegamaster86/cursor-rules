## 07. 環境・DB・時間

### 環境変数
- `.env.test` を使用し、テスト専用の環境を明示。
- 環境参照は `config.ts` 経由（技術スタック規約順守）。

### データベース
- 実DB禁止。インメモリ（例: SQLite in-memory）またはリポジトリ層のモック。
- マイグレーション相当はテストの`beforeEach`でスキーマ初期化。

### 時間と乱数
- タイマー/時計は固定。乱数はseedまたは固定値。


### 例（良い/悪い）

#### 良い例：インメモリDBと時計固定
```ts
import { vi } from 'vitest';

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date('2024-01-01'));
  // :memory: などの初期化
});

afterEach(() => {
  vi.useRealTimers();
});
```

#### 悪い例：実DB/実時間に依存
```ts
// 実DB接続や new Date() を直接比較 → 非決定・遅い
expect(new Date().toISOString()).toBe('2024-01-01T00:00:00.000Z');
```

