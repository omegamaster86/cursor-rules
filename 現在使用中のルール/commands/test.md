# 単体テスト ルール集（統合版）

---
## 単体テスト

このディレクトリは、既存の「単体テストガイドライン」を実運用しやすいルール形式に再編したものです。実務で迷わないように、Must/Should中心で簡潔に定義しています。

### 対象
- TypeScript/Node.js/Next.js/React を前提
- テストフレームワークは Jest/Vitest のいずれか（プロジェクト方針に従う）

### 使い方
1) まず `01-policy.md` を読んで最低限のMustを統一します。
2) 実装時は `02〜04` を参照してテストを書き始めます。
3) 実行・CIは `05`、品質担保は `06` を参照します。
4) 環境やDBなど外部要因は `07`、パフォーマンスは `08` を参照します。
5) 最後に `09` のチェックリストで抜け漏れ確認を行います。
6) 仕様変更や修正時は `10` を参照しテストを更新します。

注: 各章には「良い例／悪い例」を簡潔に記載しています。詳細解説は元のガイドラインを参照してください。

---

## 01-policy.md

## 01. 基本方針・適用範囲・禁止事項

### Must（必須）
- 単体テストは関数/メソッド/クラスなど最小単位を対象とし、外部I/O（ネットワーク/FS/実DB）に依存しないこと（モック/スタブを使用）。
- 各テストは独立・再現可能。グローバル状態に依存しない。時計や乱数は固定化する。
- テストはAAA（Arrange-Act-Assert）で構造化し、1テスト1アサーションの原則を基本とする（やむを得ない場合でも論理的に関連した検証に限定）。
- 命名は `対象_条件_期待結果` 形式または `should ... when ...` を用い、曖昧な名称を避ける。
- カバレッジは global 80% 以上（branches/functions/lines/statements）。しきい値はCIで強制。
- 実行はローカル/CIの双方で自動化し、失敗はブロッカーとして扱う。

### Should（推奨）
- 正常系/異常系/境界値/エッジケースを網羅する。
- テストデータはファクトリ/フィクスチャで再利用し、重複を排除する。
- モックは呼び出し検証（引数/回数）を行い、副作用のない設計を保つ。
- Describeで機能単位を構造化し、読みやすさ・保守性を優先する。

### 禁止事項
- 実ネットワーク呼び出し、実ファイルシステム操作、実データベース接続。
- テスト間の状態共有（グローバル変数、シングルトンの使い回し）。
- 手動判定（console出力のみ等）。必ずアサーションで自己検証。
- 実装に過度に結合したホワイトボックス前提の脆いテスト（過剰な内部実装前提）。

### 適用範囲
- TypeScript/Node.js/Next.js/React を中心とするアプリケーション層の単体テスト全般。
- フレームワークは Jest/Vitest。既存プロジェクト方針に従うこと。

### テスト優先度（明示）
- Critical（必須・最優先）: コアドメイン/決済/認証など。必ず網羅・維持する。
- Important（重要）: 主要機能、重要なエラーハンドリング。基本的に網羅する。
- Recommended（推奨）: 補助機能、一般的なユーティリティ。
- Optional（任意）: 非重要な表示/ログ等。

例（優先度の明示）
```ts
describe('決済処理', () => {
  // Critical: ビジネスロジックの核心
  test('正常な決済処理', () => {/* ... */});

  // Important: エラーハンドリング
  test('残高不足でエラー', () => {/* ... */});

  // Recommended: 付随機能
  test('履歴の記録', () => {/* ... */});
});
```

### 例（良い/悪い）

#### 良い例：独立かつAAAで自己検証
```ts
test('calculateDiscount_正常_10%割引を返す', () => {
  // Arrange
  const price = 1000;
  const rate = 0.1;
  // Act
  const result = calculateDiscount(price, rate);
  // Assert
  expect(result).toBe(900);
});
```

#### 悪い例：グローバル状態と手動確認
```ts
let total = 0;
test('割引', () => {
  total = calculateDiscount(1000, 0.1); // 前後テストに影響
  console.log(total); // アサーションなし
});
```

---

## 02. テスト設計

### AAA（Arrange-Act-Assert）
- 準備（Arrange）：テストデータ/依存を明示的に準備（ファクトリ活用）。
- 実行（Act）：対象関数/メソッドを1回だけ実行。
- 検証（Assert）：期待値を明確に。副作用はモック呼び出しで検証。

### 再現性
**再現性の重要性**
- バグの特定が容易
- テスト結果の信頼性
- 環境に依存しない

**再現性を保つ方法**
```ts
// ❌ 再現性がない例
test('randomNumber', () => {
  const random = Math.random(); // 毎回異なる値
  expect(random).toBeGreaterThan(0);
});

// ✅ 再現性がある例
test('calculateTax', () => {
  const price = 1000;
  const taxRate = 0.1;
  const result = calculateTax(price, taxRate);
  expect(result).toBe(100); // 常に同じ結果
});

// 日付の固定
test('formatDate', () => {
  const fixedDate = new Date('2024-01-01');
  const result = formatDate(fixedDate);
  expect(result).toBe('2024/01/01');
});
```

