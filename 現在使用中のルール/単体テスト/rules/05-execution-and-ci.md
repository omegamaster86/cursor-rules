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
- 変更の早期検知のため、pre-commit で最小のテスト実行を推奨。
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
