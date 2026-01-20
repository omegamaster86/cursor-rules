---
name: tdd-workflow
description: 新機能の実装、バグ修正、リファクタ時に使用するスキル。ユニット/統合/E2Eを含む80%+カバレッジのTDDを徹底。
---

# テスト駆動開発ワークフロー

このスキルは、すべての開発がTDD原則に従い、包括的なテストカバレッジを確保することを保証します。

## 有効化のタイミング

- 新機能/機能追加の実装
- バグ修正や不具合対応
- 既存コードのリファクタ
- APIエンドポイント追加
- 新しいコンポーネント作成

## コア原則

### 1. コードより先にテスト
必ずテストを先に書き、通すための実装を行う。

### 2. カバレッジ要件
- 最低80%（ユニット + 統合 + E2E）
- すべてのエッジケースをカバー
- エラーシナリオをテスト
- 境界条件を検証

### 3. テスト種別

#### ユニットテスト
- 個別関数/ユーティリティ
- コンポーネントロジック
- ピュア関数
- ヘルパー/ユーティリティ

#### 統合テスト
- APIエンドポイント
- DB操作
- サービス間連携
- 外部API呼び出し

#### E2Eテスト（Playwright）
- 重要ユーザーフロー
- 完全なワークフロー
- ブラウザ自動化
- UI操作

## TDDワークフローステップ

### Step 1: ユーザージャーニーを書く
```
As a [role], I want to [action], so that [benefit]

Example:
As a user, I want to search for markets semantically,
so that I can find relevant markets even without exact keywords.
```

### Step 2: テストケース生成
各ジャーニーに対して包括的テストを作成:

```typescript
describe('Semantic Search', () => {
  it('returns relevant markets for query', async () => {
    // Test implementation
  })

  it('handles empty query gracefully', async () => {
    // Test edge case
  })

  it('falls back to substring search when Redis unavailable', async () => {
    // Test fallback behavior
  })

  it('sorts results by similarity score', async () => {
    // Test sorting logic
  })
})
```

### Step 3: テスト実行（失敗するはず）
```bash
npm test
# Tests should fail - we haven't implemented yet
```

### Step 4: 実装
テストが通る最小実装を書く:

```typescript
// Implementation guided by tests
export async function searchMarkets(query: string) {
  // Implementation here
}
```

### Step 5: 再度テスト
```bash
npm test
# Tests should now pass
```

### Step 6: リファクタ
テストを通したまま品質を改善:
- 重複削除
- 命名改善
- パフォーマンス最適化
- 可読性向上

### Step 7: カバレッジ確認
```bash
npm run test:coverage
# Verify 80%+ coverage achieved
```

## テストパターン

### ユニットテスト（Jest/Vitest）
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click</Button>)

    fireEvent.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### API統合テスト
```typescript
import { NextRequest } from 'next/server'
import { GET } from './route'

describe('GET /api/markets', () => {
  it('returns markets successfully', async () => {
    const request = new NextRequest('http://localhost/api/markets')
    const response = await GET(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.success).toBe(true)
    expect(Array.isArray(data.data)).toBe(true)
  })

  it('validates query parameters', async () => {
    const request = new NextRequest('http://localhost/api/markets?limit=invalid')
    const response = await GET(request)

    expect(response.status).toBe(400)
  })

  it('handles database errors gracefully', async () => {
    // Mock database failure
    const request = new NextRequest('http://localhost/api/markets')
    // Test error handling
  })
})
```

### E2Eテスト（Playwright）
```typescript
import { test, expect } from '@playwright/test'

test('user can search and filter markets', async ({ page }) => {
  // Navigate to markets page
  await page.goto('/')
  await page.click('a[href="/markets"]')

  // Verify page loaded
  await expect(page.locator('h1')).toContainText('Markets')

  // Search for markets
  await page.fill('input[placeholder="Search markets"]', 'election')

  // Wait for debounce and results
  await page.waitForTimeout(600)

  // Verify search results displayed
  const results = page.locator('[data-testid="market-card"]')
  await expect(results).toHaveCount(5, { timeout: 5000 })

  // Verify results contain search term
  const firstResult = results.first()
  await expect(firstResult).toContainText('election', { ignoreCase: true })

  // Filter by status
  await page.click('button:has-text("Active")')

  // Verify filtered results
  await expect(results).toHaveCount(3)
})

test('user can create a new market', async ({ page }) => {
  // Login first
  await page.goto('/creator-dashboard')

  // Fill market creation form
  await page.fill('input[name="name"]', 'Test Market')
  await page.fill('textarea[name="description"]', 'Test description')
  await page.fill('input[name="endDate"]', '2025-12-31')

  // Submit form
  await page.click('button[type="submit"]')

  // Verify success message
  await expect(page.locator('text=Market created successfully')).toBeVisible()

  // Verify redirect to market page
  await expect(page).toHaveURL(/\/markets\/test-market/)
})
```