### ケース網羅
- 正常系、異常系（例外/エラー）、境界値（最小/最大/±1）、エッジケースを用意。
- 回帰視点を含め、既存仕様の保持を保証。

### 回帰テスト（短い例）
過去に発生した不具合をテストとして固定化し、再発を防ぎます。
```javascript
describe('ユーザー登録機能の回帰テスト', () => {
    test('既存機能：emailとpasswordが必須', () => {
        // 既存のテストケースが引き続き動作することを確認
        expect(() => registerUser({})).toThrow('必須項目が不足しています');
        expect(() => registerUser({ email: 'test@example.com' })).toThrow('必須項目が不足しています');
    });
    
    test('新機能：パスワード強度チェック', () => {
        // 新機能が正しく動作することを確認
        expect(() => registerUser({
            email: 'test@example.com',
            password: '123' // 8文字未満
        })).toThrow('パスワードは8文字以上である必要があります');
    });
    
    test('統合：既存機能と新機能の両方が動作', () => {
        // 両方の機能が同時に動作することを確認
        const result = registerUser({
            email: 'test@example.com',
            password: 'password123' // 8文字以上
        });
        expect(result).toBeDefined();
    });
});
```

### 命名規則
- `対象_条件_期待結果` または `should <期待> when <条件>`。

### データ戦略
- テストデータは最小限・意味のある値に限定。過剰なセットアップを避ける。
- ファクトリ/fixturesで共通化し、差分はオーバーライドで表現。

### 非同期/例外
- Promise: `await expect(promise).rejects.toThrow('message')`。
- 例外: `expect(() => fn()).toThrow('message')`。

### モック/スタブ方針
- 外部I/Oは必ずモック化。戻り値固定はスタブ、呼び出し検証はモックを使用。
- 優先度: ビジネスロジックは実物、外部境界はモック。

### 例（良い/悪い）

#### 良い例：境界値と異常系の分離
```ts
describe('validateAge', () => {
  test('境界: 0は有効', () => {
    expect(validateAge(0)).toBe(true);
  });
  test('境界: -1は無効', () => {
    expect(validateAge(-1)).toBe(false);
  });
});
```

#### 悪い例：1テストに多目的アサーションを詰め込む
```ts
test('年齢の検証まとめ', () => {
  expect(validateAge(0)).toBe(true);
  expect(validateAge(-1)).toBe(false);
  expect(validateAge(200)).toBe(false);
});
```

---

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

---

## 04. 構造・命名・分割

### ディレクトリ/命名
- テストは `tests/unit/**` または `__tests__` 配下。
- ファイル名: `*.test.ts` or `*.spec.ts`。対象ファイル名に合わせる。

### 分割基準
- describeは機能/メソッド単位。1ファイルの肥大化（~300行以上）は分割。
- 共通セットアップは `beforeEach` に抽出。テスト同士の状態共有は禁止。

### 例（良い/悪い）

#### 良い例：命名と配置
```
src/utils/calc.ts
tests/utils/calc.test.ts
```
```ts
// tests/utils/calc.test.ts
describe('calc.add', () => {
  test('should return 5 when 2 + 3', () => {
    expect(add(2, 3)).toBe(5);
  });
});
```

#### 悪い例：曖昧なテスト名と混在配置
```
misc/test1.ts  // どこに属するか不明
```
```ts
test('計算テスト', () => { /* 曖昧 */ });
```

---

## 05. 実行・CI/品質ゲート

### 実行スクリプト（例）
- `test`: 全テスト
- `test:watch`: 監視実行
- `test:coverage`: カバレッジ出力

### 並列/パフォーマンス
- maxWorkersはCIで環境に合わせて設定（例: 50%）。
- タイムアウトを明示的に設定（例: 10s）。

### CI原則
- 失敗はマージブロック。カバレッジしきい値（global 80%）を強制。
- Nodeバージョンマトリクス実行（プロジェクト規約に従う）。

### pre-commit/ローカルフック
- 変更の早期検知のため、pre-commit で最小のテスト実行を推奨（--watchは禁止）。
- Husky例（最小）：
```json
{
  "scripts": {
    "test": "jest",
    "test:ci": "jest --coverage --ci --maxWorkers=50%"
  },
  "husky": {
    "hooks": {
      "pre-commit": "npm run test:ci"
    }
  }
}
```

### 例（良い/悪い）

#### 良い例：npmスクリプト + GitHub Actions（最小）
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage --ci"
  }
}
```
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20.x', cache: 'npm' }
      - run: npm ci
      - run: npm run test:coverage
```

#### 悪い例：CIでwatch実行/しきい値なし
```yaml
# CIで--watchを使用 → ハングの原因
- run: npm run test:watch
```

---

## 06. 品質・メトリクス・失敗時対応

### 成功指標（定量/定性）
- 定量: カバレッジ>=80%（global）、失敗テスト=0、フレーク率<1%、平均実行時間の抑制。
- 定性: テスト名が仕様を語る、AAAが明確、外部依存の適切なモック化、読みやすさ/保守性/安定性。

