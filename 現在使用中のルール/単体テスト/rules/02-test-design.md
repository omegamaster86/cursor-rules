## 02. テスト設計

### AAA（Arrange-Act-Assert）
- 準備（Arrange）：テストデータ/依存を明示的に準備（ファクトリ活用）。
- 実行（Act）：対象関数/メソッドを1回だけ実行。
- 検証（Assert）：期待値を明確に。副作用はモック呼び出しで検証。

### ケース網羅
- 正常系、異常系（例外/エラー）、境界値（最小/最大/±1）、エッジケースを用意。
- 回帰視点を含め、既存仕様の保持を保証。

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


