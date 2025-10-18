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
tests/unit/utils/calc.test.ts
```
```ts
// tests/unit/utils/calc.test.ts
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