### メトリクス/継続改善
- 追跡項目: パス率、失敗数、実行時間、フレーク検知件数、遅いテスト上位N。
- 改善指針: カバレッジ不足→テスト追加、実行時間長い→モック/並列最適化、フレーク→非決定要因の排除（時計/乱数/リトライ）。

例（擬似メトリクス）
```json
{
  "total": 120,
  "passed": 120,
  "failed": 0,
  "coverage": { "branches": 82, "functions": 88, "lines": 86 },
  "durationMs": 2400,
  "flaky": 0
}
```

### カバレッジ基準（CI強制）
- Global 80%以上（branches/functions/lines/statements）。
- 重要箇所（コアドメイン）は個別しきい値の引き上げを検討。

### レビュー観点
- テスト名が仕様を語っているか（可読性）
- 正常/異常/境界/回帰の網羅
- AAAの明確さ、過剰なセットアップの排除
- 外部依存のモック化と検証の妥当性

### 失敗時対応
- エラーメッセージ/期待値ズレの分析→仕様/実装のどちらが誤りか切り分け。
- 不安定（flaky）テストの隔離・原因究明（非決定性の排除、タイマー固定）。
- 恒常的失敗はまずテストの安定化、その後リファクタリング。

#### 例（良い/悪い）

#### 良い例：閾値設定とレポート
```js
// jest.config.js
module.exports = {
  collectCoverageFrom: ['src/**/*.ts', '!src/**/*.test.ts'],
  coverageThreshold: { global: { branches: 80, functions: 80, lines: 80, statements: 80 } },
  coverageReporters: ['text', 'lcov', 'html']
};
```

#### 悪い例：閾値未設定・レポート未出力
```js
// coverage設定なし → 品質ゲートが機能しない
module.exports = {};
```

---

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

---

## 08. パフォーマンス/安定性

### 実行時間最適化
- 重いI/Oを排除し、モックで置換。テストデータは必要最小限。
- 並列度（maxWorkers）とタイムアウトを環境に合わせ最適化。

### メモリ・リソース
- 大量データテストはサイズ制限とガベコレ前提の後処理を実施。

### Flaky対策
- 時計固定、リトライ抑制、非同期待機の明示（適切なawait/タイマー）。

### 例（良い/悪い）

#### 良い例：大量データのサイズ制限と測定
```ts
test('大量データ処理は1秒未満', () => {
  const large = Array.from({ length: 5000 }, (_, i) => i);
  const t0 = Date.now();
  const result = processLarge(large);
  const t1 = Date.now();
  expect(result).toBeDefined();
  expect(t1 - t0).toBeLessThan(1000);
});
```

#### 悪い例：無制限生成と待機不足
```ts
// 100万件生成 + 適切なawaitなし → メモリ圧迫/不安定
const huge = Array.from({ length: 1_000_000 }, (_, i) => i);
processLarge(huge);
```
---

## 09. チェックリスト

### 作成チェック
- [ ] テスト名が仕様を説明している
- [ ] AAAで構造化し1テスト1検証（原則）
- [ ] 正常/異常/境界/回帰が網羅
- [ ] 外部依存はモック/スタブ
- [ ] データはファクトリ/fixturesで再利用

### レビューチェック
- [ ] 過剰なセットアップがない
- [ ] 実装に過度結合していない
- [ ] カバレッジが基準を満たす
- [ ] 失敗時のメッセージが明確

### 運用チェック（CI）
- [ ] カバレッジしきい値を強制
- [ ] 並列数/タイムアウトの妥当性
- [ ] Flaky検知と隔離フロー

### 例（補助）
```md
作成時の自問:
- そのテスト名は仕様を一読で伝えるか？
- 異常系・境界値は網羅したか？
- 実I/Oに依存していないか？
```

---

### Must（必須）
- 仕様変更/バグ修正/リファクタリングと同一PRでテストも更新する。
- 不要・重複・脆いテストは定期的に整理する。

### 更新タイミング
- 機能仕様の変更時、バグ修正時、リファクタリング時、新要件追加時。

### 更新手順（最小）
1. 変更内容の把握（仕様/受入条件）。
2. 影響範囲の特定（対象関数/モジュールの検索）。
3. テストの修正/追加（正常/異常/境界/回帰）。
4. 全テスト実行とカバレッジ確認（基準維持）。

### 整理のポイント（定期）
- 重複テストの統合（`test.each`活用）。
- 不要になったテストの削除/コメントアウト禁止。
- describe構成の見直し、fixtures/ファクトリの共通化。

### 例：重複の統合（良い）
```ts
describe('名前のバリデーション', () => {
  test.each([
    ['', '空文字'],
    ['   ', '空白'],
    [null as any, 'null'],
    [undefined as any, 'undefined']
  ])('名前が%p（%s）でエラー', (name) => {
    expect(() => registerUser({ name })).toThrow('名前は必須です');
  });
});
```

### レビュー観点（更新時）
- 変更仕様をテスト名が説明しているか。
- 回帰観点が維持されているか（既存仕様の保持）。
- 優先度（Critical/Important）の網羅が先行しているか。
