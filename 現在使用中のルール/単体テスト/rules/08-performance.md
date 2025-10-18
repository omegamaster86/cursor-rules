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
```javascript
// テスト実行時間の測定
describe('Performance Tests', () => {
    test('大量データの処理時間', () => {
        const startTime = Date.now();
        
        const largeData = Array.from({ length: 10000 }, (_, i) => ({
            id: i,
            value: Math.random()
        }));
        
        const result = processLargeData(largeData);
        
        const endTime = Date.now();
        const executionTime = endTime - startTime;
        
        expect(result).toBeDefined();
        expect(executionTime).toBeLessThan(1000); // 1秒以内
    });
});
```

**並列実行の設定:**
```javascript
// jest.config.js
module.exports = {
    maxWorkers: '50%', // CPUコア数の50%
    testTimeout: 10000, // 10秒タイムアウト
    bail: false // 1つ失敗しても続行
};
```



#### 悪い例：無制限生成と待機不足
```ts
// 100万件生成 + 適切なawaitなし → メモリ圧迫/不安定
const huge = Array.from({ length: 1_000_000 }, (_, i) => i);
processLarge(huge);
```

