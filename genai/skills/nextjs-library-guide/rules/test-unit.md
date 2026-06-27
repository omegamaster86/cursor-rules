---
title: Unit Testing with Vitest
impact: HIGH
impactDescription: 高速な単体テストによるコード品質の保証
tags: vitest, unit-test, testing
---

## Unit Testing with Vitest

Vitest を使用した単体テストのベストプラクティスです。

**インストール：**

```bash
npm install --save-dev vitest @vitejs/plugin-react
```

**設定（vitest.config.ts）：**

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    include: ['**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

**セットアップファイル（vitest.setup.ts）：**

```typescript
import '@testing-library/jest-dom/vitest'
```

**基本的なテスト：**

```typescript
// utils/format.ts
export function formatPrice(price: number): string {
  return new Intl.NumberFormat('ja-JP', {
    style: 'currency',
    currency: 'JPY',
  }).format(price)
}

// utils/format.test.ts
import { describe, it, expect } from 'vitest'
import { formatPrice } from './format'

describe('formatPrice', () => {
  it('should format price in Japanese Yen', () => {
    expect(formatPrice(1000)).toBe('￥1,000')
    expect(formatPrice(0)).toBe('￥0')
  })

  it('should handle decimal numbers', () => {
    expect(formatPrice(1000.5)).toBe('￥1,001')
  })
})
```

**モックの使用：**

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createTodo } from './todo'

// モジュールのモック
vi.mock('@/services/supabase-service/server', () => ({
  createClient: vi.fn(() => ({
    functions: {
      invoke: vi.fn(),
    },
  })),
}))

describe('createTodo', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should create a todo', async () => {
    const formData = new FormData()
    formData.append('title', 'Test Todo')

    const result = await createTodo({}, formData)
    
    expect(result.success).toBe(true)
  })
})
```

**非同期テスト：**

```typescript
import { describe, it, expect, vi } from 'vitest'

describe('async operations', () => {
  it('should handle async functions', async () => {
    const fetchData = vi.fn().mockResolvedValue({ id: 1, name: 'Test' })
    
    const result = await fetchData()
    
    expect(result).toEqual({ id: 1, name: 'Test' })
    expect(fetchData).toHaveBeenCalledTimes(1)
  })

  it('should handle errors', async () => {
    const fetchData = vi.fn().mockRejectedValue(new Error('Network error'))
    
    await expect(fetchData()).rejects.toThrow('Network error')
  })
})
```

**package.json スクリプト：**

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

**チェックリスト：**

- [ ] テストファイルは `*.test.ts` または `*.spec.ts`
- [ ] `describe` でテストをグループ化
- [ ] `beforeEach` でモックをクリア
- [ ] 非同期テストには `async/await` を使用
- [ ] カバレッジレポートを確認
