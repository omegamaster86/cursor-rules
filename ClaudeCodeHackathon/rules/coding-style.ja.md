# コーディングスタイル

## イミュータブル（CRITICAL）

必ず新しいオブジェクトを作る。絶対にミューテーションしない:

```javascript
// WRONG: Mutation
function updateUser(user, name) {
  user.name = name  // MUTATION!
  return user
}

// CORRECT: Immutability
function updateUser(user, name) {
  return {
    ...user,
    name
  }
}
```

## ファイル構成

小さいファイルを多数 > 大きいファイルを少数:
- 高凝集・低結合
- 200-400行が目安、最大800行
- 大きいコンポーネントからユーティリティを抽出
- 型ではなく機能/ドメインで整理

## エラーハンドリング

必ずエラーを包括的に処理する:

```typescript
try {
  const result = await riskyOperation()
  return result
} catch (error) {
  console.error('Operation failed:', error)
  throw new Error('Detailed user-friendly message')
}
```

## 入力検証

必ずユーザー入力を検証する:

```typescript
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150)
})

const validated = schema.parse(input)
```

## コード品質チェックリスト

完了前に:
- [ ] 読みやすく命名が適切
- [ ] 関数が小さい（<50行）
- [ ] ファイルが集中（<800行）
- [ ] 深いネストがない（>4階層）
- [ ] 適切なエラーハンドリング
- [ ] console.log がない
- [ ] ハードコード値がない
- [ ] ミューテーションなし（イミュータブル）