## テストファイル構成

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx          # Unit tests
│   │   └── Button.stories.tsx       # Storybook
│   └── MarketCard/
│       ├── MarketCard.tsx
│       └── MarketCard.test.tsx
├── app/
│   └── api/
│       └── markets/
│           ├── route.ts
│           └── route.test.ts         # Integration tests
└── e2e/
    ├── markets.spec.ts               # E2E tests
    ├── trading.spec.ts
    └── auth.spec.ts
```

## 外部サービスのモック

### Supabase モック
```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({
          data: [{ id: 1, name: 'Test Market' }],
          error: null
        }))
      }))
    }))
  }
}))
```

### Redis モック
```typescript
jest.mock('@/lib/redis', () => ({
  searchMarketsByVector: jest.fn(() => Promise.resolve([
    { slug: 'test-market', similarity_score: 0.95 }
  ])),
  checkRedisHealth: jest.fn(() => Promise.resolve({ connected: true }))
}))
```

### OpenAI モック
```typescript
jest.mock('@/lib/openai', () => ({
  generateEmbedding: jest.fn(() => Promise.resolve(
    new Array(1536).fill(0.1) // Mock 1536-dim embedding
  ))
}))
```

## テストカバレッジ確認

### カバレッジレポート実行
```bash
npm run test:coverage
```

### カバレッジ閾値
```json
{
  "jest": {
    "coverageThresholds": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## 避けるべきテストミス

### ❌ WRONG: 実装詳細のテスト
```typescript
// Don't test internal state
expect(component.state.count).toBe(5)
```

### ✅ CORRECT: ユーザー視点のテスト
```typescript
// Test what users see
expect(screen.getByText('Count: 5')).toBeInTheDocument()
```

### ❌ WRONG: 脆いセレクタ
```typescript
// Breaks easily
await page.click('.css-class-xyz')
```

### ✅ CORRECT: 意味的セレクタ
```typescript
// Resilient to changes
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
```

### ❌ WRONG: テスト非独立
```typescript
// Tests depend on each other
test('creates user', () => { /* ... */ })
test('updates same user', () => { /* depends on previous test */ })
```

### ✅ CORRECT: 独立したテスト
```typescript
// Each test sets up its own data
test('creates user', () => {
  const user = createTestUser()
  // Test logic
})

test('updates user', () => {
  const user = createTestUser()
  // Update logic
})
```

## 継続的テスト

### 開発時のウォッチモード
```bash
npm test -- --watch
# Tests run automatically on file changes
```

### Pre-Commitフック
```bash
# Runs before every commit
npm test && npm run lint
```

### CI/CD統合
```yaml
# GitHub Actions
- name: Run Tests
  run: npm test -- --coverage
- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

## ベストプラクティス

1. **テスト先行** - 常にTDD
2. **1テスト1アサート** - 単一の挙動に集中
3. **説明的なテスト名** - 何を検証するか明確に
4. **Arrange-Act-Assert** - 構造を明確に
5. **外部依存をモック** - ユニットテストを分離
6. **エッジケース** - Null/undefined/空/大規模
7. **エラー経路** - ハッピーパスだけでなく
8. **テスト高速化** - ユニット<50ms
9. **後片付け** - 副作用を残さない
10. **カバレッジ確認** - ギャップ把握

## 成功指標

- コードカバレッジ80%以上
- 全テストがグリーン
- スキップ/無効テストなし
- テスト実行が高速（ユニット<30秒）
- E2Eが重要フローをカバー
- 本番前にバグを検知

---

**Remember**: テストは任意ではない。テストは安全網であり、安心してリファクタし、迅速に開発し、本番の信頼性を高める。
