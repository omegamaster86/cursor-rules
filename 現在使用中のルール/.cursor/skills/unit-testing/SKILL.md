---
name: unit-testing
description: 単体テストの作成・修正を行う際に適用。テスト設計、テストコードの実装、テストカバレッジの改善などに使用。
---

# 単体テスト

## AAA パターン

```typescript
// Arrange（準備）
const input = { name: 'test' };
const expected = { id: 1, name: 'test' };

// Act（実行）
const result = await createUser(input);

// Assert（検証）
expect(result).toEqual(expected);
```

## 命名規則

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('有効なデータで新規ユーザーを作成できる', async () => {
      // ...
    });
  });
});
```

## モック戦略

- 外部依存（API、DB、ファイルシステム）はモック
- 純粋関数はモックしない
- モックは最小限に

```typescript
jest.mock('@/lib/api-client');
jest.mock('@/lib/prisma');
```

## テストデータ（ファクトリパターン）

```typescript
const createTestUser = (overrides?: Partial<User>): User => ({
  id: 1,
  name: 'Test User',
  email: 'test@example.com',
  ...overrides,
});
```

## カバレッジ目標

- ライン: 80% 以上
- ブランチ: 75% 以上
- 重要なビジネスロジック: 100%

## テストの種類

- **正常系**: 期待通りの入力で期待通りの出力
- **異常系**: 無効な入力でのエラーハンドリング
- **エッジケース**: 空配列、最大値/最小値、特殊文字

## React コンポーネントテスト

```typescript
import { render, screen, fireEvent } from '@testing-library/react';

it('クリック時にonClickが呼ばれる', () => {
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>Click</Button>);
  fireEvent.click(screen.getByRole('button'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```
